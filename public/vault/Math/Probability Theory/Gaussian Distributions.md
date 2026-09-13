---
title: "Gaussian Distributions"
lastmod: 2026-07-06
---

# 1. Univariate Gaussian

### 1.1 Definition

$X \sim \mathcal{N}(\mu, \sigma^2)$ has density

$$ p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right). $$

Standard normal: $Z \sim \mathcal{N}(0,1)$, with $X = \mu + \sigma Z$.

### 1.2 Moments

- $E[X] = \mu$, $\text{Var}(X) = \sigma^2$
- All odd central moments vanish; $E[(X-\mu)^4] = 3\sigma^4$ (this "3" is why **kurtosis** is defined relative to Gaussian as baseline — excess kurtosis $= 0$ for Gaussian).
- **Moment Generating Function (MGF):** $$ M_X(t) = E[e^{tX}] = \exp\left(\mu t + \frac{\sigma^2 t^2}{2}\right). $$
- **Characteristic Function (CF):** $$ \phi_X(t) = E[e^{itX}] = \exp\left(i\mu t - \frac{\sigma^2 t^2}{2}\right). $$

**Trick:** The MGF/CF of a Gaussian is itself an exponential-of-quadratic — this closure property is _why_ sums of independent Gaussians are Gaussian (MGFs multiply, and the product of two exponential-quadratics is another exponential-quadratic).

### 1.3 Sums and Linear Combinations

If $X_i \sim \mathcal{N}(\mu_i, \sigma_i^2)$ independent, and $a_i$ constants:

$$ \sum_i a_i X_i \sim \mathcal{N}\left(\sum_i a_i \mu_i,\ \sum_i a_i^2 \sigma_i^2\right). $$

This is a **closure property**: Gaussians are closed under affine combinations. No other common continuous distribution has this except the Cauchy (stable but no finite variance) and other stable distributions in general.

### 1.4 Standardization / Z-scores

$$ Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0,1). $$

Used constantly for hypothesis testing, feature normalization (though empirically — true normalization of features assumes Gaussianity, which is often just a convenient approximation).

---

# 2. Multivariate Gaussian (Gaussian Random Vectors)

### 2.1 Definition

$\mathbf{X} \in \mathbb{R}^d \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$, with $\boldsymbol{\Sigma} \succ 0$ (positive definite), has density

$$ p(\mathbf{x}) = \frac{1}{(2\pi)^{d/2} |\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x}-\boldsymbol{\mu})\right). $$

- $\boldsymbol{\mu} = E[\mathbf{X}]$
- $\boldsymbol{\Sigma} = E[(\mathbf{X}-\boldsymbol{\mu})(\mathbf{X}-\boldsymbol{\mu})^\top]$ — covariance matrix (symmetric PSD).
- $\boldsymbol{\Lambda} = \boldsymbol{\Sigma}^{-1}$ — the **precision matrix**. Off-diagonal entries of $\boldsymbol{\Lambda}$ directly encode **conditional independence**: $\Lambda_{ij} = 0 \iff X_i \perp X_j \mid \text{rest}$. This is the foundation of **Gaussian Graphical Models**.

### 2.2 Equivalent Definition (very useful)
$\mathbf{X}$ is Gaussian iff every linear combination $\mathbf{a}^\top \mathbf{X}$ is a univariate Gaussian, for all $\mathbf{a} \in \mathbb{R}^d$. This is often the cleanest way to _prove_ something is jointly Gaussian without touching the density formula (e.g., proving that a linear transform of a Gaussian vector, or a limit of Gaussian vectors, is Gaussian).

### 2.3 Alternative Construction
$\mathbf{X} = \boldsymbol{\mu} + \mathbf{A}\mathbf{Z}$, where $\mathbf{Z} \sim \mathcal{N}(0, I)$ and $\boldsymbol{\Sigma} = \mathbf{A}\mathbf{A}^\top$. This is exactly the **reparameterization trick** used in VAEs and diffusion models: sample standard noise, then apply an affine transform to get the desired distribution — critical because it makes sampling differentiable w.r.t. $\boldsymbol{\mu}, \mathbf{A}$ (pathwise gradient estimator, vs. score-function/REINFORCE estimator).

### 2.4 Isserlis' Theorem (Wick's Theorem)

For zero-mean jointly Gaussian $X_1, \dots, X_{2n}$:

$$ E[X_1 X_2 \cdots X_{2n}] = \sum_{\text{pairings}} \prod_{\text{pairs } (i,j)} E[X_i X_j]. $$

(Odd-order moments are zero.) This shows up in computing higher moments in Gaussian Processes and in diffusion model noise-schedule derivations, and is the combinatorial backbone of Feynman diagrams in physics.

---

# 3. Affine Transformations
If $\mathbf{X} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ and $\mathbf{Y} = \mathbf{A}\mathbf{X} + \mathbf{b}$:

$$ \mathbf{Y} \sim \mathcal{N}(\mathbf{A}\boldsymbol{\mu} + \mathbf{b},\ \mathbf{A}\boldsymbol{\Sigma}\mathbf{A}^\top). $$

**This single fact underlies almost everything downstream** — Kalman filter updates, linear-Gaussian state-space models, backprop through Gaussian sampling layers, forward diffusion process ($x_t = \sqrt{\bar\alpha_t} x_0 + \sqrt{1-\bar\alpha_t}\epsilon$), and more.

---

# Jointly Gaussian Random Variables

Random variables $X_1, X_2, \dots, X_n$ are said to be **jointly Gaussian** (or to have a **multivariate Gaussian distribution**) if every linear combination of them is a univariate Gaussian random variable. That is,

$$ X_1, \dots, X_n \text{ are jointly Gaussian} \iff \sum_{i=1}^{n} a_i X_i \sim \mathcal{N}(\mu, \sigma^2) \quad \text{for every choice of constants } a_1, \dots, a_n \in \mathbb{R}, $$

for some $\mu \in \mathbb{R}$ and $\sigma^2 \geq 0$ depending on the $a_i$'s. (The degenerate case $\sigma^2 = 0$, i.e. a point mass, is included.)

Equivalently, writing $\mathbf{X} = (X_1, \dots, X_n)^\top$, this means $\mathbf{X}$ has a joint density of the form

$$ p(\mathbf{x}) = \frac{1}{(2\pi)^{n/2}|\boldsymbol{\Sigma}|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right), $$

where $\boldsymbol{\mu} = E[\mathbf{X}]$ and $\boldsymbol{\Sigma} = \text{Cov}(\mathbf{X})$ (assuming $\boldsymbol{\Sigma}$ is invertible; if singular, the distribution is degenerate and supported on a lower-dimensional affine subspace).

### Key subtlety

"Jointly Gaussian" is a **stronger** condition than each $X_i$ being individually (marginally) Gaussian. It's possible to construct random variables that are each marginally Gaussian but **not** jointly Gaussian — for instance, $X \sim \mathcal{N}(0,1)$ and $Y = SX$ where $S$ is an independent random sign ($\pm 1$ with probability $1/2$ each). Both $X$ and $Y$ are individually $\mathcal{N}(0,1)$, and they're even uncorrelated, but $X+Y$ is not Gaussian (it's a point mass at $0$ half the time), so $(X,Y)$ is not jointly Gaussian.

This is exactly why the equivalence **uncorrelated ⟺ independent** (Section 5 in your Gaussian notes) requires the _jointly_ Gaussian assumption — marginal Gaussianity alone isn't enough.

---
## 4. Marginals and Conditionals (the single most useful result for ML)

Partition $\mathbf{X} = \begin{pmatrix}\mathbf{X}_1 \ \mathbf{X}_2\end{pmatrix}$ jointly Gaussian, with

$$ \boldsymbol{\mu} = \begin{pmatrix}\boldsymbol{\mu}_1 \ \boldsymbol{\mu}_2\end{pmatrix}, \qquad \boldsymbol{\Sigma} = \begin{pmatrix}\boldsymbol{\Sigma}_{11} & \boldsymbol{\Sigma}_{12} \ \boldsymbol{\Sigma}_{21} & \boldsymbol{\Sigma}_{22}\end{pmatrix}. $$



### 4.1 Marginal

$$ \mathbf{X}_1 \sim \mathcal{N}(\boldsymbol{\mu}_1, \boldsymbol{\Sigma}_{11}). $$

Just "drop the other block" — a huge simplification compared to marginalizing general distributions (no integration needed).

### 4.2 Conditional

$$ \mathbf{X}_1 \mid \mathbf{X}_2 = \mathbf{x}_2 \ \sim\ \mathcal{N}\Big(\boldsymbol{\mu}_1 + \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}(\mathbf{x}_2 - \boldsymbol{\mu}_2),\ \ \boldsymbol{\Sigma}_{11} - \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}\boldsymbol{\Sigma}_{21}\Big). $$
- The mean is shifted **linearly** in the observation — this linearity is exactly what makes the **Kalman filter** exact and closed-form for linear-Gaussian systems.
- The conditional covariance $\boldsymbol{\Sigma}_{11} - \boldsymbol{\Sigma}_{12}\boldsymbol{\Sigma}_{22}^{-1}\boldsymbol{\Sigma}_{21}$ is the **Schur complement** of $\boldsymbol{\Sigma}_{22}$ in $\boldsymbol{\Sigma}$. Crucially, it **does not depend on the observed value** $\mathbf{x}_2$ — only the mean shifts, uncertainty reduction is fixed in advance. This is the basis of **Gaussian Process regression**: the posterior variance at test points can be computed before seeing training labels.

### 4.3 Application: Gaussian Process Regression

Given $\begin{pmatrix}\mathbf{f} \\ \mathbf{f}_*\end{pmatrix} \sim \mathcal{N}\left(0, \begin{pmatrix}K & K_* \\ K_*^\top & K_{**}\end{pmatrix}\right)$ (kernel matrix blocks), the predictive distribution of test points $\mathbf{f}_*$ given training targets $\mathbf{f}$ follows directly from the conditional-Gaussian formula above:

$$
\mathbf{f}_* \mid \mathbf{f} \sim \mathcal{N}\big(K_*^\top K^{-1} \mathbf{f},\ K_{**} - K_*^\top K^{-1} K_*\big).
$$

---
## 5. Independence vs. Uncorrelatedness

- In general, **uncorrelated ⇏ independent**.
- **But** for _jointly_ Gaussian random variables, **uncorrelated ⟺ independent**. This is a special property of the Gaussian and is used constantly to simplify proofs (e.g., PCA whitening produces independent components _only because_ Gaussian assumptions are typically invoked; for non-Gaussian data, decorrelation via PCA does **not** give independence — this exact gap is what motivates **Independent Component Analysis (ICA)**).

⚠️ Caveat: individually-Gaussian-but-not-jointly-Gaussian variables can be uncorrelated yet dependent (classic counterexample: $X \sim \mathcal{N}(0,1)$, $S$ independent sign $\pm1$ w.p. $1/2$, $Y = SX$ — both marginals Gaussian, uncorrelated, but dependent).

---

## 6. Estimation (MLE, MAP, Bayesian)

### 6.1 MLE for $\mathcal{N}(\mu, \sigma^2)$ — univariate

Given i.i.d. samples $x_1, \dots, x_n$:

$$ \hat\mu_{\text{MLE}} = \frac{1}{n}\sum_i x_i, \qquad \hat\sigma^2_{\text{MLE}} = \frac{1}{n}\sum_i (x_i - \hat\mu)^2. $$

- $\hat\mu_{\text{MLE}}$ is **unbiased**.
- $\hat\sigma^2_{\text{MLE}}$ is **biased** (systematically underestimates true variance): $E[\hat\sigma^2_{\text{MLE}}] = \frac{n-1}{n}\sigma^2$. The unbiased correction is Bessel's correction: $\hat\sigma^2_{\text{unbiased}} = \frac{1}{n-1}\sum_i(x_i-\hat\mu)^2$.
- **Why biased:** using the _sample_ mean $\hat\mu$ instead of the true $\mu$ "uses up" one degree of freedom — the residuals $x_i - \hat\mu$ are constrained to sum to zero.

### 6.2 MLE for Multivariate Gaussian

$$ \hat{\boldsymbol{\mu}} = \frac{1}{n}\sum_i \mathbf{x}_i, \qquad \hat{\boldsymbol{\Sigma}} = \frac{1}{n}\sum_i (\mathbf{x}_i - \hat{\boldsymbol{\mu}})(\mathbf{x}_i - \hat{\boldsymbol{\mu}})^\top. $$

Same bias story: unbiased covariance estimator divides by $(n-1)$.

**Practical ML pitfall:** if $d > n$ (more dimensions than samples), $\hat{\boldsymbol{\Sigma}}$ is **rank-deficient / singular** — cannot invert it directly. Fixes:

- **Shrinkage estimators** (Ledoit-Wolf): $\hat{\boldsymbol{\Sigma}}_{\text{shrunk}} = (1-\alpha)\hat{\boldsymbol{\Sigma}} + \alpha \cdot \text{tr}(\hat{\boldsymbol{\Sigma}})/d \cdot I$.
- **Diagonal covariance assumption** (Naive Bayes Gaussian) — trades bias for enormously reduced variance/parameter count ($O(d)$ instead of $O(d^2)$).
- **Low-rank + diagonal structure** — exactly the assumption in **Probabilistic PCA / Factor Analysis** (Section 8).

### 6.3 MAP Estimation / Conjugate Priors

The Gaussian is **self-conjugate** for its own mean (with known variance):

- Prior: $\mu \sim \mathcal{N}(\mu_0, \tau_0^2)$
- Likelihood: $x_i \mid \mu \sim \mathcal{N}(\mu, \sigma^2)$ i.i.d.
- Posterior: $\mu \mid \mathbf{x} \sim \mathcal{N}(\mu_n, \tau_n^2)$ where

$$ \mu_n = \frac{\frac{1}{\tau_0^2}\mu_0 + \frac{n}{\sigma^2}\bar{x}}{\frac{1}{\tau_0^2} + \frac{n}{\sigma^2}}, \qquad \frac{1}{\tau_n^2} = \frac{1}{\tau_0^2} + \frac{n}{\sigma^2}. $$

**Precisions add.** This is the cleanest way to remember the update: **posterior precision = prior precision + data precision**, and the posterior mean is a **precision-weighted average** of the prior mean and the sample mean. This exact structure reappears in Kalman filter update equations (predict/update steps combine precisions the same way).

---

## 7. KL Divergence Between Gaussians (critical for VAEs / diffusion)

For $p = \mathcal{N}(\mu_1, \Sigma_1)$, $q = \mathcal{N}(\mu_2, \Sigma_2)$ in $\mathbb{R}^d$:

$$ D_{KL}(p | q) = \frac{1}{2}\left[\text{tr}(\Sigma_2^{-1}\Sigma_1) + (\mu_2-\mu_1)^\top \Sigma_2^{-1} (\mu_2-\mu_1) - d + \ln\frac{|\Sigma_2|}{|\Sigma_1|}\right]. $$

**Special case (both diagonal / scalar, used in VAE ELBO):** for $p = \mathcal{N}(\mu, \sigma^2)$, $q = \mathcal{N}(0,1)$:

$$ D_{KL}(p|q) = \frac{1}{2}\left(\sigma^2 + \mu^2 - 1 - \ln\sigma^2\right). $$

This exact closed form is what appears in the VAE loss (regularization term pushing the encoder's approximate posterior toward the standard normal prior). Its closed-form-ness is _precisely why_ Gaussian is the default choice for VAE latent priors — no Monte Carlo estimate of the KL term is needed.

**Entropy of a Gaussian** (needed to derive the KL formula, and shows up standalone in diffusion model ELBOs):

$$ H(\mathcal{N}(\mu,\Sigma)) = \frac{1}{2}\ln\left((2\pi e)^d |\Sigma|\right). $$

Notably, entropy **does not depend on $\mu$** — only on the covariance's determinant (a "volume" of uncertainty).

---

## 8. Probabilistic PCA / Factor Analysis (Gaussian latent variable models)

Model: $\mathbf{z} \sim \mathcal{N}(0, I_k)$ (latent, $k \ll d$), $\mathbf{x} \mid \mathbf{z} \sim \mathcal{N}(W\mathbf{z} + \boldsymbol{\mu}, \sigma^2 I_d)$.

Marginal: $\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}, WW^\top + \sigma^2 I)$ — follows directly from the affine transformation rule (Section 3) applied to the joint Gaussian $(\mathbf{z}, \mathbf{x})$.

- As $\sigma^2 \to 0$: MLE for $W$ recovers standard PCA (columns of $W$ span the top-$k$ eigenvector subspace of the sample covariance).
- This is the **direct conceptual ancestor of VAEs**: replace the linear map $W\mathbf{z}$ with a neural network $f_\theta(\mathbf{z})$, and you get a VAE decoder. The encoder in a VAE approximates the (generally intractable, once $f_\theta$ is nonlinear) posterior $p(\mathbf{z}\mid\mathbf{x})$ with a Gaussian — a "recognition network" — precisely because in the _linear_ Gaussian case (Probabilistic PCA) that posterior is exactly Gaussian and closed-form (Section 4.2), and this closed-form conditional structure is what VAEs try to approximate for nonlinear generative networks.

---

## 9. Gaussian Discriminant Analysis (LDA / QDA)

Classification: model $p(\mathbf{x} \mid y=k) = \mathcal{N}(\boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$, use Bayes rule for $p(y \mid \mathbf{x})$.

- **QDA (Quadratic Discriminant Analysis):** separate $\boldsymbol{\Sigma}_k$ per class → decision boundary is quadratic in $\mathbf{x}$ (log-densities have a $\mathbf{x}^\top\boldsymbol{\Sigma}_k^{-1}\mathbf{x}$ term that doesn't cancel between classes).
- **LDA (Linear Discriminant Analysis):** shared $\boldsymbol{\Sigma}$ across classes → the quadratic terms cancel in the log-odds ratio → decision boundary is **linear**. This is the direct link between "Gaussian class-conditional densities" and the "linear classifier" family.

---

## 10. Relations to Other Distributions

- **Chi-squared:** If $Z_1, \dots, Z_k$ i.i.d. $\mathcal{N}(0,1)$, then $\sum_i Z_i^2 \sim \chi^2_k$. Used in Mahalanobis-distance-based outlier detection: for $\mathbf{X} \sim \mathcal{N}(\boldsymbol{\mu},\boldsymbol{\Sigma})$, $(\mathbf{X}-\boldsymbol{\mu})^\top\boldsymbol{\Sigma}^{-1}(\mathbf{X}-\boldsymbol{\mu}) \sim \chi^2_d$ — gives a principled threshold for "how far is this point from the distribution, in standardized units."
- **Log-normal:** if $X \sim \mathcal{N}(\mu,\sigma^2)$ then $e^X$ is log-normal. Common in modeling multiplicative noise / strictly positive quantities.
- **Student's t:** arises as the marginal of $\mu$ when $\sigma^2$ itself is unknown and given an inverse-gamma prior (Normal-Inverse-Gamma conjugate model) — heavier tails than Gaussian, used when variance itself is uncertain.
- **Central Limit Theorem:** sums/averages of i.i.d. (finite variance) random variables converge in distribution to Gaussian — the deep reason Gaussian noise assumptions are so pervasive (aggregate of many small independent effects).
- **Maximum entropy:** among all distributions on $\mathbb{R}$ with a given mean and variance, the Gaussian has **maximum differential entropy**. This is arguably the deepest justification for defaulting to Gaussian assumptions when only first/second moments are known (least additional structure assumed) — this is also why Gaussian noise is the "worst case" / most conservative assumption in many robust-estimation and information-theoretic settings.

---

## 11. Short Tricks & Computational Recipes

### 11.1 Completing the square in the exponent

Whenever you see $-\frac{1}{2}(\mathbf{x}^\top A \mathbf{x} - 2\mathbf{b}^\top \mathbf{x})$ inside an exponential, it's proportional to a Gaussian density with

$$ \text{covariance} = A^{-1}, \qquad \text{mean} = A^{-1}\mathbf{b}. $$

This trick alone derives most Gaussian-conjugate-prior results (Bayesian linear regression posterior, Kalman update, GP posterior) without brute-force integration.

### 11.2 Woodbury Matrix Identity (avoiding $O(d^3)$ inversions)

$$ (A + UCV)^{-1} = A^{-1} - A^{-1}U(C^{-1}+VA^{-1}U)^{-1}VA^{-1}. $$

Used whenever covariance has structure $\Sigma = \sigma^2 I + WW^\top$ (as in Probabilistic PCA/Factor Analysis) — invert a $k\times k$ matrix instead of $d \times d$ when $k \ll d$.

### 11.3 Matrix Determinant Lemma

$$ |A + UV^\top| = |A|\cdot|I + V^\top A^{-1} U|. $$ Pairs with Woodbury — needed for the normalizing constant when using the low-rank covariance trick above.

### 11.4 Expectation of a quadratic form

For $\mathbf{X} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ and any (possibly asymmetric) matrix $A$:

$$ E[\mathbf{X}^\top A \mathbf{X}] = \text{tr}(A\boldsymbol{\Sigma}) + \boldsymbol{\mu}^\top A \boldsymbol{\mu}. $$

Constantly used in computing expected losses under Gaussian noise assumptions (e.g., expected squared error terms in Bayesian linear regression, diffusion model loss simplifications).

### 11.5 Whitening

$\mathbf{X} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$. Let $\boldsymbol{\Sigma} = LL^\top$ (Cholesky) or $\boldsymbol{\Sigma} = U\Lambda U^\top$ (eigendecomposition). Then

$$ \mathbf{Z} = L^{-1}(\mathbf{X}-\boldsymbol{\mu}) \quad \text{or} \quad \mathbf{Z} = \Lambda^{-1/2}U^\top(\mathbf{X}-\boldsymbol{\mu}) $$

gives $\mathbf{Z} \sim \mathcal{N}(0, I)$. This is exactly the "reparameterization trick" run in reverse (whitening vs. sampling are inverse operations) and is standard preprocessing to decorrelate/normalize features before many classical ML algorithms.

### 11.6 Product of two Gaussian densities (self-conjugacy trick)

The (unnormalized) product of two Gaussian densities in $\mathbf{x}$ is itself Gaussian in $\mathbf{x}$:

$$ \mathcal{N}(\mathbf{x}; \boldsymbol{\mu}_1, \boldsymbol{\Sigma}_1)\cdot\mathcal{N}(\mathbf{x}; \boldsymbol{\mu}_2, \boldsymbol{\Sigma}_2) \ \propto\ \mathcal{N}(\mathbf{x}; \boldsymbol{\mu}_c, \boldsymbol{\Sigma}_c), $$ $$ \boldsymbol{\Sigma}_c = (\boldsymbol{\Sigma}_1^{-1}+\boldsymbol{\Sigma}_2^{-1})^{-1}, \qquad \boldsymbol{\mu}_c = \boldsymbol{\Sigma}_c(\boldsymbol{\Sigma}_1^{-1}\boldsymbol{\mu}_1 + \boldsymbol{\Sigma}_2^{-1}\boldsymbol{\mu}_2). $$

This is the single algebraic fact underlying **Bayesian filtering (Kalman filter measurement update)**, precision-weighted MAP estimates (Section 6.3), and combining independent Gaussian "evidence" sources in general.

---

## 12. ML/DL-Specific Applications Summary

|Area|Where Gaussian assumptions show up|
|---|---|
|**Linear regression**|Gaussian noise on residuals ⟹ MLE = least squares; Bayesian linear regression uses Gaussian prior/posterior on weights (Section 6.3, 11.1)|
|**Kalman Filter**|Linear-Gaussian state-space model; predict step uses affine transform (Sec. 3), update step uses conditional-Gaussian / product-of-Gaussians (Sec. 4.2, 11.6)|
|**Gaussian Processes**|Infinite-dimensional generalization; prediction = conditional Gaussian formula (Sec. 4.2, 4.3)|
|**VAEs**|Encoder outputs Gaussian $q_\phi(\mathbf{z}\mid\mathbf{x})$; prior $p(\mathbf{z})=\mathcal{N}(0,I)$; reparameterization trick (Sec. 2.3); closed-form KL term in ELBO (Sec. 7)|
|**Diffusion Models**|Forward process is a fixed linear-Gaussian Markov chain ($q(x_t\mid x_{t-1})=\mathcal{N}(\sqrt{1-\beta_t}x_{t-1},\beta_t I)$); closed-form $q(x_t\mid x_0)$ via affine transform closure (Sec. 3); reverse process parameterized as Gaussian; training loss derived from KL between Gaussians at each step (Sec. 7)|
|**Naive Bayes (Gaussian)**|Diagonal-covariance class-conditional Gaussians (Sec. 6.2 pitfall fix)|
|**LDA/QDA**|Gaussian class-conditional densities → linear/quadratic decision boundaries (Sec. 9)|
|**PCA / Probabilistic PCA**|Latent Gaussian model; MLE recovers classical PCA as noise → 0 (Sec. 8)|
|**Weight initialization**|Xavier/He initialization draws from $\mathcal{N}(0,\sigma^2)$ with variance chosen to preserve activation variance across layers|
|**Batch/Layer Norm**|Explicitly re-centers/re-scales activations toward zero-mean, unit-variance — a soft Gaussian-like normalization, not distributional but statistical|
|**Label/feature noise, data augmentation**|Additive Gaussian noise as a standard regularizer/augmentation, justified via CLT + tractability|
|**Uncertainty quantification**|Gaussian likelihood heads (predict $\mu,\sigma^2$) for heteroscedastic regression; Gaussian approximations in Laplace approximation / variational inference|

---

## Summary: Why Gaussians Are Everywhere in ML

1. **Closed under affine transforms** (Sec. 3) → linear layers preserve Gaussianity, enabling exact inference in linear-Gaussian models.
2. **Closed under conditioning/marginalization** (Sec. 4) → exact, cheap posterior updates (Kalman filter, GPs, Bayesian linear regression).
3. **Self-conjugate** (Sec. 6.3, 11.6) → Bayesian updates stay in the Gaussian family, precision-additive updates.
4. **Fully characterized by 2 moments** → cheap to estimate, cheap to sample, cheap to compute KL/entropy in closed form (Sec. 7) → ideal for tractable variational objectives (ELBO in VAEs/diffusion).
5. **Maximum entropy given mean/variance** (Sec. 10) → the "least-assumption" choice whenever only first/second moments are known or estimable.
6. **CLT** (Sec. 10) → aggregate noise/errors from many small independent sources genuinely tend toward Gaussian in practice.