---
title: "MACO-Feature Visualization via Magnitude Constrained Optimization"
lastmod: 2026-07-04
---

#compvis #interpretebility #ml_tools

### Contributions
The **MACO (Magnitude Constrained Optimization)** algorithm is a feature visualization method that generates interpretable images for deep neural networks by exclusively optimizing the phase spectrum of an image while holding its Fourier magnitude constant.

Traditional feature visualization methods optimize the entire Fourier spectrum and rely on high-frequency penalties to keep images readable. However, when scaling to modern, deeper architectures like Vision Transformers (ViTs) and deep ResNets, these techniques fail because high-frequency noise leaks through and pollutes the visualizations. Inspired by human vision research showing that object recognition is driven more by phase than by magnitude, MACO treats the natural image magnitude spectrum as a hard constraint. This completely eliminates the need for complex high-frequency regularization hyperparameters or statistical generative prior models (such as GANs or autoencoders).

## Proposed Method
### The Core Concept: Phase vs. Magnitude

In Fourier space, a complex-valued image spectrum $z$ can be decomposed into its polar form: $$z = r e^{i\varphi}$$ where **$r$ represents the magnitude spectrum** and **$\varphi$ represents the phase spectrum**.

1. **Fixed Magnitude ($r$)**: MACO precomputes $r$ as the average Fourier magnitude of a set of natural images (typically from the entire ImageNet dataset ): $$r = \mathbb{E}_{x \sim \mathcal{D}}(|F(x)|)$$ This spectrum captures a natural distribution (which naturally attenuates high frequencies) and only needs to be calculated once.
2. **Optimized Phase ($\varphi$)**: The algorithm optimizes only the phase parameters $\varphi \in \mathbb{R}^{W \times H}$ via gradient ascent, cutting the number of parameters to optimize by half and ensuring the generated image naturally respects the frequency domain of natural images.

---
### Step-by-Step Feature Visualization Process

The exact process of generating a feature visualization using MACO involves an optimization loop designed to maximize a target network activation $L_v$ (which can represent a single neuron, channel, layer, or output logit):
#### 1. Initialization
- **Magnitude Constraining**: Load the precomputed natural magnitude spectrum $r$.
- **Initial Phase**: Sample an initial phase vector randomly from a uniform distribution: $\varphi_0 \sim U([-\pi, \pi])^{W \times H}$. *You start with a random image essentially this way.*
- **Transparency Accumulator**: Initialize the transparency map accumulator $\alpha = 0$.

#### 2. The Optimization Loop (typically for $N = 256$ steps)
For each step $n$ in the optimization loop, the following sequence is executed:

- **Construct the Complex Spectrum**: Combine the fixed natural magnitude $r$ and the current phase $\varphi_n$ to form the Fourier spectrum $z_n = r e^{i\varphi_n}$.
- **Reconstruct the Image**: Apply the Inverse 2-D Discrete Fourier Transform ($F^{-1}$) to translate the spectrum back into the pixel-space image: $$x_n = F^{-1}(r e^{i\varphi_n})$$
- **Apply Transformation Robustness ($\tau$)**: To prevent the optimizer from finding high-frequency adversarial patterns, apply two specific data augmentations to the reconstructed image:
    1. **Additive Uniform Noise**: Add noise $\delta \sim U([-0.1, 0.1])^{W \times H}$.
    2. **Random Cropping and Resizing**: Crop the image using a crop size drawn from a normal distribution $\mathcal{N}(0.25, 0.1)$ (on average representing 25% of the image size) and resize it back to the original dimensions.
- **Forward Pass and Activation Evaluation**: Feed the transformed image into the classifier/network to compute the target activation score $L_v(x_n)$. 
- **Backward Pass (Gradient Ascent)**:
    - Compute the gradient of the *target activation*(intermediate layer,latent vector,etc) with respect to the phase parameters: $\nabla_{\varphi} L_v(x_n)$.
    - Update the phase using an optimizer (typically NAdam with a learning rate of $1.0$): $\varphi_{n+1} = \varphi_n + \eta \nabla_{\varphi} L_v(x_n)$.
- **Accumulate Spatial Importance (The Transparency Map, $\alpha$)**: During backpropagation, the gradient of the activation with respect to the input pixels $\nabla_{x_n} L_v(x_n)$ is computed "for free" as an intermediate step to get the phase gradient. MACO stores and accumulates the absolute values of these gradients over all steps: $$\alpha = \alpha + |\nabla_{x_n} L_v(x_n)|$$ Averaging these input-space gradients behaves similarly to the SmoothGrad attribution method, highlighting which areas of the image the model attended to or modified the most during optimization.

#### 3. Output Generation
At the end of $N$ steps, the final feature visualization and transparency map are output:
- **Final Image**: Apply the final inverse Fourier transform using the optimized phase $\varphi_N$: $$x^* = F^{-1}(r e^{i\varphi_N})$$
- **Transparency Mask**: The accumulated map $\alpha$ is returned alongside the image and can be applied as a post-processing mask to fade out unimportant background patterns and isolate key diagnostic features.


## Transparency Map $\alpha$
In the MACO algorithm, **$\alpha$ (alpha)** represents the **transparency map** (or **transparency mask**). It is generated "for free" alongside the feature visualization to provide a visual attribution mechanism, explaining both "what" activates a target neuron/channel and "where" those key features are spatially located.

During the backpropagation process of optimizing the phase ($\varphi$), the intermediate gradient of the activation with respect to the input pixels ($\frac{\partial L_v(x)}{\partial x}$) is calculated naturally as part of the chain rule: $$\frac{\partial L_v(x)}{\partial \varphi} = \frac{\partial L_v(x)}{\partial x} \frac{\partial x}{\partial \varphi}$$
MACO intercepts and stores it at every optimization step without incurring any additional computational cost. Over the course of the $N$ optimization steps, the absolute values of these input gradients are accumulated: $$\alpha = \alpha + |\nabla_{x_n} L_v(x_n)|$$At the end of the optimization, averaging these accumulated gradients over all steps behaves theoretically similarly to **SmoothGrad**.
- **Locating Attention**: The map $\alpha$ highlights the specific spatial regions of the image that were modified or attended to the most by the model during the optimization process.
- **Fading Unimportant Patterns**: Feature visualizations often generate repetitive patterns or noisy background elements that can distract the user or lead to confirmation bias. Applying $\alpha$ as a transparency mask fades out these unimportant background details to isolate the core diagnostic features.
- **Post-Processing Only**: Ablation studies confirm that $\alpha$ acts strictly as a post-processing enhancement. Applying the transparency mask does not alter the optimization itself or affect the underlying objective scores (such as logit magnitude).

---
## MOCO with CRAFT for feature/concept Visualizaiton
- Using CRAFT we can decompose an images representations into a dictionary of concepts/features. 
- Then we use the MACO algorithm to visualise the said concepts - instead of computing the loss w.r.t the activations , we compute loss based on whether the current generated visual(image) when passed through the network gives us the target concept vector or not. - **This is called Feature Inversion.**

---
## Objective Function
The optimization criterion— **$L_v(x)$** in the paper—is mathematically defined as a real-valued function ($L_v(x) \in \mathbb{R}$) that measures the activation or similarity of a generated image $x$ with respect to a target component of a neural network.

Rather than using a single, rigid mathematical loss formula, the creators of MACO define $L_v(x)$ dynamically depending on the specific feature visualization task being performed. In the general MACO optimization framework, the goal is to find the optimal phase vector $\varphi^*$ that maximizes the expected value of $L_v$ across random robustness transformations $\tau$:
$$\varphi^* = \operatorname{argmax}_{\varphi \in \mathbb{R}^{W \times H}} \mathbb{E}_{\tau \sim T} \left( L_v\left((\tau \circ F^{-1})(r e^{i\varphi})\right) \right)$$

Depending on what you want to visualize, the loss function $L_v(x)$ is defined in one of three ways:
### 1. Logit and Internal Channel Visualization (Standard MACO)
When the goal is to understand what a specific part of the network's architecture is looking for, $L_v(x)$ directly targets activation magnitudes:
- **For Class Logit Visualization**: $L_v(x)$ is defined to **maximize the activation of a specific unit in the output logit vector** (corresponding to an ImageNet class like "White Shark").
- **For Internal State (Channel) Visualization**: $L_v(x)$ is defined to **maximize the activation of specific channels** located in different intermediate blocks of the network (such as Block 1, 2, 6, or 10 of a Vision Transformer or ResNet).
### 2. Feature Inversion
When you want to reconstruct what a network "sees" and preserves from a real-world image at a specific layer, the network's response to a reference image is used to construct the loss:
- **The Activation Target**: First, a reference image is passed through the model to obtain its actual activation pattern at a target layer.
- **The Loss Definition**: $L_v(x)$ is defined to **maximize the similarity** between the activation pattern produced by the generated image $x$ and the pre-computed activation pattern of the reference image. This optimization reconstructs the semantic information of the original image while naturally omitting any background details or noise that the network discarded.
### 3. Concept Visualization (MACO + CRAFT)
When explaining the latent space of a network by decomposing its activation patterns into distinct semantic directions (concepts), the loss is defined to align with these directions:
- **The Loss Definition**: $L_v(x)$ is defined to **maximize the angle of superposition** with the target concept direction vector in the network’s activation space. This forces the generated image's activations to match and strongly activate that specific conceptual pathway.
