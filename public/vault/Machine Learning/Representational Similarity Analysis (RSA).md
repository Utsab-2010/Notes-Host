---
title: "Representational Similarity Analysis (RSA)"
lastmod: 2026-07-01
---

## 1. The Core Question RSA Answers

You have two systems that process the same set of stimuli — say, a human brain viewing 100 images, and a neural network processing the same 100 images. Both produce some internal representation for each image: the brain produces patterns of neural activity, the network produces activation vectors at some layer.

You want to ask: **do these two systems represent the world in a similar way?**

The problem is that the representations live in completely different spaces. The brain's representation might be a vector of firing rates across 10,000 neurons. The network's representation might be a 512-dimensional activation vector. You can't directly compare a 10,000-dimensional brain vector to a 512-dimensional network vector — the spaces don't correspond.

RSA solves this with a elegant sidestep:

> **Don't compare the representations directly. Instead, compare the structure of pairwise similarities between stimuli. If two systems organize stimuli in the same way relative to each other, their representational geometry is similar — regardless of the dimensionality or format of the underlying representations.**

This is the core insight. RSA moves from comparing representations (hard, space-dependent) to comparing **similarity structures** (easy, space-independent). It's a second-order isomorphism: not "are these two vectors the same?" but "are the patterns of similarity between stimuli the same in both systems?"

---

## 2. The Representational Dissimilarity Matrix (RDM)

The central object in RSA is the **Representational Dissimilarity Matrix (RDM)**.

### Building an RDM

Given $n$ stimuli and a system that produces a representation $r_i \in \mathbb{R}^d$ for each stimulus $i$:

1. Compute the **pairwise dissimilarity** between every pair of stimuli $(i, j)$
2. Store these in an $n \times n$ matrix $D$ where $D_{ij}$ = dissimilarity between stimulus $i$ and stimulus $j$

Common dissimilarity measures:

- **1 − Pearson correlation**: $D_{ij} = 1 - \frac{(r_i - \bar{r}_i)^T(r_j - \bar{r}_j)}{|r_i - \bar{r}_i| |r_j - \bar{r}_j|}$
- **Euclidean distance**: $D_{ij} = |r_i - r_j|$
- **1 − cosine similarity**: $D_{ij} = 1 - \frac{r_i^T r_j}{|r_i||r_j|}$
- **Mahalanobis distance**: accounts for the covariance structure of the representations — preferred in neuroscience for cross-validated noise normalization

The RDM is:

- **Symmetric**: $D_{ij} = D_{ji}$
- **Zero on the diagonal**: $D_{ii} = 0$ (a stimulus is identical to itself)
- **$n \times n$ regardless of the dimensionality $d$ of the representations**

That last point is the key. The RDM of a 10,000-dimensional brain representation and the RDM of a 512-dimensional network activation are both $n \times n$ matrices over the same $n$ stimuli. Now they're directly comparable.

### Visualizing the RDM

The RDM is usually visualized as a heatmap with stimuli ordered in some meaningful way (e.g., by category). A good representation produces a block-diagonal structure — high dissimilarity between stimuli from different categories, low dissimilarity within a category. The pattern of this block structure is exactly what RSA reads.

---

## 3. The RSA Pipeline

### Step 1: Choose Your Stimuli

Select $n$ stimuli that span the space you care about. For vision: images from different object categories. For language: sentences with different semantic/syntactic properties. For audition: sounds with different acoustic properties.

The stimuli must be the **same** for all systems being compared — this is the shared anchor.

$n$ is typically 50–200 in neuroscience experiments (limited by scan time and trial repetitions needed for noise estimation). In computational work with models, $n$ can be much larger.

### Step 2: Measure Representations

For each system being compared:

- **Brain**: measure neural responses (fMRI BOLD signal in a brain region, EEG/MEG time-frequency power, single-unit firing rates)
- **Model layer**: extract activation vectors at a specific layer
- **Behavioral**: measure human similarity judgments, reaction times, error patterns
- **Computational model**: any feature vector — pixel values, SIFT features, semantic embeddings

Each system produces a matrix of representations $R \in \mathbb{R}^{n \times d}$ (n stimuli, d-dimensional representations).

### Step 3: Compute RDMs

For each system, compute its RDM. You now have one $n \times n$ dissimilarity matrix per system.

### Step 4: Compare RDMs

Compare pairs of RDMs using a **second-order similarity measure** — typically Spearman rank correlation between the upper triangles of the two RDMs:

$$\rho_{\text{RSA}} = \text{SpearmanCorr}(\text{upper}(D_A), \text{upper}(D_B))$$

Why the upper triangle? The RDM is symmetric and the diagonal is always zero — the upper triangle contains all $\frac{n(n-1)}{2}$ unique pairwise dissimilarities.

Why Spearman (rank correlation) rather than Pearson?

- The dissimilarities in two different systems may be on very different scales (e.g., neural distances vs. pixel distances). Rank correlation is scale-invariant.
- The relationship between dissimilarities in two systems might be monotonic but not linear. Spearman captures monotonic relationships.
- More robust to outlier dissimilarity pairs.

The RSA score $\rho \in [-1, 1]$:

- $\rho \approx 1$: the two systems organize stimuli similarly
- $\rho \approx 0$: no relationship between the two representations
- $\rho < 0$: stimuli that are similar in one system are dissimilar in the other (rare in practice but possible)

### Step 5: Statistical Testing

Is the observed $\rho$ significantly different from zero (or from another model's $\rho$)?

**Within-system**: permutation testing — randomly permute rows and columns of one RDM (corresponding to randomly reassigning stimuli) and compute the distribution of $\rho$ under the null hypothesis of no relationship. The p-value is the fraction of permuted $\rho$ values exceeding the observed $\rho$.

**Across subjects** (in neuroscience): treat each subject's RSA score as an observation. Use a t-test or Wilcoxon signed-rank test across subjects.

**Noise ceiling**: estimated upper bound on RSA performance given measurement noise (see Section 8).

---

## 4. What the RDM Actually Encodes: Representational Geometry

The RDM doesn't just capture "which stimuli are similar" — it captures the full **geometry** of the representational space in a format that abstracts away dimensionality and linear transformations.

Specifically: two representations $R_A$ and $R_B$ have identical RDMs (under Euclidean distance) if and only if one can be obtained from the other by a **rigid transformation** (rotation, reflection, translation). The RDM is invariant to:

- Rotations and reflections
- Uniform scaling (under rank-based RSA)

But sensitive to:

- Which stimuli are grouped close together vs. far apart
- The relative ordering of distances
- The presence or absence of categorical cluster structure

This is why RSA is called a "second-order" analysis — it captures the structure of structures, not the structures themselves.

### What Changes Between Layers of a Neural Network

As you move through layers of a deep network (or along the ventral visual stream in the brain), the RDM changes:

- **Early layers**: RDM reflects low-level image properties — images with similar pixel patterns are close, regardless of category
- **Middle layers**: RDM transitions — category structure begins to emerge but mixed with low-level features
- **Late layers**: RDM strongly reflects semantic category — images of the same object class cluster together regardless of viewpoint, lighting, or low-level appearance

Tracking how the RDM changes across layers tells you where and how the network/brain transforms its representation. This is one of the most powerful uses of RSA.

---

## 5. Model Comparison: The Real Power of RSA

RSA is most powerful when used to compare multiple competing models against brain data.

### The Setup

You have:

- Brain RDM: $D_{\text{brain}}$ (from fMRI data in, say, inferior temporal cortex)
- Model RDMs: $D_{\text{model}_1}, D_{\text{model}_2}, \ldots, D_{\text{model}_k}$ (from different computational models, layers, or hypotheses)

Compute RSA score for each model: $$\rho_i = \text{SpearmanCorr}(\text{upper}(D_{\text{brain}}), \text{upper}(D_{\text{model}_i}))$$

Rank the models by $\rho_i$. The model with the highest score is most similar to the brain's representational geometry.

### Example: Comparing CNN Layers to Brain Regions

Classic experiment (Khaligh-Razavi & Kriegeskorte, 2014): compare RDMs from different layers of AlexNet to RDMs from different regions along the human ventral visual stream (V1, V2, V4, IT).

Finding: Early CNN layers (conv1, conv2) correlate most with early visual areas (V1, V2). Later CNN layers (fc6, fc7) correlate most with higher visual areas (V4, IT). The representational hierarchy of CNNs mirrors the representational hierarchy of the brain.

This was landmark evidence that CNNs, despite being trained purely on image classification, develop representations similar to the primate visual system. RSA was the tool that made this comparison possible across the brain/model dimension gap.

### Model RDMs Can Come From Anywhere

The model doesn't have to be a neural network. You can construct RDMs from:

- **Categorical labels**: $D_{ij} = 0$ if same category, $1$ if different → captures pure category structure
- **Physical features**: pixel-level distance, color histogram distance, shape descriptors
- **Semantic embeddings**: Word2Vec or BERT cosine distances between object names
- **Behavioral data**: human similarity ratings, confusion matrices in recognition tasks
- **Theoretical models**: RDMs derived from cognitive science models, graphical models, etc.

This flexibility is one of RSA's greatest strengths: any hypothesis about what a system represents can be formalized as an RDM and tested.

---

## 6. RSA in Neuroscience: Specific Applications

### fMRI: Spatial RSA

In fMRI, the representation of a stimulus in a brain region is the pattern of BOLD activation across voxels. For region $R$ with $v$ voxels:

$$r_i = \text{BOLD activation pattern for stimulus } i \in \mathbb{R}^v$$

The RDM for region $R$ captures the multivariate geometry of that region's representations — much more information than a univariate analysis ("does this region activate more for condition A vs B?").

**Searchlight RSA**: Instead of analyzing predefined regions, slide a sphere (searchlight) of radius ~3–10mm across the whole brain. At each voxel, compute the RSA score for the local sphere. The result is a whole-brain map of "where in the brain does the representational geometry match this model?" Very powerful for hypothesis-free discovery.

### EEG/MEG: Temporal RSA

EEG/MEG has millisecond temporal resolution but poor spatial resolution. The representation at time $t$ is the pattern of sensor activity across electrodes:

$$r_i(t) = \text{EEG pattern for stimulus } i \text{ at time } t \in \mathbb{R}^{\text{electrodes}}$$

Compute a separate RDM at each time point $t$, then correlate each time-point RDM with model RDMs. The result: a **temporal RSA curve** showing when in the processing timeline each model's representational structure emerges.

Classic finding: categorical structure (animate vs. inanimate) emerges at ~150ms post-stimulus. Within-category distinctions emerge later, ~200–300ms. RSA on EEG data provides the time course of representational transformations.

### Combining fMRI and EEG

RSA enables something powerful: comparing fMRI RDMs with EEG RDMs. Even though fMRI and EEG measure completely different signals (hemodynamics vs. electrical potentials), their RDMs can be directly compared. If the representational geometry of an fMRI region matches the representational geometry of an EEG time point, that suggests they're measuring the same underlying computation.

---

## 7. RSA in Machine Learning and Representation Learning

RSA has become a standard tool in the ML interpretability and representation learning literature.

### Layer-wise Analysis of Deep Networks

Given a trained network and a stimulus set, compute RDMs at every layer. Track how representational geometry evolves:

- Do representations become more linearly separable across layers? (Check if categorical RDM correlation increases)
- At which layer does the network "commit" to a semantic interpretation?
- How does the representational trajectory differ between a well-trained and poorly-trained network?

This is used routinely in mechanistic interpretability research.

### Comparing Two Neural Networks

Are ResNet and VGG learning the same representations despite different architectures? Compute their layer RDMs on the same stimulus set (e.g., ImageNet validation images) and correlate them. High correlation → similar representational geometry despite different weights.

This connects to **CKA (Centered Kernel Alignment)** — a closely related method (see Section 9) that is often preferred for comparing networks because it has better statistical properties for large $n$.

### Probing What Information is Encoded

Suppose you want to know whether layer 5 of your model encodes color information. Build a model RDM based purely on color histograms of the stimuli. Correlate with the layer 5 RDM. High correlation → layer 5's representational geometry is partially explained by color.

You can do this for any feature you hypothesize: texture, shape, semantic category, depth, motion, etc. RSA turns "what does this layer encode?" into a quantitative question.

### Tracking Representation Through Training

Compute RDMs at a fixed set of checkpoints during training. How does the representational geometry evolve? Does categorical structure emerge early or late in training? Does it appear suddenly or gradually? This kind of analysis is directly relevant to understanding curriculum learning and data pruning effects on representations — if EL2N pruning distorts the Zipf distribution of latent quanta (as in your work), RSA on intermediate checkpoints could reveal when and how the representational geometry diverges from the full-data training trajectory.

---

## 8. The Noise Ceiling

A critical concept that makes RSA results interpretable: the **noise ceiling**.

### The Problem

Your brain RDM is estimated from noisy measurements. Even a perfect model of the brain would not achieve $\rho = 1$ because the brain RDM itself is noisy — if you re-ran the experiment, you'd get a slightly different brain RDM. The maximum possible RSA score for any model is bounded by the reliability of the brain data itself.

### Computing the Noise Ceiling

Compute the brain RDM separately for two halves of the data (odd and even trials, or random splits). Correlate these two "split-half" RDMs. This gives the **noise ceiling** — the expected RSA score for a perfect model:

$$\text{Noise ceiling} = \text{SpearmanCorr}(D_{\text{brain}}^{\text{half 1}}, D_{\text{brain}}^{\text{half 2}})$$

More precisely:

- **Upper bound**: correlation of each subject's RDM with the group-average RDM (the average includes the subject, which inflates the estimate slightly)
- **Lower bound**: correlation of a left-out subject's RDM with the group-average RDM computed from the remaining subjects

A model that matches the lower bound is doing as well as an individual subject matches the group — essentially as well as possible given noise.

### Why This Matters

If your best model achieves $\rho = 0.4$ and the noise ceiling is $\rho = 0.45$: the model is near-perfect, leaving little room for improvement. You should look for a better experimental design, not a better model.

If your best model achieves $\rho = 0.2$ and the noise ceiling is $\rho = 0.7$: there's substantial unexplained variance. The current models are missing important structure that the brain captures.

Always report the noise ceiling alongside RSA scores. A score without a noise ceiling is uninterpretable.

---

## 9. RSA vs. CKA: When to Use Which

**CKA (Centered Kernel Alignment)** (Kornblith et al., 2019) is a closely related method developed specifically for comparing neural network representations. It's worth understanding the relationship.

### CKA

Given representation matrices $X \in \mathbb{R}^{n \times d_1}$ and $Y \in \mathbb{R}^{n \times d_2}$:

$$\text{CKA}(X, Y) = \frac{|Y^T X|_F^2}{|X^T X|_F |Y^T Y|_F}$$

With linear kernels (as above), this is equivalent to computing the Frobenius norm of the cross-covariance matrix, normalized by the product of the norms of the auto-covariance matrices.

CKA can also be applied with nonlinear kernels (RBF): replace $X^T X$ with the kernel matrix $K_X$ where $K_{X,ij} = k(x_i, x_j)$.

### RSA vs CKA: Key Differences

||RSA|CKA|
|---|---|---|
|Invariances|Rotation, reflection, uniform scaling (with rank)|Rotation, isotropic scaling|
|Sensitivity|Monotonic structure of distances|Second-order statistics|
|Robustness to outliers|High (Spearman rank)|Low (sensitive to large distances)|
|Statistical testing|Permutation test (established)|Less established|
|Noise ceiling|Well-developed for neuroscience|Less developed|
|Typical use|Neuroscience, brain-model comparison|Comparing two neural networks|
|$n$ requirement|Works with small $n$ (50–200)|More reliable with large $n$|

**When to use RSA**:

- Comparing brain data to computational models
- Small $n$ (neuroscience experimental constraints)
- You have a noise ceiling to compute
- You want established statistical testing framework

**When to use CKA**:

- Comparing two neural networks (both representations are clean, no measurement noise)
- Large $n$ (thousands of stimuli)
- You want a measure that's invariant to orthogonal transformations but sensitive to scaling differences

In practice, if both are feasible, compute both and check that conclusions are consistent.

---

## 10. Important Nuances and Failure Modes

### The Stimuli Matter Enormously

The RSA score depends critically on which stimuli you chose. A stimulus set that only includes images of animals and vehicles will produce RDMs that reflect animacy and vehicle-ness. You cannot conclude anything about how the system represents colors, faces, or textures from such an RDM.

**Practical rule**: The stimulus set must be designed to diagnose the specific hypothesis. If you want to know whether a system encodes semantic category, include stimuli that vary in semantic category while controlling other factors. If you want to know whether it encodes viewpoint, include the same objects at different viewpoints.

This is the single most common mistake in RSA: using a convenient stimulus set and then drawing conclusions that the set cannot support.

### RSA Does Not Identify Linear Decodability

A high RSA score between a model and a brain region does not mean you could linearly decode the model's categories from that brain region (or vice versa). RSA captures the geometry of the full representational space — it's sensitive to all structure in the RDM, including nonlinear structure that a linear classifier could not use. A region might have an RSA score of 0.8 with a categorical model RDM but still be linearly non-separable if the categories are arranged in a nonlinearly separated manifold.

Conversely, a low RSA score does not mean the system doesn't encode the relevant information — it might encode it in a format that is linearly decodable but doesn't produce the right distance structure.

### Correlation of RDMs is Not the Same as Correlation of Representations

Two systems can have highly correlated RDMs while having completely uncorrelated raw representations. The RDM captures the geometry of the representational space, not the specific vectors. Don't confuse "similar geometry" with "same representations."

### Multiple Comparison Problem in Searchlight RSA

Searchlight RSA produces a statistical map at every voxel in the brain — tens of thousands of tests. Standard p-value thresholds are completely inadequate here. Always use:

- FWE (Family-Wise Error) correction: cluster-based permutation testing
- FDR (False Discovery Rate) correction at q < 0.05

Uncorrected searchlight maps reported in papers are essentially uninterpretable.

### The RDM is Not Unique to the Representation

Different representational spaces can produce the same RDM. The RDM tells you about the geometry of a representational space, but many different spaces have the same geometry (related by rotations, reflections). Don't over-interpret an RDM as uniquely identifying the underlying representation.

---

## 11. Worked Example: Comparing ResNet Layers to Human IT Cortex

**Stimuli**: 92 object images from Kriegeskorte et al. (2008) — a standard benchmark set spanning animate/inanimate objects, faces, bodies, natural/artificial objects.

**Brain data**: fMRI responses in human inferior temporal (IT) cortex while subjects viewed the 92 images. $n_{\text{subjects}} = 15$.

**Model**: ResNet-50 trained on ImageNet.

**Step 1**: For each of the 15 subjects, compute the IT cortex RDM (92×92 matrix using 1 - Pearson correlation between voxel patterns).

**Step 2**: Average RDMs across subjects → group IT RDM.

**Step 3**: For each layer of ResNet-50 (conv1 through fc1000), extract activations for all 92 images → compute layer RDM (using 1 - Pearson correlation between activation vectors).

**Step 4**: Correlate each layer RDM with the group IT RDM using Spearman rank correlation.

**Step 5**: Compute noise ceiling from split-half reliability of the group IT RDM.

**Results** (hypothetical but representative of the literature):

- conv1: $\rho = 0.12$ (low-level edge detectors, little categorical structure)
- conv3: $\rho = 0.28$
- conv4: $\rho = 0.41$
- layer3: $\rho = 0.52$
- layer4: $\rho = 0.61$
- avgpool: $\rho = 0.58$
- Noise ceiling: $\rho = 0.71$

**Conclusion**: ResNet-50 layer4 best matches human IT representational geometry, achieving 86% of the noise ceiling. The representational hierarchy of ResNet mirrors the ventral visual stream — later layers are better models of IT.

---

## 12. Implementation

```python
import numpy as np
from scipy.stats import spearmanr
from scipy.spatial.distance import pdist, squareform

def compute_rdm(representations, metric='correlation'):
    """
    Compute RDM from a matrix of representations.
    
    Parameters:
        representations: (n_stimuli, n_features) array
        metric: 'correlation' → 1 - Pearson r
                'euclidean'
                'cosine' → 1 - cosine similarity
    Returns:
        rdm: (n_stimuli, n_stimuli) symmetric dissimilarity matrix
    """
    distances = pdist(representations, metric=metric)
    rdm = squareform(distances)
    return rdm

def rsa_score(rdm_a, rdm_b):
    """
    Compute RSA score (Spearman correlation of upper triangles).
    
    Parameters:
        rdm_a, rdm_b: (n, n) RDMs
    Returns:
        rho: Spearman correlation coefficient
        p: p-value
    """
    n = rdm_a.shape[0]
    # Extract upper triangle (excluding diagonal)
    idx = np.triu_indices(n, k=1)
    vec_a = rdm_a[idx]
    vec_b = rdm_b[idx]
    rho, p = spearmanr(vec_a, vec_b)
    return rho, p

def permutation_test(rdm_a, rdm_b, n_permutations=10000):
    """
    Test significance of RSA score via permutation of stimulus labels.
    """
    observed_rho, _ = rsa_score(rdm_a, rdm_b)
    n = rdm_a.shape[0]
    
    null_distribution = []
    for _ in range(n_permutations):
        # Permute rows and columns of rdm_b simultaneously
        perm = np.random.permutation(n)
        rdm_b_perm = rdm_b[np.ix_(perm, perm)]
        rho_perm, _ = rsa_score(rdm_a, rdm_b_perm)
        null_distribution.append(rho_perm)
    
    p_value = np.mean(np.array(null_distribution) >= observed_rho)
    return observed_rho, p_value, null_distribution

def noise_ceiling(rdms_per_subject):
    """
    Compute noise ceiling from per-subject RDMs.
    
    Parameters:
        rdms_per_subject: list of (n, n) RDMs, one per subject
    Returns:
        lower_bound, upper_bound
    """
    rdms = np.array(rdms_per_subject)  # (n_subjects, n, n)
    group_avg = rdms.mean(axis=0)
    
    # Upper bound: each subject vs full group average (includes self)
    upper_scores = []
    for s in range(len(rdms_per_subject)):
        rho, _ = rsa_score(rdms[s], group_avg)
        upper_scores.append(rho)
    upper_bound = np.mean(upper_scores)
    
    # Lower bound: each subject vs leave-one-out group average
    lower_scores = []
    for s in range(len(rdms_per_subject)):
        loo_avg = np.delete(rdms, s, axis=0).mean(axis=0)
        rho, _ = rsa_score(rdms[s], loo_avg)
        lower_scores.append(rho)
    lower_bound = np.mean(lower_scores)
    
    return lower_bound, upper_bound

# ---- Example Usage ----

# Suppose you have:
# brain_activations: (n_stimuli, n_voxels) array of fMRI responses
# model_activations: (n_stimuli, n_features) array of layer activations

brain_rdm = compute_rdm(brain_activations, metric='correlation')
model_rdm = compute_rdm(model_activations, metric='correlation')

rho, p = rsa_score(brain_rdm, model_rdm)
print(f"RSA score: {rho:.3f}, p = {p:.4f}")

# With permutation test
rho, p_perm, null_dist = permutation_test(brain_rdm, model_rdm, n_permutations=10000)
print(f"RSA score: {rho:.3f}, permutation p = {p_perm:.4f}")

# Comparing multiple models
model_names = ['conv1', 'conv3', 'layer2', 'layer4', 'fc']
model_rdms = [compute_rdm(activations[layer]) for layer in model_names]

for name, mrdm in zip(model_names, model_rdms):
    rho, p = rsa_score(brain_rdm, mrdm)
    print(f"{name}: rho = {rho:.3f}, p = {p:.4f}")
```

---

## 13. RSA and Related Methods: The Landscape

RSA sits within a broader family of methods for comparing representations. Knowing where it fits helps you choose the right tool.

|Method|What it compares|Key property|
|---|---|---|
|RSA|RDM to RDM (second-order)|Geometry, invariant to dimensionality|
|CKA|Gram matrix to Gram matrix|Invariant to orthogonal transformations|
|Procrustes|Direct alignment of representation matrices|Finds best rotation to align spaces|
|Linear probing|Train linear classifier on representations|Measures linear decodability|
|SVCCA|Singular vectors of representations|Invariant to linear transformations|
|Mutual information|Activations to labels|Information-theoretic, model-free|

**Linear probing** and **RSA** answer different questions: linear probing asks "can we decode label $y$ from representation $r$?" RSA asks "does the geometry of $R$ match the geometry of another system's $R$?" A layer can pass one test and fail the other.

**Procrustes analysis** directly aligns two representation matrices by finding the optimal rotation. It requires the two representations to have the same dimensionality (or a common reduced dimensionality after PCA). More sensitive than RSA but less general.

**SVCCA** (Singular Vector Canonical Correlation Analysis) finds linear subspaces of two representations that are maximally correlated. More powerful than RSA for comparing two networks, but requires $n > d$ and is computationally heavier.

---

## 14. Key Takeaways

- RSA sidesteps the dimensionality mismatch problem by comparing **pairwise similarity structures** (RDMs) rather than raw representations. An $n \times n$ RDM is commensurable across all systems that process the same $n$ stimuli.
- The **RDM** captures the geometry of a representational space — which stimuli are close, which are far, and the full pattern of distances. It is invariant to rotation, reflection, and (under Spearman RSA) monotonic scaling.
- The **RSA score** is the Spearman rank correlation between the upper triangles of two RDMs. Spearman is used for scale-invariance and robustness to outlier pairs.
- RSA is most powerful for **model comparison**: compute RDMs from many competing models and theories, correlate each with the brain/target RDM, and rank models by how well they explain the representational geometry.
- The **noise ceiling** is essential — it tells you the maximum achievable RSA score given measurement noise. Always report it alongside RSA scores.
- **Searchlight RSA** in fMRI sweeps a sphere across the brain to produce a whole-brain map of where representational geometry matches a model. Requires strong multiple-comparison correction.
- **Temporal RSA** in EEG/MEG produces a time course showing when each representational structure emerges during processing.
- The stimulus set determines what can and cannot be concluded. A poorly chosen stimulus set produces uninterpretable RSA results regardless of how careful the analysis is.
- RSA ≠ linear decodability. High RSA score does not imply linear separability; low RSA score does not imply the information is absent.
- **CKA** is preferred over RSA for comparing two neural networks (large $n$, no measurement noise). RSA is preferred for brain-model comparisons (small $n$, established noise ceiling framework, robust statistics).
- RSA can be applied to checkpoints during training to track how representational geometry evolves — directly applicable to studying how data pruning, curriculum learning, or architectural choices shape the trajectory of representation learning.