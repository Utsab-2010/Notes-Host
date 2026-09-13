---
title: "Training Stabilization in Machine Learning"
lastmod: 2026-07-30
---

> A comprehensive reference on the techniques that keep neural networks from blowing up, collapsing, or memorizing noise.

---

## 1. Why Training Goes Wrong

Before diving into solutions, it helps to understand the failure modes you're defending against.

### The Core Problem: The Loss Landscape

A neural network's loss landscape is a high-dimensional surface, and gradient descent is trying to find its valleys. Training goes wrong when:

|Failure Mode|What's Happening|Symptom|
|---|---|---|
|**Overfitting**|Network memorizes training data|Train loss ↓↓, val loss ↑|
|**Underfitting**|Model lacks capacity or trains poorly|Both losses stay high|
|**Exploding gradients**|Gradients grow exponentially through layers|Loss becomes NaN or inf|
|**Vanishing gradients**|Gradients shrink to zero through layers|Early layers don't learn|
|**Dead neurons**|ReLU neurons stuck at zero, never activate|Effective capacity drops|
|**Covariate shift**|Distribution of activations shifts during training|Slow/unstable convergence|
|**Sharp minima**|Model finds a narrow valley that doesn't generalize|Good train, bad test|
|**Mode collapse**|Model outputs same thing regardless of input|Common in GANs|

Training stabilization techniques attack these failure modes. Most techniques address more than one simultaneously.

### The Bias-Variance Tradeoff (revisited)

Every stabilization technique is fundamentally navigating this tradeoff:

- **High variance** → model is too sensitive to training data → need regularization
- **High bias** → model is too constrained → need more capacity or less regularization
- The goal: find the sweet spot where the model is complex enough to learn the signal but constrained enough to not learn the noise

---

## 2. Regularization

Regularization is the family of techniques that add a **penalty** to the loss function to discourage the model from fitting noise.

### 2.1 L2 Regularization (Weight Decay)

**The idea:** Add a penalty proportional to the _square_ of each weight. Large weights get penalized more.

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \frac{\lambda}{2} \sum_i w_i^2$$

**What happens during gradient descent:**

Each weight update becomes:

$$w \leftarrow w - \eta \frac{\partial \mathcal{L}}{\partial w} - \eta \lambda w$$

The extra $-\eta \lambda w$ term _decays_ the weight toward zero each step — hence the name **weight decay**. Weights only survive if the gradient signal is strong enough to overcome this decay.

**Geometric interpretation:** L2 constrains weights to live in a _sphere_ around the origin. The solution is pulled toward the center.

**Effect on singular values:** L2 regularization effectively shrinks all singular values of weight matrices toward zero — same structure as the Ridge regression modification we saw in SVD.

**Practical notes:**

- Most common regularization in deep learning
- In modern frameworks, `weight_decay` in the optimizer (e.g., `AdamW`) is not identical to adding L2 to the loss when using adaptive optimizers — AdamW decouples the decay from the gradient scaling, which is correct
- Typical values: $\lambda \in [10^{-4}, 10^{-2}]$
- **Don't apply to biases or normalization layer parameters**

```python
# PyTorch: weight decay in AdamW (preferred)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

# Manual L2 in loss (less common in deep learning)
l2_penalty = sum(p.pow(2).sum() for p in model.parameters())
loss = criterion(output, target) + lambda_ * l2_penalty
```

---

### 2.2 L1 Regularization (Lasso)

**The idea:** Penalty proportional to the _absolute value_ of each weight.

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda \sum_i |w_i|$$

**The key difference from L2:** L1 pushes weights all the way to _exactly zero_. This produces **sparse** solutions — many weights become zero.

**Why sparsity?** Geometrically, L1 constrains weights to a _diamond_ (L1 ball). The corners of the diamond align with the axes, so optimal solutions tend to land on corners where some coordinates are exactly zero.

**Use cases:**

- Feature selection: zero weights = irrelevant features
- Interpretability: sparse models are easier to analyze
- Less common in deep learning than in traditional ML (lasso regression, sparse coding)

**Practical note:** L1 is not differentiable at zero. In practice you use subgradients or smooth approximations.

---

### 2.3 Elastic Net

Combines L1 and L2:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda_1 \sum_i |w_i| + \frac{\lambda_2}{2} \sum_i w_i^2$$

Gets the sparse solutions of L1 while keeping the numerical stability of L2. Useful when you have correlated features (L1 tends to pick one arbitrarily; Elastic Net can keep groups).

---

### 2.4 Max-Norm Constraint

Instead of penalizing large weights in the loss, directly **clip** the weight norms:

$$|w|_2 \leq c$$

After each gradient step, if any weight vector's norm exceeds $c$, rescale it back:

$$w \leftarrow w \cdot \frac{c}{|w|_2}$$

Often used in conjunction with dropout (original Dropout paper used this). Less common today but still appears in some NLP and RL settings.

---

## 3. Dropout and Its Variants

### 3.1 Standard Dropout

**The idea (Srivastava et al., 2014):** During training, randomly set each neuron's output to zero with probability $p$ (the "dropout rate"). At test time, use all neurons but scale outputs by $(1-p)$.

$$h_i^{\text{train}} = \begin{cases} \frac{a_i}{1-p} & \text{with probability } 1-p \ 0 & \text{with probability } p \end{cases}$$

The division by $(1-p)$ is **inverted dropout** — it keeps the expected value of the output the same, so you don't need to rescale at test time. This is what modern frameworks implement.

**Why does it work?**

Several complementary explanations:

1. **Ensemble interpretation:** Each forward pass uses a different sub-network (there are $2^n$ possible masks for $n$ neurons). Dropout trains an exponentially large ensemble and approximates averaging them at test time.
    
2. **Co-adaptation prevention:** Neurons can't rely on specific other neurons always being present, so they learn more independent, robust features.
    
3. **Noise injection:** Adding multiplicative Bernoulli noise forces the network to learn features that work even under noise — a form of robustness training.
    
4. **Implicit regularization:** Dropout adds noise proportional to the magnitude of activations, which implicitly penalizes large activations.
    

**When to apply dropout:**

- After fully connected layers: yes, heavily
- After convolutional layers: yes, but use Spatial Dropout (see 3.3)
- After attention layers (Transformers): yes, on attention weights and MLP outputs
- On very small datasets: high dropout (0.5–0.7)
- On large datasets: lower dropout (0.1–0.3) or skip

**What dropout doesn't fix:**

- Doesn't help much if you're _underfitting_
- Interacts poorly with Batch Normalization (because BN estimates statistics over the batch, dropout changes those statistics)

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(512, 256),
    nn.ReLU(),
    nn.Dropout(p=0.5),  # 50% dropout
    nn.Linear(256, 10)
)
# Dropout automatically activates in train mode and deactivates in eval mode
model.train()   # dropout ON
model.eval()    # dropout OFF
```

---

### 3.2 DropConnect

**Variant:** Instead of dropping neuron _outputs_, drop individual _weights_ randomly.

$$h = (W \odot M) x \quad M_{ij} \sim \text{Bernoulli}(1-p)$$

More granular than standard dropout. Theoretically cleaner (it's truly an ensemble over weight subsets) but computationally more expensive. Rarely used in practice — standard dropout is simpler and nearly as effective.

---

### 3.3 Spatial Dropout (2D Dropout)

For **convolutional networks**, standard dropout drops individual pixels — but adjacent pixels in feature maps are highly correlated, so this doesn't remove much information.

**Spatial Dropout** drops entire _channels_ (feature maps) at once. If a channel is dropped, the entire spatial slice is zeroed out.

This forces convolutional features to be redundant across channels, which is the right inductive bias for conv nets.

```python
nn.Dropout2d(p=0.2)  # drops entire channels
```

---

### 3.4 Variational Dropout

Frames dropout in a Bayesian framework. Instead of a fixed dropout mask per forward pass, learn the dropout _rate_ $\alpha_i$ for each weight. Weights with high learned dropout rates are effectively pruned.

Can be used for **automatic model compression** — you train the network, then prune weights whose learned dropout rate is high.

---

### 3.5 Monte Carlo Dropout (MC Dropout)

**A test-time trick (Gal & Ghahramani, 2016):** Keep dropout ON at test time and run $T$ forward passes. The variance across outputs gives an **uncertainty estimate**.

$$\text{prediction} = \frac{1}{T} \sum_{t=1}^T f_{\theta, m_t}(x)$$

$$\text{uncertainty} \approx \text{Var}_{t}\left[f_{\theta, m_t}(x)\right]$$

This turns any dropout network into an approximate Bayesian neural network. Extremely cheap to implement — no architecture changes needed.

Useful when you care about knowing when the model doesn't know (medical imaging, robotics, autonomous driving).

---

## 4. Normalization Layers

Normalization layers standardize the distribution of activations during training, attacking **internal covariate shift** — the problem that each layer's input distribution keeps changing as upstream weights update.

### 4.1 Batch Normalization (BatchNorm)

**The idea (Ioffe & Szegedy, 2015):** For each mini-batch, normalize each feature to have zero mean and unit variance, then apply learnable scale $\gamma$ and shift $\beta$.

**During training**, for a mini-batch ${x_1, \ldots, x_B}$:

$$\mu_B = \frac{1}{B}\sum_{i=1}^B x_i, \quad \sigma_B^2 = \frac{1}{B}\sum_{i=1}^B (x_i - \mu_B)^2$$

$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta$$

**During inference**, use the **running mean and variance** accumulated during training (exponential moving average), not the batch statistics.

**Why it works:**

1. **Reduces sensitivity to initialization** — gradients flow more smoothly
2. **Allows higher learning rates** — the normalization prevents activations from growing too large
3. **Acts as regularization** — the noise from batch statistics has a regularizing effect (similar to dropout, but milder)
4. **Smoother loss landscape** — makes the loss surface more predictable for SGD

**Drawbacks:**

- Requires large enough batch sizes (≥ 8, ideally ≥ 32) for stable statistics
- Fails on very small batches and single-sample inference
- Behavior differs between train and eval modes — a common bug source
- Interacts badly with dropout in some configurations
- Not suitable for RNNs or Transformers (use LayerNorm instead)

```python
nn.BatchNorm2d(num_features=64)  # for conv layers
nn.BatchNorm1d(num_features=256)  # for FC layers
```

---

### 4.2 Layer Normalization (LayerNorm)

**The idea (Ba et al., 2016):** Normalize across the _feature dimension_ for each sample independently, rather than across the batch.

$$\hat{x} = \frac{x - \mu_{\text{layer}}}{\sigma_{\text{layer}} + \epsilon}, \quad y = \gamma \hat{x} + \beta$$

where $\mu_{\text{layer}}$ and $\sigma_{\text{layer}}$ are computed over all features of a single sample.

**Key difference from BatchNorm:** No dependence on other samples in the batch. Statistics computed per-sample, not per-batch.

**Where it's used:**

- **Transformers:** Standard choice (used in GPT, BERT, ViT, LLaMA — essentially every modern LLM/vision transformer)
- **RNNs:** Works well because it's sequence-position agnostic
- **Any setting with variable batch sizes or sequence lengths**

**Pre-norm vs Post-norm:**

Original Transformer used Post-norm (LayerNorm _after_ residual addition). Modern LLMs use Pre-norm (LayerNorm _before_ the sublayer):

```
Post-norm: x → Sublayer(x) → x + Sublayer(x) → LayerNorm(...)
Pre-norm:  x → LayerNorm(x) → Sublayer(LayerNorm(x)) → x + ...
```

Pre-norm is more stable and is now the default in most architectures.

---

### 4.3 Instance Normalization

Normalizes each sample _and_ each channel independently. No inter-channel or inter-sample statistics.

Used almost exclusively in **style transfer** — the channel-wise normalization aligns well with the style statistics (Gram matrices) that style transfer manipulates.

---

### 4.4 Group Normalization

**The idea (Wu & He, 2018):** Divide channels into $G$ groups, normalize within each group.

Interpolates between LayerNorm ($G=1$) and InstanceNorm ($G=C$). Works well for medium batch sizes and is used in detection/segmentation models (e.g., Mask R-CNN, DETR).

```python
nn.GroupNorm(num_groups=32, num_channels=256)
```

---

### 4.5 RMS Norm

A simplified LayerNorm used in modern LLMs (LLaMA, Mistral, Gemma):

$$\hat{x}_i = \frac{x_i}{\text{RMS}(x) + \epsilon} \cdot \gamma_i, \quad \text{RMS}(x) = \sqrt{\frac{1}{n}\sum_j x_j^2}$$

Drops the mean-centering step (subtracting $\mu$). Slightly faster, empirically equivalent to LayerNorm in practice.

---

### 4.6 When to Use Which

|Setting|Recommended Norm|
|---|---|
|CNNs, large batches|BatchNorm|
|CNNs, small batches / detection|GroupNorm|
|Transformers / LLMs|LayerNorm or RMSNorm|
|RNNs|LayerNorm|
|Style transfer|InstanceNorm|
|Single-sample inference|LayerNorm, GroupNorm, or InstanceNorm|

---

## 5. Gradient Management

### 5.1 Gradient Clipping

**The problem:** In deep networks or RNNs, gradients can grow exponentially through backpropagation (the "exploding gradients" problem). A single large gradient can overwrite everything the model has learned.

**Two forms:**

**Norm clipping (most common):** If the global gradient norm exceeds threshold $\tau$, scale all gradients down:

$$g \leftarrow g \cdot \frac{\tau}{|g|_2} \quad \text{if } |g|_2 > \tau$$

**Value clipping:** Clip each gradient component individually to $[-\tau, \tau]$. Less principled — it changes gradient direction. Avoid for most applications.

```python
# After loss.backward(), before optimizer.step()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

**When to use:**

- RNNs / LSTMs: almost always (gradients through long sequences explode easily)
- Transformers: often used with max_norm=1.0
- CNNs with BatchNorm: usually not needed (BN stabilizes gradients)
- RL: frequently needed (off-policy updates can produce large gradients)

**Monitoring:** Log `grad_norm` before clipping. If clipping fires every step, your learning rate is probably too high.

---

### 5.2 Gradient Accumulation

**The problem:** You want to train with a large effective batch size, but GPU memory limits you to small batches.

**The solution:** Accumulate gradients over $k$ mini-batches before stepping:

```python
accumulation_steps = 4
optimizer.zero_grad()

for i, (inputs, targets) in enumerate(dataloader):
    outputs = model(inputs)
    loss = criterion(outputs, targets) / accumulation_steps
    loss.backward()  # gradients accumulate in .grad

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

Effective batch size = `batch_size × accumulation_steps`. This is how LLMs are trained with effective batch sizes of millions of tokens on limited hardware.

**Gotcha:** If using BatchNorm, stats are computed on each sub-batch, not the accumulated batch. Consider switching to GroupNorm or LayerNorm.

---

### 5.3 Gradient Checkpointing

**The problem:** Backpropagation requires storing all intermediate activations in memory (for the chain rule). For deep networks, this can be prohibitively expensive.

**The solution:** Don't store intermediate activations — recompute them during backpropagation.

Trade-off: ~33% more compute for ~√N memory savings (where N is number of layers).

```python
from torch.utils.checkpoint import checkpoint

# Instead of:
out = layer(x)

# Use:
out = checkpoint(layer, x)  # recomputes layer(x) during backward
```

Essential for training very deep networks or long sequences (e.g., long-context LLMs).

---

## 6. Weight Initialization

### 6.1 Why Initialization Matters

Before training begins, the initial weights determine:

- Whether gradients vanish or explode in the first backward pass
- How quickly the network starts learning
- Whether neurons are differentiated enough to learn different features

If all weights start at the same value, all neurons in a layer are identical — they compute the same thing and receive the same gradients. They'll always be identical (**symmetry breaking problem**). Random initialization breaks this symmetry.

If weights are too large: activations saturate (especially with sigmoid/tanh), gradients vanish.  
If weights are too small: signals diminish layer by layer, gradients also vanish.

---

### 6.2 Xavier / Glorot Initialization

**For: sigmoid, tanh, linear activations**

Designed to keep variance constant across layers during both forward and backward passes.

For a layer with $n_{\text{in}}$ inputs and $n_{\text{out}}$ outputs:

$$W \sim \mathcal{U}!\left[-\frac{\sqrt{6}}{\sqrt{n_{\text{in}} + n_{\text{out}}}},\ \frac{\sqrt{6}}{\sqrt{n_{\text{in}} + n_{\text{out}}}}\right]$$

or equivalently from a normal distribution with variance:

$$\text{Var}(W) = \frac{2}{n_{\text{in}} + n_{\text{out}}}$$

**Intuition:** Scale weights so the variance of the output equals the variance of the input.

---

### 6.3 He Initialization (Kaiming)

**For: ReLU and its variants (Leaky ReLU, ELU, GELU)**

Xavier doesn't account for the fact that ReLU kills half the neurons (negative inputs → zero output). He initialization corrects for this:

$$\text{Var}(W) = \frac{2}{n_{\text{in}}}$$

The factor of 2 compensates for the half of activations that ReLU zeroes out.

```python
# PyTorch default for Linear layers is Kaiming Uniform
nn.init.kaiming_normal_(layer.weight, mode='fan_in', nonlinearity='relu')
nn.init.kaiming_normal_(layer.weight, mode='fan_out', nonlinearity='relu')
# fan_in: preserves variance of forward pass
# fan_out: preserves variance of backward pass
```

---

### 6.4 Orthogonal Initialization

Initialize weight matrices to be orthogonal (via QR decomposition or SVD of a random Gaussian matrix).

$$W = Q \quad \text{where } Q^T Q = I$$

Orthogonal matrices preserve vector norms: $|Wx|_2 = |x|_2$. This prevents both exploding and vanishing across layers.

Particularly useful for:

- Deep linear networks
- RNNs (helps with long-range dependencies)
- Deep networks where you want to train for many iterations before the signal degrades

---

## 7. Learning Rate Scheduling

The learning rate is the most important hyperparameter. Schedules systematically change it during training.

### 7.1 Step Decay

Multiply LR by a factor $\gamma < 1$ every $k$ epochs:

$$\eta_t = \eta_0 \cdot \gamma^{\lfloor t/k \rfloor}$$

Simple and effective. Classic choice for ResNets trained on ImageNet (reduce LR by 10× at epoch 30 and 60, for 90 total epochs). The downside is you have to manually choose the decay points.

---

### 7.2 Cosine Annealing

Smoothly decay LR following a cosine curve from $\eta_{\max}$ to $\eta_{\min}$:

$$\eta_t = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min})\left(1 + \cos\frac{\pi t}{T}\right)$$

The smooth decay avoids the abrupt drops of step decay. Very widely used — ViT, DINO, SimCLR, most self-supervised methods use cosine schedules.

**Cosine with Warm Restarts (SGDR):** After each cycle, reset LR to $\eta_{\max}$ and restart. Helps escape local minima and encourages exploration.

---

### 7.3 Warmup

Start with a very small LR and increase it linearly (or as a square root) for the first $W$ steps:

$$\eta_t = \eta_{\max} \cdot \frac{t}{W} \quad \text{for } t \leq W$$

**Why warmup is necessary for Transformers and large models:**

At initialization, weight matrices are random and the gradient estimates are noisy. Taking large steps immediately causes instability. Warmup lets the model first establish a reasonable loss landscape before taking large gradient steps.

- Small models / CNNs: warmup optional, but helps
- Transformers: warmup is essentially mandatory
- LLMs: warmup over 1–5% of total training steps is standard

---

### 7.4 Cyclical LR / OneCycleLR

**Cyclical LR (Smith, 2017):** Oscillate LR between a minimum and maximum in a cycle. Instead of monotonically decreasing, keep bumping the LR up and down.

**OneCycleLR:** Start at $\eta_{\min}$, ramp up to $\eta_{\max}$ for the first 30% of training, then anneal back down to $\eta_{\min}/10$ for the remaining 70%.

The counterintuitive finding: temporarily _increasing_ the LR can help escape sharp minima and find flatter, better-generalizing solutions.

---

### 7.5 Linear Decay (LLMs)

The standard for LLM training: linear warmup then linear decay to 0.

```
LR: 0 → peak (warmup) → 0 (linear decay over full training)
```

Simple, predictable, works well at scale. GPT-2, LLaMA, and most LLMs use this.

---

## 8. Data-Level Stabilization

Sometimes the most effective regularization isn't in the model — it's in how you present data.

### 8.1 Data Augmentation

Transform training inputs randomly so the model sees more diverse examples:

|Domain|Common Augmentations|
|---|---|
|Images|Random crop, flip, color jitter, rotation, Gaussian blur|
|Audio|Time stretching, pitch shift, SpecAugment (mask frequency/time)|
|Text|Random deletion, synonym replacement, back-translation|
|Tabular|Gaussian noise, feature dropout, SMOTE|

**Strong augmentation (for self-supervised / contrastive learning):** Methods like SimCLR and DINO use aggressive augmentation (large crops, heavy color jitter, grayscale conversion) because the training signal comes from the network recognizing two views as the same image.

**RandAugment:** Randomly select $n$ augmentations from a library and apply them at magnitude $m$. State-of-the-art for supervised image classification.

---

### 8.2 Mixup and CutMix

**Mixup (Zhang et al., 2018):** Blend two training examples and their labels:

$$\tilde{x} = \lambda x_i + (1-\lambda) x_j, \quad \tilde{y} = \lambda y_i + (1-\lambda) y_j \quad \lambda \sim \text{Beta}(\alpha, \alpha)$$

Creates convex combinations of training examples. Forces the network to predict a mix of labels for a mix of inputs, discouraging overconfident predictions and encouraging linear behavior between training points.

**CutMix (Yun et al., 2019):** Instead of blending pixels, cut a rectangular patch from one image and paste it onto another. Labels are mixed proportionally to the area of each image used.

CutMix is generally stronger than Mixup for vision tasks because it creates more realistic local patches.

Both are standard in modern image training recipes and are part of the ImageNet training recipe used for ViTs.

---

### 8.3 Label Smoothing

**The problem with hard labels:** One-hot labels push the model toward infinite logits (to make softmax → 1.0 for the correct class). This overconfidence hurts generalization.

**Label smoothing:** Replace hard labels with a soft distribution:

$$y_{\text{smooth}} = (1-\epsilon) \cdot y_{\text{hard}} + \frac{\epsilon}{K}$$

where $K$ is the number of classes and $\epsilon$ is typically 0.1.

Instead of training the correct class to probability 1.0, you train it to probability $1 - \epsilon + \epsilon/K \approx 0.9$, and all other classes to $\epsilon/K \approx 0.01$.

**Effects:**

- Prevents logits from growing without bound
- Encourages the model to maintain some uncertainty
- Acts as a regularizer, improving calibration
- Standard in Transformers (machine translation, LLMs) and modern image classifiers

---

## 9. Loss Function Design

### 9.1 Cross-Entropy and Numerical Stability

The standard cross-entropy loss for classification:

$$\mathcal{L} = -\sum_k y_k \log p_k$$

**Numerical issue:** Computing $p = \text{softmax}(z)$ then $\log(p)$ can cause numerical overflow (if logits are large) or underflow (if probabilities are very small).

**The fix:** Use `log_softmax` which computes $\log(\text{softmax}(z))$ in a numerically stable way:

$$\log \text{softmax}(z_k) = z_k - \log\sum_j e^{z_j} = z_k - \left(z_{\max} + \log\sum_j e^{z_j - z_{\max}}\right)$$

Subtracting $z_{\max}$ before exponentiation prevents overflow. Always use `nn.CrossEntropyLoss()` in PyTorch (which does this internally) rather than computing softmax and log separately.

---

### 9.2 Focal Loss

**The problem:** Class imbalance. If 99% of examples are class A, the model learns to always predict A and achieves 99% accuracy without learning anything useful.

**Focal loss (Lin et al., 2017):** Down-weight easy examples, focus training on hard ones:

$$\mathcal{L}_{\text{focal}} = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$

- $p_t$: probability assigned to the correct class
- $(1-p_t)^\gamma$: the **focusing factor** — reduces loss for well-classified examples
- $\gamma = 2$ is typical
- When $p_t \approx 1$ (easy example): $(1-p_t)^2 \approx 0$, loss is nearly zero
- When $p_t \approx 0$ (hard example): factor ≈ 1, full loss

Originally developed for object detection (RetinaNet) where background patches vastly outnumber objects. Now widely used in any class-imbalanced setting.

---

### 9.3 Huber Loss

For regression tasks, MSE ($L_2$ loss) is sensitive to outliers because errors are squared. MAE ($L_1$ loss) is robust but non-differentiable at 0.

**Huber loss** combines both:

$$\mathcal{L}_\delta(r) = \begin{cases} \frac{1}{2}r^2 & \text{if } |r| \leq \delta \ \delta(|r| - \frac{\delta}{2}) & \text{otherwise} \end{cases}$$

- Quadratic (like MSE) for small errors → smooth gradients near zero
- Linear (like MAE) for large errors → robustness to outliers

Used in: regression tasks with outliers, RL (Q-learning loss), depth estimation.

---

## 10. Early Stopping

**The simplest regularization:** Stop training when validation loss stops improving.

**Algorithm:**

1. Monitor validation loss after each epoch
2. Keep track of the best validation loss seen so far
3. If validation loss doesn't improve for `patience` epochs, stop and restore the best checkpoint

```python
best_val_loss = float('inf')
patience = 10
counter = 0

for epoch in range(max_epochs):
    train(...)
    val_loss = evaluate(...)

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        save_checkpoint(model)
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping!")
            load_checkpoint(model)
            break
```

**Why it works:** Overfit models usually start with decreasing validation loss (learning the true signal) then increasing (memorizing noise). Early stopping catches the model at the sweet spot.

**Practical tips:**

- Don't stop too early — use `patience ≥ 5–10` epochs
- Monitor the _right_ metric (validation F1 or AUC, not just loss, for imbalanced problems)
- Learning rate schedules interact with early stopping — a LR drop might rescue a plateau

---

## 11. Ensemble Methods as Regularizers

### Snapshot Ensembles

Train one model with cosine warm restarts. Save checkpoints at each LR cycle minimum. Average predictions of saved checkpoints at test time.

Free ensemble — no extra training cost.

### Stochastic Weight Averaging (SWA)

Toward the end of training, average model weights across multiple SGD iterates:

$$w_{\text{SWA}} = \frac{1}{T} \sum_{t=1}^T w_t$$

The averaged weights typically land in flatter, wider minima than any single iterate. Consistently improves generalization by 0.5–2% across tasks. Almost free to implement.

```python
from torch.optim.swa_utils import AveragedModel, SWALR

swa_model = AveragedModel(model)
swa_scheduler = SWALR(optimizer, swa_lr=0.05)

for epoch in range(swa_start, total_epochs):
    train(model)
    swa_model.update_parameters(model)
    swa_scheduler.step()

# Update BN stats for the averaged model
torch.optim.swa_utils.update_bn(train_loader, swa_model)
```

---

## 12. Modern / Advanced Techniques

### 12.1 Stochastic Depth (Drop Path)

**For: deep networks (ResNets, ViTs)**

During training, randomly skip entire residual blocks:

$$\text{output} = x + \text{Block}(x) \cdot m \quad m \sim \text{Bernoulli}(1-p_l)$$

where $p_l$ is the drop probability for layer $l$ (linearly increases with depth — deeper layers are dropped more often).

- Reduces effective depth during training → trains as if it were a distribution of shallower networks
- Acts like Dropout but at the layer level
- Improves training speed and generalization for very deep networks
- Standard in ViT training recipes (DeiT, DINOv2 use it with drop_path_rate ≈ 0.1–0.4)

---

### 12.2 LayerScale

**For: deep ViTs**

Training very deep ViTs (24+ layers) is unstable. LayerScale adds a learnable diagonal scaling matrix $\Lambda$ (initialized to very small values, e.g., $10^{-4}$ or $10^{-5}$) to each residual branch:

$$\text{output} = x + \Lambda \cdot \text{Block}(x)$$

At initialization, $\Lambda \approx 0$, so the network starts as nearly an identity function. As training progresses, layers gradually learn to contribute. This enables training 24–36 layer ViTs stably.

---

### 12.3 Exponential Moving Average (EMA) of Weights

Maintain a shadow copy of the model that tracks a moving average of weights:

$$\theta_{\text{EMA}} \leftarrow m \cdot \theta_{\text{EMA}} + (1-m) \cdot \theta \quad m \in [0.99, 0.9999]$$

At inference, use $\theta_{\text{EMA}}$ rather than the current weights.

**Why it works:** The EMA model is smoother and lands in a flatter region of the loss landscape. The current model may be oscillating around a minimum; the EMA tracks the center of those oscillations.

Used in: DINO, BYOL, many diffusion models, detection models. Critical for self-supervised methods where the EMA model serves as a teacher.

---

### 12.4 Sharpness-Aware Minimization (SAM)

**The insight (Foret et al., 2021):** Generalization correlates with the _flatness_ of the minimum — not just its depth. A flat minimum (low loss over a neighborhood) generalizes better than a sharp one.

**SAM's approach:** Instead of minimizing loss at the current point, minimize the _worst-case loss in a neighborhood_:

$$\min_w \max_{|\epsilon|_2 \leq \rho} \mathcal{L}(w + \epsilon)$$

**Two-step update:**

1. Compute the perturbation $\hat{\epsilon}$ that maximizes the loss in the ball of radius $\rho$ (one gradient step up)
2. Compute gradient at the perturbed point and update original weights

```python
# SAM optimizer step
predictions = model(inputs)
loss = criterion(predictions, targets)
loss.backward()
optimizer.first_step(zero_grad=True)   # step to worst-case neighbor

predictions = model(inputs)
criterion(predictions, targets).backward()
optimizer.second_step(zero_grad=True)  # step with gradient at perturbed point
```

SAM consistently improves generalization across tasks and is especially effective in fine-tuning scenarios. Cost: 2× the compute of standard SGD per step.

---

### 12.5 Gradient Noise Injection

Add Gaussian noise to gradients during training:

$$g_t \leftarrow g_t + \mathcal{N}(0, \sigma_t^2 I), \quad \sigma_t^2 = \frac{\eta}{(1+t)^{0.55}}$$

Helps escape sharp minima and saddle points. Can also be viewed as a form of implicit regularization. Used in some RL training pipelines and occasionally in LLM fine-tuning.

---

## 13. Diagnosing Training Instability

When your training is misbehaving, here's a systematic diagnosis framework:

### Is the loss NaN or Inf?

1. Check for **exploding gradients** → add gradient clipping
2. Check for **log of zero** in loss → add numerical stability (epsilon, log_softmax)
3. Check for **very large learning rate** → reduce LR
4. Check for **bad data** (NaN in inputs) → add data validation

### Is validation loss diverging from train loss?

→ **Overfitting**

Fix priority: More data → Data augmentation → Dropout → Weight decay → Reduce model size → Early stopping

### Are both losses stuck high?

→ **Underfitting** or optimization failure

Fix priority: Increase LR → Increase model capacity → Better initialization → Reduce regularization → Check for bugs in data pipeline

### Are gradients dying (near zero in early layers)?

→ **Vanishing gradients**

Fix priority: Use residual connections → Switch to ReLU/GELU → Better initialization (He) → Add normalization → Reduce depth

### Are gradients exploding?

→ **Exploding gradients**

Fix priority: Gradient clipping → Reduce LR → Add normalization → Check for activation saturation

### Is training very noisy / oscillating?

→ **LR too high** or **batch size too small**

Fix priority: Reduce LR → Increase batch size → Add LR warmup → Use gradient accumulation

### Useful things to monitor

```python
# Log these every N steps
- train_loss, val_loss
- grad_norm (before clipping)
- weight_norm (for each layer)
- activation_mean, activation_std (per layer)
- learning_rate (especially with schedules)
- GPU memory usage
```

Tools: TensorBoard, Weights & Biases (wandb), custom matplotlib plots.

---

## 14. Quick Reference Cheatsheet

### By Problem

|Problem|First Line|Second Line|Third Line|
|---|---|---|---|
|Overfitting|Dropout (0.3–0.5)|L2 / Weight decay|Data augmentation|
|Exploding gradients|Gradient clipping (1.0)|Reduce LR|Add BatchNorm|
|Vanishing gradients|Residual connections|He init + ReLU|BatchNorm|
|Training instability|LR warmup|Gradient clipping|Reduce LR|
|Bad generalization|Label smoothing|Mixup/CutMix|SAM optimizer|
|Class imbalance|Focal loss|Class-weighted CE|Oversample|
|Memory limits|Gradient checkpointing|Gradient accumulation|Mixed precision|

### By Architecture

|Architecture|Key Stabilizers|
|---|---|
|CNN (ResNet etc.)|BatchNorm + He init + Dropout + Step/Cosine LR|
|Transformer / ViT|LayerNorm (pre) + Warmup + Dropout + StochasticDepth + LayerScale|
|RNN / LSTM|Gradient clipping + LayerNorm + Orthogonal init|
|GAN|Spectral norm + Instance norm + Label smoothing + Gradient penalty|
|LLM fine-tuning|Weight decay + Warmup + Linear decay + EMA|

### Typical Hyperparameter Ranges

|Technique|Common Values|
|---|---|
|L2 / Weight Decay|`1e-4` to `1e-2`|
|Dropout rate|`0.1` to `0.5`|
|Gradient clip norm|`0.5` to `5.0`|
|Label smoothing $\epsilon$|`0.05` to `0.2`|
|LR warmup steps|`1–5%` of total steps|
|EMA momentum $m$|`0.999` to `0.9999`|
|StochasticDepth rate|`0.1` to `0.4` (deep ViTs)|
|SAM $\rho$|`0.05` to `0.2`|

---

## Summary

Training stabilization is not one thing — it's a layered defense:

1. **Initialization** sets up a sane starting point
2. **Normalization layers** keep activations well-behaved throughout training
3. **Gradient management** prevents the optimization from blowing up
4. **Regularization** (L1/L2, dropout) prevents overfitting
5. **LR scheduling** navigates the loss landscape intelligently
6. **Data techniques** (augmentation, Mixup, label smoothing) improve the training signal
7. **Advanced methods** (SAM, EMA, StochasticDepth) squeeze out extra generalization

The art is knowing which layer of defense to reach for first — and the diagnostic framework in §13 is your map.