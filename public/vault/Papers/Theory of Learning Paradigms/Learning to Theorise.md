---
title: "Learning to Theorise"
lastmod: 2026-09-05
---

#world-models #representations 







### What are Primitives?
**Primitives** are the foundational, reusable operations that serve as the basic vocabulary of a learned "Language of Thought". Within the Learning-to-Theorize (L2T) framework, they are abstract symbols without any pre-defined symbolic meaning; instead, their operational semantics are learned directly from raw observations based on how they transform states



### 1. The Generative Process (Equations 1 & 2)
The marginal conditional likelihood of the target observation $y$ given the source observation $x$ is defined as: $$p_\theta(y | x) = \int p_\theta(y | s_{K+1}) p_\theta(\tau, s | x) d\tau ds \quad \text{— (Eq. 1)} \quad \text{}$$

Where:
- $\tau = (z_{i_1}, \dots, z_{i_K})$ represents the program (sequence of discrete primitives).
- $s = (s_1, \dots, s_{K+1})$ is the sequence of latent state transitions.
- The integral models the process of marginalizing over all possible programs and latent state trajectories to evaluate how likely it is that $x$ transforms into $y$.

The prior over the program sequence $\tau$ and transition states $s$ factorizes sequentially under a Markov assumption: $$p_\theta(\tau, s | x) = p_\theta(s_1 | x) \prod_{k=1}^K p_\theta(z_{i_k} | s_k) p_\theta(s_{k+1} | s_k, z_{i_k}) \quad \text{— (Eq. 2)} \quad \text{}$$

1. **State Encoding ($p_\theta(s_1 | x)$):** Maps the raw observation $x$ to the initial latent state $s_1$.
2. **Generative Prior Policy ($p_\theta(z_{i_k} | s_k)$):** Dictates the probability of choosing a primitive $z_{i_k}$ based only on the current latent state $s_k$.
3. **Transition Operator ($p_\theta(s_{k+1} | s_k, z_{i_k})$):** Implements the execution of the selected primitive on the latent state to transition to the next step.

---

### 2. The Variational Posterior (Equation 4)

Because calculating the exact marginal likelihood over all possible combinations of discrete programs and continuous states is intractable, NEO uses a variational posterior $q_\phi(\tau, s | x, y)$ to approximate the true posterior: $$q_\phi(\tau, s | x, y) = p_\theta(s_1 | x) \prod_{k=1}^K q_\phi(z_{i_k} | s_k, y) p_\theta(s_{k+1} | s_k, z_{i_k}) \quad \text{— (Eq. 4)} \quad \text{}$$

The variational posterior is structured to align directly with the generative prior's factorization, sharing the exact same encoder $p_\theta(s_1 | x)$ and transition model $p_\theta(s_{k+1} | s_k, z_{i_k})$.

The critical distinction is the **theory programmer** $q_\phi(z_{i_k} | s_k, y)$. Unlike the prior policy which only knows the current state, the theory programmer is **goal-conditioned**—meaning it takes both the current state $s_k$ and the target observation $y$ to choose primitives that actively guide the execution trace to explain the target.

---

### 3. Deconstructing the Evidence Lower Bound (ELBO) (Equation 3)

The training objective maximizes the Evidence Lower Bound (ELBO): $$\log p_\theta(y | x) \ge \mathbb{E}_{q_\phi(\tau, s | x, y)} [\log p_\theta(y | s_{K+1})] - \text{KL}(q_\phi(\tau, s | x, y) \parallel p_\theta(\tau, s | x)) \quad \text{— (Eq. 3)} \quad \text{}$$

Expanding the Kullback-Leibler (KL) divergence reveals a complete algebraic cancellation of the state transitions, which simplifies optimization: $$\text{KL}(q_\phi(\tau, s | x, y) \parallel p_\theta(\tau, s | x)) = \mathbb{E}_{q_\phi} \left[ \log \frac{q_\phi(\tau, s | x, y)}{p_\theta(\tau, s | x)} \right]$$

Plugging in the equations for both joint distributions: $$\log \frac{q_\phi(\tau, s | x, y)}{p_\theta(\tau, s | x)} = \log \frac{p_\theta(s_1 | x) \prod_{k=1}^K q_\phi(z_{i_k} | s_k, y) p_\theta(s_{k+1} | s_k, z_{i_k})}{p_\theta(s_1 | x) \prod_{k=1}^K p_\theta(z_{i_k} | s_k) p_\theta(s_{k+1} | s_k, z_{i_k})}$$

Because the encoder $p_\theta(s_1 | x)$ and transition models $p_\theta(s_{k+1} | s_k, z_{i_k})$ are identical in both the numerator and denominator, they cancel out entirely: $$\log \frac{q_\phi(\tau, s | x, y)}{p_\theta(\tau, s | x)} = \log \left( \prod_{k=1}^K \frac{q_\phi(z_{i_k} | s_k, y)}{p_\theta(z_{i_k} | s_k)} \right) = \sum_{k=1}^K \log \frac{q_\phi(z_{i_k} | s_k, y)}{p_\theta(z_{i_k} | s_k)}$$

This simplifies the KL term in the ELBO to a sequential sum of step-wise action KL divergences: $$\text{KL}(q_\phi(\tau, s | x, y) \parallel p_\theta(\tau, s | x)) = \sum_{k=1}^K \mathbb{E}_{q_\phi} \left[ \text{KL}(q_\phi(z_{i_k} | s_k, y) \parallel p_\theta(z_{i_k} | s_k)) \right]$$

This mathematical cancellation means the model does not have to compute KL divergences over the continuous latent spaces of states $s_k$, focusing regularization solely on aligning the goal-directed theory programmer with the prior action space.

---

### 4. Deterministic Transition Case (Section 3.4)

In the practical implementation, transitions are modeled deterministically: $$p_\theta(s_{k+1} | s_k, z_{i_k}) = \delta(s_{k+1} - f_\theta(s_k, z_{i_k})) \quad \text{}$$

This collapses the probability distribution into a Dirac delta function $\delta$, turning the transition expectation into recursive functional evaluation: $$s_{k+1} = f_\theta(s_k, z_{i_k}) \quad \text{}$$

Consequently, the reconstruction likelihood reduces to the standard MSE reconstruction loss $\ell(y, \hat{y}_\tau)$ of the final decoded state $\hat{y}_\tau = D_\theta(s_{K+1})$.

---

# How is Program Length Decided?
The optimal explanation length **$k^*$ is calculated dynamically at every step of a program rollout by finding the step that minimizes the penalized reconstruction error**. Here is the exact breakdown of how this is calculated, the values it checks, and how it is utilized during training:

### 1. The Mathematical Calculation of $k^*$

For each step $k$, the model decodes the intermediate latent state $s_k$ to produce a raw, observation-space reconstruction $\hat{y}_k = D_\theta(s_k)$. It then evaluates the reconstruction error against the target observation $y$. The optimal step $k^*$ is chosen using the following formula: $$k^* = {argmin}_{k \in {1, \dots, K+1}} \lambda_{\text{MDL}}^k \ell(y, \hat{y}_k)$$
- **$\ell(y, \hat{y}_k)$** represents the reconstruction loss (such as MSE or $L_1$ distance) between the target and the prediction at step $k$.
- **$\lambda_{\text{MDL}} > 1$** is the simplicity penalty coefficient. Raising it to the power of $k$ ensures that longer program rollouts are **penalized exponentially**, meaning a longer program is only selected if it yields a substantial reduction in reconstruction error.

The maximum value checked is **$K+1$**. This varies depending on the specific domain and whether the model is training or running out-of-distribution (OOD) tests:
- **GridWorld:**
    - _During Training:_ $K = 4$, so it checks up to **$5$**.
    - _Length OOD Evaluation:_ $K = 10$, so it checks up to **$11$**.
- **Arithmetic Factorization:**
    - _During Training:_ $K = 3$, so it checks up to **$4$**.
    - _Length OOD Evaluation:_ $K = 6$, so it checks up to **$7$**.
- **Image Editing:**
    - _During Training:_ $K = 3$, so it checks up to **$4$**.
    - _Length OOD Evaluation:_ $K = 6$, so it checks up to **$7$**.

### 4. Does it Check $k^*$ for Each Training Iteration?

**Yes, $k^*$ is calculated at every single training iteration for every sample in the minibatch**.

During training:

1. **Full Sequential Rollout:** The initial observation is encoded, and the model unrolls the transitions for the full maximum length $K$ (e.g., choosing a primitive $z_{i_k}$ and computing $s_{k+1}$ at each step).
2. **Dynamic $k^*$ Selection:** After completing the rollout, the model computes the penalized reconstruction loss for all $k \in {1, \dots, K+1}$ to select $k^*$ for each individual sequence.
3. **Truncated Backpropagation:** The overall reconstruction loss is set to $L_{\text{rec}} = \ell(y, \hat{y}_{k^*})$, and gradients are **backpropagated only through the chosen step $k^*$**, ignoring all subsequent transition steps in that sequence to enforce the simplicity bias.

This calculation also occurs during **inference support rollouts** to extract the program length before query transfer, and during **test-time search (NEO-S)** to find the best length for each of the $B$ sampled candidates.

📊 I can update the technical PDF report in your Studio panel to include a visual diagram of this unrolled training loop and the truncated backpropagation path.