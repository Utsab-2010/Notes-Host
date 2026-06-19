---
title: "Diffusion-LM"
lastmod: 2026-05-03
---

#diffusion #nlp 
Link: [Diffusion-LM Improves Controllable Text Generation \| alphaXiv](https://www.alphaxiv.org/abs/2205.14217?chatId=019cf49a-83b5-7d97-acaa-8094eda3aaac)

The training workflow of Diffusion-LM adapts continuous diffusion models to discrete text by modifying the standard diffusion process to include an **embedding step** mapping discrete words to a continuous space, and a **rounding step** mapping continuous vectors back to words. The model is trained end-to-end, jointly learning the diffusion model's parameters and the word embeddings.

Here is the detailed workflow and the underlying mathematics:

### 1. The Forward Process (Noising)

The forward process incrementally adds Gaussian noise to the data to create a sequence of continuous latent variables $x_0 \dots x_T$.

- **Embedding Step:** A discrete sequence of words $w = [w_1, \dots, w_n]$ is mapped to a continuous space using a learned embedding function, where $EMB(w) = [EMB(w_1), \dots, EMB(w_n)]$.
- **Transition to Latent Space:** A Markov transition is added to map the discrete words to the initial continuous state $x_0$, parameterized by $q_\phi(x_0|w) = \mathcal{N}(EMB(w), \sigma_0 I)$.
- **Gradual Noising:** The forward process incrementally adds noise to $x_0$ until the sample $x_T$ is approximately pure Gaussian noise. Each intermediate transition $x_{t-1} \to x_t$ is defined without trainable parameters as: $q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t I)$.

### 2. The Reverse Process (Denoising)

The reverse process involves training a neural network to reverse the noise additions, incrementally reconstructing the data from Gaussian noise.[Diffusion-LM Denoising](/vault/deep-learning/diffusion-lm-denoising/)

- **Denoising Transitions:** Starting from $x_T$, the model predicts the prior states, transitioning from $x_t \to x_{t-1}$. This is parameterized by the model as: $p_\theta(x_{t-1}|x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$.
- **Rounding Step:** After reaching $x_0$, the model uses a trainable rounding step to map the continuous vector back to discrete text. This is parameterized by a softmax distribution: $p_\theta(w|x_0) = \prod_{i=1}^n p_\theta(w_i|x_i)$.

### 3. End-to-End Training Objectives

To learn both the diffusion model parameters and the embedding function, Diffusion-LM optimizes a modified version of the variational lower bound (VLB).

The exact **end-to-end variational lower bound** is: $$\mathcal{L}_{vlb}^{e2e}(w) = \mathbb{E}_{q_\phi(x_0|w)}[\mathcal{L}_{vlb}(x_0) + \log q_\phi(x_0|w) - \log p_\theta(w|x_0)]$$ 
Where the standard $\mathcal{L}_{vlb}(x_0)$ is: $$\mathcal{L}_{vlb}(x_0) = \mathbb{E}_{q(x_{1:T}|x_0)} \left[ \log \frac{q(x_T|x_0)}{p_\theta(x_T)} + \sum_{t=2}^T \log \frac{q(x_{t-1}|x_0, x_t)}{p_\theta(x_{t-1}|x_t)} - \log p_\theta(x_0|x_1) \right]$$

Because optimizing the VLB directly can be unstable, the model employs a **simplified surrogate objective** that expands and reweights each KL-divergence term into a mean-squared error (MSE) loss. The simplified end-to-end objective becomes: $$\large 
\mathcal{L}_{simple}^{e2e}(w) = \mathbb{E}_{q_\phi(x_{0:T}|w)} \left[ \mathcal{L}_{simple}(x_0) + ||EMB(w) - \mu_\theta(x_1, 1)||^2 - \log p_\theta(w|x_0) \right]$$
where the simplified inner loss $\mathcal{L}_{simple}(x_0)$ matches the model's predicted mean $\mu_\theta$ to the true posterior mean $\hat{\mu}$: $\mathcal{L}_{simple}(x_0) = \sum_{t=1}^T \mathbb{E}_{q(x_t|x_0)} ||\mu_\theta(x_t, t) - \hat{\mu}(x_t, x_0)||^2$.

### 4. Re-parameterization to Reduce Rounding Errors

Empirically, the *model struggles to generate an $x_0$ that commits perfectly to a single word embedding* because the constraint to do so only heavily influences terms where $t$ is near 0. To force the model to explicitly structure $x_0$ at every timestep, the objective is re-parameterized.

Instead of predicting the mean $\mu_\theta$, **the neural network $f_\theta(x_t, t)$ is trained to directly predict $x_0$** in every term of the objective. The final re-parameterized objective used for training is: $$\mathcal{L}_{x_0-simple}^{e2e}(w) = \mathbb{E}_{q_\phi(x_{0:T}|w)} \left[ ||\hat{\mu}(x_T; x_0)||^2 + \sum_{t=2}^T [||x_0 - f_\theta(x_t, t)||^2] \right] + \mathbb{E}_{q_\phi(x_{0:1}|w)} \left[ ||EMB(w) - f_\theta(x_1, 1)||^2 - \log p_\theta(w|x_0) \right]$$ 

Through this [x_0-parameterization](/vault/deep-learning/x-0-parameterization/) and the reparameterization trick to backpropagate through sampling steps, the model quickly learns that $x_0$ must precisely center on a discrete word embedding, substantially improving sample quality.