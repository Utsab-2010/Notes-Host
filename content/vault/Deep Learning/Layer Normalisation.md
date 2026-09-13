---
title: "Layer Normalisation"
lastmod: 2026-07-30
---

# Introduction

Deep networks are hard to train partly because as activations flow through many layers, their scale can drift — some layers end up with huge activations, others tiny, and this shifts around as the weights update during training ("internal covariate shift"). Whatever the exact cause, empirically: normalizing activations at each layer makes training dramatically more stable and lets you use higher learning rates.

## Why BatchNorm is Insufficient?
BatchNorm was the first popular fix, but it normalizes _across the batch dimension_ — for a given feature, it computes mean/variance across all examples in the batch. That's a problem for two reasons that matter a lot for transformers:
1. It makes the model's output for one example depend on which other examples happen to be in its batch -  `weird for anything sequential/variable-length`.
2. It falls apart with small batches or variable-length sequences, which is basically the default situation with sequence models. Batchnorm would take the norm across all the elements in a sequence including stuff like padding and special tokens which would not lead to meaningful normalisation - the mean/var get contaminated by the effect of the special tokens.

**LayerNorm's fix**: normalize across the _feature dimension_, per example, independently of everything else in the batch.

## The Actual Computation

For a single vector $x \in \mathbb{R}^d$ (say, one token's hidden state, of dimension $d$):

$$\mu = \frac{1}{d}\sum_{i=1}^d x_i, \qquad \sigma^2 = \frac{1}{d}\sum_{i=1}^d (x_i - \mu)^2$$

$$\hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}$$

$$y_i = \gamma_i \hat{x}_i + \beta_i$$

Where $\gamma, \beta \in \mathbb{R}^d$ are learned scale and shift parameters (one pair per feature dimension), and $\epsilon$ is just a small constant for numerical stability (avoids dividing by zero if variance happens to collapse).

Notice the mean and variance here are computed **over the $d$ features of a single token**, not over the batch and not across other tokens in the sequence. Every token, in every example, in every position, gets normalized independently using only its own $d$ numbers. That's the entire operation — mean-center, divide by std, then apply a learned affine transform to give the network back the freedom to un-normalize if that's actually better for a given feature.

## Why the Learned $\gamma, \beta$ Matter

If you just normalized and stopped there, you'd be forcibly constraining every layer's output to have mean 0, variance 1 in every feature — which might genuinely **hurt representational capacity** (some features might legitimately need a different scale to be useful downstream). The $\gamma,\beta$ give the network an escape hatch: it can learn to undo the normalization entirely for any feature that needs it ($\gamma_i \to \sigma_i^{original}$, $\beta_i \to \mu_i^{original}$ recovers the original value), or dampen it partially. 

So LayerNorm doesn't remove information, it removes the _burden of the network having to self-regulate its own scale_ — the scale becomes a small number of extra learned parameters instead of an emergent, uncontrolled property of the weights.

---
## Why This Specific Axis for Transformers

Transformers process variable-length sequences, batch size is often small (especially at inference — sometimes batch size 1), and you want a token's representation to be processed identically regardless of what else is in its batch or how long the sequence is. Normalizing per-token, over the feature dimension, satisfies all of this automatically:

- No batch-size dependence at all (doesn't even look at other examples)
- No sequence-length dependence (doesn't look at other positions)
- Every token gets treated identically whether it's alone or part of a huge batch

This is really the core reason LayerNorm (not BatchNorm) became the default for transformers — it's not that LayerNorm is universally superior to BatchNorm, it's that the specific structural properties of sequence data make BatchNorm awkward and LayerNorm a clean fit.

## Where It Sits in the Transformer Block

Two placements you'll see, and the difference actually matters a lot for training stability:

**Post-LN (original "Attention Is All You Need" design):** $$x_{l+1} = \text{LayerNorm}\big(x_l + \text{Sublayer}(x_l)\big)$$ Norm applied _after_ the residual addition.

**Pre-LN (what basically everything uses now — GPT-2 onward, most modern LLMs):** $$x_{l+1} = x_l + \text{Sublayer}(\text{LayerNorm}(x_l))$$ Norm applied _inside_ the residual branch, before the sublayer (attention or FFN), with the residual stream itself left un-normalized.

Why Pre-LN won out: with Post-LN, gradients have to flow back through a LayerNorm at every single layer, which empirically made very deep transformers unstable to train without a careful learning-rate warmup — the gradient signal through the norm layers didn't behave well early in training. Pre-LN keeps the residual stream itself completely clean and unnormalized, so gradients have a direct, unobstructed path all the way back through every layer via the residual connections (basically the same "gradient highway" argument as ResNets) — LayerNorm only ever touches the _branch_ being added in, never the main trunk. This is why Pre-LN transformers train more stably at depth and mostly don't even need warmup, or need much shorter warmup, compared to Post-LN.

The tradeoff: Pre-LN transformers empirically tend to have a slightly worse final performance ceiling at a given depth compared to a _successfully trained_ Post-LN model of the same size — but Post-LN becomes so hard to train reliably beyond moderate depth that in practice Pre-LN wins by default for large-scale models.

---
## The Other Wrinkle: RMSNorm

Most modern LLMs (LLaMA, and lots of others) actually use **RMSNorm**, a simplified variant that drops the mean-centering step entirely:

$$\hat{x}_i = \frac{x_i}{\sqrt{\frac{1}{d}\sum_j x_j^2 + \epsilon}}, \qquad y_i = \gamma_i \hat{x}_i$$

No $\mu$ subtraction, no $\beta$. The empirical finding was that the mean-centering part of LayerNorm wasn't doing much of the actual work — most of the benefit came from the variance/scale normalization — so RMSNorm keeps that part and drops the rest, which is cheaper to compute and has fewer parameters, for basically no loss in quality. Worth knowing since if you look at a LLaMA-style architecture diagram and see "Norm" you should assume RMSNorm rather than the original LayerNorm unless stated otherwise.
