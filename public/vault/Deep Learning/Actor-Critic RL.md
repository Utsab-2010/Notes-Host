---
title: "Actor-Critic RL"
lastmod: 2026-07-30
---

## Two Families This Sits Between

Worth placing this before diving in, since actor-critic is explicitly a hybrid of two older ideas:

**Value-based methods** (like DQN): learn $Q(s,a)$, derive a policy implicitly by acting greedily w.r.t. it. Needs $\arg\max_a$ over actions — clean for discrete actions, doesn't work for continuous ones.

**Policy-gradient methods** (like REINFORCE): learn an explicit policy $\pi_\theta(a|s)$ directly, and push its parameters in the direction that increases the probability of actions that led to high return. Works fine for continuous actions, but as we'll see below, plain REINFORCE has a serious variance problem.

**Actor-critic**: learn _both_ — a policy (the **actor**) and a value function (the **critic**) — where the critic's whole job is to make the actor's gradient estimates less noisy. Neither piece is doing what DQN's or REINFORCE's single network did in isolation; they're built specifically to lean on each other.

## Starting Point: The Policy Gradient Theorem

The actor wants to directly maximize expected return $J(\theta) = \mathbb{E}_{\pi_\theta}[\text{Return}]$ via gradient ascent on $\theta$. The **policy gradient theorem** gives the gradient in a workable form:

$$\nabla_\theta J(\theta) = \mathbb{E}\Big[\nabla_\theta \log\pi_\theta(a|s)\cdot Q^{\pi}(s,a)\Big]$$

Read this intuitively: $\nabla_\theta\log\pi_\theta(a|s)$ is the direction in parameter space that increases the probability of having taken action $a$ in state $s$. You scale that direction by $Q^\pi(s,a)$ — how good that action actually turned out to be. So the whole update is: **nudge the policy toward actions in proportion to how good they were.** Good actions get reinforced (their log-probability pushed up); bad actions get suppressed.

**REINFORCE** is the simplest instantiation: replace $Q^\pi(s,a)$ with the actual observed Monte Carlo return $G_t$ from that episode, since $Q^\pi(s,a) = \mathbb{E}[G_t\mid s_t=s,a_t=a]$, so the return itself is an unbiased (if noisy) sample of it.

## The Problem: REINFORCE's Variance Is Brutal

Using the raw Monte Carlo return $G_t$ as the scaling factor is unbiased, but extremely high variance — a single episode's return is a noisy sum of many random rewards and transitions, and this noise gets baked directly into every single gradient update. High-variance gradients mean slow, unstable learning; you need a huge number of episodes to average out the noise before the signal becomes usable.

The standard trick to reduce this variance without introducing bias: subtract a **baseline** $b(s)$ that doesn't depend on the action:

$$\nabla_\theta J(\theta) = \mathbb{E}\Big[\nabla_\theta\log\pi_\theta(a|s)\cdot\big(Q^\pi(s,a) - b(s)\big)\Big]$$

This stays unbiased for _any_ choice of $b(s)$ as long as it doesn't depend on $a$ (the extra term introduced by subtracting $b(s)$ has expectation exactly zero, since $\mathbb{E}_a[\nabla_\theta\log\pi_\theta(a|s)] = 0$ — a clean, worth-remembering identity). But the _variance_ of the estimator absolutely does depend on the choice of $b(s)$, and a well-chosen baseline can shrink it dramatically.

## The Critic's Job: Be That Baseline

The best natural choice of baseline is the state-value function $V^\pi(s)$ — the expected return from state $s$ averaged over actions. This is exactly the **critic**. Once you subtract $V^\pi(s)$ as the baseline, the term multiplying the log-probability becomes:

$$A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s)$$

This is the **advantage function** — how much better action $a$ is compared to the _average_ action in state $s$. This is a genuinely nice quantity to scale your gradient by: instead of asking "was this action good in absolute terms," you're asking "was this action better or worse than what I'd typically do here." An action that led to a mediocre-but-still-positive return in a state where every action leads to high return should get _suppressed_ relative to the better alternatives — raw $Q$ doesn't capture that, advantage does.

$$\nabla_\theta J(\theta) = \mathbb{E}\big[\nabla_\theta\log\pi_\theta(a|s)\cdot A^\pi(s,a)\big]$$

## How the Critic Actually Estimates the Advantage

You don't have $Q^\pi$ or $V^\pi$ exactly — the critic is a learned function $V_\phi(s)$, trained the same TD-bootstrapping way as DQN's value function (see the DQN note): regress $V_\phi(s)$ toward $r + \gamma V_\phi(s')$ using observed transitions.

Given a learned $V_\phi$, the simplest advantage estimate uses the one-step TD error as a stand-in for the advantage:

$$A(s_t,a_t) \approx \delta_t = r_t + \gamma V_\phi(s_{t+1}) - V_\phi(s_t)$$

This is a genuinely elegant substitution: the TD error is already exactly measuring "how much better did things turn out than $V_\phi$ predicted" — which is precisely what advantage is asking. One-step TD error trades off bias (from bootstrapping off a possibly-inaccurate $V_\phi$) against variance (much lower than a full Monte Carlo return, since it only involves one real reward rather than a whole trajectory's worth). **GAE (Generalized Advantage Estimation)** is the standard refinement — an exponentially-weighted average of multi-step TD errors, controlled by a parameter $\lambda$, letting you smoothly dial between low-variance/high-bias (small $\lambda$, close to one-step TD) and low-bias/high-variance (large $\lambda$, close to full Monte Carlo return).

## The Actual Training Loop

Two networks (or a shared trunk with two heads, common in practice), trained simultaneously:

- **Actor** $\pi_\theta(a|s)$: updated via the policy gradient, scaled by the advantage from the critic
- **Critic** $V_\phi(s)$: updated via ordinary TD regression, i.e. minimize $(V_\phi(s_t) - (r_t+\gamma V_\phi(s_{t+1})))^2$

Both losses get combined (often with an added entropy bonus on the policy, encouraging continued exploration by penalizing overly-confident/deterministic policies too early) and optimized jointly with the same optimizer step.

$$L = L_{\text{actor}} + c_1 L_{\text{critic}} - c_2, H(\pi_\theta)$$

## A2C vs A3C — the Parallelization Detail

**A3C (Asynchronous Advantage Actor-Critic)**: many parallel worker processes, each running its own copy of the environment and its own local actor-critic network, computing gradients and asynchronously pushing updates to a shared global network. The asynchrony itself was originally framed as a variance-reduction trick — parallel workers exploring different parts of state-space simultaneously naturally decorrelates the gradient updates, doing a similar decorrelation job to what experience replay does for DQN, just via parallelism instead of a buffer.

**A2C (Advantage Actor-Critic)**: the synchronous simplification — run the same parallel workers, but wait for all of them to finish a batch of steps, average their gradients, and do one synchronous update. Empirically performs comparably to A3C (the asynchrony wasn't actually buying much) while being simpler to implement and more GPU-friendly, since synchronous batched updates parallelize far better on GPU hardware than asynchronous scattered updates do. A2C is what most modern implementations actually use.

## Why This Matters as a Stepping Stone to PPO

The actor-critic framework above has one glaring practical weakness worth calling out explicitly, since it's exactly what PPO exists to fix: naive policy-gradient updates use each batch of collected data for a **single** gradient step, then throw the data away — reusing it for further updates (to get more mileage out of expensive environment interaction) tends to push $\pi_\theta$ too far from the policy that actually collected the data, making the advantage estimates and the gradient direction itself stale and unreliable, sometimes catastrophically collapsing training. PPO is the fix for exactly this problem — see the companion note.

## Connecting Back

- DQN note → the critic here is trained with essentially the same TD-bootstrapping machinery as DQN's $Q$-network; actor-critic is really "DQN's value-learning trick, plus an explicit policy network on top, with the value function repurposed as a variance-reducing baseline rather than the thing you act greedily on"
- modes of convergence note → REINFORCE's raw gradient estimator is unbiased but high-variance; introducing a baseline is a clean, concrete example of the classic bias-variance tradeoff, done in a way that provably doesn't sacrifice any bias at all — worth remembering as the textbook case of a "free variance reduction"
- PPO note → actor-critic is the base architecture PPO builds directly on top of; PPO changes _how_ the actor's loss is computed per batch, not the actor-critic decomposition itself