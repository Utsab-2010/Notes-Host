---
title: "Different ML Optimizers"
lastmod: 2026-06-08
---

> A detailed reference on gradient-based optimization — the math, the intuition, and why it matters.

---

## 0. The Setup

We're minimizing a loss function $\mathcal{L}(\theta)$ over parameters $\theta \in \mathbb{R}^d$. At each step $t$ we compute the gradient $g_t = \nabla_\theta \mathcal{L}(\theta_t)$ (or a stochastic approximation over a minibatch) and update $\theta$.

The central tension in optimizer design:

- **Gradient noise** — stochastic gradients are unbiased but high-variance.
- **Curvature** — the loss landscape curves differently in every direction; a single global learning rate is a crude approximation.
- **Adaptivity** — different parameters may need different effective step sizes.

Every optimizer below is an attempt to address some subset of these problems.

---

## 1. Gradient Descent (GD)

### Update Rule
$$\theta_{t+1} = \theta_t - \eta , g_t$$
where $\eta$ is the learning rate (step size).
### Variants

|Variant|Batch size|Notes|
|---|---|---|
|Batch GD|Full dataset|Exact gradient; slow per step|
|Stochastic GD (SGD)|1 sample|Noisy gradient; acts as regularizer|
|Mini-batch SGD|$B$ samples|Standard in practice|

### Why It Works (and Doesn't)

The update moves $\theta$ in the direction of steepest descent in $\ell_2$ space. For a quadratic loss with Hessian $H$, convergence rate is:

$$\mathcal{L}(\theta_t) - \mathcal{L}^* \leq \left(1 - \frac{\eta}{\kappa}\right)^t \cdot [\mathcal{L}(\theta_0) - \mathcal{L}^*]$$

where $\kappa = \lambda_{\max}(H) / \lambda_{\min}(H)$ is the **condition number**. High $\kappa$ → slow convergence. Vanilla SGD has no mechanism to handle ill-conditioned curvature.

---

## 2. SGD with Momentum

### Motivation

Gradient noise causes SGD to oscillate. Momentum smooths out the noisy gradient signal by accumulating a velocity in directions of persistent gradient.

### Update Rule

$$v_t = \beta v_{t-1} + g_t$$ $$\theta_{t+1} = \theta_t - \eta , v_t$$

$\beta \in [0, 1)$ is the momentum coefficient (typical: $\beta = 0.9$).

**Expanded form:** $v_t = \sum_{k=0}^{t} \beta^{t-k} g_k$ — a geometrically-weighted moving average of past gradients.

### Nesterov Momentum (NAG)

A smarter variant: compute the gradient _after_ taking the momentum step.

$$v_t = \beta v_{t-1} + \nabla_\theta \mathcal{L}(\theta_t - \eta \beta v_{t-1})$$ $$\theta_{t+1} = \theta_t - \eta , v_t$$

The key idea: look ahead to where momentum would take you, then correct. This gives better theoretical convergence and tends to overshoot less.

**Convergence:** For convex functions, SGD+Momentum achieves $O(1/t)$ convergence; NAG achieves $O(1/t^2)$ — matches the lower bound for first-order methods.

### Significance

Momentum is still the optimizer of choice for large-scale vision (ResNets, ViTs). With a well-tuned learning rate schedule (cosine, linear warmup), SGD+Momentum often outperforms adaptive methods on image classification benchmarks.

---

## 3. AdaGrad

### Motivation

Different parameters receive vastly different gradient magnitudes. Sparse features (e.g., rare words in NLP) get tiny gradient signals; dense features dominate. AdaGrad adapts the learning rate _per parameter_ based on the cumulative gradient history.

### Update Rule

$$G_t = G_{t-1} + g_t^2 \quad \text{(element-wise)}$$ $$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{G_t + \epsilon}} \odot g_t$$

$G_t \in \mathbb{R}^d$ accumulates the sum of squared gradients per parameter. $\epsilon \approx 10^{-8}$ for numerical stability.

**Effective learning rate per parameter:** $\eta_i^{\text{eff}} = \frac{\eta}{\sqrt{G_t^{(i)}}}$. Parameters that receive large gradients get their LR reduced.

### The Problem

$G_t$ is monotonically increasing — the effective learning rate decays to zero and training stops. AdaGrad works well for convex problems but fails for deep networks with long training runs.

---

## 4. RMSProp

### Motivation

Fix AdaGrad's shrinking LR by using an exponential moving average (EMA) instead of a cumulative sum.

### Update Rule

$$v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$ $$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{v_t + \epsilon}} \odot g_t$$

$\beta_2 \approx 0.99$ is the decay rate. This gives a sliding window of second-moment estimates.

### Interpretation

$v_t$ approximates $\mathbb{E}[g^2]$ locally. Dividing by $\sqrt{v_t}$ approximately normalizes the gradient by its RMS, giving a dimensionless update. The effective LR is stationary if the gradient statistics are stationary.

### Significance

RMSProp was proposed by Hinton (unpublished, 2012 Coursera lecture). It remains the optimizer of choice for RNNs due to its stability with exploding gradients.

---

## 5. Adam (Adaptive Moment Estimation)

### Motivation

Combine momentum (first moment) with RMSProp (second moment), and correct for initialization bias.

### Update Rule

**First moment (momentum):** $$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t$$

**Second moment (variance):** $$v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$

**Bias correction** (crucial for early steps when $m_t, v_t \approx 0$): $$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$

**Parameter update:** $$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \cdot \hat{m}_t$$

**Defaults:** $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$, $\eta = 10^{-3}$.

### Why Bias Correction Matters

At $t=1$: $m_1 = (1 - \beta_1) g_1 \approx 0.1 g_1$. Without correction, $m_1$ severely underestimates the true first moment. $\hat{m}_1 = m_1 / (1 - 0.9) = g_1$. Bias vanishes as $t \to \infty$.

### Convergence

Adam is a stochastic gradient method with per-coordinate adaptive learning rates. Convergence to a stationary point is guaranteed under certain conditions (bounded gradients, decreasing LR), but Reddi et al. (2018) showed Adam can _diverge_ for simple convex problems. This motivated AMSGrad.

### Why Adam Is Dominant

- Robust to LR choice — works reasonably well without tuning.
- Handles sparse gradients.
- Fast early progress due to adaptive LRs.
- Used by default in most NLP, multimodal, and generative model training.

---

## 6. AdamW (Adam with Decoupled Weight Decay)

### The Problem with L2 Regularization + Adam

In SGD, L2 regularization ($\mathcal{L} + \frac{\lambda}{2}|\theta|^2$) and weight decay ($\theta \leftarrow (1-\lambda)\theta$) are equivalent. **In Adam they are not.** Adding L2 to the loss modifies the gradient, and that modified gradient gets scaled by $1/\sqrt{\hat{v}_t}$. The effective weight decay becomes larger for low-variance parameters, breaking the intended regularization.

### Fix: Decouple Weight Decay

$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \cdot \hat{m}_t - \eta \lambda \theta_t$$

The weight decay term $\eta \lambda \theta_t$ is applied _directly_ to the parameters, bypassing the adaptive scaling.

### Significance

AdamW is the optimizer behind BERT, GPT, ViT, and essentially all modern large-scale pretraining. Loshchilov & Hutter (2019) showed it consistently outperforms Adam+L2 across language and vision tasks.

---

## 7. AMSGrad

### Motivation

Fix Adam's non-convergence by ensuring the second-moment estimate is non-decreasing.

### Update Rule

$$v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$ $$\hat{v}_t = \max(\hat{v}_{t-1}, v_t)$$ $$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \cdot \hat{m}_t$$

The $\max$ operation guarantees the denominator never decreases, ensuring the effective LR never _increases_ over time.

### In Practice

AMSGrad converges more reliably in theory but is often slower in practice than Adam/AdamW on large-scale benchmarks. It matters more for non-stationary problems.

---

## 8. Adagrad Variants Summary Table

|Optimizer|First Moment|Second Moment|Bias Correction|Weight Decay|
|---|---|---|---|---|
|SGD|—|—|—|Optional|
|Momentum|EMA of $g$|—|—|Optional|
|AdaGrad|—|Cumulative sum $g^2$|—|—|
|RMSProp|—|EMA of $g^2$|—|—|
|Adam|EMA of $g$|EMA of $g^2$|Yes|Coupled|
|AdamW|EMA of $g$|EMA of $g^2$|Yes|Decoupled|
|AMSGrad|EMA of $g$|max EMA of $g^2$|Yes|—|

---

## 9. LARS (Layer-wise Adaptive Rate Scaling)

### Motivation

In large-batch training (batch sizes in the thousands to millions), the gradient noise decreases and you can compute larger steps. But naively scaling the learning rate causes instability. LARS adapts the LR _per layer_ using the ratio of weight norm to gradient norm.

### Update Rule

$$\lambda^{(l)} = \eta \cdot \frac{|\theta^{(l)}|}{|g^{(l)}| + \beta |\theta^{(l)}|}$$ $$\theta_{t+1}^{(l)} = \theta_t^{(l)} - \lambda^{(l)} \cdot \frac{g_t^{(l)} + \beta \theta_t^{(l)}}{|g_t^{(l)}| + \beta |\theta_t^{(l)}|}$$

where $l$ indexes layers and $\beta$ is the weight decay coefficient.

**Key insight:** The local LR $\lambda^{(l)}$ is proportional to the trust ratio $|\theta^{(l)}| / |g^{(l)}|$. If the gradient is small relative to the weight, take a larger step; if the gradient dominates, be conservative.

### Significance

LARS enables training ImageNet with batch sizes of 32,768+ in minutes. It's widely used in self-supervised contrastive learning (SimCLR, BYOL).

---

## 10. LAMB (Layer-wise Adaptive Moments for Batch training)

### Motivation

Apply the LARS idea to Adam — use per-layer trust ratios but with Adam's adaptive moment estimates.

### Update Rule

$$r_t = \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_t \quad \text{(Adam update + weight decay)}$$ $$\theta_{t+1} = \theta_t - \eta \cdot \frac{|\theta_t|}{|r_t|} \cdot r_t$$

The ratio $|\theta_t| / |r_t|$ is the trust ratio, applied per layer.

### Significance

LAMB enabled BERT pretraining with batch size 65,536, reducing training time from days to ~76 minutes. Used heavily in large language model pretraining.

---

## 11. Lion (EvoLved Sign Momentum)

### Motivation

A newer optimizer (2023, Chen et al.) discovered via program search. Extremely memory-efficient — only stores momentum, no second moment.

### Update Rule

$$u_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t$$ $$\theta_{t+1} = \theta_t - \eta (\text{sign}(u_t) + \lambda \theta_t)$$ $$m_t = \beta_2 m_{t-1} + (1 - \beta_2) g_t$$

**Defaults:** $\beta_1 = 0.9$, $\beta_2 = 0.99$, $\eta = 10^{-4}$ (typically smaller than Adam's LR).

### Key Idea

The update uses only the **sign** of the interpolated momentum — all parameters are updated by a fixed magnitude each step (up to weight decay). This is a form of $\ell_\infty$-normalized update, in contrast to Adam's per-coordinate $\ell_2$ normalization.

### Significance

Lion matches or exceeds AdamW on image and language tasks at roughly 2/3 the memory cost (no $v_t$). Still being evaluated at scale.

---

## 12. Second-Order Methods (Brief Overview)

First-order methods use only $\nabla \mathcal{L}$. Second-order methods additionally use $\nabla^2 \mathcal{L}$ (the Hessian) to account for curvature.

### Newton's Method

$$\theta_{t+1} = \theta_t - H_t^{-1} g_t$$

Optimal step: accounts for curvature in every direction. Converges in $O(\log(1/\epsilon))$ iterations for strongly convex functions. But computing and inverting $H \in \mathbb{R}^{d \times d}$ is $O(d^3)$ — infeasible for $d \sim 10^9$.

### Natural Gradient

Replace the Euclidean metric with the Fisher information metric: $$\theta_{t+1} = \theta_t - \eta , F^{-1} g_t$$

where $F = \mathbb{E}[(\nabla \log p_\theta)({\nabla \log p_\theta})^\top]$ is the Fisher matrix. Invariant to reparameterization; theoretically superior but computationally expensive.

### K-FAC (Kronecker-Factored Approximate Curvature)

Approximates $F^{-1}$ layer-wise using Kronecker products of smaller matrices, making natural gradient feasible. Used in some large-scale training regimes.

### Why Adam Is Often Better Than Exact Second-Order

In practice, the loss landscape is non-convex, the Hessian is poorly conditioned, and the noise in stochastic gradients makes exact curvature information useless. Adam's diagonal approximation to the curvature is surprisingly competitive.

---

## 13. Learning Rate Schedules

Optimizers don't operate in isolation — the LR schedule is often as important as the optimizer itself.

### Common Schedules

**Step Decay:** $$\eta_t = \eta_0 \cdot \gamma^{\lfloor t / T \rfloor}$$

Decay by factor $\gamma$ every $T$ steps.

**Cosine Annealing:** $$\eta_t = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min})\left(1 + \cos\left(\frac{\pi t}{T}\right)\right)$$

Smooth decay; popular for vision. Can be combined with warm restarts (SGDR).

**Linear Warmup + Cosine Decay (Transformer standard):** $$\eta_t = \begin{cases} \eta_{\max} \cdot \frac{t}{T_{\text{warm}}} & t \leq T_{\text{warm}} \ \text{cosine decay} & t > T_{\text{warm}} \end{cases}$$

**Warmup rationale:** At initialization, parameters are far from any optimum and gradients are noisy. Starting with a small LR prevents instability. As the model finds a basin, $\eta$ can safely increase.

**Inverse Square Root Decay** (original Transformer): $$\eta_t = d_{\text{model}}^{-0.5} \cdot \min(t^{-0.5}, t \cdot T_{\text{warm}}^{-1.5})$$

---

## 14. Gradient Clipping

A necessary complement to any optimizer for training deep networks (especially RNNs and transformers).

**Norm clipping:** $$g_t \leftarrow g_t \cdot \min\left(1, \frac{\tau}{|g_t|}\right)$$

If the gradient norm exceeds threshold $\tau$, rescale it to have norm $\tau$. Preserves direction, controls magnitude.

**Value clipping:** clip each element of $g_t$ to $[-\tau, \tau]$ — changes direction, cruder.

Norm clipping is standard. Without it, a single large-gradient step can destabilize training irreversibly.

---

## 15. Practical Decision Guide

```
Training large transformer/language model?
  → AdamW + linear warmup + cosine decay + grad clipping
  → Consider Lion if memory is constrained

Training a vision model from scratch on ImageNet?
  → SGD + Momentum + cosine LR + weight decay
  → Adam/AdamW also works; SGD often gives slightly higher final accuracy

Large-batch distributed training?
  → LARS (for SGD-based) or LAMB (for Adam-based)

Fine-tuning a pretrained model?
  → AdamW with small LR (e.g., 1e-5 to 5e-5)

RNN training?
  → RMSProp or Adam + aggressive gradient clipping

Sparse features / NLP embeddings?
  → Adam or AdaGrad (handles sparsity well)
```

---

## 16. Key Takeaways

1. **SGD+Momentum** is theoretically elegant and still competitive on vision benchmarks when tuned carefully. Its lack of adaptivity is actually useful: it generalizes better in some regimes (flat minima tend to generalize; adaptive methods may converge to sharp ones).
    
2. **Adam** dominates NLP and generative modeling because robustness to LR is worth more than the marginal accuracy from tuning SGD.
    
3. **AdamW** is Adam done correctly — always use decoupled weight decay.
    
4. **Adaptive methods tend to converge faster but generalize slightly worse** — a consistent empirical finding. The gap narrows with large datasets.
    
5. **The optimizer is only one piece.** LR schedule, weight decay, batch size, and gradient clipping are equally important. A badly scheduled SGD loses to a well-tuned Adam; a well-scheduled SGD often beats Adam.
    
6. **No free lunch.** Every optimizer encodes an inductive bias about the loss landscape. Understanding that bias is more valuable than chasing the latest optimizer.
    

---

## References

- Kingma & Ba (2015): _Adam: A Method for Stochastic Optimization_ — [arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980)
- Loshchilov & Hutter (2019): _Decoupled Weight Decay Regularization_ — [arxiv.org/abs/1711.05101](https://arxiv.org/abs/1711.05101)
- Reddi et al. (2018): _On the Convergence of Adam and Beyond_ — [arxiv.org/abs/1904.09237](https://arxiv.org/abs/1904.09237)
- You et al. (2020): _Large Batch Optimization for Deep Learning: Training BERT in 76 minutes_ — [arxiv.org/abs/1904.00962](https://arxiv.org/abs/1904.00962)
- Chen et al. (2023): _Symbolic Discovery of Optimization Algorithms (Lion)_ — [arxiv.org/abs/2302.06675](https://arxiv.org/abs/2302.06675)
- Bottou et al. (2018): _Optimization Methods for Large-Scale Machine Learning_ — SIAM Review