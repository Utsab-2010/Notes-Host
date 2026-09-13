---
title: "Proximal Policy Optimization (PPO)"
lastmod: 2026-07-30
---

## The Problem PPO Is Fixing

Picking up directly from the actor-critic note: plain policy-gradient updates (REINFORCE, vanilla A2C) have a structural weakness. You collect a batch of trajectories using the *current* policy $\pi_{\theta_{\text{old}}}$, compute a gradient, take a step to get $\pi_\theta$ — and then that batch of data is stale, because it was collected by a policy that no longer exists. If you try to reuse that same batch for several more gradient steps (to be more sample-efficient, since environment interaction is expensive), $\theta$ can drift far enough from $\theta_{\text{old}}$ that the gradient estimates computed from that old data become actively misleading, and updates can wildly overshoot — sometimes catastrophically destroying a previously-good policy in one bad update, with no way to recover since the bad policy now collects worse data going forward.

So the real goal: **reuse data for multiple gradient steps, but somehow prevent the policy from moving too far away from the one that collected the data.** That's the entire motivation — everything else in this note is machinery to enforce that one constraint cheaply.

## The More Principled (But Impractical) Precursor: TRPO

Before PPO, **TRPO (Trust Region Policy Optimization)** tackled this directly: maximize the policy objective subject to an explicit constraint that the KL divergence between old and new policy stays under some threshold $\delta$:

$$\max_\theta\ \mathbb{E}\Big[\frac{\pi_\theta(a|s)}{\pi_{\theta_{\text{old}}}(a|s)}A(s,a)\Big] \quad \text{subject to}\quad \mathbb{E}[D_{KL}(\pi_{\theta_{\text{old}}}\|\pi_\theta)] \le \delta$$

This is exactly the "stay close to the old policy" idea made mathematically explicit via a genuine constrained-optimization trust region. It works well, but solving a constrained optimization problem with a KL constraint at every update requires second-order information (conjugate gradient methods, computing Fisher-information-vector products) — complicated to implement correctly and expensive per step.

**PPO's whole pitch**: get almost the same "don't move too far from the old policy" effect as TRPO, using nothing more sophisticated than first-order SGD and a clipped objective — no constrained optimization, no second-order machinery, just a modified loss function you can optimize with Adam like anything else.

## The Probability Ratio

Define the ratio between new and old policy probabilities for the action actually taken:

$$r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}$$

At the very start of an update (before any gradient steps), $r_t = 1$ exactly, since $\theta = \theta_{\text{old}}$. As you take gradient steps using the same batch of old data, $r_t$ drifts away from 1 — and how far it's drifted is a direct, cheap-to-compute proxy for "how far has the policy moved from the one that collected this data." This ratio is the quantity PPO directly controls, instead of an explicit KL constraint.

The plain policy-gradient objective, rewritten using this ratio (this is just importance sampling under the hood — reweighting samples collected under the old policy so they still form a valid, roughly unbiased estimate of the new policy's expected advantage):

$$L^{CPI}(\theta) = \mathbb{E}\big[r_t(\theta)\,A_t\big]$$

(CPI = "conservative policy iteration," the older name for this unclipped surrogate). Maximizing this directly, with no safeguard, is exactly the naive approach that blows up: nothing stops $r_t(\theta)$ from growing arbitrarily large for actions with large positive advantage, driving $\theta$ arbitrarily far in one step.

## The Clipped Objective — PPO's Actual Contribution

PPO's fix is almost embarrassingly simple given the buildup above. Just clip the ratio to a small range around 1, and take the **minimum** of the clipped and unclipped objective:

$$L^{CLIP}(\theta) = \mathbb{E}\Big[\min\big(r_t(\theta)A_t,\ \ \text{clip}(r_t(\theta),\,1-\epsilon,\,1+\epsilon)\,A_t\big)\Big]$$

with $\epsilon$ typically around $0.2$. Worth actually tracing through why the min-of-clipped-and-unclipped construction does what it's supposed to, case by case:

**Case $A_t > 0$ (good action).** You'd like to increase $r_t$ (make this action more likely), but the clip caps the benefit of doing so once $r_t$ exceeds $1+\epsilon$ — pushing $r_t$ far beyond that stops improving the objective at all, so gradient ascent has no incentive to keep pushing $\theta$ further in that direction once the ratio's already moved enough. The min with the unclipped term matters here too: it makes sure the clip only ever acts as a *ceiling* on the incentive, never accidentally creating a perverse incentive to push $r_t$ even higher for extra reward past the clip boundary.

**Case $A_t < 0$ (bad action).** Symmetric logic — you'd like to decrease $r_t$ (make the action less likely), and the clip caps the benefit once $r_t$ drops below $1-\epsilon$, again removing the incentive to keep moving $\theta$ further once you've already sufficiently suppressed the bad action.

Net effect: the objective **only rewards moving $\theta$ within the trust region $[1-\epsilon, 1+\epsilon]$ around the old policy**, and flatlines (removes gradient signal) once you'd be moving further than that. This is a soft, first-order stand-in for TRPO's hard KL constraint — instead of solving a constrained problem exactly, you shape the *objective itself* so that ordinary unconstrained gradient ascent naturally stops pushing once the ratio leaves the trust region. Much cheaper, only slightly less principled, and empirically works about as well as TRPO in practice.

## The Full PPO Loss

In practice, PPO combines the clipped policy objective with a critic (value function) loss and an entropy bonus, exactly mirroring the actor-critic combined loss from the companion note:

$$L(\theta,\phi) = L^{CLIP}(\theta) - c_1\big(V_\phi(s_t) - V_t^{\text{target}}\big)^2 + c_2\, H(\pi_\theta)$$

- $L^{CLIP}$: the clipped surrogate above (the actor's objective)
- Value loss: ordinary regression toward a return/TD target (the critic, same as vanilla actor-critic)
- Entropy bonus: encourages continued exploration, discourages the policy collapsing to overconfident/deterministic too early

## The Actual Training Loop

This is the part that operationally distinguishes PPO from vanilla A2C, and is really the whole payoff of the clipping trick:

1. Run the current policy $\pi_{\theta_{\text{old}}}$ in the environment, collect a batch of trajectories.
2. Compute advantage estimates for the whole batch (typically via GAE — see the actor-critic note).
3. **Run several epochs of minibatch SGD over this same fixed batch of data**, optimizing $L^{CLIP}$ (plus value + entropy terms) each time.
4. After these epochs, throw the batch away, set $\theta_{\text{old}}\leftarrow\theta$, and collect a fresh batch.

Step 3 is exactly the thing vanilla actor-critic couldn't safely do — reuse the same batch for multiple gradient steps — and the clipping mechanism is precisely what makes this safe: even after several epochs on the same stale batch, the objective's gradient signal vanishes once the policy has drifted the "allowed" amount, so you get several epochs of useful learning per batch of environment interaction instead of just one, without the instability that plain policy gradients would suffer from doing the same thing.

## Why PPO Won Out in Practice

- **Simplicity**: first-order optimization only, no conjugate gradients, no Fisher-vector products, no explicit constrained optimization — just a modified loss function, trivially compatible with standard deep learning tooling (Adam, standard autodiff).
- **Sample efficiency relative to vanilla policy gradients**: multiple epochs per batch, safely, thanks to the clip.
- **Robustness**: empirically much less prone to the catastrophic policy collapse that plagues naive policy gradient methods, without needing extremely careful tuning of learning rates.
- This combination of "works about as well as TRPO, way easier to implement and tune" is why PPO became (and largely remains) the default choice for a huge swath of RL applications, and is also the RL algorithm underlying RLHF fine-tuning of language models — same core mechanism, just with the "environment" being a single-step text generation episode and the "reward" coming from a learned reward model instead of a game score.

## Connecting Back

- actor-critic note → PPO is actor-critic with one specific, carefully-designed change to the actor's loss (the clipped surrogate) — everything about the critic, the advantage estimation via GAE, and the overall two-network structure carries over unchanged
- DQN note → interesting contrast in how each family handles "stale data": DQN handles it via a target network (freeze the *target*, let the online network move freely) plus a replay buffer that can be reused indefinitely since Q-learning is off-policy by construction; PPO handles staleness the opposite way — it's fundamentally on-policy, so instead of tolerating staleness like DQN's replay buffer does, it explicitly constrains how far the policy is allowed to drift before the data becomes too stale to trust
- AlphaZero-from-scratch project → worth noting PPO and AlphaZero-style training solve a similar "stay close to a reference policy" problem from very different angles — AlphaZero's MCTS search itself acts as a built-in trust-region-like improvement operator (the tree search never proposes wildly implausible policies since it's built on top of the current network's own priors), whereas PPO enforces the trust region explicitly via the clip; possibly a useful lens if you ever look at MuZero, which is a genuinely direct hybrid of these two lineages