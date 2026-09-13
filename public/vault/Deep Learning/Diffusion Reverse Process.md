---
title: "Diffusion Reverse Process"
lastmod: 2026-03-27
---

To implement the reverse process (sampling), we essentially perform a "denoising" loop. We start with a tensor of pure Gaussian noise and gradually subtract the noise predicted by our trained model until we reach a clean image.

Here is the step-by-step algorithmic breakdown for the **Reverse Diffusion (Sampling)**. Before starting the loop, you need:

- **A Trained Model ($\epsilon_\theta$):** Usually a U-Net that takes $(x_t, t)$ as input and outputs the predicted noise.
- **Variance Schedule ($\alpha, \bar{\alpha}, \beta$):** These must be the exact same values used during the training (Forward) phase.
- **Total Steps ($T$):** The number of iterations (e.g., 1000).

---
### The Sampling Algorithm

For each image you want to generate:

1. **Initialize:** Start with $x_T \sim \mathcal{N}(0, \mathbf{I})$ (pure white noise).
2. **Iterate:** For $t = T, T-1, \dots, 1$:
    - **Sample random noise:** $z \sim \mathcal{N}(0, \mathbf{I})$ if $t > 1$, else $z = 0$.
    - **Predict the noise:** Pass the current image $x_t$ and the time step $t$ into your model to get $\epsilon_\theta(x_t, t)$.
    - **Compute the Mean ($\mu_\theta$):** This is the "de-noised" version of the current image.$$\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(x_t, t) \right)$$
    - **Update the Image:** Calculate the next step $x_{t-1}$ by adding back a tiny bit of controlled variance ($\sigma_t z$) to keep the process stochastic:$$x_{t-1} = \mu_\theta(x_t, t) + \sigma_t z$$
3. **Result:** $x_0$ is your generated image.

---

### Implementation Details (Pseudocode)

```python
def sample(model, schedule, shape):
    # 1. Start with pure noise
    img = torch.randn(shape) 
    
    for t in reversed(range(0, T)):
        # t_tensor tells the model which noise level we are at
        t_batch = torch.full((shape[0],), t, dtype=torch.long)
        
        # 2. Predict noise using the U-Net
        predicted_noise = model(img, t_batch)
        
        # 3. Calculate coefficients (from our pre-defined schedule)
        alpha = schedule.alphas[t]
        alpha_bar = schedule.alphas_bar[t]
        beta = schedule.betas[t]
        
        # 4. Remove a portion of the predicted noise
        mean = (1 / sqrt(alpha)) * (img - (beta / sqrt(1 - alpha_bar)) * predicted_noise)
        
        if t > 0:
            noise = torch.randn_like(img)
            sigma = sqrt(beta) # Or use the posterior variance formula
            img = mean + sigma * noise
        else:
            img = mean
            
    return img
```

##### Why do we add noise back ($z$) in the reverse step?
It seems counter-intuitive to add noise while trying to clean an image. However, if we didn't add that tiny bit of random noise $\sigma_t z$ at each step, the model would be purely deterministic. Adding it allows the model to explore the distribution of "natural images" more effectively, *preventing it from getting stuck or collapsing into blurry averages*.

