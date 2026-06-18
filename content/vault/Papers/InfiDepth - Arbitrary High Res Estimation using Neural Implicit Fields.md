---
tags:
  - Depth_Estimation
---
*Link*: https://zju3dv.github.io/InfiniDepth/#pointcloud
Paper: https://arxiv.org/pdf/2601.03252



### Depth as Neural Implicit Fields
They  have extended the concept of [Neural Implicit Fields](/vault/deep-learning/neural-implicit-fields/) which maps any 2d coordinate to a depth value conditioned on the input RGB image of a fixed resolution.$$d_{I}(x,y) = N_{\mathbb{\theta}}(I,(x,y))$$
They implemented this NIF model using a **Local Implicit Decoder**.  It has two modules:
- #### Feature Query:  
	- They use a VIT  encoder to capture Global information. 
	- This is followed by a **Reassemble Block** . They upsample shallow-layer features to higher resolutions.
	- They retain the deeper-layer features at their native(original resolution).
	- Constructed feature pyramid of form: $\{f^k\}^L_{k=1}$  where $f^k\in \mathbb{R}^{h_{k}*w_{k}*C^k}$
		- Output of each $f^k$ is a **feature map** of the original image.
		
	- ##### **Continuous Position Query**:
		-  $(x, y)$ in an image of size $W \times H$, the model first scales that coordinate to match the specific dimensions of each layer in the feature pyramid $(h_k, w_k)$:$$(x_k, y_k) = \left( x \cdot \frac{w_k}{W}, y \cdot \frac{h_k}{H} \right)$$
		- Because $(x_k, y_k)$ will almost never be a perfect integer (e.g., it might be $112.4$), the model looks at the **four nearest pixels** in that feature map. This is defined as the neighborhood $\mathcal{N}_k$: $$\mathcal{N}_k(x_k, y_k) = \{ (i, j) \mid i \in \{\lfloor x_k \rfloor, \lfloor x_k \rfloor + 1 \}, j \in \{\lfloor y_k \rfloor, \lfloor y_k \rfloor + 1 \} \}$$
	- **Bilinear Interpolation**: Now instead of taking closer of the 4 pixels, we take the bilinear interpolation between them. This gives us a single value per feature map at scale k per query (x,y). $$f^k_{(x,y)} \in \mathbb{R}^{1 \times C^k}$$
 
- #### Depth Decoding
	Given the multi-scale local descriptors $\{f^k_{(x,y)}\}_{k=1}^L$, the model fuses them hierarchically from shallow (detail) to deep (semantic) features to capture fine-grained geometric variations and global context.
	
	- **Initialization**: Let $\mathbf{h}_1 := f^1_{(x,y)} \in \mathbb{R}^{C_1}$ denote the queried feature at the shallowest, highest-resolution scale.
	    
	- **Residual Gated Fusion**: For each scale $k = 1, \dots, L-1$, the current feature $\mathbf{h}_k$ is fused with the next-scale feature $f^{k+1}_{(x,y)}$ using a gated mechanism:
	    
	    $$\mathbf{h}_{k+1} = \text{FFN}_k \left( f^{k+1}_{(x,y)} + \mathbf{g}_k \odot \text{Linear}(\mathbf{h}_k) \right)$$
	    
	- **Gating Mechanism**: $\mathbf{g}_k \in (0, 1)^{C_{k+1}}$ is a learnable channel-wise gate, and $\odot$ denotes element-wise multiplication.
	    
	- **Transformation**: $\text{Linear}(\cdot)$ is a ==projection to match feature dimensions==, and $\text{FFN}_k(\cdot)$ is a ==two-layer== feed-forward network with non-linear activation.
    
	- **Final Prediction**: This process repeats until the deepest scale $L$ is reached, resulting in the final fused feature $\mathbf{h}_L \in \mathbb{R}^{C_L}$. The final depth value $d_I(x, y)$ is predicted by an MLP head:
	    $$d_I(x, y) = \text{MLP}(\mathbf{h}_L)$$

## Implementation Details
- They use **DINOv3 ViT Large** model as the image encoder. 
	- Extract feature maps from layers - 4,11, 23 and project them to 256,512 and 1024 dimensions respectively.
- #### Datasets
	- HyperSim
	- VKITTI
	- UnrealStereo4K
- #### Loss and Training
	- They training flexibly on sparse samples due to their depth representation instead of going for the entire depth map.
	- Randomly sample N coordinate-depth pairs and compute the L1 - loss over these points.
	- **AdamW** with LR=$10^{-5}$ 
	- 800k training steps on 8 NVIDIA GPUs with batch size of 4 per GPU.

| **Stage**              | **Operation Type** | **Data Shape**                                         |
| ---------------------- | ------------------ | ------------------------------------------------------ |
| **Feature Extraction** | Global (ViT)       | $1 \times \text{Tokens} \times \text{Channels}$        |
| **Coordinate Grid**    | Batch Generation   | $H_{out} \times W_{out} \times 2$                      |
| **Point Sampling**     | Vectorized Lookup  | $(H_{out} \cdot W_{out}) \times \text{Channels}$       |
| **Gated Fusion**       | Point-wise MLP     | $(H_{out} \cdot W_{out}) \times \text{Fused Channels}$ |
| **Final Output**       | Reshape            | $H_{out} \times W_{out} \times 1$                      |
