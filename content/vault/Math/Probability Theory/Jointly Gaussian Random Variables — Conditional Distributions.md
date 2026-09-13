---
title: "Jointly Gaussian Random Variables — Conditional Distributions"
lastmod: 2026-07-19
---

## 1. Setup

Let $X, Y$ be jointly Gaussian scalar random variables with

$$ \mu_X = E[X], \quad \mu_Y = E[Y], \quad \sigma_X^2 = \text{Var}(X), \quad \sigma_Y^2 = \text{Var}(Y), \quad \rho = \frac{\text{Cov}(X,Y)}{\sigma_X\sigma_Y} $$

**Key fact:** the Gaussian family is closed under conditioning. If $(X,Y)$ is jointly Gaussian, then $Y \mid X = x$ is _also_ Gaussian — not just approximately, exactly.

---

## 2. Scalar result

$$ Y \mid X = x ;\sim; \mathcal{N}!\left(\mu_{Y|X},\ \sigma_{Y|X}^2\right) $$

**Conditional mean:** $$ \mu_{Y|X} = \mu_Y + \rho,\frac{\sigma_Y}{\sigma_X}(x - \mu_X) $$

**Conditional variance:** $$ \sigma_{Y|X}^2 = \sigma_Y^2(1-\rho^2) $$

### Observations

- **Mean is linear in $x$** — this is exactly the regression line of $Y$ on $X$. In the Gaussian case, the best linear predictor coincides with the best predictor of any form.
- **Variance is independent of $x$** (homoscedasticity) — the spread around the conditional mean doesn't depend on where $X$ landed.
- As $|\rho| \to 1$: $\sigma_{Y|X}^2 \to 0$ (perfect predictability).
- As $\rho \to 0$: $\sigma_{Y|X}^2 \to \sigma_Y^2$, recovering independence.

By symmetry, swapping roles gives $X \mid Y$: $$ \mu_{X|Y} = \mu_X + \rho\frac{\sigma_X}{\sigma_Y}(y-\mu_Y), \qquad \sigma_{X|Y}^2 = \sigma_X^2(1-\rho^2) $$

---

## 3. Matrix (multivariate) form

Let $\mathbf{Z} = \begin{bmatrix}\mathbf{X}\ \mathbf{Y}\end{bmatrix}$, $\mathbf{X}\in\mathbb{R}^m$, $\mathbf{Y}\in\mathbb{R}^n$, jointly Gaussian:

$$ \mathbf{Z}\sim\mathcal{N}(\boldsymbol\mu,\boldsymbol\Sigma),\qquad \boldsymbol\mu = \begin{bmatrix}\boldsymbol\mu_{X}\\ \boldsymbol\mu_Y \end{bmatrix},\qquad \boldsymbol\Sigma = \begin{bmatrix}\boldsymbol\Sigma_{XX} & \boldsymbol\Sigma_{XY}\ \boldsymbol\Sigma_{YX} & \boldsymbol\Sigma_{YY}\end{bmatrix} $$

with $\boldsymbol\Sigma_{XY} = \boldsymbol\Sigma_{YX}^T = \text{Cov}(\mathbf{X},\mathbf{Y})$.

**Conditional mean vector:** $$ \boldsymbol\mu_{Y|X} = \boldsymbol\mu_Y + \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}(\mathbf{x}-\boldsymbol\mu_X) $$

**Conditional covariance (Schur complement):** $$ \boldsymbol\Sigma_{Y|X} = \boldsymbol\Sigma_{YY} - \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} $$

### Observations

- $\boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}$ is the multivariate regression coefficient matrix of $\mathbf{Y}$ on $\mathbf{X}$.
- $\boldsymbol\Sigma_{Y|X}$ doesn't depend on $\mathbf{x}$ — homoscedasticity generalizes exactly.
- $\boldsymbol\Sigma_{Y|X} \preceq \boldsymbol\Sigma_{YY}$ (PSD ordering): conditioning never increases uncertainty.
- If $\boldsymbol\Sigma_{XY}=\mathbf{0}$, recovers independence: $\boldsymbol\mu_{Y|X}=\boldsymbol\mu_Y$, $\boldsymbol\Sigma_{Y|X}=\boldsymbol\Sigma_{YY}$.

**Scalar check:** setting $m=n=1$, $\Sigma_{XX}=\sigma_X^2$, $\Sigma_{YY}=\sigma_Y^2$, $\Sigma_{XY}=\rho\sigma_X\sigma_Y$ recovers the scalar formulas exactly.

---
## Rigorous derivation via orthogonality / linear innovations

### Step 0: The one fact we need as a lemma

**Lemma:** Any linear transformation of a jointly Gaussian vector is jointly Gaussian.

_Proof:_ If $\mathbf{Z}$ is Gaussian with characteristic function $\phi_Z(\mathbf{t}) = \exp(i\mathbf{t}^T\boldsymbol\mu - \frac12\mathbf{t}^T\boldsymbol\Sigma\mathbf{t})$, then for $\mathbf{W} = \mathbf{A}\mathbf{Z}$, $\phi_W(\mathbf{t}) = E[e^{i\mathbf{t}^T\mathbf{A}\mathbf{Z}}] = \phi_Z(\mathbf{A}^T\mathbf{t}) = \exp(i\mathbf{t}^T\mathbf{A}\boldsymbol\mu - \frac12\mathbf{t}^T\mathbf{A}\boldsymbol\Sigma\mathbf{A}^T\mathbf{t})$, which is the characteristic function of $\mathcal{N}(\mathbf{A}\boldsymbol\mu, \mathbf{A}\boldsymbol\Sigma\mathbf{A}^T)$. $\blacksquare$

This one fact does almost all the work below.

### Step 1: Construct a candidate "error" variable

Define the linear predictor and residual:

$$ \hat{\mathbf{Y}} = \boldsymbol\mu_Y + \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}(\mathbf{X}-\boldsymbol\mu_X), \qquad \mathbf{e} = \mathbf{Y} - \hat{\mathbf{Y}} $$

Note $\mathbf{e}$ is a fixed linear combination of $\mathbf{X}$ and $\mathbf{Y}$:

$$ \mathbf{e} = \mathbf{Y} - \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\mathbf{X} - \left(\boldsymbol\mu_Y - \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\mu_X\right) $$

Since $(\mathbf{X}, \mathbf{e})$ is a linear transformation of $(\mathbf{X}, \mathbf{Y})$, which is jointly Gaussian, **Step 0's lemma guarantees $(\mathbf{X}, \mathbf{e})$ is jointly Gaussian too.**

### Step 2: Show $\mathbf{e}$ has mean zero and is uncorrelated with $\mathbf{X}$

Mean: $E[\mathbf{e}] = E[\mathbf{Y}] - \boldsymbol\mu_Y = 0$ by construction (linear in $\mathbf{X}-\boldsymbol\mu_X$ which has mean zero).

Cross-covariance — this is the step that actually needs checking, not asserting:

$$ \text{Cov}(\mathbf{X}, \mathbf{e}) = \text{Cov}(\mathbf{X}, \mathbf{Y}) - \text{Cov}\left(\mathbf{X},\ \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\mathbf{X}\right) $$

$$ = \boldsymbol\Sigma_{XY} - \boldsymbol\Sigma_{XX}\left(\boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\right)^T = \boldsymbol\Sigma_{XY} - \boldsymbol\Sigma_{XX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} = \boldsymbol\Sigma_{XY}-\boldsymbol\Sigma_{XY} = \mathbf{0} $$

(using $\text{Cov}(\mathbf{X}, \mathbf{A}\mathbf{X}) = \text{Cov}(\mathbf{X},\mathbf{X})\mathbf{A}^T = \boldsymbol\Sigma_{XX}\mathbf{A}^T$, and $\boldsymbol\Sigma_{XX}$ symmetric). So $\mathbf{X}$ and $\mathbf{e}$ are **uncorrelated**.

### Step 3: Uncorrelated + jointly Gaussian $\Rightarrow$ independent

This is the crucial special property of Gaussians (false for general distributions). Since $(\mathbf{X},\mathbf{e})$ is jointly Gaussian with $\text{Cov}(\mathbf{X},\mathbf{e})=\mathbf{0}$, their joint covariance matrix is block-diagonal:

$$ \text{Cov}\begin{pmatrix}\mathbf{X}\\mathbf{e}\end{pmatrix} = \begin{bmatrix}\boldsymbol\Sigma_{XX} & \mathbf{0}\ \mathbf{0} & \boldsymbol\Sigma_{ee}\end{bmatrix} $$

A Gaussian density with block-diagonal covariance **factors exactly** into the product of the marginals (check directly: $\boldsymbol\Sigma^{-1}$ is also block-diagonal, so the joint exponent splits into a sum of two independent quadratic forms, and the normalizing constant $|\boldsymbol\Sigma|^{-1/2}$ splits as $|\boldsymbol\Sigma_{XX}|^{-1/2}|\boldsymbol\Sigma_{ee}|^{-1/2}$). So:

$$ \mathbf{X} \perp \mathbf{e} $$

### Step 4: Assemble the conditional distribution

Since $\mathbf{Y} = \hat{\mathbf{Y}}(\mathbf{X}) + \mathbf{e}$, and $\mathbf{e}$ is **independent of $\mathbf{X}$**, conditioning on $\mathbf{X}=\mathbf{x}$ just fixes the first term and leaves $\mathbf{e}$'s distribution untouched:

$$ \mathbf{Y}\mid\mathbf{X}=\mathbf{x} ;\stackrel{d}{=}; \hat{\mathbf{Y}}(\mathbf{x}) + \mathbf{e}, \qquad \mathbf{e}\sim\mathcal{N}(\mathbf{0}, \boldsymbol\Sigma_{ee}) $$

which is exactly $\mathcal{N}(\hat{\mathbf{Y}}(\mathbf{x}), \boldsymbol\Sigma_{ee})$, matching $\boldsymbol\mu_{Y|X}$ from before. It remains only to compute $\boldsymbol\Sigma_{ee} = \text{Var}(\mathbf{e})$ explicitly:

$$ \boldsymbol\Sigma_{ee} = \text{Var}(\mathbf{Y}) - \text{Var}(\hat{\mathbf{Y}}) \quad(\text{since } \mathbf{Y} = \hat{\mathbf{Y}}+\mathbf{e}, \ \hat{\mathbf{Y}}\perp\mathbf{e} \text{ — need this too, shown below}) $$

Actually cleanest is direct computation:

$$ \boldsymbol\Sigma_{ee} = \text{Var}(\mathbf{Y} - \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\mathbf{X}) = \boldsymbol\Sigma_{YY} - \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} - \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} + \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} $$

$$ = \boldsymbol\Sigma_{YY} - 2\boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} + \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} = \boldsymbol\Sigma_{YY} - \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}\boldsymbol\Sigma_{XY} $$

using $\text{Var}(\mathbf{A}\mathbf{X}) = \mathbf{A}\boldsymbol\Sigma_{XX}\mathbf{A}^T$ and $\text{Cov}(\mathbf{Y},\mathbf{A}\mathbf{X}) = \boldsymbol\Sigma_{YX}\mathbf{A}^T$ with $\mathbf{A} = \boldsymbol\Sigma_{YX}\boldsymbol\Sigma_{XX}^{-1}$. This **exactly** matches $\boldsymbol\Sigma_{Y|X}$. $\blacksquare$


---
## 5. Sanity checks / intuition

- **Geometric picture:** the joint density is an elliptical hill in $(x,y)$. Slicing at fixed $x$ gives a 1D Gaussian bump in $y$, centered on the ellipse's ridge at that $x$ (the linear conditional mean) with width set by the ellipse's shape after accounting for correlation.
- **$\rho \to 0$:** recovers marginal independence.
- **$\rho \to \pm1$:** conditional variance $\to 0$, i.e. $Y$ becomes a deterministic linear function of $X$.
- **PSD ordering** ($\boldsymbol\Sigma_{Y|X}\preceq\boldsymbol\Sigma_{YY}$) is the multivariate analog of "conditioning reduces variance," consistent with the law of total variance: $$ \text{Var}(Y) = E[\text{Var}(Y|X)] + \text{Var}(E[Y|X]) ;\geq; E[\text{Var}(Y|X)] $$

---

## 6. Where this shows up

- **Gaussian Processes** — the entire predictive posterior of a GP is derived from exactly this conditioning formula, with $X$ = training points, $Y$ = test points.
- **Kalman filter** — the update step is this same Schur-complement conditioning, applied recursively.
- **Linear regression under Gaussian assumptions** — the OLS solution is the MLE of $\boldsymbol\mu_{Y|X}$ here; ties back nicely to the Wiener/Kalman framing you've used before for diffusion models.

## Related Notes
- [Gaussian Distributions](/vault/math/probability-theory/gaussian-distributions/)
- [Power of Test Statistic](/vault/math/probability-theory/power-of-test-statistic/)
- [Total Expectation Theorem](/vault/math/probability-theory/total-expectation-theorem/)
- [p-values](/vault/math/probability-theory/p-values/)
