---
title: "MaxEnRL via Energy-based Normalising Flows 1"
---

## Abstract
In traditional Max Entropy RL methods for continuous action spaces , typically actor-critic is used. There are usually two parts of the training which happen at each iteration:
- policy eval: update the Q-fuction(Critic)
- policy improvement: updating the Actor

Proposed method is a **single objective training process**.
- supports **multi-modal** action distributions with efficient action sampling
- does policy evaluation without monte carlo approximation

### 1. Soft Actor-Critic (SAC) Approximation

This is the most common method, used in algorithms like SAC. It reformulates the soft value function as an expectation and approximates it by averaging over $M$ samples drawn from the current policy $\pi_\phi$:

$$V_\theta(s_t) \approx \frac{1}{M} \sum_{i=1}^M \left( Q_\theta(s_t, a^{(i)}) - \alpha \log \pi_\phi(a^{(i)}|s_t) \right)$$

- **Assumption:** This method assumes the current policy $\pi_\phi$ is a close approximation of the energy-based distribution defined by the critic, minimizing the **Kullback-Leibler divergence** between them.
- **Drawback:** It relies on the assumption that $\pi_\phi \approx \pi_\theta$ and introduces estimation errors when the sample size $M$ is small.

### 2. Soft Q-Learning (SQL) Approximation

This method uses importance sampling to approximate the integral of the exponentiated Q-values. It estimates the soft value using samples ${a^{(i)}}_{i=1}^M$ drawn from the policy $\pi_\phi$:

$$V_\theta(s_t) \approx \alpha \log \left( \frac{1}{M} \sum_{i=1}^M \frac{\exp(Q_\theta(s_t, a^{(i)})/\alpha)}{\pi_\phi(a^{(i)}|s_t)} \right)$$

- **Context:** $b_1$This estimator theoretically has the least variance when the sampling distribution is proportional to the exponentiated Q-function.
- **Drawback:** While it is guaranteed to converge to the true value as $M \to \infty$, empirical convergence is slow, often requiring larger sample sizes (e.g., $M=32$) compared to SAC-like estimation,.

### The Paper's Solution (MEow)

The authors emphasize that these Monte Carlo approximations introduce **estimation errors and variances**, particularly when using a small number of samples. Their proposed framework, **MEow**, avoids this entirely by using Energy-Based Normalizing Flows to calculate the soft value function **exactly** via the determinant of the Jacobian, eliminating the need for Monte Carlo approximation,.



## Experiments and Setup
- Mujoco and Isaac Sym Environments were used.