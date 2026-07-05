---
title: "Principal Component Analysis (PCA)"
lastmod: 2026-06-27
---

## 1. The Problem: Too Many Dimensions
Real-world data is almost always high-dimensional. A grayscale image of 100×100 pixels is a point in $\mathbb{R}^{10000}$. A gene expression profile might measure 20,000 genes. A bag-of-words document vector might have 50,000 features. Word2Vec embeddings live in $\mathbb{R}^{300}$.

High dimensionality creates several problems:
- **Visualization is impossible** beyond 3D. 
- **The curse of dimensionality**: in high dimensions, all points become approximately equidistant. Distance-based methods break down.
- **Redundancy**: many features are correlated. Gene expression levels of related genes co-vary. Pixel values in a face image are not independent — eyes, nose, and mouth all have structured correlations.
- **Noise**: many dimensions carry no signal, only noise. Including them hurts downstream models.
- **Computational cost**: algorithms scale with $d$. Unnecessary dimensions slow everything down.

PCA answers a precise question:
> **What is the low-dimensional subspace that captures the most variance in the data?**

Or equivalently: *what is the best linear approximation to a high-dimensional dataset using fewer dimensions?*

---
## 2. The Geometric Intuition

Before any math, build the picture.
Imagine you have a cloud of data points in 2D that looks like a stretched ellipse — most of the spread is along one diagonal direction, and there's much less spread perpendicular to it.

PCA finds the direction of maximum spread (the long axis of the ellipse) and calls it the **first principal component**. Then it finds the direction of maximum remaining spread, perpendicular to the first — the short axis — and calls it the **second principal component**.

If you projected all your 2D points onto just the first principal component (a 1D line), you'd retain most of the information about where points differ from each other. The projection onto the short axis loses relatively little — it's mostly noise.

This generalizes: in $d$ dimensions, PCA finds $d$ orthogonal directions ordered by how much variance they capture. You keep the top $k$ and discard the rest.

The fundamental principle:
> **Directions of high variance carry signal. Directions of low variance carry noise.**

*This assumption is not always true — it's the central assumption of PCA.* When it fails, PCA fails. But it's correct surprisingly often in practice.

---
## 3. Formalizing: What PCA Optimizes
### Setup
- $n$ data points $x_1, x_2, \ldots, x_n \in \mathbb{R}^d$
- Stored in a matrix $X \in \mathbb{R}^{n \times d}$ (rows are data points)
- **Always center the data first**: subtract the mean $\bar{x} = \frac{1}{n}\sum_i x_i$ from every point

Why center? PCA finds directions of maximum variance. Variance is measured relative to the mean. If you don't center, the first principal component often just points toward the mean of the data, capturing "where the data is" rather than "how the data varies."

### The Optimization Problem
Find a unit vector $\mathbf{u}_1 \in \mathbb{R}^d$ (the first principal component direction) such that the **variance of the projections** of data points onto $\mathbf{u}_1$ is maximized:

$$\mathbf{u}_1 = \arg\max_{|\mathbf{u}|=1} \frac{1}{n} \sum_{i=1}^{n} (\mathbf{u}^T x_i)^2 = \arg\max_{|\mathbf{u}|=1} \mathbf{u}^T \Sigma \mathbf{u}$$

where $\Sigma = \frac{1}{n} X^T X$ is the **covariance matrix** (assuming centered data). $u^Tx_{i}$ is just the projected distance of point $x_i$ on u. Hence we are maximising the sum of the squared projected distances of the sample points.

The second principal component $\mathbf{u}_2$ maximizes the same objective subject to being orthogonal to $\mathbf{u}_1$: $\mathbf{u}_2 \perp \mathbf{u}_1$.
And so on for $\mathbf{u}_3, \ldots, \mathbf{u}_d$ where each u is orthogonal to all the previous i-th u vectors

### The Solution
By the Lagrangian method, the maximum of $\mathbf{u}^T \Sigma \mathbf{u}$ subject to $|\mathbf{u}|=1$ is achieved when $\mathbf{u}$ is an **eigenvector** of $\Sigma$, and the maximum value equals the corresponding **eigenvalue** $\lambda$.
So:
$$\Sigma \mathbf{u}_j = \lambda_j \mathbf{u}_j$$
The principal components are the **eigenvectors of the covariance matrix**, ordered by decreasing eigenvalue:
$$\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d \geq 0$$
And eigenvalue $\lambda_j$ equals the **variance explained** by the $j$-th principal component — the variance of the projections onto $\mathbf{u}_j$.

This is the core result:
> **PCA = eigendecomposition of the covariance matrix.**

---
## 4. The Algorithm Step by Step

**Input**: Data matrix $X \in \mathbb{R}^{n \times d}$, target dimension $k < d$

**Step 1: Center the data**

$$X \leftarrow X - \bar{x}$$

Subtract the mean of each feature across all samples.

**Step 2: Compute the covariance matrix**

$$\Sigma = \frac{1}{n-1} X^T X \in \mathbb{R}^{d \times d}$$

(Using $n-1$ for unbiased estimate of population covariance — in practice the difference is negligible for large $n$.)

**Step 3: Eigendecomposition**

$$\Sigma = U \Lambda U^T$$

where $U = [\mathbf{u}_1 | \mathbf{u}_2 | \cdots | \mathbf{u}_d]$ is the matrix of eigenvectors (columns) and $\Lambda = \text{diag}(\lambda_1, \ldots, \lambda_d)$ with $\lambda_1 \geq \lambda_2 \geq \cdots$.

**Step 4: Project**

Take the top $k$ eigenvectors $U_k = [\mathbf{u}_1 | \cdots | \mathbf{u}_k] \in \mathbb{R}^{d \times k}$.

Project data onto them: $$Z = X U_k \in \mathbb{R}^{n \times k}$$

$Z$ is the **low-dimensional representation** — the principal component scores. Each row of $Z$ is a point in the $k$-dimensional PC space.

**Step 5 (Optional): Reconstruct**
To go back to the original space (approximately): $$\hat{X} = Z U_k^T = X U_k U_k^T$$

*$\hat{X}$ is the best rank-$k$ approximation to $X$ in terms of Frobenius norm — the Eckart-Young theorem.*

---
## 5. The SVD Connection: How PCA is Actually Computed

Computing the covariance matrix $\Sigma = X^T X / (n-1)$ and then doing eigendecomposition is mathematically equivalent to doing SVD on $X$ directly — but the SVD approach is **numerically superior** and is what every practical implementation uses.
### Singular Value Decomposition
$$X = U \Sigma V^T$$

where:
- $U \in \mathbb{R}^{n \times n}$: left singular vectors (orthonormal)
- $\Sigma \in \mathbb{R}^{n \times d}$: diagonal matrix of singular values $\sigma_1 \geq \sigma_2 \geq \cdots \geq 0$
- $V \in \mathbb{R}^{d \times d}$: right singular vectors (orthonormal) — **these are the principal component directions**

The connection:
$$X^T X = (U\Sigma V^T)^T (U \Sigma V^T) = V \Sigma^T U^T U \Sigma V^T = V \Sigma^2 V^T$$
So the eigenvectors of $X^T X$ are the columns of $V$ (right singular vectors), and the eigenvalues are $\sigma_j^2$ (squared singular values).

The principal component scores: $$Z = X V = U \Sigma$$
### Why SVD and Not Eigendecomposition?
1. **Numerical stability**: Computing $X^T X$ *squares the condition number of $X$, making numerical errors worse.* SVD works directly on $X$.
2. **Efficiency**: For $n \ll d$ or $d \ll n$, truncated SVD only computes the top $k$ singular vectors without computing the full decomposition — $O(ndk)$ instead of $O(d^3)$.
3. **Memory**: You never need to store the full $d \times d$ covariance matrix.

In sklearn, `PCA` uses SVD internally. The `n_components` parameter controls $k$ — the number of singular vectors computed.

---
## 6. Explained Variance and Choosing $k$

### Explained Variance Ratio
The total variance in the data (after centering) is: $$\text{Total variance} = \sum_{j=1}^{d} \lambda_j = \text{tr}(\Sigma)$$
The proportion of variance explained by the $j$-th PC: $$\text{EVR}_j = \frac{\lambda_j}{\sum_{l=1}^{d} \lambda_l}$$
The cumulative explained variance for the top $k$ components: $$\text{Cumulative EVR}(k) = \frac{\sum_{j=1}^{k} \lambda_j}{\sum_{j=1}^{d} \lambda_j}$$
### How to Choose $k$
**The explained variance threshold**: Choose the smallest $k$ such that cumulative EVR exceeds some threshold — typically 90%, 95%, or 99% depending on how much information loss is acceptable.

```
Cumulative EVR
1.0 |                    ___________
    |              _____/
0.9 |         ____/   ← 95% threshold
    |     ___/
0.5 |  __/
    | /
    |/__________________________
              k →
```

**The scree plot**: Plot eigenvalues (or EVR) vs component index. Look for an "elbow" where the eigenvalues stop dropping sharply. Similar to the k-means elbow but usually more reliable because eigenvalues genuinely tend to drop fast then level off.

**Domain-specific targets**: For visualization, $k = 2$ or $k = 3$. For preprocessing before a downstream model, often $k$ is chosen to retain 95% variance. For noise reduction in images, even 50% might be fine.

**Nuance**: There is no universally correct answer for $k$. It depends on what you're going to do with the reduced representation. Always evaluate downstream task performance for different $k$, not just EVR.

---

## 7. What PCA Actually Does: Four Equivalent Views
PCA is deep enough that it has multiple completely equivalent interpretations. Understanding all of them is what separates surface knowledge from genuine understanding.
### View 1: Maximum Variance Projection
Find the $k$-dimensional subspace onto which the projected data has maximum variance. (The optimization problem in Section 3.)
### View 2: Minimum Reconstruction Error
Find the $k$-dimensional subspace that minimizes the average squared reconstruction error:

$$\min_{U_k} \frac{1}{n} \sum_{i=1}^n |x_i - U_k U_k^T x_i|^2$$
These two views — maximize variance of projections vs. minimize reconstruction error — give **exactly the same answer**. This is because:
$$\text{Total variance} = \text{Variance retained} + \text{Reconstruction error}$$
Maximizing retained variance is equivalent to minimizing what's thrown away.

### View 3: Best Low-Rank Matrix Approximation (Eckart-Young Theorem)

Among all rank-$k$ matrices $\hat{X}$, the one closest to $X$ in Frobenius norm is:
$$\hat{X} = X U_k U_k^T = \sum_{j=1}^{k} \sigma_j \mathbf{u}_j \mathbf{v}_j^T$$

PCA gives you the best rank-$k$ approximation to the data matrix. This is the Eckart-Young theorem. It's why PCA is the optimal linear dimensionality reduction.

### View 4: Decorrelation
The projected coordinates $Z = X U_k$ are **uncorrelated** — the covariance matrix of $Z$ is diagonal:
$$\text{Cov}(Z) = U_k^T \Sigma U_k = \Lambda_k$$

PCA rotates the coordinate system so that the new axes (PCs) are uncorrelated with each other. The first axis captures the most variance, the second captures the most of what's left, and so on.

This decorrelation view is why PCA is useful as preprocessing for algorithms that assume independent features (like Naive Bayes or methods that use diagonal covariance matrices).

---

## 8. Case Study 1: PCA on Face Images (Eigenfaces)
This is the canonical example that makes PCA's power visceral.

**Setup**: 1000 grayscale face images, each 100×100 pixels. Each image is a point in $\mathbb{R}^{10000}$.

**Apply PCA**: Compute the top 100 principal components.

**What the PCs look like**: The first few PCs, when reshaped back to 100×100 images, look like ghostly face-like templates — blurry averages capturing the dominant modes of variation. These are called **eigenfaces**. Early PCs capture overall lighting, face orientation, and broad structural variation. Later PCs capture finer details.

**Reconstruction with $k$ components**:
- $k = 1$: barely recognizable blob
- $k = 10$: recognizable as a face, blurry
- $k = 50$: recognizable as the specific person, somewhat blurry
- $k = 100$: nearly indistinguishable from original

**The punchline**: You need 100 numbers instead of 10,000 to approximately represent a face. 99% compression with recognizable quality. The other 9,900 dimensions were mostly lighting variation, noise, and redundancy that PCA identified and discarded.

This is the low-rank structure of natural images: faces don't live anywhere in $\mathbb{R}^{10000}$ — they live on a low-dimensional manifold that PCA approximately captures with a linear subspace.

---

## 9. Case Study 2: PCA on Word Embeddings
You have 300-dimensional Word2Vec embeddings for 50,000 words. Project to 2D with PCA for visualization.

In the 2D PCA plot:
- Verbs cluster separately from nouns
- Country names cluster together
- Days of the week form a recognizable group
- Antonyms are often in opposite directions from the origin

**What the principal components mean**: The first PC often captures a "frequency" or "generality" axis (common words vs. rare words). The second might capture a semantic axis (concrete vs. abstract). These emerge from the structure of co-occurrence patterns, not from any labels.

**Beyond visualization**: Reduce 300D embeddings to 50D with PCA before feeding to a downstream classifier. Often improves performance because:
1. Removes noise dimensions that confuse the classifier
2. Reduces the curse of dimensionality
3. Speeds up training

This is the standard preprocessing pipeline for embeddings used as features in classical ML models.

---
## 10. Case Study 3: PCA for Noise Reduction

**Setup**: Signal $s$ corrupted by Gaussian noise $\epsilon$: observed data $x = s + \epsilon$.

If the true signal $s$ lies in a low-dimensional subspace (e.g., a 10-dimensional subspace of $\mathbb{R}^{1000}$), then:
- The top 10 PCs capture mostly signal (high variance, structured)
- PCs 11–1000 capture mostly noise (low variance, unstructured)

Project to 10D and reconstruct: $$\hat{x} = U_{10} U_{10}^T x$$
The reconstruction discards the noise components and retains the signal. This is **PCA denoising**.

**How well does it work?** It depends on the signal-to-noise ratio and whether the signal genuinely lives in a low-dimensional subspace. For highly structured signals (audio, medical imaging, spectroscopy), it works remarkably well. For truly random high-dimensional signals, it fails.

**Connection to Wiener filter**: PCA denoising is optimal (minimizes MSE) when the signal is Gaussian and the subspace is known. In practice neither condition holds exactly, but performance is often good.

---
## 11. Case Study 4: PCA in Single-Cell RNA Sequencing
One of the most important real applications of PCA in modern science.

**Setup**: Measure expression of 20,000 genes across 10,000 individual cells. Data matrix: $10{,}000 \times 20{,}000$.

**Why PCA**: Cells of the same type (neuron, immune cell, muscle cell) express similar sets of genes — they lie near each other in a low-dimensional subspace of gene expression space. Different cell types lie in different subspaces.

**What happens**: The first 30–50 PCs capture the biologically meaningful structure. Cells cluster by type in PC space. The remaining 19,950+ PCs are mostly technical noise from measurement variability.

**Standard pipeline**: Raw counts → normalize → log transform → PCA (50 PCs) → UMAP (2D visualization) → k-means or Leiden clustering.

PCA is the critical denoising step between raw measurements and the clustering that identifies cell types. Without it, the noise in 20,000 dimensions drowns the signal in 50 biologically relevant dimensions.

This is why PCA remains central in bioinformatics despite the existence of fancier methods.

---

## 12. The Assumptions PCA Makes (And When They Break)
Understanding what PCA assumes is more important than memorizing the algorithm.
### Assumption 1: Linearity
PCA finds a **linear** subspace. *If the true structure is nonlinear (points on a sphere, a Swiss roll, a curved manifold), PCA will do a poor job.*

**Example**: Points sampled uniformly from a circle in 2D. The first two PCs span the whole plane, but the actual structure is 1D (the circle). PCA can't find the circular structure.

**Fix**: Kernel PCA (apply PCA in a high-dimensional feature space induced by a kernel), UMAP, t-SNE, autoencoders. These find nonlinear low-dimensional structure.

### Assumption 2: Variance = Signal
PCA assumes high variance = important structure. This is often true but not always.

**Counterexample**: You have two features — *one that varies a lot (age, ranging 0–80) and one that varies little but is highly discriminative for your task* (a binary disease indicator). PCA will weight age heavily and may discard the disease indicator. In a supervised setting, you might actually want to keep low-variance but highly predictive features.

**Fix**: Supervised dimensionality reduction (Linear Discriminant Analysis, supervised PCA) when you have labels and care about discriminability, not just variance.
### Assumption 3: Gaussianity (Soft)
PCA is the optimal linear encoder for Gaussian data. For non-Gaussian distributions, it may miss important structure. Independent Component Analysis (ICA) is better when you want to find statistically independent (not just uncorrelated) components — relevant for signal separation (the "cocktail party problem").

### Assumption 4: Global Structure
*PCA is a global method* — it finds the subspace that captures variance across the entire dataset. If different parts of the dataset have different local structure (e.g., multiple clusters each with their own local geometry), PCA averages over all of them.

**Fix**: Local methods *(UMAP, t-SNE) that preserve local neighborhood structure r*ather than global variance.
### Assumption 5: No Important Outliers
A single extreme outlier can dramatically pull the first PC toward it, distorting the entire decomposition. PCA is not robust to outliers.

**Fix**: Robust PCA (RPCA), which decomposes the matrix as low-rank + sparse, explicitly modeling outliers.

---

## 13. PCA vs Other Dimensionality Reduction Methods

|Method|Type|Preserves|Best For|
|---|---|---|---|
|PCA|Linear|Global variance|General preprocessing, noise reduction|
|LDA|Linear, supervised|Class separability|When you have labels and want discrimination|
|ICA|Linear|Statistical independence|Signal separation, non-Gaussian structure|
|Kernel PCA|Nonlinear|Kernel-induced geometry|Nonlinear structure, known kernel|
|t-SNE|Nonlinear|Local neighborhoods|Visualization only (not for features)|
|UMAP|Nonlinear|Local + some global|Visualization, preserves cluster structure better than t-SNE|
|Autoencoders|Nonlinear|Learned (task-dependent)|When you have enough data and want learned features|

### When to Definitely Use PCA
- Preprocessing before a classical ML model when $d$ is large
- Denoising when signal is approximately low-rank
- Visualization as a quick first look (2D/3D PCA plot)
- When you need fast, interpretable, deterministic dimensionality reduction
- When data has approximately linear low-dimensional structure

### When to Not Use PCA
- You have labels and care about discriminability → LDA
- Structure is manifold-shaped (curved) → UMAP or kernel PCA
- You're visualizing cluster structure in high-dimensional embeddings → UMAP or t-SNE (but use PCA first to reduce to ~50D, then UMAP to 2D)
- You have extreme outliers → Robust PCA
- You have very few samples relative to dimensions ($n \ll d$) → be careful (see Section 14)

---
## 14. Important Nuances and Failure Modes

### The $n < d$ Problem

When you have fewer samples than features ($n < d$), the covariance matrix $\Sigma \in \mathbb{R}^{d \times d}$ has rank at most $n-1$. There are at most $n-1$ nonzero eigenvalues — the rest are exactly zero (or numerically near-zero).

This is fine — just means you can only get $\min(n-1, d)$ meaningful PCs. But it also means the empirical covariance matrix is a poor estimate of the true population covariance. With $n = 50$ samples and $d = 10{,}000$ features, the top PC of the empirical covariance matrix is largely a sampling artifact.

**Fix**: Regularized covariance estimation (Ledoit-Wolf shrinkage), or use randomized SVD on $X$ directly and keep only PCs with eigenvalues well above the bulk.

### Feature Scaling is Usually Required

PCA is not scale-invariant. If features have very different scales (one ranges 0–1, another ranges 0–1000), the high-scale feature will dominate all variance and the first PC will essentially be that feature alone.

Standard practice: **standardize each feature** to zero mean and unit variance before PCA. This ensures PCA treats all features equally.

**When not to standardize**: If you have domain-specific reasons to believe one feature should dominate. Or if all features are already on the same scale (e.g., pixels in an image).

This is different from mean-centering (which is always required) — standardization divides by the standard deviation as well.

### PCA is Sensitive to the Sign of Eigenvectors

Eigenvectors are only defined up to sign — $-\mathbf{u}$ is just as valid an eigenvector as $\mathbf{u}$. Different implementations may flip signs. When comparing PCA outputs across runs or implementations, project data onto eigenvectors and check that the sign of the projections is consistent.

sklearn handles this with `svd_flip` — it deterministically flips signs so the largest absolute value in each eigenvector is positive.

### Incremental/Online PCA

When the dataset doesn't fit in memory, you can't compute $X^T X$ in one pass. **Incremental PCA** processes data in chunks, updating the decomposition incrementally. sklearn has `IncrementalPCA` for this.

**Randomized SVD**: When $k \ll d$ and $n$ is very large, randomized SVD (Halko et al., 2011) computes approximate top-$k$ singular vectors in $O(ndk)$ time instead of $O(nd^2)$ or $O(d^3)$ — often 5–10× faster with negligible accuracy loss. This is what sklearn's `PCA(svd_solver='randomized')` uses for large data.

### Kernel PCA

When data lies on a nonlinear manifold, you can apply PCA in a high-dimensional feature space defined by a kernel function $k(x_i, x_j) = \phi(x_i)^T \phi(x_j)$:

1. Compute the kernel matrix $K \in \mathbb{R}^{n \times n}$ where $K_{ij} = k(x_i, x_j)$
2. Center $K$ (kernel centering, analogous to mean-centering)
3. Eigendecompose $K$

Common kernels: RBF ($k(x,z) = \exp(-|x-z|^2/2\sigma^2)$), polynomial. RBF kernel PCA can "unroll" the Swiss roll manifold that linear PCA cannot.

**Cost**: $O(n^2)$ to compute $K$, $O(n^3)$ to eigendecompose — expensive for large $n$. Approximate kernel PCA using Nyström approximation exists for large datasets.

---

## 15. PCA in Deep Learning

PCA appears throughout deep learning — sometimes explicitly, more often implicitly.

### Whitening as Preprocessing

Before training a neural network on images, **ZCA whitening** (a variant of PCA) is sometimes applied:

$$\tilde{x} = \Sigma^{-1/2} (x - \bar{x})$$

This decorrelates input features and normalizes their variance. The result: training is faster, features have comparable scale, and optimization landscapes are better conditioned. Less common now that Batch Normalization handles this implicitly.

### Analyzing Learned Representations

After training a neural network, you can apply PCA to the activations of a hidden layer. This reveals:

- How many effective dimensions the representation uses (fast eigenvalue decay = low intrinsic dimensionality)
- Whether the network has learned a disentangled representation (PCs correspond to interpretable factors)
- How representations evolve across layers (the eigenvalue spectrum changes dramatically from early to late layers)

This is a standard tool in representation learning research and directly relevant to your work on dataset pruning and representation structure.

### PCA Initialization for Embeddings

Instead of random initialization of embedding matrices, initialize with PCA of a co-occurrence matrix. Historically this was the LSA approach. Less common now since random init + SGD works well, but PCA init can speed up convergence.

### Low-Rank Weight Matrices

Large weight matrices $W \in \mathbb{R}^{m \times n}$ can be approximated as $W \approx AB$ where $A \in \mathbb{R}^{m \times k}$ and $B \in \mathbb{R}^{k \times n}$, $k \ll \min(m,n)$. This is low-rank approximation via SVD — the same operation as PCA. Used in LoRA (Low-Rank Adaptation) for efficient fine-tuning of LLMs: instead of updating full weight matrices, learn low-rank updates $\Delta W = AB$.

### Dimensionality Reduction Before Clustering (The Standard Pipeline)

As mentioned in the k-means note: high-dimensional embeddings → PCA (50D) → UMAP (2D) → k-means or visualization. PCA is the denoising step. Without it, UMAP and k-means struggle with the noisy high-dimensional space.

---

## 16. PCA and Information Theory

PCA has an elegant information-theoretic interpretation when data is Gaussian.

For Gaussian data $x \sim \mathcal{N}(\mu, \Sigma)$, encoding into $k$ dimensions using a linear encoder $z = U_k^T x$ and then decoding $\hat{x} = U_k z$, the mutual information between $z$ and $x$ is:

$$I(z; x) = \frac{1}{2} \sum_{j=1}^{k} \log(1 + \lambda_j / \sigma^2_{\text{noise}})$$

For a fixed $k$, this is maximized by the PCA projection (choosing the top $k$ eigenvectors). PCA is the optimal linear encoder under the Gaussian assumption in the information-theoretic sense — it maximizes the mutual information between the compressed and original representations.

This connects PCA to rate-distortion theory and to autoencoders: a linear autoencoder with MSE loss and a bottleneck of size $k$ learns exactly the PCA subspace (the top $k$ PCs) as its encoding.

**The linear autoencoder ↔ PCA equivalence**: Train a neural network with architecture $d \to k \to d$ (linear layers only, MSE loss, no nonlinearities). The weight matrices of the optimal solution span the same subspace as the top $k$ PCs. Not the same matrices (not the same rotation within the subspace), but the same subspace. Add nonlinearities → nonlinear autoencoder, which can find curved manifolds that PCA cannot.

---

## 17. Implementation

```python
from sklearn.decomposition import PCA, IncrementalPCA, KernelPCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# Step 1: Always standardize (usually)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)   # zero mean, unit variance per feature

# Step 2: Fit PCA
pca = PCA(n_components=50)           # keep top 50 PCs
# pca = PCA(n_components=0.95)       # keep enough PCs to explain 95% variance
# pca = PCA(svd_solver='randomized') # faster for large data and small k
pca.fit(X_scaled)

# Explained variance
print(pca.explained_variance_ratio_)         # EVR per component
print(pca.explained_variance_ratio_.cumsum()) # cumulative EVR

# Transform
Z = pca.transform(X_scaled)         # shape: (n_samples, 50)

# Reconstruct (for denoising or visualization)
X_reconstructed = pca.inverse_transform(Z)
X_reconstructed = scaler.inverse_transform(X_reconstructed)  # undo scaling

# For large datasets that don't fit in memory
ipca = IncrementalPCA(n_components=50, batch_size=500)
for batch in batches:
    ipca.partial_fit(scaler.transform(batch))
Z = ipca.transform(X_scaled)

# Kernel PCA for nonlinear structure
kpca = KernelPCA(n_components=10, kernel='rbf', gamma=0.1)
Z_kpca = kpca.fit_transform(X_scaled)

# Quick 2D visualization
pca_2d = PCA(n_components=2)
Z_2d = pca_2d.fit_transform(X_scaled)
# plt.scatter(Z_2d[:, 0], Z_2d[:, 1], c=labels)
```

### Choosing `svd_solver`

|Solver|When|Speed|
|---|---|---|
|`'auto'`|Default, picks best|—|
|`'full'`|Small data, need exact solution|Slow for large $d$|
|`'randomized'`|Large data, small $k$|Fast|
|`'arpack'`|Sparse data|Efficient for sparse|

For most practical use: `svd_solver='randomized'` with explicit `n_components` is the right default for large datasets.

---

## 18. Key Takeaways

- PCA finds the linear subspace of dimension $k$ that **maximizes the variance** of projected data — equivalently, **minimizes reconstruction error**. These are the same problem.
- The solution is the **eigendecomposition of the covariance matrix**: principal components are eigenvectors, eigenvalues are the variance explained.
- In practice, PCA is computed via **SVD on the data matrix** — numerically more stable and often faster than eigendecomposing $X^T X$.
- **Always center the data** before PCA (subtract the mean). Usually standardize too (divide by std per feature) unless features are naturally on the same scale.
- The $j$-th eigenvalue $\lambda_j$ equals the variance explained by the $j$-th PC. Cumulative explained variance ratio guides the choice of $k$.
- PCA has four equivalent views: maximum variance projection, minimum reconstruction error, best low-rank matrix approximation (Eckart-Young), and decorrelation of features.
- PCA assumes **linearity**, **variance = signal**, and is **sensitive to scale and outliers**. When these fail: kernel PCA, UMAP, robust PCA, LDA.
- A **linear autoencoder** (no nonlinearities, MSE loss, bottleneck of size $k$) learns exactly the PCA subspace — this is the bridge to deep representation learning.
- The standard high-dimensional pipeline: raw data → standardize → PCA (~50D) → UMAP (2D for visualization) or downstream model.
- PCA appears throughout deep learning: ZCA whitening, representation analysis, LoRA (low-rank weight updates), and as the baseline against which learned representations are compared.