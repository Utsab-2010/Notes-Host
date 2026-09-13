---
title: "Deep Q-Networks (DQN)"
lastmod: 2026-07-30
---

## The Problem: Q-Learning Needs a Table

Start from ordinary tabular Q-learning, since DQN is really just "what happens when you can't use a table anymore."

Q-learning tries to learn the **action-value function**: $$Q(s,a) = \text{expected discounted return from taking action } a \text{ in state } s, \text{ then acting optimally after}$$

If you know $Q^*(s,a)$ exactly, the optimal policy is trivial: $\pi^*(s) = \arg\max_a Q^*(s,a)$. The classic tabular update, driven by the Bellman equation:

$$Q(s,a) \leftarrow Q(s,a) + \alpha\Big[r + \gamma\max_{a'}Q(s',a') - Q(s,a)\Big]$$

This works fine when $Q$ is literally a lookup table (one entry per state-action pair). It completely breaks down once the state space is enormous or continuous — e.g. raw Atari pixel frames — because there's no way to have a table entry for every possible screen. You need a **function approximator** to generalize across similar states instead of memorizing each one individually. The obvious idea: replace the table with a neural network, $Q(s,a;\theta)$, and train it to approximate the Bellman equation.

That obvious idea, tried directly, is unstable and tends to diverge. DQN (Mnih et al., 2015) is the specific set of fixes that made it actually work.

## Why Naive "Q-Learning + Neural Net" Blows Up

Two structural problems, both stemming from the fact that you're now doing **function approximation** instead of an isolated table lookup:

**1. Correlated, non-stationary data.** In standard supervised learning you assume i.i.d. training samples. In RL, consecutive experiences $(s_t,a_t,r_t,s_{t+1})$ collected while an agent plays are highly correlated — one trajectory drifts smoothly through similar states. **Training a neural net on a stream of highly correlated inputs violates the i.i.d. assumption most optimization theory (and stochastic gradient descent's good behavior) relies on**, and in practice causes the network to overfit to whatever narrow region of state-space it's currently wandering through, forgetting earlier experience.

**2. Moving target.** The Bellman update's target, $r + \gamma\max_{a'}Q(s',a';\theta)$, uses the _same_ network $\theta$ you're currently updating. Every gradient step changes $\theta$, which immediately changes the target for the next update — you're chasing a target that moves every time you take a step toward it. With a table this is fine (updates are localized to one cell), but with a shared function approximator, updating $Q(s,a)$ can inadvertently shift $Q$ at _other_ states too (that's the whole point of generalization), which can shift the very targets you're trying to fit, and this feedback loop is what actually causes the classic divergence/oscillation.

## The Two Fixes That Make DQN Work

**Fix 1 — Experience Replay.** Instead of training on the live stream of experience directly, store every transition $(s,a,r,s')$ in a large replay buffer, and train by sampling **random minibatches** from this buffer instead of using the most recent transitions directly.

This directly attacks problem 1: sampling uniformly at random from a big buffer of past experience breaks the temporal correlation between consecutive training examples, making the training data look much closer to i.i.d. It also has a second nice side-effect: each transition can be reused for many gradient updates instead of being seen once and discarded, which is much more sample-efficient — genuinely valuable in RL where environment interaction is expensive.

**Fix 2 — Target Network.** Keep a **second copy** of the network, $\theta^-$, used _only_ to compute the Bellman target, and freeze it for a fixed number of steps (e.g. update it to match $\theta$ every $C$ steps, or with Polyak/soft averaging in continuous variants) rather than updating it every gradient step alongside $\theta$.

$$\text{target} = r + \gamma \max_{a'} Q(s',a';\theta^-)$$

This directly attacks problem 2: the target is now a temporarily fixed quantity for a stretch of training, so you're doing something much closer to ordinary supervised regression toward a fixed label for a while, rather than chasing a target that shifts on every single step. Periodically syncing $\theta^- \leftarrow \theta$ lets the target slowly catch up to reflect the network's improved estimates, without the update-to-update instability of a fully live target.

---
# The Loss Function

Putting it together, DQN trains $\theta$ by sampling minibatches from the replay buffer and minimizing:

$$L(\theta) = \mathbb{E}_{(s,a,r,s')\sim \text{Buffer}}\Big[\big(r + \gamma\max_{a'}Q(s',a';\theta^-) - Q(s,a;\theta)\big)^2\Big]$$

This is literally just **regression** — the network's prediction $Q(s,a;\theta)$ is trained to match a target $y = r+\gamma\max_{a'}Q(s',a';\theta^-)$ via ordinary squared-error loss, exactly like fitting a supervised regression target, except the "label" is bootstrapped from the network's own (frozen, lagged) estimates rather than being a ground-truth value from a dataset. That bootstrapping — using your own estimate as part of the target — is the defining feature of TD-learning methods generally, and it's precisely the part that makes the two fixes above necessary in the first place.

## The Full Algorithm, Roughly

1. Initialize $Q(\cdot,\cdot;\theta)$ and target network $Q(\cdot,\cdot;\theta^-)$ with $\theta^-\leftarrow\theta$, and an empty replay buffer.
2. For each environment step:
    - With probability $\epsilon$ take a random action, otherwise take $\arg\max_a Q(s,a;\theta)$ (**$\epsilon$-greedy exploration** — necessary since acting greedily on an undertrained $Q$ would never explore alternatives that might actually be better)
    - Store the resulting transition $(s,a,r,s')$ in the buffer
    - Sample a random minibatch from the buffer, compute the target using $\theta^-$, take a gradient step on $\theta$ toward that target
    - Every $C$ steps, sync $\theta^- \leftarrow \theta$
3. Decay $\epsilon$ over training (start near-random, end near-greedy) to shift gradually from exploration to exploitation as $Q$ becomes more trustworthy.

DQN also used a few practical tricks in the original Atari paper worth knowing exist even if secondary to the two core fixes above: preprocessing frames (grayscale, downsampled, stacking 4 consecutive frames so the network can infer velocity/motion, since a single frame is not Markovian for something like Pong), reward clipping to ${-1,0,1}$ to keep gradient scales comparable across very different games, and a CNN architecture processing raw pixels directly rather than requiring hand-engineered features — this last point being a big part of why DQN was a notable result: end-to-end pixels-to-Q-values with a single architecture across dozens of different Atari games.

---
# Other Variants

**Double DQN.** Vanilla DQN has a known systematic **overestimation bias**: taking $\max_{a'}Q(s',a';\theta^-)$ tends to overestimate true values, because max-of-noisy-estimates is itself a biased (upward) estimator of the true max — you're both selecting the best action _and_ evaluating it using the same noisy $Q$ values, so overestimation errors self-reinforce. Double DQN decouples selection from evaluation: use the **online** network $\theta$ to pick the best action, but the **target** network $\theta^-$ to evaluate it: $$y = r + \gamma, Q\big(s', \arg\max_{a'}Q(s',a';\theta);\ \theta^-\big)$$ Simple change, meaningfully reduces the overestimation bias in practice.

**Dueling DQN.** Splits the network's output into two streams — a scalar **state-value** $V(s)$ and a per-action **advantage** $A(s,a)$ — recombined as $$Q(s,a) = V(s) + \Big(A(s,a) - \frac{1}{|\mathcal{A}|}\sum_{a'}A(s,a')\Big)$$ (the mean-subtraction is needed for identifiability — otherwise $V$ and $A$ aren't uniquely determined from $Q$ alone). Intuition: in many states, the _choice_ of action barely matters (e.g. nothing bad is about to happen regardless of what you do), and only the overall state value matters; separating these lets the network learn a good $V(s)$ from experience even for actions it hasn't tried much in that state, since $V(s)$ is shared across all actions.

**Prioritized Experience Replay (PER).** Instead of sampling uniformly from the replay buffer, sample transitions with probability proportional to their TD-error magnitude — transitions the network is currently predicting badly get replayed more often, since they carry more learning signal than transitions it already predicts well. Requires an importance-sampling correction in the loss to remain unbiased, since you've deliberately skewed the sampling distribution.

**Rainbow DQN.** Simply combines Double DQN, Dueling, PER, and a handful of other independently-developed improvements (multi-step returns, distributional RL, noisy nets for exploration) into one agent — an empirical demonstration that these fixes are largely complementary rather than redundant, each contributing separately to final performance.

# Where DQN Sits in the Bigger RL Picture

DQN is fundamentally **value-based** and works with **discrete action spaces** — you need to compute $\max_a Q(s,a;\theta)$ at every step, which is trivial to do exactly when $a$ ranges over a small discrete set, but becomes intractable for continuous action spaces (no clean way to maximize over a continuum). This is precisely why continuous-control RL moved toward actor-critic / policy-gradient methods instead (DDPG, TD3, SAC), which learn an explicit policy network rather than requiring an explicit max over actions.

Worth contrasting directly with the AlphaZero-style setup: AlphaZero's value network is trained via **self-play and MCTS-improved targets** (the tree search itself supplies the improved policy/value targets to regress toward), which sidesteps the moving-target instability differently — the MCTS search provides a much stronger, look-ahead-corrected target than pure bootstrapped one-step TD, at the cost of needing a perfect simulator to run the tree search in the first place. DQN, by contrast, is model-free — it never simulates the environment, it only ever bootstraps off its own one-step value estimates, which is both its main weakness (noisier bootstrapping, no lookahead) and its main strength (works in any environment you can interact with, no simulator/model of the dynamics required).
