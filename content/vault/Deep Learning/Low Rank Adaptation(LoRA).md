---
title: "Low Rank Adaptation(LoRA)"
lastmod: 2026-05-16
---

#deep_learning #fine-tuning 


> This is built upon the hypothesis that the weight update during fine-tuning often exists an **low intrinsic rank**, thus a low-rank decomposition matrices could potentially mimic the weight changes with a few trainable parameters.

More background regarding the hypothesis:
- [Measuring the Intrinsic Dimension of Objective Landscapes](https://arxiv.org/abs/1804.08838)
- [Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning](https://arxiv.org/abs/2012.13255)

## 1. Introduction

Scaling up pre-trained language models has yielded unprecedented performance on a wide range of downstream tasks. However, full fine-tuning — updating all model parameters — becomes increasingly impractical as model sizes grow into hundreds of billions of parameters. Storing and serving a separate full copy of the model for each task is prohibitively expensive in terms of memory, compute, and storage.

**Parameter-efficient fine-tuning $PEFT$** methods seek to adapt large pre-trained models by modifying only a small subset of parameters or by injecting lightweight task-specific modules, leaving the original weights frozen. LoRA (Hu et al., 2021) belongs to the reparameterization family of PEFT methods and has gained widespread adoption due to its simplicity, strong performance, and zero inference latency overhead.


## 2. The Low-Rank Update Hypothesis

The central postulate driving LoRA is:

> **During fine-tuning, the weight updates $\Delta W$ required to adapt a pre-trained model to a downstream task live in a low-dimensional subspace, i.e., they have a low *intrinsic rank*.**

Formally, for a pre-trained weight matrix $W_0 \in \mathbb{R}^{d \times k}$ e.g., an attention projection, full fine-tuning learns an update $\Delta W \in \mathbb{R}^{d \times k}$ such that the adapted weight is $W_0 + \Delta W$. If $\Delta W$ were an arbitrary dense matrix, its rank could be as high as $\min$d,k, requiring $d\cdot k$ trainable parameters. 

The hypothesis asserts that an excellent approximation can be achieved with a matrix $\Delta W$ of rank $r \ll \min$d,k.

### 2.1 Empirical and Theoretical Motivation
- **Intrinsic dimensionality of objective landscapes** $Li et al., 2018$: Over-parameterized neural networks possess a very low-dimensional subspace $often a few hundred dimensions$ within which optimization can find solutions as good as those in the full parameter space.
- **Intrinsic dimension of fine-tuning** $Aghajanyan et al., 2020$: Explicit measurement of the intrinsic dimension required for solving various NLP tasks shows that only a few hundred free parameters $out of hundreds of millions$ are sufficient to achieve near full fine-tuning performance.
- **Spectral analysis of full fine-tuning updates**: Direct inspection of $W_{\text{fine-tuned}} - W_{\text{pre-trained}}$ across tasks reveals a rapid decay in singular values, with most of the energy concentrated in the top few components.

Thus, the *task-specific shift* from pre-trained knowledge is strongly compressible, and a low-rank decomposition can capture it with minimal loss of information.

---

## 3. LoRA: Method Formulation

LoRA enforces the low-rank structure on the weight update by construction. For a target layer parameterized by a pre-trained weight matrix $W_0 \in \mathbb{R}^{d \times k}$, LoRA models the update as a product of two low-rank matrices:

$$
\Delta W = BA,
$$

where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$, with the rank $r \ll \min$d,k. The forward pass becomes:
$$
h = W_0 x + \Delta W x = W_0 x + B A x,
\tag{1}
$$

where $x \in \mathbb{R}^{k}$ is the input to the layer $e.g., the hidden states projected into value space$. During training, $W_0$ is frozen and does not receive gradient updates; only the parameters in $A$ and $B$ are optimized.

### 3.1 Scaling Factor

In practice, the update is often scaled by a factor $\frac{\alpha}{r}$:

$$
h = W_0 x + \frac{\alpha}{r} B A x,
\tag{2}
$$

where $\alpha$ is a constant $usually set in the same order as $r$$. The scaling reduces the need to retune the learning rate when the rank $r$ is changed, because the product $BA$ naturally scales with $r$ if $A$ and $B$ are initialized with appropriate variance. With $\frac{\alpha}{r}$, varying $r$ keeps the effective learning dynamics roughly invariant. LoRA authors typically fix $\alpha$ at the first $r$ tried and then tune only the learning rate.

### 3.2 Initialization

- $A$ is initialized with a random Gaussian distribution: $A_{ij} \sim \mathcal{N}(0, \sigma^2)$ .
- $B$ is initialized to zero: $B = \mathbf{0}$.

This ensures that at the start of training, $\Delta W = 0$ and the model’s output exactly matches that of the pre-trained model. The trajectory then gradually introduces the low-rank adaptation.

### 3.3 Which Layers to Adapt?

In the original formulation on Transformer models, LoRA is applied to the attention weight matrices. The authors experiment with adapting only the query $W_q$ and value $W_v$ projections, which yields strong results while being parameter-efficient. 
More generally, LoRA can be applied to any dense layer. Empirical studies show that adapting the attention layers often suffices, and adding the feed-forward layers can provide small additional gains at the cost of extra parameters.

---

## 4. Mathematical and Structural Properties

### 4.1 Parameter Count

For a single weight matrix of shape $d \times k$, full fine-tuning requires $d \cdot k$ trainable parameters. With LoRA, the number becomes $r$d + k$$. When $r \ll \min$d,k$$, the reduction is dramatic. For instance, in GPT-3 175B with $d = 12288$ and $k = 12288$ for a typical attention matrix, full update would have $\approx 1.5\times 10^8$$ parameters, while LoRA with $r=4$ uses only $$4 \times (12288+12288) \approx 9.8\times 10^4 $$ – a reduction by over three orders of magnitude.

### 4.2 Low-Rank Constraint and Expressivity

The rank-$r$ constraint explicitly confines the weight update to an $r$-dimensional subspace of the full $\mathbb{R}^{d \times k}$ space. This subspace is spanned by the $r$ columns of $B$ and the $r$ rows of $A$. Because the pre-trained weights $W_0$ remain frozen and provide a rich representation basis, the low-rank adaptation only needs to capture the *task-specific deviation*. The decomposition can be seen as learning a linear transformation $A$ that projects the input into a low-dimensional “task space,” and $B$ that maps that task-space back to the output dimension.

### 4.3 Gradient Flow

Consider the loss $\mathcal{L}$. The gradient with respect to the trainable parameters is:

$$
\frac{\partial \mathcal{L}}{\partial A} = B^T \frac{\partial \mathcal{L}}{\partial h} x^T, \quad
\frac{\partial \mathcal{L}}{\partial B} = \frac{\partial \mathcal{L}}{\partial h} A x^T.
\tag{3}
$$

Since $B$ is initially zero, $A$ receives zero gradients from the very first step (through $B^T$), while $B$  starts to update from the start. $As $B\neq0$ , A begins to receive non‑zero gradients and adapts.

The two matrices co‑evolve, but their gradient magnitudes can be very different, often requiring asymmetric learning rates (as in LoRA+) for optimal training.

### 4.4 Merging Weights at Inference

After training, $W = W_0 + \frac{\alpha}{r} BA$ can be computed offline and stored as a single dense matrix. The inference forward pass then becomes $h = W x$, which is identical in computational cost to the original pre-trained model. This **zero-inference-latency** property is a key advantage of LoRA over adapter-based methods that add extra serial layers.

For multi-task serving, one can keep the base model $W_0$ shared and switch between different LoRA matrices $BA$ by swapping the merged weights on the fly, or by keeping the low-rank factors separate and computing $h = W_0 x + BA x$ with very little overhead.

---

## 5. Practical Considerations
### 5.1 Choosing the Rank $r$

The rank $r$ controls the trade-off between adaptation capacity and parameter efficiency. Remarkably, the original LoRA paper shows that even $r = 1$ or $2$ can achieve performance comparable to full fine-tuning on many benchmarks. As $r$ increases, performance tends to saturate quickly. Typical values used in practice range from 4 to 64.

The near-invariance of optimal $r$ with respect to model size further validates the low-rank hypothesis: the intrinsic dimension needed for adaptation does not scale with the width or depth of the model.

### 5.2 Scaling Factor $\alpha$
$\alpha$ determines the magnitude of the update relative to the original weights. When varying $r$, setting $\alpha$ to a fixed multiple of the initial $r$ $e.g., $\alpha = 2r$ or $\alpha = r$$ makes the effective step size similar. The common practice is to fix $\alpha$ at a value that works well $e.g., 16$ and then tune the learning rate.

### 5.3 Choosing Target Modules

While the original application focused on the query and value projections in Transformer self-attention, LoRA can be extended to:
- Key and output projections.
- Feed-forward network layers.
- Embedding layers  - *though not typically recommended* due to high dimensionality and the discrete nature of token embeddings.

Applying LoRA to more modules increases trainable parameters but may improve performance, especially on complex tasks. A common setup is to apply LoRA to all attention matrices $$W_q, W_k, W_v, W_o$$

### 5.4 Combining with Other PEFT Methods

LoRA is orthogonal to many other efficient methods. It can be combined with:
- **Prefix tuning**: prepend learnable vectors to the input sequence.
- **Adapters**: small bottleneck layers inserted between transformer blocks.
- **Prompt tuning**: learnable soft prompts in the input embedding space.

However, combining multiple methods often saturates the gain and increases complexity; LoRA alone typically suffices.

---

## 6. Variants and Extensions

Since its introduction, numerous improvements and variants of LoRA have been proposed:

- **LoRA+** (*Hayou et al., 2024*): 
	- Identifies that the standard initialization and scaling leads to inefficient learning of $A$ and $B$. By using different learning rates for the two matrices and a specific initialization scheme, LoRA+ accelerates convergence and improves performance without additional parameters.
- **VeRA** (*Kopiczko et al., 2023*): 
	- Shares a single pair of frozen random matrices across layers and only learns small scaling vectors, further reducing the number of trainable parameters.
- **DoRA** (*Liu et al., 2024*):
	- Decomposes pre-trained weights into magnitude and direction components, applying low-rank updates only to the directional part. This mimics the learning dynamics of full fine-tuning more closely and yields consistent improvements.
- **AdaLoRA**(*Zhang et al., 2023*): 
	- Parameterizes the weight update in SVD form and adaptively prunes less important singular values during training, dynamically allocating the parameter budget to critical directions.
- **QLoRA** (*Dettmers et al., 2023*):
	- Combines LoRA with 4-bit quantized pre-trained models, enabling fine-tuning of huge models $e.g., 65B$ on a single GPU while preserving performance.

---
## 7. Empirical Validation

The LoRA paper presents extensive experiments on large language models $RoBERTa, DeBERTa, GPT-2, GPT-3 175B$. Key findings:

- **Performance matches full fine-tuning:** On the GLUE benchmark, RoBERTa-base with LoRA achieves scores comparable to or slightly better than full fine-tuning, using only $0.5\%$ of the trainable parameters.
- **Extremely low ranks suffice:** For GPT-3 175B, LoRA with $r = 1$ or $r = 2$ on $W_q$ and $W_v$ attains accuracies very close to full fine-tuning on tasks like MNLI, QQP, and SST-2.
- **Insensitivity to rank:** The performance improvement from increasing $r$ from 1 to 4 is marginal, confirming that the adaptation update has a very low intrinsic dimension.
- **No inference overhead:** After merging, throughput is identical to the pre-trained model.

These results strongly corroborate the low-rank update hypothesis and have made LoRA a default tool in the fine-tuning of large language and vision models.

---

## 8. Limitations and Open Questions
- **Not a silver bullet:** 
	- *For tasks requiring entirely new knowledge* or reasoning patterns far from the pre-training distribution e.g., learning a new language from scratch, the low-rank assumption may break and require higher rank or full fine-tuning.
- **Rank selection:** 
	- While $r$ is generally robust, the optimal value still depends on the task complexity, and automated rank selection remains an active area of research.
- **Gradient asymmetry:** 
	- The standard initialization leads to *imbalanced gradient magnitudes* for $A$ and $B$ early in training, which can slow down convergence. This has been *addressed by LoRA+* and other works.
- **Interaction with other PEFT methods:**
	- Combining LoRA with prompt tuning, adapters, or other techniques can sometimes lead to instability or diminishing returns; systematic guidelines are needed.
- **Theoretical understanding:** 
	- The exact relationship between the intrinsic dimension of the fine-tuning task and the optimal rank $r$ is still an open theoretical question.

---

