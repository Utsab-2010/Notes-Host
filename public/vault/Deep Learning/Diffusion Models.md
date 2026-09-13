---
title: "Diffusion Models"
lastmod: 2026-03-17
---

Diffusion models might look like a mess of Gaussian noise at first glance, but the math is actually a very elegant "tug-of-war" between destroying information and reconstructing it.

Think of it like this: If you dip a drop of ink into water, it’s easy to predict how it spreads out (Forward), but incredibly hard to figure out exactly where the drop started once it's fully mixed (Reverse). Diffusion models learn to do exactly that.

---

## The Forward Process (Diffusion)

The goal here is to slowly turn an image $x_0$ into pure noise $x_T$ over $T$ steps. We don't "learn" anything here; we just follow a fixed schedule.

At each step $t$, we add a small amount of Gaussian noise controlled by a variance schedule $\beta_t \in (0, 1)$.

$$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t}x_{t-1}, \beta_t\mathbf{I})$$

- **$x_0$**: Your original clean image.
- **$q(x_t | x_{t-1})$**: The probability of getting $x_t$ given the previous step.
- **$\sqrt{1 - \beta_t}$**: A scaling factor that slightly shrinks the image so the variance doesn't explode.

**The "Jump" Trick:** We don't actually have to iterate $T$ times. Using the property of Gaussians, we can jump from $x_0$ to any step $t$ directly:

$$x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1 - \bar{\alpha}_t}\epsilon$$

where $\alpha_t = 1 - \beta_t$ and $\bar{\alpha}_t$ is the product of all $\alpha$ up to $t$. $\epsilon$ is just random noise.

---

## The Reverse Process (Generative)

[Diffusion Reverse Process](/vault/deep-learning/diffusion-reverse-process/)
This is where the Deep Learning happens. We want to go from pure noise $x_T$ back to $x_0$. Since we can't easily calculate $q(x_{t-1} | x_t)$ \[**the posterior**] (it requires knowing the distribution of all possible images), we train a Neural Network to **estimate** it.

The network tries to predict the parameters (mean $\mu$ and variance $\Sigma$) of the reverse Gaussian:

$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

- **$\theta$**: The weights of our neural network (usually a U-Net).
- p is a distribution conditioned on previous state and parameterized by $\theta$
- **Objective**: In practice, we don't predict the image $x_{t-1}$ directly. It’s much easier for the network to predict the **noise** $\epsilon$ (i.e the mean, since $\sigma$ is known) that was added at step $t$.

---

## Training: The Loss Function

We train the model by picking a random image $x_0$, a random step $t$, and some random noise $\epsilon$. We then ask the model: _"Hey, I added this noise to the image at step $t$. Can you guess what the noise looked like?"_

The loss function is a Simple Mean Squared Error (MSE):

$$L_{simple} = \mathbb{E}_{t, x_0, \epsilon} \left[ \| \epsilon - \epsilon_\theta(x_t, t) \|^2 \right]$$

1. **$\epsilon$**: The true noise we added.
2. **$\epsilon_\theta(x_t, t)$**: The noise the model predicted.