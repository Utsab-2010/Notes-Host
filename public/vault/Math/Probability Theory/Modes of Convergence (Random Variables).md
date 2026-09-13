---
title: "Modes of Convergence (Random Variables)"
lastmod: 2026-07-23
---

# Why There's More Than One Kind

With regular sequences of numbers, convergence is unambiguous — $x_n \to x$ means the distance $|x_n - x|$ eventually gets and stays small. With sequences of **random variables**, there isn't one obvious notion of "closeness" anymore, because each $X_n$ is a whole distribution, not a single number. Depending on what you actually care about — individual sample paths, probabilities of deviation, the shape of the distribution, or average error — you get a genuinely different (and non-equivalent) definition of convergence. This is why there are four standard flavors, and why it's worth keeping them straight instead of hand-waving "it converges" without saying which kind.

## Almost Sure Convergence (a.s.)

$$X_n \xrightarrow{a.s.} X \quad \iff \quad P\left(\lim_{n\to\infty} X_n = X\right) = 1$$

This is the strongest, most intuitive one, and also the trickiest to actually verify. It says: if you fix a single outcome $\omega$ from the sample space and just watch the whole sequence $X_1(\omega), X_2(\omega), X_3(\omega), \dots$ play out, that specific sequence of numbers converges to $X(\omega)$ — and this holds for almost every $\omega$ (i.e. except possibly on a set of probability zero).

Intuition: this is about **entire sample paths** settling down, not about probabilities of being close on any given step. It's the "pathwise" notion of convergence. The Strong Law of Large Numbers is the canonical a.s. convergence result: the running sample average $\bar{X}_n = \frac{1}{n}\sum X_i$ converges almost surely to the true mean $\mu$.

## Convergence in Probability

$$X_n \xrightarrow{P} X \quad \iff \quad \forall \epsilon > 0, \quad \lim_{n\to\infty} P(|X_n - X| > \epsilon) = 0$$

Weaker than a.s. This says: the _probability_ of being far from $X$ shrinks to zero as $n$ grows, but it says nothing about individual sample paths behaving nicely — you could still have occasional large deviations happening infinitely often, as long as they get rarer and rarer, and that's still consistent with convergence in probability.

The classic way people distinguish a.s. from in-probability: convergence in probability only cares about the probability of a bad event _at each fixed $n$_; a.s. convergence cares about the probability that bad events happen _infinitely often_ as $n \to \infty$. That "infinitely often" condition is strictly stronger, which is exactly why a.s. convergence implies convergence in probability but not the reverse.

The Weak Law of Large Numbers is the canonical example here: $\bar{X}_n \xrightarrow{P} \mu$.

## Convergence in Distribution (a.k.a. Weak Convergence)

$$X_n \xrightarrow{d} X \quad \iff \quad F_{X_n}(x) \to F_X(x) \text{ at every continuity point of } F_X$$

The weakest of the four, and also the one that doesn't require $X_n$ and $X$ to even live on the same probability space or be related to each other at all — it's purely a statement about the CDFs getting close, not about the random variables themselves getting close in any pathwise sense.

This is the one behind the **Central Limit Theorem**: $\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$. Notice CLT is a statement about _shape of the distribution_ converging to a Gaussian — it says nothing about any individual sequence of sample paths settling down, which is why CLT is a distributional statement, not an a.s. or in-probability one.

## Convergence in $L^p$ (Mean-Square / Mean Convergence)

$$X_n \xrightarrow{L^p} X \quad \iff \quad E[|X_n - X|^p] \to 0$$

Most common case in practice is $p = 2$, i.e. **mean-square convergence**: $E[(X_n - X)^2] \to 0$. This is a statement about **average squared error** shrinking to zero — very natural in an ML/estimation context because it's literally the thing you're often directly optimizing (MSE).

Requires $X_n$ to actually have finite $p$-th moments to even be well-defined, which the other three don't require.

## The Hierarchy — What Implies What

This is the part actually worth memorizing cleanly, because it's asked about constantly and the arrows only go one way:

$$\text{a.s.} \implies \text{in probability} \implies \text{in distribution}$$ $$L^p \implies \text{in probability} \implies \text{in distribution}$$

- **a.s. $\Rightarrow$ in probability**: always true.
- **$L^p \Rightarrow$ in probability**: always true (this is basically Markov/Chebyshev's inequality doing the work — bound the probability of a big deviation using the expected squared error).
- **in probability $\Rightarrow$ in distribution**: always true.
- **None of the reverse arrows hold in general.** In particular, a.s. and $L^p$ convergence don't imply each other either — they're not nested with respect to each other, both just happen to imply "in probability."
- **Exception where the arrows _do_ reverse**: if $X_n \xrightarrow{d} c$ for a _constant_ $c$ (not a general random variable), then convergence in distribution to a constant _does_ imply convergence in probability to that constant. Worth remembering as the one special case where "weakest" becomes "as strong as" — because convergence to a degenerate point mass removes the ambiguity that distributional convergence normally allows.

---
## Classic Counterexamples Worth Keeping in Your Back Pocket

**In probability but NOT a.s.** — the standard example: a sequence of indicator random variables on $[0,1]$ that "sweep" across the interval — like $X_n = \mathbb{1}[\omega \in [\frac{k}{2^j}, \frac{k+1}{2^j}]]$ for an appropriately indexed sequence covering the unit interval repeatedly as $n$ increases. $P(X_n \neq 0) \to 0$ so it converges in probability to 0, but for _any_ fixed $\omega$, $X_n(\omega) = 1$ infinitely often as the sweeping interval passes back over that point — so the sequence never actually settles down pointwise for any $\omega$, meaning it fails to converge a.s. anywhere.

**In probability but NOT in $L^p$** — take $X_n$ that's 0 with probability $1 - 1/n$ and equal to $n$ with probability $1/n$. $P(|X_n| > \epsilon) = 1/n \to 0$, so it converges to 0 in probability, but $E[X_n^2] = n^2 \cdot (1/n) = n \to \infty$, so it diverges in $L^2$. The rare-but-huge event is invisible to "in probability" (which just checks if the _probability mass_ of being far away shrinks) but is exactly what blows up an expectation.
