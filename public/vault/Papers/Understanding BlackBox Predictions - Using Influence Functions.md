---
title: "Understanding BlackBox Predictions - Using Influence Functions"
lastmod: 2026-05-21
---

#continual_learning 

paper: [\[1703.04730\] Understanding Black-box Predictions via Influence Functions](https://arxiv.org/abs/1703.04730)



## Setup

You have training points $z_1, \dots, z_n$ where each $z_i = (x_i, y_i)$. You train a model by minimising the empirical risk:

$$\hat{\theta} = \arg\min_\theta \frac{1}{n} \sum_{i=1}^n L(z_i, \theta)$$

The fundamental question is: **how does removing a single training point $z$ change $\hat{\theta}$, and consequently change predictions on a test point $z_{test}$?**

Retraining from scratch for every candidate point is prohibitively expensive, so the paper approximates this.

---

## Step 1 — Upweighting instead of removing

Rather than removing $z$ outright, consider **upweighting** it by a small amount $\epsilon$:

$$\hat{\theta}_{\epsilon,z} = \arg\min_\theta \frac{1}{n} \sum_{i=1}^n L(z_i, \theta) + \epsilon \cdot L(z, \theta)$$

Removing $z$ is equivalent to setting $\epsilon = -\frac{1}{n}$, so this is a natural reparameterisation. The trick is that now you can **differentiate with respect to $\epsilon$**, which is something calculus handles cleanly.

---

## Step 2 — Deriving the influence on parameters

How do the parameters $\hat{\theta}_{\epsilon,z}$ change as $\epsilon$ varies? Differentiate with respect to $\epsilon$ at $\epsilon = 0$.

At the optimum, the gradient of the objective is zero:

$$\frac{1}{n} \sum_{i=1}^n \nabla_\theta L(z_i, \hat{\theta}_{\epsilon,z}) + \epsilon \cdot \nabla_\theta L(z, \hat{\theta}_{\epsilon,z}) = 0$$

Differentiating both sides with respect to $\epsilon$ and applying the chain rule:

$$\left[ \frac{1}{n} \sum_{i=1}^n \nabla^2_\theta L(z_i, \hat{\theta}) + \epsilon \cdot \nabla^2_\theta L(z, \hat{\theta}) \right] \frac{d\hat{\theta}_{\epsilon,z}}{d\epsilon} + \nabla_\theta L(z, \hat{\theta}) = 0$$

At $\epsilon = 0$, the bracketed term is just the Hessian $H_{\hat{\theta}} = \frac{1}{n}\sum_i \nabla^2_\theta L(z_i, \hat{\theta})$, so:

$$H_{\hat{\theta}} \frac{d\hat{\theta}_{\epsilon,z}}{d\epsilon}\bigg|_{\epsilon=0} + \nabla_\theta L(z, \hat{\theta}) = 0$$

Solving for the derivative:

$$\mathcal{I}_{up,params}(z) \stackrel{\text{def}}{=} \frac{d\hat{\theta}_{\epsilon,z}}{d\epsilon}\bigg|_{\epsilon=0} = -H_{\hat{\theta}}^{-1} \nabla_\theta L(z, \hat{\theta})$$

This is the **influence on parameters** — it tells you how the model weights shift when you upweight $z$. The $H^{-1}$ term is why the Hessian is necessary, as we discussed.

To approximate removing $z$ entirely, you set $\epsilon = -\frac{1}{n}$:

$$\hat{\theta}_{-z} - \hat{\theta} \approx -\frac{1}{n} \mathcal{I}_{up,params}(z) = \frac{1}{n} H_{\hat{\theta}}^{-1} \nabla_\theta L(z, \hat{\theta})$$

---

## Step 3 — Influence on the test loss

You don't actually care about the parameters directly — you care about how the **loss on a test point** changes. Apply the chain rule:

$$\mathcal{I}_{up,loss}(z, z_{test}) \stackrel{\text{def}}{=} \frac{dL(z_{test}, \hat{\theta}_{\epsilon,z})}{d\epsilon}\bigg|_{\epsilon=0}$$

$$= \nabla_\theta L(z_{test}, \hat{\theta})^\top \cdot \frac{d\hat{\theta}_{\epsilon,z}}{d\epsilon}\bigg|_{\epsilon=0}$$

Substituting Step 2:

$$\boxed{\mathcal{I}_{up,loss}(z, z_{test}) = -\nabla_\theta L(z_{test}, \hat{\theta})^\top H_{\hat{\theta}}^{-1} \nabla_\theta L(z, \hat{\theta})}$$

This is the **central equation of the paper**. Intuitively:

- $\nabla_\theta L(z_{test}, \hat{\theta})$ — which direction does the test loss want to push the parameters?
- $\nabla_\theta L(z, \hat{\theta})$ — which direction does training point $z$ push the parameters?
- $H^{-1}$ — how much does a push in that direction actually move the parameters, accounting for the curvature from all other data?

If these two gradients point in the same direction (inner product is large and positive), removing $z$ hurts test performance. If they point in opposite directions, $z$ was actually harmful.

---

## Step 4 — Perturbing a training input

Now a finer question: instead of removing $z$, what if you **slightly modify its input** $x \to x + \delta$? Call the perturbed point $z_\delta = (x + \delta, y)$.

The effect on parameters of swapping $z$ for $z_\delta$ is:

$$\hat{\theta}_{z_\delta, -z} - \hat{\theta} \approx \frac{1}{n}\left(\mathcal{I}_{up,params}(z_\delta) - \mathcal{I}_{up,params}(z)\right)$$

$$= -\frac{1}{n} H_{\hat{\theta}}^{-1} \left[\nabla_\theta L(z_\delta, \hat{\theta}) - \nabla_\theta L(z, \hat{\theta})\right]$$

For small $\delta$, Taylor expand the gradient difference:

$$\nabla_\theta L(z_\delta, \hat{\theta}) - \nabla_\theta L(z, \hat{\theta}) \approx \left[\nabla_x \nabla_\theta L(z, \hat{\theta})\right] \delta$$

This is a $p \times d$ matrix (parameters × input dimensions) times $\delta$. Substituting back and differentiating with respect to $\delta$:

$$\mathcal{I}_{pert,loss}(z, z_{test}) \stackrel{\text{def}}{=} \nabla_\delta L(z_{test}, \hat{\theta}_{z_\delta,-z})\bigg|_{\delta=0} = -\nabla_\theta L(z_{test}, \hat{\theta})^\top H_{\hat{\theta}}^{-1} \nabla_x \nabla_\theta L(z, \hat{\theta})$$

This gives you a vector over input dimensions — it tells you **which features of training point $z$ most affect the prediction on $z_{test}$**, and in which direction to perturb them to maximally increase the test loss (used for training-set attacks).

---

## Step 5 — Computing $H^{-1}v$ efficiently

The bottleneck is computing $s_{test} = H_{\hat{\theta}}^{-1} \nabla_\theta L(z_{test}, \hat{\theta})$. Explicitly forming and inverting $H$ costs $O(p^2)$ in memory and $O(p^3)$ to invert — completely infeasible for neural nets with millions of parameters.

The key insight is you never need $H^{-1}$ explicitly — you only need **Hessian-vector products** $Hv$, which cost $O(p)$ via the Pearlmutter trick (a clever application of automatic differentiation).

The paper uses a stochastic estimator based on the Taylor expansion:

$$H^{-1} = \sum_{j=0}^{\infty} (I - H)^j$$

Truncate this and estimate $H$ with single-sample minibatches at each step, giving an unbiased estimator that converges without ever materialising the full matrix. Once $s_{test}$ is computed, influence scores for all training points are just cheap dot products $-s_{test} \cdot \nabla_\theta L(z_i, \hat{\theta})$.

---

That's the complete mathematical story of the paper. The elegance is that it reduces a seemingly expensive retraining problem to a handful of gradient and Hessian-vector computations.