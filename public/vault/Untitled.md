---
title: "Untitled"
lastmod: 2026-09-10
---



Ran command: `git status`
Ran command: `git add .`
Ran command: `git status`
Ran command: `git commit -m "KSD experiments with c10 as the main distribution and checking ID vs OOD histogram plots for the test statistic."`
Ran command: `git push origin main`
Viewed ksd_utils.py:67-104

Here is the complete step-by-step mathematical breakdown of the vectorized KSD calculation in `compute_per_sample_ksd_single_scale`:

---

### 1. Inputs & Data Vectors (Lines 45–50)
* **Input**: $N$ image samples $x_1, x_2, \dots, x_N$, each of dimension $d = 32 \times 32 \times 3 = 3072$.
* **Perturbation**: At noise scale $\sigma_k$, Gaussian noise is added:
  $$\mathbf{x}_i^{\text{noisy}} = \mathbf{x}_i + \sigma_k \boldsymbol{\epsilon}_i, \quad \boldsymbol{\epsilon}_i \sim \mathcal{N}(0, \mathbf{I})$$
* **Flattened Tensor $X$**: Shape $(N, d)$ where row $i$ is $x_i \in \mathbb{R}^d$.

---

### 2. Pairwise Distances & RBF Kernel $K$ (Lines 52–63)
* **Pairwise Distance Matrix $D^2$** (`dists_sq`):
  $$D_{ij}^2 = \|x_i - x_j\|_2^2 \quad (\text{shape } N \times N)$$
* **Median Heuristic Bandwidth $\gamma$**:
  $$\gamma = \sqrt{\frac{\text{median}(D_{ij}^2)}{2}}, \quad \text{gamma\_sq} = \gamma^2, \quad \text{gamma\_quad} = \gamma^4$$
* **Gaussian RBF Kernel Matrix $K$**:
  $$K_{ij} = k(x_i, x_j) = \exp\left( -\frac{\|x_i - x_j\|^2}{2 \gamma^2} \right) \quad (\text{shape } N \times N)$$

---

### 3. Score Network Matrix $S$ (Line 66)
* Score network predicts score gradient vectors $s_i = s_\theta(x_i, \sigma_k) \approx \nabla_{x_i} \log p_{\sigma_k}(x_i)$ for all $N$ images.
* **Score Matrix $S$**: Shape $(N, d)$ where row $i$ is vector $s_i \in \mathbb{R}^d$.

---

### 4. Analytical Stein Kernel Formula

The analytical Stein Kernel $u_q(x_i, x_j)$ between two points $x_i$ and $x_j$ using score function $s(x)$ and kernel $k(x_i, x_j)$ is:

$$u_q(x_i, x_j) = s(x_i)^T s(x_j) \, k(x_i, x_j) + s(x_i)^T \nabla_{x_j} k(x_i, x_j) + \nabla_{x_i} k(x_i, x_j)^T s(x_j) + \text{Tr}\left(\nabla_{x_i, x_j} k(x_i, x_j)\right)$$

For the **Gaussian RBF Kernel** $k(x_i, x_j) = \exp\left(-\frac{\|x_i - x_j\|^2}{2\gamma^2}\right)$, the gradients are:
1. $\nabla_{x_j} k(x_i, x_j) = \frac{x_i - x_j}{\gamma^2} k(x_i, x_j)$
2. $\nabla_{x_i} k(x_i, x_j) = -\frac{x_i - x_j}{\gamma^2} k(x_i, x_j)$
3. $\text{Tr}\left(\nabla_{x_i, x_j} k(x_i, x_j)\right) = \left( \frac{d}{\gamma^2} - \frac{\|x_i - x_j\|^2}{\gamma^4} \right) k(x_i, x_j)$

Substituting these gradient terms into $u_q(x_i, x_j)$ yields:

$$u_q(x_i, x_j) = \left[ \underbrace{s(x_i)^T s(x_j)}_{\text{Term 1}} + \underbrace{\frac{s(x_i)^T(x_i - x_j)}{\gamma^2}}_{\text{Term 2}} - \underbrace{\frac{(x_i - x_j)^T s(x_j)}{\gamma^2}}_{\text{Term 3}} + \underbrace{\frac{d}{\gamma^2} - \frac{\|x_i - x_j\|^2}{\gamma^4}}_{\text{Term 4}} \right] k(x_i, x_j)$$

---

### 5. Fast $O(N^2)$ Matrix Vectorization (Lines 70–91)

To compute $u_q(x_i, x_j)$ for all $N \times N$ pairs in parallel without allocating massive 3D/4D tensors:

1. **Term 1 (`SS_T`)**:
   $$\text{SS\_T}[i, j] = s_i^T s_j = (S S^T)_{ij} \quad (\text{shape } N \times N)$$

2. **Self Dot-Product Vector $v$**:
   $$v_i = s_i^T x_i \quad (\text{shape } N)$$

3. **Term 2 (`term2`)**:
   $$s_i^T (x_i - x_j) = s_i^T x_i - s_i^T x_j = v_i - (S X^T)_{ij} \implies \text{term2} = v \mathbf{1}^T - S X^T$$

4. **Term 3 (`term3`)**:
   $$(x_i - x_j)^T s_j = x_i^T s_j - x_j^T s_j = (X S^T)_{ij} - v_j \implies \text{term3} = X S^T - \mathbf{1} v^T$$

5. **Bracket Matrix Assembly**:
   $$\text{brackets} = \text{SS\_T} + \frac{\text{term2}}{\gamma^2} - \frac{\text{term3}}{\gamma^2} + \frac{d}{\gamma^2} - \frac{D^2}{\gamma^4} \quad (\text{shape } N \times N)$$

6. **Stein Kernel Matrix $U$**:
   $$U = \text{brackets} \odot K \quad (\text{shape } N \times N)$$

---

### 6. Per-Sample Average KSD Statistic (Lines 93–97)

1. **Diagonal zeroing**: `U.fill_diagonal_(0.0)` sets $U_{ii} = 0$ to satisfy the unbiased U-statistic formulation.
2. **Per-sample average KSD contribution**:
   $$h(x_i, \sigma_k) = \frac{1}{N - 1} \sum_{j \neq i} U_{ij}$$
   * `per_sample_ksd = U.sum(dim=1) / (N - 1)` (shape $N$)

This gives $N$ scalar KSD metrics for sample $\{x_i\}_{i=1}^N$ at noise scale $\sigma_k$.