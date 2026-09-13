---
title: "Why Iterative Reverse Sampling Recovers the Data Distribution?"
lastmod: 2026-09-06
---

## 1. The setup: a forward corruption process

Let $X_0 \sim p_{\mathrm{data}}$. Define a forward diffusion (SDE) that gradually destroys structure:

$$ dX_t = f(X_t,t),dt + g(t),dW_t, \qquad X_0 \sim p_{\mathrm{data}}. $$

For the common variance-exploding choice, $f=0$ and $g(t)=\sigma(t)$, this reduces to additive Gaussian corruption $X_t = X_0 + \sigma(t)\epsilon$. Denote by $p_t$ the marginal density of $X_t$. As $t$ ranges from $0$ to $T$, $p_t$ traces a path

$$ p_0 = p_{\mathrm{data}} ;\longrightarrow; p_T \approx \mathcal N(0,\sigma_T^2 I), $$

interpolating from the data distribution to a simple, tractable prior.

## 2. The forward process obeys a Fokker–Planck equation

The density $p_t$ is not arbitrary — it is fully determined by the SDE through the Fokker–Planck (Kolmogorov forward) equation:

$$ \partial_t p_t(x) = -\nabla\cdot\big(f(x,t)p_t(x)\big) + \tfrac12 g(t)^2 \Delta p_t(x). $$

This is the key structural fact that makes _reversal_ possible: the entire family ${p_t}$, and its infinitesimal evolution, is a well-defined deterministic object once $f$ and $g$ are fixed — it is not just "data at various noise levels" but a genuine solution to a PDE.

## 3. Anderson's time-reversal theorem

The central result (Anderson, 1982) states that the _time-reversed_ process $\bar X_t = X_{T-t}$ is itself a diffusion, satisfying

$$ d\bar X_t = \Big[f(\bar X_t,t) - g(t)^2 \nabla_x \log p_t(\bar X_t)\Big],dt

- g(t),d\bar W_t, $$

run backward in time, where $\bar W_t$ is a Brownian motion for the reversed time direction. Two facts make this remarkable:

1. **The reverse process is a legitimate diffusion** — it has the same Fokker–Planck structure as the forward one, just with a modified drift.
2. **The only new ingredient needed is the score** $\nabla_x \log p_t(x)$. Everything else ($f$, $g$) is already known from the forward process we chose.

This is _not_ a heuristic — it is an exact statement about the marginals of a diffusion process. If we could compute $\nabla_x \log p_t(x)$ exactly at every $(x,t)$, then simulating the reverse SDE starting from $\bar X_0 \sim p_T$ produces, at time $T$, a sample exactly distributed as $p_0 = p_{\mathrm{data}}$.

## 4. Why the score is exactly the missing piece

Intuitively: to reverse a diffusion, you need to know, at every point and every noise level, _which direction "more data" lies in_. That directional information is precisely $\nabla_x \log p_t(x)$ — it points toward higher-density regions of $p_t$, weighted by how sharply density increases. Without it, the only thing you could do is run the forward noise process (which increases entropy); with it, you can exactly counteract the entropy production term $\tfrac12 g(t)^2 \Delta p_t$ from the Fokker–Planck equation, because $\Delta p_t = \nabla\cdot(p_t \nabla \log p_t)$.

So the reverse-time correction term $-g(t)^2\nabla_x\log p_t(x)$ is not an ad hoc denoising heuristic — it is the exact term required to invert the diffusion operator itself.

## 5. From exact scores to exact recovery

Putting it together:

$$ \boxed{ \text{exact } s(x,t)=\nabla_x\log p_t(x) ;+; \text{exact reverse SDE integration} ;\Longrightarrow; \bar X_T \sim p_0 = p_{\mathrm{data}}. } $$

This is why "iterative reverse sampling" is meaningful at all: each infinitesimal reverse step moves the current distribution from $p_t$ to $p_{t-dt}$ _exactly_, because the reverse SDE's marginals are guaranteed by Anderson's theorem to coincide with the forward marginals, traversed backward. Iterating (integrating) this all the way to $t=0$ recovers $p_{\mathrm{data}}$ by construction — not by approximation, in the idealized continuous-time, exact-score setting.

## 6. Why _iteration_ specifically (not a single jump)

A single-step map from $p_T$ (Gaussian noise) directly to $p_0$ would require inverting a highly nonlinear, high-entropy transformation in one shot — effectively requiring a globally accurate score at a distribution very far from where it was estimated. Iterating in small steps has two advantages:

- **Local validity**: at each step, we only need the score to be accurate in the neighborhood of the current point and current noise level — a much easier local regression problem than a single global inversion.
- **Consistency with the Fokker–Planck evolution**: the reverse SDE is only guaranteed to track $p_t$ if the correction is applied continuously (or in sufficiently fine discrete steps) as $t$ decreases — it is a _flow_ statement, not a one-shot mapping. Skipping intermediate noise levels breaks the guarantee that the marginal at each step matches $p_t$.

This is also why the schedule is typically run from **large noise to small noise**: at large $t$, $p_t$ is smooth and easy to represent (barriers between modes have been washed out); as $t \to 0$, the distribution's fine structure is reintroduced gradually, guided at each step by a score that only needs to be locally correct.

## 7. What actually gets used in practice

In practice we do not have the exact score. We have $s_\theta(x,t)$ learned via denoising score matching, and we integrate the reverse SDE (or the associated probability-flow ODE) with a discrete-step numerical solver. The exact-recovery statement above becomes approximate:

$$ q_\theta \approx p_{\mathrm{data}}, $$

with the gap controlled by:

- score estimation error, $s_\theta(x,t) \neq \nabla_x\log p_t(x)$,
- the mismatch between $p_T$ and the chosen simple prior,
- discretization error from finite step size,
- and finite-data / optimization error in training $s_\theta$.

But the _reason_ iterative reverse sampling targets the data distribution at all — rather than being an arbitrary denoising heuristic — is precisely Anderson's time-reversal result: reversing a diffusion with its own score is mathematically exact, and iteration is simply the discretized simulation of that exact continuous-time reverse flow.

## 8. One-line summary

Iterative reverse sampling works because a forward diffusion's time-reversal is itself an exact diffusion whose drift is fully determined by the time-dependent score $\nabla_x\log p_t(x)$; with exact scores, integrating this reverse process step by step exactly retraces the path from noise back to $p_{\mathrm{data}}$, and finite, learned-score iteration is simply a numerical approximation of that exact continuous-time reversal.