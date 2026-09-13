---
title: "Linear MMSE Estimation"
lastmod: 2026-07-27
---

## The Problem This Solves

You want to estimate an unobserved random variable $X$ from an observed $Y = y$. The best possible estimator in a mean-squared-error sense is the full conditional expectation:

$$\large g(y) = E[X \mid Y = y]$$

This is the "true" MMSE estimator — **no other function of $y$ beats it on average squared error**. The catch is that it's often impractical: computing $E[X|Y=y]$ requires knowing the full conditional density $f_{X|Y}(x|y)$, which can be nasty or entirely unknown, especially once $X, Y$ become vectors.

**Linear MMSE is the practical compromise**: instead of allowing $g(y)$ to be any function, restrict it to a straight line,

$$\hat{X}_L = aY + b$$

and just pick the best $a, b$. You give up some accuracy (unless the joint distribution happens to be linear/Gaussian, in which case linear MMSE _is_ the true MMSE) in exchange for needing only first and second moments — means, variances, one covariance — instead of the entire joint density. This is the real appeal: cheap to compute, and works even when you don't know the distribution shape at all, only its summary statistics.

## Setting Up the Optimization

Pick $a, b$ to minimize:

$$h(a,b) = E[(X - aY - b)^2]$$

This is just a quadratic in $a$ and $b$ (expand the square, take expectations term by term), so you can minimize it with plain calculus — take partials w.r.t. $a$ and $b$, set to zero, solve the resulting two linear equations. That's the entire derivation; no fancy machinery needed, which is part of why this is such an approachable result.

## The Result

$$a^* = \frac{\text{Cov}(X,Y)}{\text{Var}(Y)}, \qquad b^* = E[X] - a^*E[Y]$$

Plugging back in, the estimator is usually written in this cleaner "centered" form:

$$\hat{X}_L = \frac{\text{Cov}(X,Y)}{\text{Var}(Y)}\big(Y - E[Y]\big) + E[X]$$

Or, in terms of the correlation coefficient $\rho = \rho(X,Y)$ and standard deviations $\sigma_X, \sigma_Y$ (using $\text{Cov}(X,Y) = \rho\sigma_X\sigma_Y$):

$$\large \hat{X}_L = \frac{\rho,\sigma_X}{\sigma_Y}\big(Y - E[Y]\big) + E[X]$$

## Intuition Behind the Formula

This form is worth staring at directly rather than just memorizing:

- Start at your best guess with **no information at all** — just $E[X]$.
- Look at how far $Y$ deviates from its own mean: $(Y - E[Y])$.
- Scale that deviation by $\rho \sigma_X / \sigma_Y$ and add it as a correction.

The scaling factor is doing something very natural: $\sigma_X/\sigma_Y$ converts a deviation measured in $Y$'s units into $X$'s units, and $\rho$ shrinks the correction based on how reliable $Y$ actually is as a predictor. If $\rho = 0$ ($X, Y$ uncorrelated), the correction term vanishes entirely and $\hat{X}_L = E[X]$ — you ignore $Y$ completely, which makes total sense since an uncorrelated observation gives you nothing useful, at least linearly. If $|\rho| = 1$ (perfect linear relationship), the correction fully tracks $Y$'s deviation, rescaled — you'd be able to predict $X$ from $Y$ essentially exactly.

---
# The Orthogonality Principle

Define the estimation error $\tilde{X} = X - \hat{X}_L$. The theorem shows this error satisfies:

$$\large E[\tilde{X}] = 0, \qquad \text{Cov}(\tilde{X}, Y) = E[\tilde{X},Y] = 0$$

This is the **orthogonality principle**, and it's the geometric heart of why linear MMSE works the way it does. Think of random variables with finite variance as living in a vector space, where the "inner product" between two variables is $E[UV]$ (or, for centered variables, the covariance). Under that lens, $\hat{X}_L$ is literally the **orthogonal projection** of $X$ onto the subspace spanned by $\{1, Y\}$ (constants and linear functions of $Y$). The leftover error $\tilde{X}$ is perpendicular to that subspace (this is essentially why it's called an orthogonal projection) — exactly like the residual in ordinary least-squares regression being orthogonal to the fitted line. 

This isn't a coincidence: **linear MMSE estimation and linear regression are the same projection operation, just arrived at from a probability framing instead of a data-fitting framing.**

This also gives you a fast sanity check for any linear MMSE computation: if you compute $\hat{X}_L$ correctly, then $E[(X - \hat{X}_L),Y]$ should come out to exactly zero. Worth using as a routine check on any worked example (see below).

## The Resulting Minimum MSE

Plugging $a^*, b^*$ back into $h(a,b)$ gives a strikingly clean result:

$$\large \text{MSE} = E[\tilde{X}^2] = (1 - \rho^2)\text{Var}(X)$$

This is worth sitting with. $\text{Var}(X)$ is the error you'd have with _no information_ about $Y$ at all (just guessing $E[X]$ every time). The factor $(1-\rho^2)$ tells you exactly what fraction of that original uncertainty survives after using $Y$ optimally (in the linear sense):

- $\rho = 0$ → $(1-\rho^2) = 1$ → no reduction in error, $Y$ was useless (linearly)
- $\rho = \pm 1$ → $(1-\rho^2) = 0$ → error goes to zero, $Y$ determines $X$ exactly (linearly)
- anything in between → $\rho^2$ is literally the **fraction of variance in $X$ explained by the linear relationship with $Y$**

This is exactly the $R^2$ you'd recognize from linear regression — same object, same interpretation, because it's the same underlying projection.

---
# Worked Example

Let $X \sim \text{Uniform}(1,2)$, and given $X = x$, let $Y \mid X=x \sim \text{Exponential}(1/x)$ (so the average of $Y$ given $X=x$ is $x$ itself).

**Step 1 — get the moments**, using the law of iterated expectations throughout since we only know things conditionally on $X$:

$$E[X] = \tfrac{3}{2} \quad (\text{mean of Uniform}(1,2))$$ $$E[Y] = E[E[Y|X]] = E[X] = \tfrac{3}{2}$$ $$E[Y^2] = E[E[Y^2|X]] = E[2X^2] = \int_1^2 2x^2,dx = \tfrac{14}{3}$$ $$\text{Var}(Y) = E[Y^2] - (E[Y])^2 = \tfrac{14}{3} - \tfrac{9}{4} = \tfrac{29}{12}$$ $$E[XY] = E[X \cdot E[Y|X]] = E[X \cdot X] = \int_1^2 x^2,dx = \tfrac{7}{3}$$ $$\text{Cov}(X,Y) = E[XY] - E[X]E[Y] = \tfrac{7}{3} - \tfrac{9}{4} = \tfrac{1}{12}$$

**Step 2 — plug into the formula:**

$$\hat{X}_L = \frac{1/12}{29/12}\Big(Y - \tfrac{3}{2}\Big) + \tfrac{3}{2} = \frac{1}{29}\Big(Y - \tfrac{3}{2}\Big) + \tfrac{3}{2} = \frac{Y}{29} + \frac{42}{29}$$

**Step 3 — MSE**, using $\text{Var}(X) = \tfrac{1}{12}$ for a Uniform$(1,2)$ and $\rho^2 = \text{Cov}(X,Y)^2 / [\text{Var}(X)\text{Var}(Y)] = \tfrac{1}{29}$:

$$\text{MSE} = \Big(1 - \tfrac{1}{29}\Big)\cdot\tfrac{1}{12} = \tfrac{7}{87}$$

**Step 4 — sanity check via orthogonality.** With $\tilde{X} = X - \tfrac{Y}{29} - \tfrac{42}{29}$, computing $E[\tilde{X},Y]$ using the moments above collapses to exactly $0$, confirming the estimator was computed correctly.

Notice the coefficient on $Y$ came out tiny ($1/29$) — correctly reflecting that $\rho^2 = 1/29$ is small, i.e. $Y$ is only weakly (linearly) informative about $X$ here, so the estimator barely moves off the prior mean $E[X] = 3/2$ regardless of what $Y$ is observed to be.

## Connecting Back

- optimizers note → the quadratic-minimization-via-calculus trick used to derive $a^*, b^*$ is the exact same move as deriving the normal equations in least-squares regression
- SVD/EVD note → the projection-onto-a-subspace framing here generalizes directly to the vector case (Section 9.1.7 on the source page, "estimation for random vectors") — that version needs an actual matrix inverse (the "normal equations" in matrix form) instead of a scalar ratio, worth reading next
- modes of convergence note → linear MMSE is a finite-sample/population-moments object; worth keeping distinct from asymptotic estimator behavior (consistency, CLT-based confidence intervals) which is a different axis of "how good is my estimator" entirely