---
title: "t-SNE (t-Distributed Stochastic Neighbor Embedding)"
lastmod: 2026-06-27
---

## 1. The Problem PCA Doesn't Solve
We know PCA finds the best **linear** subspace — the projection that maximizes variance. It's optimal for linear structure.

But consider this: you have 10,000 cells from 20 different cell types. In 50-dimensional PCA space, cells of the same type cluster together, but the clusters are squished, overlapping, and hard to distinguish visually. You reduce to 2D with PCA — now it's worse. The two PCs that capture the most global variance spread out the data, but cluster boundaries blur into each other.

Why? Because **PCA preserves global structure** (overall variance, large-scale distances) and 2D can only hold so much. When you need to visualize 20 tight clusters simultaneously, global structure is not what matters. What matters is that:
- **Points in the same cluster stay close together**
- **Different clusters stay far apart**

This is a fundamentally different objective than maximizing variance. You don't care where the clusters are in absolute terms — you care that similar things are near each other and dissimilar things are far away. This is **local structure preservation**.

t-SNE (van der Maaten & Hinton, 2008) was designed specifically for this. It is a **nonlinear** dimensionality reduction method built for **visualization** of high-dimensional data, and it is extraordinarily good at that specific task.

The central idea:
> **Model pairwise similarities in high-dimensional space as a probability distribution, model pairwise similarities in low-dimensional space as another probability distribution, and minimize the KL divergence between them.**

---
## 2. The Predecessor: SNE
To understand t-SNE, first understand its predecessor, **SNE** (Stochastic Neighbor Embedding, Hinton & Roweis, 2002), and then see exactly what t-SNE changes and why.
### SNE: The Core Idea
In high-dimensional space, define the **similarity** between point $x_j$ and point $x_i$ as the probability that $x_i$ would pick $x_j$ as its neighbor under a Gaussian centered at $x_i$:

$$p_{j|i} = \frac{\exp\left(-|x_i - x_j|^2 / 2\sigma_i^2\right)}{\sum_{k \neq i} \exp\left(-|x_i - x_k|^2 / 2\sigma_i^2\right)}$$
Note: $p_{i|i} = 0$ by convention. The bandwidth $\sigma_i$ is point-specific (explained in Section 4 — perplexity).

These are **conditional probabilities** — they are not symmetric: $p_{j|i} \neq p_{i|j}$.
In low-dimensional space (say 2D), define the analogous similarity between map points $y_j$ and $y_i$:

$$q_{j|i} = \frac{\exp\left(-|y_i - y_j|^2\right)}{\sum_{k \neq i} \exp\left(-|y_i - y_k|^2\right)}$$
The fixed bandwidth $\frac{1}{\sqrt{2}}$ in the low-dimensional space is arbitrary — the optimization will find positions $y_i$ that work.

**Objective**: Minimize the sum of KL divergences between $P_i$ and $Q_i$ for each point $i$:
$$L = \sum_i \text{KL}(P_i | Q_i) = \sum_i \sum_j p_{j|i} \log \frac{p_{j|i}}{q_{j|i}}$$
Gradient descent on the $y_i$ positions (start random, iterate until convergence).

### The Problem with SNE
**The crowding problem**: In a Gaussian distribution, the volume of space at distance $r$ from a point grows as $r^{d-1}$. In high dimensions, most volume is concentrated at intermediate distances. The "bulk" of the mass sits at moderate distances. 
When you try to map this to 2D, there's a fundamental mismatch: 2D doesn't have enough space to accommodate all the moderately-distant points from the high-dimensional space. They all need to be somewhere in 2D, but they can't all be at moderate distance without crowding each other. Hence, clusters collapse. Points that should be at moderate distances end up forced into the same region because 2D doesn't have room. The visualization becomes a blob.

**The asymmetry problem**: SNE's conditional probabilities $p_{j|i}$ are asymmetric. This complicates gradient computation and causes optimization instability.
t-SNE fixes both problems with two key changes.

---
## 3. t-SNE: The Two Key Changes
### Change 1: Symmetrized Similarities in High-D
Replace the asymmetric conditional probabilities with **joint probabilities**:

$$p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}$$

Now $p_{ij} = p_{ji}$ — the similarity between $i$ and $j$ is symmetric. This ensures $\sum_{i,j} p_{ij} = 1$ (a proper joint distribution).

**Why this helps**: Outlier points with very small $p_{j|i}$ (they're far from everyone) get pulled toward the map by the $p_{i|j}$ term. Symmetry prevents outliers from being ignored by the optimization.

### Change 2: Student-t Distribution in Low-D

This is the crucial fix for the crowding problem.

In the low-dimensional map, replace the Gaussian similarity with a **Student-t distribution with 1 degree of freedom** (a Cauchy distribution):

$$q_{ij} = \frac{(1 + |y_i - y_j|^2)^{-1}}{\sum_{k \neq l}(1 + |y_k - y_l|^2)^{-1}}$$

The t-distribution has **heavy tails** — it assigns much more probability to large distances than a Gaussian does.

### Why Heavy Tails Fix the Crowding Problem
Compare the tails of Gaussian vs. Student-t:
- Gaussian: $\exp(-r^2)$ — falls off rapidly
- Student-t (df=1): $(1 + r^2)^{-1}$ — falls off slowly (polynomially)

The heavy tails mean: for two points to have a **small** $q_{ij}$ (meaning "dissimilar" in the map), they need to be placed **much farther apart** in 2D than a Gaussian would require.

Put differently: the t-distribution allows moderate high-dimensional distances to map to **large** low-dimensional distances. This "stretches" space in the low-D map, creating room for clusters to spread out and be visually separated.

The effect is dramatic. *Clusters that collapse into a blob under SNE become well-separated under t-SNE.* This is the defining visual characteristic of t-SNE plots — tight, well-separated clusters that seem too clean to be true.

---
## 4. The Full t-SNE Algorithm

### Step 1: Compute High-Dimensional Similarities
For each pair $(i, j)$, compute:
$$p_{j|i} = \frac{\exp\left(-|x_i - x_j|^2 / 2\sigma_i^2\right)}{\sum_{k \neq i} \exp\left(-|x_i - x_k|^2 / 2\sigma_i^2\right)}$$
Then symmetrize:
$$p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}$$

This gives you an $n \times n$ matrix of pairwise similarities. **Computed once** and fixed throughout optimization.

### Step 2: Choose $\sigma_i$ via Perplexity
The bandwidth $\sigma_i$ is different for each point — it is set so that the **perplexity** of the conditional distribution $P_i$ equals a user-specified value:

$$\text{Perplexity}(P_i) = 2^{H(P_i)}$$

where $H(P_i) = -\sum_j p_{j|i} \log_2 p_{j|i}$ is the Shannon entropy of $P_i$.

>Perplexity can be thought of as a **smooth measure of the effective number of neighbors** of point $i$.

- Low perplexity (e.g., 5): each point considers only ~5 neighbors — very local view
- High perplexity (e.g., 50): each point considers ~50 neighbors — more global view

$\sigma_i$ is found by binary search: for each $i$, find the $\sigma_i$ such that $\text{Perplexity}(P_i)$ equals the target perplexity. Dense regions of data get smaller $\sigma_i$ (tight Gaussians), sparse regions get larger $\sigma_i$ (wide Gaussians). This **adaptive bandwidth** ensures that the probability distributions are meaningful regardless of local density.

### Step 3: Initialize Low-Dimensional Map
Initialize $y_1, \ldots, y_n \in \mathbb{R}^2$ (or $\mathbb{R}^3$) from a Gaussian: $y_i \sim \mathcal{N}(0, 10^{-4} I)$. Small initial values keep points close together at the start.

**Better initialization**: Use the first 2 PCs of the data. This gives t-SNE a better starting point and often produces more consistent layouts. sklearn supports this with `init='pca'`.
### Step 4: Compute Low-Dimensional Similarities

$$q_{ij} = \frac{(1 + |y_i - y_j|^2)^{-1}}{\sum_{k \neq l}(1 + |y_k - y_l|^2)^{-1}}$$

This is recomputed at every gradient step as the $y_i$ positions change.

### Step 5: Minimize KL Divergence

$$L = \text{KL}(P | Q) = \sum_{i \neq j} p_{ij} \log \frac{p_{ij}}{q_{ij}}$$

Take gradient with respect to map point $y_i$:

$$\frac{\partial L}{\partial y_i} = 4 \sum_j (p_{ij} - q_{ij})(y_i - y_j)(1 + |y_i - y_j|^2)^{-1}$$

The gradient has a beautiful physical interpretation: it looks like a force system. Each pair of points $(i, j)$ exerts a **force** on $y_i$ along the direction $(y_i - y_j)$:

- If $p_{ij} > q_{ij}$: they're closer in the original than the projection → **attractive force** needed to pull them together
- If $p_{ij} < q_{ij}$: they're farther in the original → **repulsive force** needed to push them apart
t-SNE optimization is literally simulating a system of springs: nearby points (high $p_{ij}$) attract, far points (low $p_{ij}$, high $q_{ij}$) repel.

Update positions using gradient descent:
$$y_i^{(t)} = y_i^{(t-1)} - \eta \frac{\partial L}{\partial y_i} + \alpha (y_i^{(t-1)} - y_i^{(t-2)})$$
where $\eta$ is the learning rate and $\alpha$ is the momentum coefficient.

### Step 6: Tricks for Stable Optimization
**Early exaggeration**: In the first ~250 iterations, multiply all $p_{ij}$ by a factor (typically 12). This makes the attractive forces much stronger, forcing natural clusters to form tightly. Once clusters are formed (after exaggeration ends), the map is refined.

**Adaptive learning rate**: Adjust $\eta$ per parameter (similar to Adam) to handle different scales of movement.

---
## 5. The Gradient: Intuition as a Force System

The gradient formula deserves more attention:

$$\frac{\partial L}{\partial y_i} = 4 \sum_j \underbrace{(p_{ij} - q_{ij})}_{\text{error}} \underbrace{(y_i - y_j)}_{\text{direction}} \underbrace{(1 + |y_i - y_j|^2)^{-1}}_{\text{attenuation}}$$
Three parts:
1. **$(p_{ij} - q_{ij})$**: The signed error. Positive = points are too far apart in map (need to attract). Negative = points are too close in map (need to repel).
2. **$(y_i - y_j)$**: Direction of the force — along the line connecting the two map points.
3. **$(1 + |y_i - y_j|^2)^{-1}$**: Attenuation from the t-distribution. For points **far** in the map, the t-distribution already assigns low $q_{ij}$, so the repulsive force between them is attenuated. This is crucial: it means t-SNE doesn't try to push all non-neighbors infinitely far apart — only close-enough non-neighbors.

This force attenuation is what prevents the map from collapsing. Without it, repulsive forces would dominate and push everything apart.

---

## 6. The KL Divergence is Asymmetric — And That's Intentional
$$\text{KL}(P | Q) = \sum_{i,j} p_{ij} \log \frac{p_{ij}}{q_{ij}}$$

KL divergence is not symmetric. $\text{KL}(P|Q) \neq \text{KL}(Q|P)$. This asymmetry has a specific consequence for t-SNE:
- The cost is **large** when $p_{ij}$ is large and $q_{ij}$ is small — meaning nearby high-D points are far apart in the map. The optimization strongly penalizes this.
- The cost is **small** when $p_{ij}$ is small and $q_{ij}$ is large — meaning distant high-D points are close in the map. The optimization barely penalizes this.

**Translation**: t-SNE is obsessively focused on getting **neighbors right**. If two points are nearby in high-D space, they must be nearby in the map. But if two points are far apart in high-D space, t-SNE doesn't care much whether they're somewhat close or very far in the map.

This is why t-SNE produces tight local clusters: the cost function is designed to not let neighborhood relationships be violated. But it also explains why **global structure is not preserved** — inter-cluster distances in a t-SNE plot are essentially meaningless.

---

## 7. What t-SNE Preserves and What It Doesn't
This is the most practically important section. Misreading t-SNE plots is extremely common, and the misreadings are consequential.
- **Local Neighbour Structure:** Points that are close in high-D space will be close in the t-SNE map. Clusters that exist in the high-D space will appear as clusters in the map. Membership in a cluster is meaningful.

### What t-SNE Does NOT Preserve
- **Inter-cluster distances are meaningless.** The distance between two clusters in a t-SNE plot tells you nothing about how similar those clusters are in the original space. Two clusters that are 10cm apart in the plot might be just as similar as two clusters 1cm apart — or they might be completely unrelated. You cannot compare cluster similarity from their visual proximity.
- **Cluster sizes are meaningless.** The area occupied by a cluster in a t-SNE plot has no relationship to the density or size of that cluster in the original space. A small, dense cluster in high-D and a large, diffuse cluster in high-D can appear the same size in the t-SNE plot.
- **Global structure is not preserved.** Unlike PCA, t-SNE doesn't tell you about the overall "shape" of the data — whether it's elongated, what the dominant axes of variation are, etc.

### The Distortion is Systematic, Not Random
These are not random distortions — they're **systematic** consequences of the objective function. t-SNE is specifically designed to prioritize local structure at the expense of global structure. Once you understand this, you can read t-SNE plots correctly: only trust local cluster membership, nothing else.

---

## 8. Case Study 1: MNIST Digits
The canonical t-SNE demonstration.
**Setup**: 70,000 MNIST images (28×28 = 784 dimensions). Reduce to 2D.

**Result**: 10 tight, well-separated clouds, each corresponding to one digit class. Within each cloud, you can see sub-clusters corresponding to different handwriting styles (different ways people write "7", for example).

**What this tells you** (correctly):
- The 10 digit classes are well-separated in pixel space
- There is sub-structure within each class

**What this does NOT tell you**:
- Whether "4" is more similar to "9" than to "1" (you can't read this from proximity of clusters)
- Whether the cluster for "1" is more compact than the cluster for "8" (cluster size is meaningless)

The MNIST t-SNE plot is beautiful and informative about local structure. It is not informative about global structure.

---

## 9. Case Study 2: Single-Cell RNA-seq
t-SNE became the dominant visualization tool in single-cell genomics.

**Setup**: 10,000 cells × 20,000 genes → PCA (50 PCs) → t-SNE (2D).

**Why PCA first?**: Computing pairwise distances in 20,000 dimensions is expensive and noisy. PCA reduces to 50 meaningful dimensions, denoises, and makes t-SNE tractable. This is the **standard pipeline**: high-dimensional data → PCA (50D) → t-SNE (2D).

**What the t-SNE plot shows**: Cells of the same type form tight islands. Rare cell populations (e.g., a cell type comprising 0.1% of cells) appear as a distinct small island separate from the main masses.

**A key misreading that happens in papers**: Authors see that a disease condition and a healthy condition produce cells that "look close" in the t-SNE plot and conclude the transcriptomes are similar. This is wrong — inter-cluster distance is not preserved. The correct analysis is to compare the cells statistically in the high-dimensional PCA space, not to eyeball t-SNE proximity.

**The reproducibility problem**: Two t-SNE runs on the same data with different random seeds produce different-looking plots (different rotations, reflections, sometimes different topology). The cluster membership is stable, but the layout is not. Always set a random seed and never report visual layout as a finding.

---

## 10. Case Study 3: Word Embeddings
Take 50,000 Word2Vec embeddings (300D) → PCA (50D) → t-SNE (2D).
**What you see**:
- Sports-related words cluster together
- Country names form a cluster
- Days of the week, months of the year form small tight groups
- Programming languages cluster separately from natural languages

**What's useful**: Finding unexpected semantic groupings, discovering that certain words have ambiguous/mixed context (they might sit between clusters), quality-checking embeddings.

**What's not useful**: Saying "sports words and programming words are far apart so they're semantically different" — the inter-cluster distance is not meaningful.

---

## 11. Perplexity: The Key Hyperparameter

Perplexity is the only critical hyperparameter of t-SNE, and it's the most misunderstood one.

### What Perplexity Controls
Perplexity ≈ the effective number of neighbors each point considers. It sets the balance between local and global structure:
- **Low perplexity (5–10)**: Very local. Each point only pays attention to its 5–10 nearest neighbors. The result: many small, tight clusters. Sub-clusters within true clusters become apparent. But noise can fracture true clusters into many small islands.
- **High perplexity (50–100)**: More global. Each point considers 50–100 neighbors. The result: fewer, larger clusters. Sub-structure within clusters is smoothed out.
- **Too low (< 5)**: Each point's Gaussian only covers a handful of points. The high-D similarities become very spiky — some $p_{ij}$ are huge, most are tiny. The resulting map has many isolated points and tiny fragmented clusters.
- **Too high (> $n/3$)**: All points start looking similar to each other. The map loses structure entirely.
### Typical Range
5–50 for most datasets. The original paper suggests 5–50 with 30 as a default. sklearn defaults to 30.
### The Critical Insight: You Must Try Multiple Perplexities
A single perplexity value might miss important structure or create false structure. **Always run t-SNE at multiple perplexities** (e.g., 5, 30, 100) and check whether the structure you see is consistent across them. If a cluster appears only at one perplexity, treat it with suspicion.

This is a known problem in the literature: Wattenberg, Viégas & Johnson (2016) in their excellent distill.pub article "How to Use t-SNE Effectively" showed that:
- Random noise can produce structured-looking clusters in t-SNE plots
- Cluster sizes and inter-cluster distances are not interpretable
- You need many perplexity values to understand the data

---

## 12. Computational Complexity: The Scalability Problem
### Naive t-SNE
Computing all pairwise similarities: $O(n^2)$ time and space. For $n = 100{,}000$ points, this is 10 billion pairs — infeasible.
### Barnes-Hut t-SNE (van der Maaten, 2014)
The key observation: when computing gradients, the repulsive forces from distant points can be approximated by treating them as a single "super-point" at their center of mass. This is the Barnes-Hut approximation from computational physics (originally for N-body gravity simulations).

**Quadtree/Octree**: Partition space into cells. For gradient computation at point $y_i$, if a cell is sufficiently far away (determined by a threshold $\theta$), treat all points in the cell as a single point with combined weight.

Complexity: $O(n \log n)$ per iteration for both similarity computation and gradient.

This makes t-SNE feasible for up to ~1 million points with sufficient time.

### FIt-SNE (Fourier-interpolated t-SNE, 2019)
Uses interpolation on a grid to approximate the repulsive forces even faster: $O(n)$ per iteration. Makes t-SNE practical for millions of points.

### UMAP vs t-SNE for Scale
For $n > 100{,}000$: UMAP is almost always preferred over t-SNE for practical reasons:

- *UMAP is $O(n)$ vs t-SNE's $O(n \log n)$*
- UMAP is typically 5–10× faster
- UMAP can be used for generating features (it has an `transform()` method for new data); t-SNE cannot
- *UMAP often produces comparably good or better visualizations*

---

## 13. t-SNE Cannot Be Used for New Data Points
t-SNE optimizes positions for a fixed set of points. If you train t-SNE on a training set and then want to project a new test point, **you cannot do it** without re-running the entire optimization including the new point.

There is no `transform()` equivalent for standard t-SNE (unlike PCA or UMAP). *Every time you want to visualize a different set of points, you run the full algorithm again.*

**Workarounds**:
- **Parametric t-SNE**: Train a neural network to learn the t-SNE mapping. Given a new point, pass it through the network. Approximate but fast.
- **UMAP**: Has a proper `transform()` method. For new data projection, UMAP is strictly better.
- **Rerun**: For offline analysis where you always have the full dataset, just rerun.

This is one of the primary reasons UMAP has displaced t-SNE in many workflows — UMAP is a "proper" dimensionality reduction that can be fit on training data and applied to new data.

---
## 14. t-SNE vs PCA vs UMAP

Understanding when to use each requires understanding what each preserves:

|Property|PCA|t-SNE|UMAP|
|---|---|---|---|
|Preserves global structure|Yes|No|Partially|
|Preserves local structure|Partially|Yes|Yes|
|Can project new points|Yes|No (standard)|Yes|
|Deterministic|Yes|No (random init)|No (random init)|
|Speed|Fast|Slow ($O(n \log n)$)|Faster ($O(n)$)|
|Interpretable axes|Yes (variance explained)|No|No|
|Good for features|Yes|No|Sometimes|
|Good for visualization|Okay|Excellent|Excellent|
|Cluster sizes meaningful|Yes (relative)|No|Partially|
|Inter-cluster distances meaningful|Yes|No|Partially|
|Handles nonlinear structure|No|Yes|Yes|

### The Standard Pipeline
For high-dimensional data visualization:
1. **PCA to ~50D**: Denoising, speed-up, remove linearly redundant dimensions
2. **t-SNE or UMAP to 2D**: Nonlinear layout for visualization

Never run t-SNE directly on 10,000-dimensional data — both for computational reasons and because the pairwise distances in very high dimensions are dominated by noise (distance concentration from the k-means note).

### When to Use t-SNE Over UMAP
- You need the best possible local cluster separation for publication-quality figures
- You have a dataset where t-SNE is known to work well (e.g., biological cell atlases)
- You don't need to project new points

### When UMAP is Better
- You need to project new data points
- Speed matters ($n > 50{,}000$)
- You want to preserve more global structure
- You want to use the embedding as features for a downstream model

---
## 15. Common Misinterpretations and How to Avoid Them

### Misinterpretation 1: "These two clusters are close, so they're similar"
**Wrong.** Inter-cluster distance in t-SNE is not meaningful. Two clusters can appear adjacent simply because t-SNE couldn't find a better layout, not because they're actually similar in the original space.
**Fix**: Compare clusters statistically in the original (or PCA-reduced) space. t-SNE is for finding that clusters exist, not for measuring their similarity.

### Misinterpretation 2: "This cluster is bigger, so it's more common/more varied"
**Wrong.** Cluster area in t-SNE depends on the local density relative to other clusters and on perplexity, not on actual cluster size or variance.

**Fix**: Count actual members of each cluster. Measure within-cluster variance in original space.

### Misinterpretation 3: "I see 7 clusters so there are 7 subtypes"
**Wrong.** The number of visible clusters in t-SNE depends heavily on perplexity. At low perplexity, one true cluster can appear as many small islands. At high perplexity, several true clusters can merge.
**Fix**: Validate cluster structure with multiple perplexities and with quantitative methods (silhouette score, statistical testing) in the original space.

### Misinterpretation 4: "t-SNE showed this structure, it must be real"
**Wrong.** *t-SNE can produce structured-looking plots* from **random noise**. Wattenberg et al. demonstrated this empirically — Gaussian noise produces visually convincing cluster structures in t-SNE.
**Fix**: Always sanity-check with ground truth labels if available. Run multiple perplexities. Compare to PCA to see if the structure is present at all.

### Misinterpretation 5: "Different runs give different plots, so the method is unreliable"
**Partially wrong.** The layout (positions, orientations, which clusters are adjacent) changes between runs. But cluster **membership** is usually stable. The clusters that exist are reliable; their visual positions relative to each other are not.
**Fix**: Set `random_state` for reproducibility. Use consistent seeds across papers. Report cluster memberships quantitatively, not by eyeballing positions.

---

## 16. Why t-SNE Uses df=1 (Cauchy) Specifically
The Student-t distribution with 1 degree of freedom is the **Cauchy distribution**:

$$f(x) = \frac{1}{\pi(1 + x^2)}$$

Why df=1 specifically and not df=2 or df=5?

Van der Maaten experimented with different degrees of freedom and found that df=1 worked best empirically. But there's a theoretical argument too:

The Cauchy distribution is the heaviest-tailed Student-t that is still a proper distribution and has a closed-form density. Its tails decay as $r^{-2}$ in 2D, compared to the Gaussian's $\exp(-r^2)$.

The ratio of the high-D Gaussian similarity to the low-D Cauchy similarity at distance $r$:

$$\frac{p_{ij}}{q_{ij}} \propto \frac{\exp(-r^2/2\sigma^2)}{(1+r^2)^{-1}}$$

For moderate $r$, the Cauchy places more mass than the Gaussian — this is what allows moderate high-D distances to "expand" into large low-D distances, solving the crowding problem.

For very small $r$, both distributions give similar values — nearby points in high-D stay nearby in the map.

The degree of freedom is a hyperparameter that could in principle be tuned, but df=1 has become the standard because it works and has become the definition of t-SNE.

---

## 17. The Optimization Landscape

t-SNE's loss function is **non-convex**. There are many local minima. Different random initializations produce different solutions, some better than others.

### Why This Usually Doesn't Matter
For well-separated data, the global structure (cluster membership) is consistent across runs even though the layout differs. The optimization reliably finds the right clusters even if their positions rotate, reflect, or swap.

### When It Does Matter
For data with ambiguous or continuous structure (a manifold rather than discrete clusters), different runs can produce qualitatively different topologies. This is a genuine failure mode — the plots are inconsistent and you can't trust either of them.

### Practical Mitigation
- **PCA initialization** (`init='pca'` in sklearn): gives t-SNE a deterministic, globally-consistent starting point. The subsequent optimization typically converges to similar solutions across runs.
- **Multiple runs**: Run 5–10 times, visualize all, check for consistent cluster structure.
- **Sufficient iterations**: Make sure the optimization converges (`n_iter=1000` or more; monitor loss).

---

## 18. Implementation
```python
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# Standard pipeline: standardize → PCA → t-SNE
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 1: PCA to reduce to 50D (denoising + speed)
pca = PCA(n_components=50, random_state=42)
X_pca = pca.fit_transform(X_scaled)

# Step 2: t-SNE to 2D
tsne = TSNE(
    n_components=2,
    perplexity=30,          # effective number of neighbors; try 5, 30, 100
    n_iter=1000,            # number of optimization steps; increase if loss not converged
    learning_rate='auto',   # sklearn auto-sets based on n; or set ~200 manually
    init='pca',             # PCA init for deterministic, better results
    random_state=42,        # for reproducibility
    n_jobs=-1               # parallel nearest neighbor computation
)
Z = tsne.fit_transform(X_pca)   # shape: (n, 2)

print(f"Final KL divergence: {tsne.kl_divergence_:.4f}")
# Lower KL divergence = better fit. Use this to compare runs.

# Run at multiple perplexities to check stability
for perp in [5, 15, 30, 50, 100]:
    tsne = TSNE(n_components=2, perplexity=perp, init='pca',
                random_state=42, n_iter=1000)
    Z = tsne.fit_transform(X_pca)
    # visualize Z, check for consistent clusters

# For large datasets: use openTSNE (faster, more options)
# pip install openTSNE
from openTSNE import TSNE as openTSNE
tsne = openTSNE(
    perplexity=30,
    initialization='pca',
    n_jobs=-1,
    random_state=42
)
Z = tsne.fit(X_pca)

# openTSNE supports transforming new points (approximate)
Z_new = Z.transform(X_new_pca)
```

### Diagnosing Convergence
Always check `tsne.kl_divergence_`. If it's still decreasing at the end of training, increase `n_iter`. A typical well-converged KL divergence is < 1.0 for clean datasets; noisy or high-dimensional data may be higher.

### openTSNE vs sklearn
For serious t-SNE work, prefer **openTSNE** over sklearn:

- Supports FIt-SNE (faster for large $n$)
- Better initialization options
- Approximate transform for new points
- More control over optimization schedule
- Actively maintained

---

## 19. Key Takeaways
- t-SNE converts pairwise similarities into probability distributions and minimizes the KL divergence between high-D and low-D distributions. The two innovations over SNE: **symmetrized joint probabilities** in high-D and a **Student-t (Cauchy) distribution** in low-D.
- The heavy-tailed Cauchy distribution in low-D fixes the **crowding problem**: it allows moderate high-D distances to map to large low-D distances, creating visual separation between clusters.
- The KL divergence is asymmetric: t-SNE **strongly penalizes placing neighbors far apart** but barely penalizes placing non-neighbors close together. This is why it obsessively preserves local structure and ignores global structure.
- **Perplexity ≈ effective number of neighbors**. The only critical hyperparameter. Always try multiple values (5, 30, 100). Structure that appears only at one perplexity is suspect.
- **What to trust**: cluster membership, existence of clusters. **What not to trust**: inter-cluster distances, cluster sizes, cluster positions relative to each other.
- t-SNE **cannot project new data points** (no `transform()`). This is a fundamental limitation — use UMAP if you need to project new data.
- Standard pipeline: raw data → standardize → **PCA (~50D)** → **t-SNE (2D)**. Never run t-SNE on raw high-dimensional data.
- Use `init='pca'` and set `random_state` for reproducibility. Run multiple perplexities. Check KL divergence for convergence.
- For $n > 50{,}000$: prefer UMAP (faster, preserves more global structure, supports new data). For publication-quality cluster visualization on smaller data: t-SNE often wins.
- Random Gaussian noise **can produce structured-looking t-SNE plots**. Always validate cluster structure in the original space, not just from the t-SNE plot.