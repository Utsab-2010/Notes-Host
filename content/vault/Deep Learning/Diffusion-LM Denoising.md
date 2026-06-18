---
title: "Diffusion-LM Denoising"
---

The denoising inference step in Diffusion-LM is the reverse process of the diffusion model, where the system starts with a sequence of pure Gaussian noise vectors ($x_T$) and iteratively removes the noise step-by-step to recover the continuous word vectors ($x_0$), which are finally converted back into discrete text.

Here is the detailed workflow and mathematics behind this process:

### 1. The Denoising Transition

At each step $t$ during inference, the model aims to transition from the current noisy state $x_t$ to a slightly less noisy state $x_{t-1}$. This transition is *typically* modeled as a Gaussian distribution: $$p_\theta(x_{t-1}|x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$
Instead of predicting the mean $\mu_\theta$ directly, the Diffusion-LM uses a neural network $f_\theta(x_t, t)$ to directly predict the fully denoised state $x_0$ at every step.

### 2. Computing the Posterior Mean

Once the model has an estimate for $x_0$ via $f_\theta(x_t, t)$, it computes the mean of the *tractable Gaussian posterior $q(x_{t-1} | x_0, x_t)$* to sample the next state. The exact closed-form expression for this true posterior mean $\hat{\mu}(x_t, x_0)$ is: **$\hat{\mu}(x_t, x_0) = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}x_0 + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}x_t$**.

**Definitions of the terms:**

- **$x_0$**: The fully denoised, continuous latent vector (estimated in practice by $f_\theta(x_t, t)$).
- **$x_t$**: The current noisy continuous vector at step $t$.
- **$\beta_t$**: The hyperparameter dictating the amount of noise added at diffusion step $t$.
- **$\alpha_t$**: Defined implicitly as $1 - \beta_t$ (standard in diffusion literature and used in the posterior calculation).
- **$\bar{\alpha}_t$**: The cumulative product of noise variances up to step $t$, defined mathematically as $\bar{\alpha}_t = \prod_{s=0}^t(1-\beta_s)$.

To perform the actual denoising step, the model substitutes its prediction $f_\theta(x_t, t)$ in place of $x_0$ and samples the new state $x_{t-1}$ from the resulting distribution $q(x_{t-1} | f_\theta(x_t, t), x_t)$.

### 3. The Clamping Trick

To further reduce rounding errors during inference, Diffusion-LM introduces the **"clamping trick"**. Instead of using the raw continuous prediction $f_\theta(x_t, t)$, the model maps this vector to its nearest actual discrete word embedding before sampling $x_{t-1}$.

The modified sampling step becomes: **$x_{t-1} = \sqrt{\bar{\alpha}} \cdot Clamp(f_\theta(x_t, t)) + \sqrt{1 - \bar{\alpha}}\epsilon$**. _(Where $\epsilon \sim \mathcal{N}(0, I)$ is standard Gaussian noise)_.

By clamping the intermediate predictions, the model is forced to commit to specific words earlier in the diffusion process, making the continuous trajectory more precise.

### 4. Final Rounding to Discrete Text

After completing all denoising steps (typically $T=2000$ or downsampled to $200$ for speed), the model arrives at the final continuous representation $x_0$. The final step is **rounding**, which maps $x_0$ back to discrete text $w$. This is done by selecting the most probable word for each sequence position using a softmax distribution: **$\text{argmax } p_\theta(w|x_0) = \prod_{i=1}^n p_\theta(w_i|x_i)$**.

