---
title: "VQ-VAE (Vector Quantized Variational Autoencoder)"
lastmod: 2026-07-06
---

_Reference: van den Oord et al., "Neural Discrete Representation Learning" (NeurIPS 2017)_

---
A Good Video - [VQ-VAE \| Everything you need to know about it \| Explanation and Implementation - YouTube](https://youtu.be/1ZHzAOutcnw?si=YhM5zyJSOL7jri7j)
## 1. Motivation

Standard VAEs learn a **continuous** latent space with a Gaussian prior. This works, but has known issues:

- **Posterior collapse**: powerful decoders (autoregressive, PixelCNN-style) can ignore the latent entirely, since a continuous Gaussian latent gives no strong incentive to use it.
- Continuous latents don't match the fact that many real-world modalities (speech phonemes, image textures/objects, tokens in text) are naturally **discrete**.
- Discrete latents pair well with powerful autoregressive priors (PixelCNN, Transformers) trained _after_ the VQ-VAE, enabling high-fidelity generation (this is the direct precursor to DALL-E's dVAE and many modern image/audio tokenizers).

VQ-VAE replaces the continuous latent with a **discrete latent from a learned codebook**, while keeping the encoder-decoder (autoencoder) structure.

---

## 2. Architecture

Three components:
1. **Encoder** $E$: maps input $x$ to a continuous latent tensor $z_e(x) = E(x)$.
    - For images, this is typically a CNN producing a spatial grid of vectors, e.g. shape $H' \times W' \times D$ (not a single vector — VQ-VAE usually quantizes a _grid_ of latent vectors, giving it enough capacity to reconstruct spatial detail).
2. **Codebook (embedding space)** $e \in \mathbb{R}^{K \times D}$: a set of $K$ learnable embedding vectors $e_1, \dots, e_K$, each of dimension $D$ (matching the encoder output channel dim).
    
3. **Decoder** $D$: maps the quantized latent $z_q(x)$ back to reconstruct $\hat{x}$.
### The quantization step

For every spatial location in $z_e(x)$, find the nearest codebook vector (nearest-neighbor lookup in $L_2$ distance):

$$ z_q(x) = e_k, \quad \text{where } k = \arg\min_j | z_e(x) - e_j |_2 $$

This is done independently per spatial position, so the output is a grid of discrete codebook indices (like a "latent image" of integers, each in $[1, K]$) — this discrete grid is the actual compressed representation.

**Architecture diagram (conceptually):**

```
x → Encoder → z_e(x) → [Nearest-neighbor lookup in codebook] → z_q(x) → Decoder → x̂
                              ↑
                     Codebook e_1...e_K (learned)
```

---

## 3. The Objective Function

VQ-VAE's loss has **three terms**:

$$ \mathcal{L} = \underbrace{|x - \hat{x}|_2^2}_{\text{reconstruction loss}} + \underbrace{| \text{sg}[z_e(x)] - e |_2^2}_{\text{codebook loss}} + \underbrace{\beta |z_e(x) - \text{sg}[e]|_2^2}_{\text{commitment loss}} $$

where `sg[·]` is the **stop-gradient** operator (identity in forward pass, zero gradient in backward pass).

### Why three terms?
- **Reconstruction loss**: standard autoencoder term — trains encoder + decoder to reconstruct $x$ well through the quantized bottleneck. (In the original paper this can be an MSE or a negative log-likelihood depending on the output distribution assumed.)
    
- **Codebook loss**: the argmin operation is non-differentiable, so the codebook vectors don't get gradients from the reconstruction loss directly. This term explicitly pulls the chosen codebook vector $e$ toward the encoder output $z_e(x)$ — it's essentially a **vector-quantization / clustering loss** (like k-means: move the "centroid" toward the assigned points). Gradient flows only into $e$ here (encoder output is stop-gradiented).
    
- **Commitment loss**: the encoder's output space is unconstrained in scale, and could grow arbitrarily to try to "escape" quantization error or keep switching which codebook vector it's near. This term penalizes the encoder for producing outputs far from the codebook vector it's assigned to — it makes the encoder "commit" to a codebook entry rather than fluctuating. Gradient flows only into the encoder here (codebook vector is stop-gradiented). $\beta$ is a hyperparameter (paper uses $\beta = 0.25$; result is fairly insensitive to exact value in range 0.1–2.0).
    

**Important nuance**: many later implementations (and often EMA-based ones, see below) replace the codebook loss with an **exponential moving average (EMA) update** of the codebook instead of backpropagating through it — this tends to be more stable (see Section 5).

---

## 4. Gradient Propagation — the Straight-Through Estimator (STE)

This is the trickiest and most important part of VQ-VAE.

**Problem**: the mapping $z_e(x) \to z_q(x)$ via nearest-neighbor lookup is a hard `argmin` — it's a discrete, piecewise-constant function. Its true gradient is zero almost everywhere (and undefined at the boundaries), so you cannot backpropagate reconstruction loss through it to train the encoder normally.

**Solution — Straight-Through Estimator**: on the backward pass, VQ-VAE simply **copies the gradient from $z_q(x)$ directly to $z_e(x)$**, as if quantization were the identity function. Formally, in the forward pass you compute:

$$ z_q(x) = z_e(x) + \text{sg}[z_q(x) - z_e(x)] $$

- **Forward pass**: this evaluates to exactly $z_q(x)$ (the quantized vector), since `sg[·]` is identity in forward mode.
- **Backward pass**: since the `sg[...]` term has zero gradient, $\partial z_q(x) / \partial z_e(x) = I$ (identity), so whatever gradient $\hat{x}$'s reconstruction loss sends to $z_q(x)$ is passed straight through, unchanged, to $z_e(x)$ — hence the encoder receives a training signal even though the operation it went through was non-differentiable.

This is a **biased gradient estimator** (it's an approximation, not the true gradient of the argmin), but empirically it works well because nearby codebook vectors have similar decoder outputs, so the approximation error is small in practice.

So overall gradient flow per term:

|Loss term|Gradient flows into|
|---|---|
|Reconstruction loss|Encoder (via STE) + Decoder (normal backprop)|
|Codebook loss|Codebook vectors only|
|Commitment loss|Encoder only|

---

## 5. Training Procedure

1. Forward pass: $x \to E \to z_e(x)$, quantize to get $z_q(x)$ and the associated codebook indices.
2. Decode: $z_q(x) \to D \to \hat{x}$.
3. Compute the three-term loss above.
4. Backward pass:
    - Reconstruction gradient flows through decoder normally, then via STE straight into the encoder (skipping the quantization step).
    - Codebook loss gradient updates only the codebook.
    - Commitment loss gradient updates only the encoder.
5. Update encoder, decoder, and codebook (all jointly, single optimizer, single training loop — end-to-end, no separate stages needed for the base VQ-VAE itself).

### EMA codebook updates (common alternative, used in the original paper as an option and standard in most later work e.g. VQ-VAE-2, VQGAN)

Instead of the codebook loss term with gradient descent, update each codebook vector as an EMA of the encoder outputs assigned to it (like online k-means / mini-batch k-means):
$$ N_k^{(t)} = \gamma N_k^{(t-1)} + (1-\gamma) n_k^{(t)}, \qquad m_k^{(t)} = \gamma m_k^{(t-1)} + (1-\gamma) \sum_i z_{e,i}(x) $$$$ e_k^{(t)} = m_k^{(t)} / N_k^{(t)} $$
where $n_k^{(t)}$ is the count of encoder vectors assigned to code $k$ in the current batch. This tends to converge faster and more stably than gradient-based codebook updates.

### Second-stage prior training (why VQ-VAE is a two-stage pipeline in practice)
But sadly, the learnt codebook of the VQ-VAE(prior) is not structured enough to be used effectively by the decoder that we trained atleast for arbitrary input of codebook vectors into something meaningful.

Hence we use something like transformers or the PixelCNN to learn a seperate decoder for a our generation purpose. After the VQ-VAE is trained, the discrete latent codes for the training set are extracted, and a separate **autoregressive prior** (PixelCNN for images, WaveNet for audio, Transformer in later work) is trained over the discrete code sequence itself. Sampling: sample codes from the prior → look up embeddings → decode. This is what makes VQ-VAE generative rather than just a discrete autoencoder — the base VQ-VAE alone doesn't give you a way to sample _new_ latents, only to encode/decode.

---

## 6. Benefits

- **Avoids posterior collapse**: because the latent is discrete and the decoder is not given a free continuous knob it can learn to ignore in the same way, and the commitment loss explicitly ties encoder output to actual codebook usage.
- **Compact, symbolic representation**: turns images/audio into sequences of discrete tokens — same representation format as language, enabling reuse of powerful sequence models (Transformers, autoregressive priors) as generative priors.
- **High compression + high fidelity**: because decoder capacity isn't bottlenecked by forcing a simple prior (unlike vanilla VAE, where the ELBO forces the aggregate posterior toward a fixed simple prior at some fidelity cost), VQ-VAE reconstructions tend to be sharper.
- **Scalability**: this discrete-tokenization idea generalizes directly — VQ-VAE-2 (hierarchical, multi-scale codebooks), VQGAN (adds adversarial + perceptual loss for photorealism), and it underlies token-based generation in DALL-E, and many modern image/audio/video tokenizers used before autoregressive or diffusion generation.
- **No need for reparameterization trick**: unlike Gaussian VAEs, there's no need to sample from a stochastic continuous distribution during training — the quantization is deterministic given the encoder output, and STE handles the gradient issue directly.

---

## 7. Known Failure Modes / Practical Tricks

- **Codebook collapse**: only a small subset of the $K$ codebook vectors ever get used ("dead codes"), wasting capacity. Common fixes:
    - Re-initialize or randomly reset dead codes periodically (reset unused codes to a randomly sampled encoder output from the current batch).
    - Use EMA updates (tends to reduce collapse vs. pure gradient descent on codebook loss).
    - k-means initialization of the codebook instead of random init.
- **Choice of $K$ (codebook size) and $D$ (embedding dim)**: too small $K$ → poor reconstruction (not enough discrete "vocabulary"); too large $K$ → many dead codes, harder to learn a good prior over codes later.
- **Commitment loss weight $\beta$**: too low → encoder outputs drift, unstable quantization boundaries; too high → discourages encoder from exploring, can hurt reconstruction quality.

---

## 8. Quick Comparison: VAE vs VQ-VAE

||VAE|VQ-VAE|
|---|---|---|
|Latent type|Continuous|Discrete (codebook index)|
|Prior|Fixed (e.g. $\mathcal{N}(0,I)$), used directly in ELBO|Learned separately, post-hoc (PixelCNN/Transformer)|
|Reparameterization|Needed (sampling trick)|Not needed (deterministic quantization)|
|Main failure mode|Posterior collapse|Codebook collapse|
|Non-differentiability handled by|N/A|Straight-through estimator|
|Typical use today|Density estimation, small-scale generative modeling|Tokenizer stage for downstream AR/diffusion generative models|

---

## 9. Key Equation Summary

$$ z_q(x) = e_k, \quad k = \arg\min_j |z_e(x) - e_j|_2 $$

$$ \mathcal{L} = |x - \hat{x}|_2^2 + |\text{sg}[z_e(x)] - e|_2^2 + \beta|z_e(x) - \text{sg}[e]|_2^2 $$

$$ \text{STE: } z_q(x) = z_e(x) + \text{sg}[z_q(x) - z_e(x)] \quad \Rightarrow \quad \frac{\partial \mathcal{L}}{\partial z_e(x)} := \frac{\partial \mathcal{L}}{\partial z_q(x)} $$

---

_Related directions worth cross-linking in your vault: VQ-VAE-2 (hierarchical codebooks), VQGAN (adversarial + perceptual loss, used in taming transformers), dVAE (DALL-E's Gumbel-softmax based discretization — an alternative to STE worth contrasting), FSQ (finite scalar quantization — a newer, simpler alternative to VQ that avoids codebook collapse entirely)._