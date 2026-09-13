---
title: "K-Means Clustering"
lastmod: 2026-06-27
---

## 1. The Problem: What is Clustering?

Clustering is **unsupervised learning** — you have data points but no labels. The goal is to discover natural groupings in the data purely from the structure of the input itself.

K-means is the most widely used clustering algorithm. It answers one question:

> **Given $n$ data points and a number $k$, partition the points into $k$ groups such that points within a group are similar to each other and dissimilar from points in other groups.**

Before anything else: note that $k$ is given to you (or chosen by you). K-means does not discover the number of clusters — it takes $k$ as input and finds the best partition into exactly $k$ groups. Choosing $k$ is a separate, harder problem addressed later.

---

## 2. The Algorithm

### Setup
- $n$ data points: $x_1, x_2, \ldots, x_n$ where each $x_i \in \mathbb{R}^d$
- Number of clusters: $k$
- Goal: assign each point to one of $k$ clusters, represented by **centroids** $\mu_1, \mu_2, \ldots, \mu_k \in \mathbb{R}^d$

### The Objective Function
K-means minimizes the **within-cluster sum of squares (WCSS)**, also called **inertia**:

$$J = \sum_{j=1}^{k} \sum_{x_i \in C_j} |x_i - \mu_j|^2$$

This is the sum of squared distances from each point to its assigned cluster centroid. Lower is better — tight, compact clusters.

### The Algorithm (Lloyd's Algorithm)
**Step 1 — Initialize**: Place $k$ centroids $\mu_1, \ldots, \mu_k$ somewhere (how you do this matters enormously — see Section 4).

**Step 2 — Assignment step**: Assign each point to the nearest centroid: $$c_i = \arg\min_{j \in {1,\ldots,k}} |x_i - \mu_j|^2$$

**Step 3 — Update step**: Recompute each centroid as the mean of all points assigned to it: $$\mu_j = \frac{1}{|C_j|} \sum_{x_i \in C_j} x_i$$

**Step 4 — Repeat**: Go back to Step 2. Repeat until assignments stop changing (convergence).

### Does It Always Converge?

Yes. Each iteration either decreases $J$ or keeps it the same — it never increases. Since there are finitely many possible assignments ($k^n$ partitions), the algorithm must terminate. The number of steps is finite.

**But**: it converges to a **local minimum**, not necessarily the global minimum. This is the most important limitation of k-means and everything about how we use it in practice stems from this.

---

## 3. A Worked Example

Five points in 2D: ${(1,1), (1.5, 2), (3,4), (5,7), (3.5,5)}$, $k=2$.

**Initialize**: Randomly pick centroids $\mu_1 = (1,1)$, $\mu_2 = (5,7)$.

**Round 1 — Assignment**:

- $(1,1)$: closer to $\mu_1$ → Cluster 1
- $(1.5,2)$: closer to $\mu_1$ → Cluster 1
- $(3,4)$: distance to $\mu_1 = \sqrt{4+9}=3.6$, distance to $\mu_2=\sqrt{4+9}=3.6$ — tie, say Cluster 1
- $(5,7)$: closer to $\mu_2$ → Cluster 2
- $(3.5,5)$: closer to $\mu_2$ → Cluster 2

**Round 1 — Update**:

- $\mu_1 = \text{mean}{(1,1),(1.5,2),(3,4)} = (1.83, 2.33)$
- $\mu_2 = \text{mean}{(5,7),(3.5,5)} = (4.25, 6)$

**Round 2 — Assignment**: With new centroids, reassign all points. Some may switch clusters.

**Continue** until no point changes cluster. This usually takes very few iterations (5–20) in practice.

---

## 4. Initialization: The Single Biggest Practical Issue

K-means converges to a local minimum. A bad initialization can trap you in a terrible local minimum — clusters that are clearly wrong but stable under the assignment-update loop.

### Random Initialization

Pick $k$ data points uniformly at random as initial centroids. Simple, but can fail badly:

- Two centroids might start very close together → they "compete" for the same region, leaving another region uncovered
- If two centroids land in the same natural cluster, they'll likely stay there, giving a suboptimal partition

### K-Means++ Initialization (Arthur & Vassilvitskii, 2007)

This is the standard today. Instead of random initialization, it spreads initial centroids out deliberately:

1. Pick the first centroid $\mu_1$ uniformly at random from the data
2. For each remaining centroid:
    - Compute $D(x)$ = distance from each point to its nearest already-chosen centroid
    - Sample the next centroid with probability proportional to $D(x)^2$
3. Repeat until $k$ centroids are chosen

The $D(x)^2$ weighting means points far from existing centroids are more likely to be chosen next. This spreads centroids across the data, dramatically reducing the chance of bad initializations.

**Theoretical guarantee**: K-means++ gives an expected cost within $O(\log k)$ of the global optimum before the Lloyd iterations even begin.

**Practical impact**: K-means++ almost always produces better results than random initialization and converges faster. In sklearn, this is the default (`init='k-means++'`).

### Multiple Restarts

Even with K-means++, you should run the algorithm multiple times with different random seeds and keep the solution with the lowest inertia $J$.

```python
# sklearn runs 10 initializations by default
KMeans(n_clusters=k, init='k-means++', n_init=10)
```

The more restarts, the more confident you are in avoiding bad local minima. 10 is usually enough; 20–50 for small datasets where each run is cheap.

---

## 5. What K-Means Is Actually Optimizing (And Why That Matters)

### The WCSS Objective

K-means minimizes: $$J = \sum_{j=1}^{k} \sum_{x_i \in C_j} |x_i - \mu_j|^2$$

This uses **squared Euclidean distance**. This choice has major consequences:

**Consequence 1: Sensitive to scale**  
If one feature has values in $[0, 1000]$ and another in $[0, 1]$, the first feature dominates all distance calculations. The clustering will effectively ignore the second feature. **Always standardize features before running k-means.**

**Consequence 2: Sensitive to outliers**  
Squared distance heavily penalizes points far from centroids. A single outlier can pull a centroid far from the true center of its cluster. This is the squared part — distance gets amplified.

**Consequence 3: Assumes spherical, equal-sized clusters**  
WCSS is minimized when clusters are roughly spherical (equal spread in all directions) and roughly equal in size. K-means will produce poor results on:

- Elongated clusters (ellipses, arcs)
- Clusters of very different sizes
- Clusters of very different densities

This is not a bug — it's a consequence of what the objective function measures.

**Consequence 4: The centroid is the mean**  
The update step computes $\mu_j = \text{mean}(C_j)$ because the mean minimizes the sum of squared distances within a cluster. If you changed the distance metric, the update step would change too (e.g., using Manhattan distance leads to the median, giving K-medians).

---

## 6. Choosing K: The Real Hard Problem

K-means requires you to specify $k$ in advance. But in real applications, you usually don't know how many clusters there are. This is arguably the hardest part of using k-means in practice.

### The Elbow Method

Run k-means for $k = 1, 2, 3, \ldots, K_{\max}$. Plot inertia $J$ vs $k$.

As $k$ increases, $J$ always decreases (with $k = n$, every point is its own cluster and $J = 0$). Look for an "elbow" — a point where the rate of decrease sharply slows down.

```
J
|
|*
| *
|  *
|    *
|       *
|           * * * * *  ← Elbow here — adding more k doesn't help much
|_________________________
         k →
```

**The honest assessment**: The elbow is often ambiguous or absent in real data. Real clusters don't always produce a clean elbow. Don't rely solely on this — use it alongside other methods.

### Silhouette Score

For each point $i$, compute:

- $a(i)$: mean distance to all other points **in the same cluster** (cohesion)
- $b(i)$: mean distance to all points **in the nearest other cluster** (separation)

$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$

- $s(i) \in [-1, 1]$
- $s(i) \approx 1$: well-clustered (far from neighbors, close to own cluster)
- $s(i) \approx 0$: on the boundary between clusters
- $s(i) < 0$: probably assigned to the wrong cluster

The **mean silhouette score** across all points measures overall clustering quality. Run k-means for multiple values of $k$ and pick the $k$ that maximizes mean silhouette score.

**This is more reliable than the elbow method** because it measures both cohesion and separation, not just inertia.

### Gap Statistic (Tibshirani et al., 2001)

Compare the inertia of your clustering to the expected inertia under a null reference distribution (data with no cluster structure, typically uniform random data). The gap statistic:

$$\text{Gap}(k) = \mathbb{E}[\log J_{\text{reference}}(k)] - \log J(k)$$

Choose $k$ where $\text{Gap}(k)$ is maximized or where the gap stops increasing significantly. This is more principled than the elbow method because it accounts for what inertia would look like with no clusters.

**Downside**: Computationally expensive (requires running k-means on many random reference datasets).

### Domain Knowledge

Often the most reliable guide. If you're clustering customer segments for 5 product lines, $k=5$ or nearby values make business sense. If you're clustering gene expression data and biology suggests 3 subtypes, start there. Never treat the choice of $k$ as a purely statistical question when you have domain context.

---

## 7. The Assumptions K-Means Makes (And When They Break)

Understanding what k-means assumes is more useful than memorizing its steps.

### Assumption 1: Clusters are convex and roughly spherical

K-means draws Voronoi boundaries between centroids — each region is a convex polygon. It cannot find non-convex clusters (crescents, rings, interlocking spirals).

**Example that breaks k-means**: Two concentric rings. K-means will split them vertically/horizontally, completely ignoring the ring structure. DBSCAN or spectral clustering handle this.

### Assumption 2: Clusters are roughly equal in size

If one true cluster has 1000 points and another has 10, k-means will tend to split the large cluster to minimize WCSS rather than correctly identifying the small one.

### Assumption 3: Clusters are roughly equal in density

If one cluster is dense and another is sparse, the sparse cluster's centroid may attract points from the dense cluster's edges.

### Assumption 4: The number of clusters is known

Already covered. The hardest assumption to satisfy in practice.

### What to Do When These Break

|Problem|Better Algorithm|
|---|---|
|Non-convex clusters|DBSCAN, Spectral Clustering|
|Unknown number of clusters|DBSCAN, HDBSCAN, GMM with BIC|
|Very different cluster sizes|GMM with different covariances, HDBSCAN|
|Need soft assignments (probabilistic)|Gaussian Mixture Models|
|Very high-dimensional data|Dimensionality reduction first, then cluster|
|Outliers must be detected|DBSCAN (has noise class), HDBSCAN|

---

## 8. K-Means vs Gaussian Mixture Models (GMM)

GMM is the "soft" probabilistic version of k-means and understanding the connection deepens your understanding of both.

### Hard vs Soft Assignment

K-means: each point belongs to exactly one cluster (hard assignment).  
GMM: each point has a probability of belonging to each cluster (soft assignment).

Point $x_i$ in GMM has assignment probabilities $r_{ij} = P(\text{cluster } j | x_i)$.

### What GMM Assumes vs K-Means

K-means assumes all clusters have the same spherical covariance (radius). GMM assumes each cluster is a Gaussian with its own mean **and covariance** — so clusters can be elliptical, rotated, different sizes.

K-means is actually a **special case of GMM** where:

- All Gaussians have the same fixed covariance $\sigma^2 I$ (spherical)
- As $\sigma \to 0$: soft assignments become hard — the highest-probability cluster gets all the weight
- The E-step of EM (Expectation-Maximization for GMMs) converges to the k-means assignment step
- The M-step converges to the k-means update step

So k-means is EM for GMMs in the limit of zero variance, with hard assignments. This isn't trivia — it tells you exactly what k-means is assuming about your data's generative process.

### When to Use GMM Instead

- Clusters have different shapes or orientations
- You need probabilistic membership (how confident is the assignment?)
- Clusters have different sizes
- You can use BIC/AIC to select $k$ (GMM has a proper likelihood, k-means doesn't)

**Tradeoff**: GMM has more parameters to estimate, needs more data, and can have convergence issues. K-means is faster, simpler, and works well when its assumptions hold.

---

## 9. Computational Complexity and Scaling

### Basic Complexity

Each iteration of k-means: compute distance from every point to every centroid → $O(nkd)$ per iteration.

With $T$ iterations: $O(nkdT)$ total.

For $n = 10^6$, $k = 100$, $d = 50$, $T = 20$: that's $10^{10}$ operations — too slow for naive implementation.

### Mini-Batch K-Means

Instead of computing over the full dataset per iteration, sample a mini-batch $B \subset {1,\ldots,n}$ and do assignment + update on just those points:

1. Sample mini-batch of size $b$ (e.g., $b = 1000$)
2. Assign mini-batch points to nearest centroids
3. Update centroids using only mini-batch points (with a running average)

This gives approximate solutions much faster, especially for large $n$. On very large datasets (millions of points), mini-batch k-means often reaches similar quality to full k-means while being 10–100× faster.

```python
from sklearn.cluster import MiniBatchKMeans
model = MiniBatchKMeans(n_clusters=k, batch_size=1024)
model.fit(X)
```

**Tradeoff**: Noisier convergence, slightly higher inertia than exact k-means. Usually acceptable.

### Approximate Nearest Neighbors

The assignment step (find nearest centroid for each point) can be accelerated with data structures like KD-trees for low dimensions, or approximate nearest neighbor search (e.g., FAISS) for high dimensions.

FAISS (Facebook AI Similarity Search) is the standard for large-scale k-means on high-dimensional data (e.g., clustering image embeddings).

---

## 10. K-Means in High Dimensions: The Curse

In high dimensions ($d \gg k$), k-means behaves poorly for a fundamental reason: **distances concentrate**.

In high dimensions, all pairwise distances between random points converge to nearly the same value. The signal-to-noise ratio in distance — the ratio of between-cluster distance to within-cluster distance — vanishes.

Formally, for points drawn uniformly from a hypersphere: $$\frac{\max_{i,j} |x_i - x_j| - \min_{i,j} |x_i - x_j|}{\min_{i,j} |x_i - x_j|} \to 0 \text{ as } d \to \infty$$

When all points are equidistant, cluster assignment becomes essentially random.

**What to do**: Dimensionality reduction before clustering. PCA, UMAP, or an autoencoder to reduce $d$ to something manageable (10–50 dimensions), then run k-means.

This is the standard pipeline for clustering images, text embeddings, or any high-dimensional data:

1. Extract embeddings from a pretrained model (ResNet, BERT, etc.)
2. Reduce dimensionality (PCA to 50 dims, or UMAP to 2–10 dims for visualization)
3. Run k-means on the reduced representation

---

## 11. Feature Preprocessing: What You Must Do

### Standardization (Z-score normalization)

$$x' = \frac{x - \mu}{\sigma}$$

Transforms each feature to zero mean and unit variance. **This is almost always necessary before k-means.** Without it, features with large numeric ranges dominate distances.

Example: clustering customers by age (0–80) and annual income (0–500,000). Without standardization, income dominates completely — the clustering is essentially just income-based.

### When Not to Standardize

If you have a principled reason to believe one feature should have more influence on the clustering, you can weight features by adjusting their scale. Standardization gives all features equal weight — sometimes that's wrong.

### Normalization (L2 normalization)

$$x' = \frac{x}{|x|}$$

Projects each point onto the unit hypersphere. Useful when the direction of a vector matters more than its magnitude (e.g., document embeddings — a short and long document on the same topic should cluster together regardless of length).

K-means on L2-normalized vectors with cosine distance is commonly used for text and embedding clustering.

### Categorical Features

K-means requires numeric features (it computes means). For categorical features:

- One-hot encode (and be aware this increases dimensionality)
- Use K-modes (a variant that replaces means with modes and uses Hamming distance)
- Use K-prototypes (handles mixed numeric and categorical data)

---

## 12. Evaluating Clustering: The Hard Part

Clustering evaluation is genuinely difficult because there are no labels to compare against (it's unsupervised). Two types of evaluation:

### Internal Metrics (No Ground Truth Needed)

**Inertia (WCSS)**: Lower is better, but always decreases with $k$ — only useful for comparing models with the same $k$.

**Silhouette Score**: Higher is better. Valid range $[-1, 1]$. Good for comparing different $k$ values.

**Davies-Bouldin Index**: Ratio of within-cluster scatter to between-cluster separation. Lower is better.

**Calinski-Harabasz Index (Variance Ratio)**: Ratio of between-cluster variance to within-cluster variance. Higher is better. Faster to compute than silhouette.

None of these perfectly capture "good clustering" in all cases. They all make assumptions about what a good cluster looks like.

### External Metrics (When Ground Truth Exists)

If you have labels (e.g., you know the true classes and are clustering to recover them):

**Adjusted Rand Index (ARI)**: Measures similarity between two partitions, adjusted for chance. Range $[-1, 1]$, higher is better. 0 = random, 1 = perfect match.

**Normalized Mutual Information (NMI)**: Measures information shared between clustering and true labels. Range $[0, 1]$.

**Homogeneity, Completeness, V-measure**: Homogeneity = each cluster contains only members of one class. Completeness = all members of a class are in one cluster. V-measure = harmonic mean of both. All range $[0, 1]$.

**Important nuance**: These external metrics are for evaluating how well clustering recovers known structure, not for general unsupervised evaluation. In most real applications you don't have ground truth labels — that's the whole point of unsupervised learning.

---

## 13. Common Failure Modes

### Empty Clusters

If a centroid ends up in an empty region and no points are assigned to it, the update step is undefined (mean of zero points). This is rare with K-means++ initialization but can happen.

**Fix**: Reinitialize the empty centroid (e.g., move it to the point farthest from its current centroid, or reinitialize randomly).

### Centroid Instability

With randomly initialized centroids close to each other, they may oscillate between very similar configurations without truly converging. Multiple restarts and K-means++ reduce this.

### All Points in One Cluster

If $k$ is too large for the data's actual structure, some clusters collapse (very few points) and others absorb almost everything. The solution is the right $k$, not a algorithmic fix.

### Sensitive to Outliers

A single outlier point far from all clusters can pull a centroid away from the true cluster center, distorting the entire partition. Options:

- Remove outliers before clustering
- Use K-medoids (uses actual data points as centers, more robust) instead of K-means
- Use DBSCAN which explicitly labels outliers as noise

---

## 14. Practical Variants

### K-Medoids (PAM — Partitioning Around Medoids)

Instead of using the mean as the cluster center, use an **actual data point** (the medoid — the point that minimizes average distance to other cluster members).

Advantages:

- Works with any distance metric (not just Euclidean)
- More robust to outliers (the center is always a real data point)
- Interpretable centers (you can look at the representative example)

Disadvantage: Slower — finding the medoid requires $O(|C_j|^2)$ per cluster vs $O(|C_j|)$ for the mean.

### Fuzzy C-Means

Soft-assignment variant. Each point has a degree of membership $u_{ij} \in [0,1]$ to each cluster, with $\sum_j u_{ij} = 1$.

The objective: $$J = \sum_{i=1}^{n} \sum_{j=1}^{k} u_{ij}^m |x_i - \mu_j|^2$$

where $m > 1$ is a fuzziness parameter. As $m \to 1$: approaches hard k-means. As $m \to \infty$: all membership degrees equal $1/k$ (completely fuzzy, no structure).

Useful when cluster boundaries are genuinely gradual rather than sharp.

### K-Means for Vector Quantization

K-means was originally developed for vector quantization — compressing high-dimensional data by representing each point with the index of its nearest centroid (codeword). The set of centroids is the codebook.

This is still used in image compression, audio coding, and as the final step in hierarchical feature learning. Product quantization (used in FAISS for approximate nearest neighbor search) is a generalization.

### Spherical K-Means

For text and embedding data, cosine similarity often makes more sense than Euclidean distance. Spherical k-means:

- L2-normalize all data points
- Use cosine distance in the assignment step
- Renormalize centroids after each update step

Effectively clusters by direction rather than magnitude.

---

## 15. K-Means in Deep Learning

K-means appears in deep learning more than you might expect:

### Feature Quantization and Codebooks

Vector Quantized VAE (VQ-VAE) uses k-means-style quantization in the latent space. The encoder output is snapped to the nearest codebook vector (centroid), with straight-through gradients for backpropagation. Used in DALL-E (original), AudioLM, MusicLM.

### Clustering for Pseudo-Labels (Self-Supervised Learning)

DeepCluster (Caron et al., 2018) alternates between:

1. Clustering feature representations with k-means
2. Using cluster assignments as pseudo-labels to train the network with a classification loss

This bootstraps visual representations from unlabeled images. The cluster assignments give the model something to predict, which forces it to learn meaningful features.

SwAV, a follow-up, does this online (without full k-means at each epoch) by swapped prediction — predict the cluster assignment of one augmented view from the representation of another.

### Attention and Soft Clustering

Cross-attention in Transformers is related to soft clustering — query vectors are "assigned" to key-value pairs by a softmax over dot products. This is a differentiable, learned version of cluster assignment.

---

## 16. Implementation in sklearn

```python
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np

# Always standardize first
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Run k-means with k-means++ init and multiple restarts
kmeans = KMeans(
    n_clusters=k,
    init='k-means++',    # smart initialization
    n_init=10,           # 10 random restarts, keep best
    max_iter=300,        # max iterations per run
    tol=1e-4,            # convergence tolerance
    random_state=42
)
kmeans.fit(X_scaled)

labels = kmeans.labels_           # cluster assignment for each point
centroids = kmeans.cluster_centers_  # centroid coordinates
inertia = kmeans.inertia_         # final WCSS value

# Choosing k: compare silhouette scores
scores = []
for k in range(2, 11):
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_scaled)
    score = silhouette_score(X_scaled, km.labels_)
    scores.append((k, score))
    print(f"k={k}, silhouette={score:.4f}")

best_k = max(scores, key=lambda x: x[1])[0]

# For large datasets
mbkm = MiniBatchKMeans(n_clusters=k, batch_size=1024, n_init=10, random_state=42)
mbkm.fit(X_scaled)
```

---

## 17. Key Takeaways

- K-means partitions $n$ points into $k$ clusters by minimizing **within-cluster sum of squares (WCSS / inertia)** — the sum of squared distances from each point to its cluster centroid.
- The algorithm alternates between **assignment** (assign each point to nearest centroid) and **update** (recompute centroids as cluster means). Guaranteed to converge, but to a **local minimum**.
- **K-means++ initialization** spreads initial centroids far apart via $D(x)^2$-weighted sampling, avoiding bad local minima. Always use it over random init.
- **Always standardize features** before k-means — squared Euclidean distance is scale-sensitive. High-variance features dominate otherwise.
- K-means assumes **spherical, equally-sized, equally-dense** clusters. It fails on non-convex shapes, very different cluster sizes, and noisy/outlier-heavy data.
- Choosing $k$ is hard. Silhouette score is more reliable than the elbow method. Domain knowledge is often the most useful guide.
- K-means is a **special case of EM for Gaussian Mixture Models** with spherical covariance and hard assignments — understanding this tells you exactly what it assumes about data.
- **High dimensions kill k-means** (distance concentration). Reduce dimensionality first (PCA, UMAP, learned embeddings).
- For large-scale data: **Mini-Batch K-Means** (sklearn) or **FAISS** (for embedding-scale clustering).
- In deep learning, k-means appears in VQ-VAE codebooks, DeepCluster pseudo-labels, and SwAV — it's not just a classical ML tool.