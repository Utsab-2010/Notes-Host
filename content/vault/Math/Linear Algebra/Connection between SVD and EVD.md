---
title: "Connection between SVD and EVD"
lastmod: 2026-07-21
---

## The Two Decompositions, Side by Side

**Eigenvalue decomposition (EVD)**: only defined (nicely) for square matrices, and only guaranteed to exist in this clean form if the matrix is diagonalizable. $$A = Q \Lambda Q^{-1}$$ If $A$ is symmetric, this gets even nicer: $Q$ is orthogonal ($Q^{-1} = Q^T$) and $\Lambda$ is real. $$A = Q \Lambda Q^T$$

**Singular value decomposition (SVD)**: exists for _any_ matrix, square or not. $$A = U \Sigma V^T$$ $U$ and $V$ are orthogonal (different spaces — $U$ lives in the `output/column space`, $V$ in the `input/row space`), $\Sigma$ is diagonal and non-negative.

The immediate thing to notice: SVD doesn't need square, doesn't need diagonalizable, doesn't even need real eigenvalues to exist. It always exists. That's the whole appeal — it's the "eigendecomposition that always works."

## The Actual Connection

This is the part that made it click for me: **SVD of $A$ is basically the EVD of $A^TA$ and $AA^T$, done simultaneously.**

Take $A^TA$. This is always square and symmetric (even if $A$ isn't), so it always has a clean eigen-decomposition: $$A^TA = V \Lambda V^T$$

Now compare to $A^TA$ computed from the SVD of $A$: $$A^TA = (U\Sigma V^T)^T(U\Sigma V^T) = V\Sigma^T U^T U \Sigma V^T = V \Sigma^2 V^T$$ (using $U^TU = I$ since $U$ is orthogonal)

Match the two expressions and you get:

- $V$ = eigenvectors of $A^TA$
- $\Sigma^2 = \Lambda$, i.e. **singular values of $A$ = square roots of eigenvalues of $A^TA$**

Same story for $AA^T$: its eigen-decomposition gives you $U$ (left singular vectors), and again the eigenvalues are $\sigma_i^2$.

So concretely, to compute SVD by hand you'd:

1. Form $A^TA$ (or $AA^T$, whichever is smaller)
2. Eigendecompose it → eigenvectors are $V$, eigenvalues are $\sigma_i^2$
3. Get $U$ from $U = AV\Sigma^{-1}$ (or eigendecompose $AA^T$ directly)

Nobody actually computes SVD this way in practice (squaring $A$ squares the condition number, numerically ugly), but this is the _conceptual_ bridge, and it's genuinely how you'd derive SVD from EVD if you had to.

## When SVD and EVD Literally Coincide

`Important`: If $A$ is symmetric **and positive semi-definite** (all eigenvalues $\geq 0$), then EVD and SVD are literally the same decomposition: $$\Large A = Q\Lambda Q^T = U \Sigma V^T \quad \text{with } U = V = Q, \ \Sigma = \Lambda$$

This makes sense given the derivation above — if $A$ is symmetric PSD, $A^TA = A^2$, and the eigenvectors of $A^2$ are the same as the eigenvectors of $A$, with eigenvalues squared and then square-rooted back to the original ones.

If $A$ is symmetric but has **negative** eigenvalues, EVD and SVD diverge slightly: singular values are always non-negative by definition ($\sigma_i = |\lambda_i|$), so wherever $\lambda_i < 0$, the **SVD absorbs the sign** into the corresponding **singular vector (flips its direction)** to keep $\sigma_i \geq 0$. So $U \neq V$ in that case even though $A$ is symmetric — they differ by sign flips on the columns corresponding to negative eigenvalues.

If $A$ is **not symmetric**, EVD and SVD are just genuinely different objects, telling you different things (see below), and in general $U \ne V$ and $\Sigma \ne \Lambda$ even if both existed.

## Why This Distinction Actually Matters, Not Just Algebra Bookkeeping

EVD answers: "are there directions that $A$ maps to a scalar multiple of themselves?" This is an intrinsic, single-space question — input and output live in the same space, and you're asking about self-consistency of the map. That's why it needs square matrices and can fail to exist nicely (e.g. rotation matrices have no real eigenvectors — nothing maps to a scaled version of itself under a pure rotation).

SVD answers a different question entirely: `"what's the best orthogonal basis for the input space, and the best orthogonal basis for the output space, such that the map between them is just diagonal scaling?"` It doesn't require self-consistency at all — input and output space can be totally different dimensions. This is why SVD always exists: you're not asking the matrix to have some special self-referential structure, you're just asking "if I'm allowed to pick different bases for domain and codomain, can I make this diagonal?" and the answer is always yes.

This is also why SVD is the one that shows up for **rectangular / non-square** matrices — data matrices (samples × features), covariance-adjacent things, low-rank approximation of any general matrix, etc. EVD only makes sense once you've already restricted to square matrices, and it only tells you something clean if the matrix is diagonalizable (symmetric matrices are always diagonalizable, which is why EVD is so often introduced alongside symmetric matrices specifically).

## PCA Is the Classic Place Both Show Up at Once

Worth cementing since I'll forget otherwise: for data matrix $X$ (centered, $n$ samples × $d$ features), covariance is $C = \frac{1}{n}X^TX$, which is symmetric PSD.

- EVD of $C$ gives you the principal components directly (eigenvectors of the covariance).
- SVD of $X$ itself gives you the same principal directions as $V$, with singular values related to eigenvalues of $C$ by $\sigma_i^2 = n\lambda_i$.

People do PCA via SVD of the raw data matrix rather than EVD of the covariance matrix specifically because forming $X^TX$ explicitly squares the condition number and loses numerical precision — same reason mentioned above. SVD-based PCA is just the numerically stable version of the exact same math.

## Connecting Back

- spectral norm note → literally defined as $\sigma_{\max}(A)$, which by everything above is $\sqrt{\lambda_{\max}(A^TA)}$ — so spectral norm note and this one are really just two views of one derivation
- optimizers note → Hessian eigendecomposition (EVD, since Hessian is symmetric) is the "pure" curvature picture; SVD-style thinking shows up more when you're looking at Jacobians / non-square linear maps between layers
- attention note → worth double-checking whether attention weight matrices being non-square is why people reach for SVD-style analysis (e.g. rank of $W_Q W_K^T$) rather than eigen-analysis when studying attention head behavior
