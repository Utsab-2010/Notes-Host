---
title: "p-values"
lastmod: 2026-07-19
---

## Step 1: Recall what α actually is

α is a **threshold you pick in advance**, before seeing data. It's the maximum false-positive rate you're willing to tolerate. You commit to a rule: "I'll reject H₀ if my data lands in some rejection region R, and I've built R so that P(reject H₀ | H₀ true) ≤ α."

Common choices: α = 0.05, α = 0.01. You pick **one** α, run your test, and get a binary answer: reject or don't reject.

**The limitation:** if you tested at α = 0.05 and rejected, you don't know _how strongly_ you rejected. Would you have also rejected at α = 0.01 (very strong evidence)? Or would you have failed to reject at α = 0.04 (borderline)? Testing at one fixed α throws this information away.

## Step 2: The p-value fixes this — it summarizes ALL possible α at once

> **The p-value is the smallest α at which we would reject H₀.**

Think of it like a dial. As you slide α from 0 up to 1, at some point your test flips from "don't reject" to "reject" — and it stays "reject" for all larger α from then on (this is what "we reject at all α ≥ p" is describing — it's a one-way switch, not something that flickers back and forth).

The p-value is exactly the location of that switch.

**Intuitive picture:**

```
α:        0 -------- p -------- 1
Decision: [ don't reject ][ reject ]
```

So instead of running your test separately at α = 0.05, then α = 0.01, then α = 0.10, etc., the p-value tells you the _entire history_ of what would've happened at every α, compressed into one number.

**This is why "p < α" is the rejection rule.** If p = 0.03:

- At α = 0.05: since 0.05 ≥ 0.03, you reject. ✓
- At α = 0.01: since 0.01 < 0.03, you don't reject. ✓

The smaller the p-value, the stronger the evidence — it means you'd reject even at very strict (small) α thresholds.

## Step 3: Theorem 11 — how to actually compute a p-value

$$p = \sup_{\theta \in \Theta_0} P_\theta\big(T_n(X_1,\ldots,X_n) \geq T_n(x_1,\ldots,x_n)\big)$$

Don't let the sup scare you — break it into pieces:

- $T_n(x_1, \ldots, x_n)$ is just a number: the test statistic **you actually observed** in your real data. Call this the "observed value."
- $T_n(X_1, \ldots, X_n)$ is the test statistic as a **random variable** — what you'd get from a hypothetical fresh dataset.
- $P_\theta(T_n(X) \geq T_n(x))$ asks: "If θ were the true parameter, what's the probability that a fresh random dataset gives a test statistic _at least as extreme_ as what I actually observed?"
- The $\sup_{\theta \in \Theta_0}$ (supremum over the null region) says: check this probability for _every_ θ allowed under H₀, and take the worst case (largest probability) — this ensures your p-value is valid no matter which specific θ within Θ₀ happens to be true.

**Intuition:** the p-value answers _"assuming H₀, how surprising/extreme is the data I actually got?"_ A small p-value means "this data would be really unusual if H₀ were true" — that's evidence against H₀.

## Step 4: Example 12 — seeing this in action

Setup: $X_1, \ldots, X_n \sim N(\theta, 1)$, testing $H_0: \theta = \theta_0$ vs $H_1: \theta \neq \theta_0$ (two-sided test).

Here $\Theta_0$ is just a single point, ${\theta_0}$ — so no need for sup, just plug in $\theta_0$ directly.

- $T_n = \sqrt{n}(\bar{X}_n - \theta_0)$ — this measures how far your sample mean is from the hypothesized value, scaled by sample size.
- $t_n$ = the actual observed value of $T_n$ from your real data.
- We reject when $|T_n|$ is large (far from 0 in either direction — makes sense for a two-sided test).

Under $H_0$, $T_n \sim N(0,1)$ exactly (that's why they call it $Z$). So:

$$p = P_{\theta_0}(|T_n| \geq |t_n|) = P(|Z| \geq |t_n|) = 2\Phi(-|t_n|)$$

**In words:** "If H₀ is true, what's the probability a fresh sample would give a $|T_n|$ value at least as extreme as what I got?" The $2\Phi(-|t_n|)$ formula is just the standard normal tail probability, doubled because it's two-sided (extreme in either direction counts).

If your observed $t_n$ was huge (far from 0), that tail probability is tiny → small p-value → strong evidence against H₀. Exactly matches intuition: "my data is really unlikely under H₀" = "evidence against H₀."

## Step 5: Theorem 13 — p ~ Uniform(0,1) under H₀

This is a slightly deeper fact, but here's the intuition: if H₀ is really true, then your p-value is **just as likely to be 0.5 as 0.05 as 0.83** — it's uniformly random over [0,1]. There's no reason for it to systematically be small unless H₀ is actually false.

This is _why_ p < α gives you a valid test with false-positive rate α: if H₀ is true, $P(p < \alpha) = \alpha$ exactly (since p is uniform). So testing "reject if p < α" automatically controls your Type I error rate at α, by construction.

## Step 6: The crucial warning — p ≠ P(H₀ | data)

This is probably the single most common misinterpretation of p-values, so it's worth being very explicit:

- **p-value** = P(data this extreme or more | H₀ is true) — this is a **frequentist** quantity. It says nothing directly about whether H₀ is true; it's about how surprising your data would be _if_ H₀ were true.
- **P(H₀ | data)** = "given what I observed, what's the probability H₀ is true?" — this is a **Bayesian** quantity, and requires a prior probability on H₀ to even define. Classical (frequentist) hypothesis testing doesn't compute this at all.

**Common wrong interpretation:** "p = 0.03 means there's a 3% chance H₀ is true." **This is false.** The p-value is a statement about the data's extremity assuming H₀, not a probability statement about H₀ itself.

---

**Summary intuition to hold onto:** the p-value is a _dial-sweep_ over all possible α thresholds, condensed into one number that tells you exactly how strong your evidence against H₀ is — small p = would've rejected even under very strict standards = strong evidence.