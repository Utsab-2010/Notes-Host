---
title: "Markov, Chebyshev, and Jensen's Inequalities"
lastmod: 2026-07-04
---

# Markov's Inequality

### Statement

Let $X$ be a non-negative random variable (i.e., $X \geq 0$ almost surely), and let $a > 0$. Then

$$ P(X \geq a) \leq \frac{E[X]}{a}. $$

### Proof

Define the indicator random variable

$$ \mathbb{1}_{{X \geq a}} = \begin{cases} 1 & \text{if } X \geq a \ 0 & \text{otherwise}. \end{cases} $$

**Key pointwise inequality.** We claim that for every outcome $\omega$,

$$ a \cdot \mathbb{1}_{{X(\omega) \geq a}} \leq X(\omega). $$

- If $X(\omega) \geq a$: the left side is $a$, and since $X(\omega) \geq a$, we have $a \leq X(\omega)$. ✓
- If $X(\omega) < a$: the left side is $0$, and since $X(\omega) \geq 0$ (non-negativity), we have $0 \leq X(\omega)$. ✓

So the inequality holds in both cases, for every outcome. Taking expectations on both sides (expectation preserves $\leq$):

$$ E\left[a \cdot \mathbb{1}_{{X \geq a}}\right] \leq E[X] $$

$$ a \cdot P(X \geq a) \leq E[X] $$

$$ P(X \geq a) \leq \frac{E[X]}{a}. \qquad \blacksquare $$

### Remark

This is the workhorse inequality — nearly every other concentration bound (Chebyshev, Chernoff) is derived by applying Markov's inequality to a cleverly transformed version of $X$.

---

# Chebyshev's Inequality

### Statement
Let $X$ be a random variable with finite mean $\mu = E[X]$ and finite variance $\sigma^2 = \text{Var}(X)$. Then for any $k > 0$,
$$ P(|X - \mu| \geq k) \leq \frac{\sigma^2}{k^2}. $$

### Proof
Define the non-negative random variable
$$ Y = (X - \mu)^2. $$

Note that $Y \geq 0$ always, so Markov's inequality applies to $Y$. Also observe that
$$ |X - \mu| \geq k \quad \Longleftrightarrow \quad (X-\mu)^2 \geq k^2 \quad \Longleftrightarrow \quad Y \geq k^2, $$

since both sides are non-negative and squaring is monotonic on $[0, \infty)$.

Apply Markov's inequality to $Y$ with threshold $k^2$:

$$ P(Y \geq k^2) \leq \frac{E[Y]}{k^2}. $$

But $E[Y] = E[(X-\mu)^2] = \text{Var}(X) = \sigma^2$ by definition of variance. Substituting,

$$ P(|X - \mu| \geq k) = P(Y \geq k^2) \leq \frac{\sigma^2}{k^2}. \qquad \blacksquare $$

### Remark

Chebyshev's inequality is really just Markov's inequality applied to the squared deviation $(X-\mu)^2$. It gives a **distribution-free** bound on how much a random variable can deviate from its mean, using only two moments ($\mu, \sigma^2$).

A common alternate form: setting $k = c\sigma$ for $c > 0$,

$$ P(|X - \mu| \geq c\sigma) \leq \frac{1}{c^2}. $$

---
# Jensen's Inequality

### Statement

Let $\varphi: \mathbb{R} \to \mathbb{R}$ be a **convex** function, and let $X$ be a random variable with finite expectation. Then

$$ \varphi(E[X]) \leq E[\varphi(X)]. $$

(If $\varphi$ is concave, the inequality reverses: $\varphi(E[X]) \geq E[\varphi(X)]$.)

### Proof

The proof relies on the **supporting line** property of convex functions.

**Supporting line lemma.** If $\varphi$ is convex, then at any point $x_0$, there exists a line $L(x) = \varphi(x_0) + m(x - x_0)$ (where $m$ is the slope, e.g. a subgradient of $\varphi$ at $x_0$) such that

$$ \varphi(x) \geq L(x) = \varphi(x_0) + m(x - x_0) \quad \text{for all } x. $$

Intuitively: a convex function always lies _above_ any tangent/supporting line drawn at a point on its graph.

**Applying the lemma.** Let $\mu = E[X]$, and take the supporting line of $\varphi$ at the point $x_0 = \mu$:

$$ \varphi(x) \geq \varphi(\mu) + m(x - \mu) \quad \text{for all } x. $$

Substitute the random variable $X$ in place of $x$ (this holds for every realization of $X$):

$$ \varphi(X) \geq \varphi(\mu) + m(X - \mu). $$

Take expectations of both sides:

$$ E[\varphi(X)] \geq E[\varphi(\mu) + m(X - \mu)] = \varphi(\mu) + m\big(E[X] - \mu\big). $$

But $E[X] = \mu$, so the last term vanishes:

$$ E[\varphi(X)] \geq \varphi(\mu) = \varphi(E[X]). \qquad \blacksquare $$

### Remark

- Equality holds iff $\varphi$ is affine on the support of $X$, or $X$ is a.s. constant.
- This inequality is why, e.g., $E[X^2] \geq (E[X])^2$ (taking $\varphi(x) = x^2$, convex), which is equivalent to $\text{Var}(X) \geq 0$.
- It's also the basis for many information-theoretic results (e.g., non-negativity of KL divergence follows from Jensen applied to $-\log$, which is convex).

---

## Summary Table

|Inequality|Requires|Gives a bound on|
|---|---|---|
|Markov|$X \geq 0$|$P(X \geq a)$ using only $E[X]$|
|Chebyshev|Finite mean & variance|$P(\lvert X-\mu\rvert \geq k)$ using $\mu, \sigma^2$|
|Jensen|Convexity of $\varphi$|Relates $\varphi(E[X])$ and $E[\varphi(X)]$|

**Logical chain:** Chebyshev is derived directly from Markov (applied to $(X-\mu)^2$). Jensen is independent — it relies on convexity rather than a moment bound — but is frequently combined with Markov/Chebyshev-style arguments in deriving concentration inequalities (e.g., Chernoff bounds use Markov applied to $e^{tX}$, and convexity of the exponential is what makes the bound tight after optimizing over $t$).