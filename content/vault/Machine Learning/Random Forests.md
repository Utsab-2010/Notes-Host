---
title: "Random Forests"
lastmod: 2026-06-24
---

## 1. The Core Idea: From One Tree to Many

A single decision tree has a well-known problem: it overfits. Given enough depth, a decision tree will memorize the training data perfectly — zero training error, poor generalization. The tree is high variance: small changes in the training data produce very different trees.

The fix isn't to make one better tree. It's to make many trees and average them.
> **Random Forest = Bagging + Random Feature Subsampling, applied to decision trees.**

Two independent mechanisms work together to reduce variance:
1. **Bagging** (Bootstrap Aggregation): *train each tree on a different bootstrap sample of the data*
2. **Random feature subsampling**: at each split, only consider a random subset of features

*Both mechanisms serve the same goal: make the trees as **uncorrelated** as possible.* Uncorrelated errors cancel when averaged; correlated errors compound.

---
## 2. Bagging: Bootstrap Aggregation

### What is Bootstrapping?

Given a dataset of $n$ samples, a bootstrap sample is created by sampling $n$ instances **with replacement**. On average:
- Each bootstrap sample contains about **63.2%** of the unique original samples
- The remaining **36.8%** are never selected — these are called **out-of-bag (OOB)** samples

Why 63.2%? The probability that a specific sample is _not_ selected in a single draw is $1 - 1/n$. Over $n$ draws:
$$\lim_{n \to \infty} \left(1 - \frac{1}{n}\right)^n = e^{-1} \approx 0.368$$
So about 36.8% of samples are excluded from each bootstrap sample, giving 63.2% unique inclusion.

### Training with Bagging
For $B$ trees:
1. Draw bootstrap sample $D_b$ from training data $D$
2. Train a full decision tree $T_b$ on $D_b$ (usually grown to maximum depth — no pruning)
3. Repeat for $b = 1, \ldots, B$

### Prediction with Bagging
- **Classification**: majority vote across all $B$ trees
- **Regression**: average prediction across all $B$ trees
$$\hat{y} = \frac{1}{B} \sum_{b=1}^{B} T_b(x) \quad \text{(regression)}$$
$$\hat{y} = \text{mode}{T_1(x), T_2(x), \ldots, T_B(x)} \quad \text{(classification)}$$
### Why Does Averaging Reduce Variance?
If $B$ trees each have variance $\sigma^2$ and are **independent**, the variance of their average is $\sigma^2 / B$ — variance shrinks linearly with the number of trees.

But trees trained on bootstrap samples from the same dataset are not independent — they're correlated (they share data and structure). If the pairwise correlation between trees is $\rho$, the variance of the averaged prediction is:
$$\text{Var}(\bar{T}) = \rho \sigma^2 + \frac{1-\rho}{B} \sigma^2$$

As $B \to \infty$, the second term vanishes. *The irreducible floor is $\rho \sigma^2$.

>**Key insight**: To reduce ensemble variance, you need to reduce $\rho$ — the inter-tree correlation. Bagging alone reduces correlation somewhat (different data subsets). Random feature subsampling reduces it further. This is the mathematical justification for why Random Forests are better than plain bagging.

---
## 3. Random Feature Subsampling: The Key Innovation

Plain bagging of decision trees still produces correlated trees. Why? *If one feature is very strong (highly predictive), almost every tree will split on it near the root. The trees end up looking similar regardless of which bootstrap sample they were trained on.*

Breiman's solution (introduced in the original Random Forests paper, 2001): **at each node, when choosing a split, only consider a random subset of $m$ features** out of the total $p$ features.

$$m \ll p$$

Standard choices:
- **Classification**: $m = \lfloor \sqrt{p} \rfloor$
- **Regression**: $m = \lfloor p/3 \rfloor$

These are *heuristics, not theoretically derived* — they work well empirically and $m$ is a hyperparameter to tune.

### Effect: Forced Decorrelation
If the dominant feature is excluded from a given node's candidate set, other features get a chance to split. Over many trees, many different features end up being used, producing structurally diverse trees.

This diversity = lower $\rho$ = lower ensemble variance = better generalization.

>**Nuance**: The optimal $m$ is task-dependent. When features are mostly irrelevant, larger $m$ is better (you need to see enough features to find the good ones). When many features are predictive, smaller $m$ forces more diversity. Always treat $m$ as a hyperparameter.

---
## 4. Out-of-Bag (OOB) Error: Free Cross-Validation

Since each tree is trained on ~63.2% of the data, the remaining ~36.8% (OOB samples) were never seen by that tree. You can evaluate each tree on its OOB samples — effectively getting a validation estimate without holding out a separate validation set.

### OOB Error Estimation
For each sample $i$:
- Collect predictions from all trees $T_b$ for which sample $i$ was **not** in the bootstrap sample $D_b$
- Aggregate these predictions (vote or average)
- Compare to the true label $y_i$

Average this over all samples → *OOB error estimate*. 

- **Why OOB error is reliable**: Each sample is evaluated by ~36.8% of the total trees (the ones that didn't train on it). With $B = 500$ trees, that's ~180 trees per sample — a stable estimate.
- **Practical implication**: With random forests, you often don't need a separate validation set for model selection. OOB error gives a nearly unbiased estimate of generalization error. This is especially useful on small datasets.

>**Nuance**: OOB error is not identical to cross-validation. It tends to be slightly pessimistic because each OOB predictor uses fewer trees than the full forest. But it's close enough and orders of magnitude cheaper.

---
## 5. Feature Importance

Random forests provide a natural measure of feature importance. Two main types:

### Mean Decrease in Impurity (MDI) / Gini Importance

For each feature $j$, sum up the total impurity decrease it caused across all splits in all trees, weighted by the number of samples passing through that node:

$$\text{Importance}(j) = \frac{1}{B} \sum_{b=1}^{B} \sum_{\substack{t \in T_b \ \text{split on } j}} n_t \cdot \Delta \text{impurity}(t)$$

where $n_t$ is the number of samples at node $t$ and $\Delta \text{impurity}(t)$ is the impurity reduction at that split.

**Pros**: Computed for free during training, fast.

**Cons — critical**: MDI is **biased toward high-cardinality features**. A feature with many unique values (e.g., a continuous variable, or an ID) will appear to be more important than a binary feature even if both have the same predictive power. This is because high-cardinality features have more possible split points, giving them more opportunities to reduce impurity by chance. Never trust MDI importance blindly for features with very different cardinalities.

### Mean Decrease in Accuracy (MDA) / Permutation Importance

1. Evaluate the forest on OOB samples → get baseline OOB accuracy
2. For feature $j$: randomly permute the values of feature $j$ in the OOB samples (break its relationship with the target)
3. Re-evaluate the forest on the permuted OOB samples → get degraded accuracy
4. Importance of feature $j$ = drop in accuracy

$$\text{Importance}(j) = \text{Accuracy}_{\text{baseline}} - \text{Accuracy}_{\text{permuted } j}$$

Average over all trees and OOB sets.

**Pros**: Unbiased, doesn't favor high-cardinality features, model-agnostic in principle.

**Cons**: Slower (requires re-evaluation for each feature), can underestimate importance when features are correlated (permuting one correlated feature doesn't destroy all the information since the model can still access it through the correlated feature).

### Which to Use?

For correlated features: neither is perfect. MDA underestimates importance of correlated features; MDI is biased. For truly independent features, MDA (permutation importance) is more trustworthy.

---

## 6. Hyperparameters

### Number of Trees ($B$ / `n_estimators`)

More trees = better, always (or at worst, the same). The ensemble variance strictly decreases or stays flat as you add trees. Unlike neural networks, you cannot overfit by having too many trees.

**But**: returns are diminishing. Going from 10 to 100 trees gives a huge improvement. Going from 500 to 1000 gives marginal improvement. In practice, 100–500 trees covers most use cases. Monitor OOB error as you increase $B$ — stop when it plateaus.

### Max Features ($m$ / `max_features`)

The number of features considered at each split. Most important hyperparameter to tune.

- `"sqrt"`: $\lfloor \sqrt{p} \rfloor$ — default for classification in sklearn
- `"log2"`: $\lfloor \log_2 p \rfloor$ — aggressive decorrelation
- `None` or `p`: all features — degenerates to plain bagging, no extra decorrelation
- Any integer or float: explicit count or fraction

Smaller $m$ → more decorrelation → lower variance but higher bias per tree. There's a sweet spot.

### Max Depth (`max_depth`)

Default for random forests: **None** (grow trees fully until all leaves are pure or have fewer than `min_samples_split` samples). Unlike single decision trees, you usually don't prune trees in a random forest — deep trees have high variance individually, but the ensemble averages it out.

Restricting depth acts as a form of regularization but at the cost of bias. Useful if you're memory-constrained or trees are becoming very slow to train.

### Min Samples Split / Min Samples Leaf

`min_samples_split`: minimum number of samples required to split a node (default: 2)  
`min_samples_leaf`: minimum number of samples required to be at a leaf (default: 1)

Increasing these regularizes the trees (smaller, simpler trees), which increases bias and reduces variance. Useful for noisy datasets or when you want faster inference.

### Max Samples (`max_samples`)

By default, each bootstrap sample has size $n$ (same as training set). You can set `max_samples` < $n$ for smaller bootstrap samples — more diversity but higher bias per tree. Useful for very large datasets where training time is a bottleneck.

---

## 7. Bias-Variance Tradeoff in Random Forests

Since individual trees are grown to full depth:
- Each tree has **low bias, high variance**
- Averaging reduces variance without increasing bias
$$\text{Bias}^2(\text{forest}) \approx \text{Bias}^2(\text{single tree})$$ $$\text{Variance}(\text{forest}) \approx \rho \cdot \text{Variance}(\text{single tree})$$
where $\rho$ is the average pairwise correlation between trees.

Random forests directly minimize $\rho$ through feature subsampling. The ensemble bias stays roughly the same as a single tree's bias *(deep, fully grown trees have low bias*). The variance reduction is the primary gain.

**Contrast with boosting** (e.g., gradient boosting): Boosting reduces bias by building shallow trees sequentially, each correcting the residual errors of the previous. Boosting trades variance reduction for bias reduction. Random forests do the opposite — they work by reducing variance while keeping bias low.

---
## 8. Extremely Randomized Trees (Extra-Trees)

A variant of random forests with an additional layer of randomization:
- Instead of finding the **optimal** split threshold for each candidate feature, **randomly sample** the split threshold
- Pick the feature + threshold pair that gives the best impurity reduction

Effect: even faster training (no need to search over thresholds), even more decorrelation between trees. Sometimes slightly worse accuracy than standard random forests, sometimes slightly better — dataset-dependent.

In sklearn: `ExtraTreesClassifier`, `ExtraTreesRegressor`.

The name "Extremely Randomized" comes from the double randomization: random feature subset + random split threshold.

---

## 9. What Random Forests Can and Cannot Do

### What They're Good At
- **Tabular data**: Random forests are one of the strongest baselines on structured/tabular data, often competitive with gradient boosting
- **High-dimensional data**: Handle many features well, especially with feature subsampling
- **Mixed feature types**: Handle continuous, ordinal, and (with encoding) categorical features
- **Robust to outliers**: Splitting decisions are based on rank/order of values, not magnitudes
- **Robust to irrelevant features**: Random subsampling means irrelevant features don't dominate
- **No feature scaling needed**: Tree-based splits are invariant to monotonic transformations of features (standardization, normalization don't matter)
- **Implicit feature selection**: Low-importance features naturally get split on less
- **Parallelizable**: Each tree is independent — trivially parallelizable across cores (`n_jobs=-1` in sklearn)
- **Built-in uncertainty estimate**: Variance of tree predictions gives a rough uncertainty estimate

### What They're Bad At
- **Extrapolation**: *Random forests cannot predict outside the range of training target values.* For regression, the prediction is always a weighted average of training targets. If test data has targets outside the training range, performance degrades badly. (Gradient boosting has the same problem; neural networks can extrapolate better but still struggle.)
- **Very high-dimensional sparse data**: NLP bag-of-words with 100k features — most splits will be on zeros. Linear models or sparse methods often work better here.
- **Sequential/temporal data**: No natural handling of time-ordered dependencies (unlike RNNs or Transformers)
- **Image/audio/text (raw)**: Need engineered features; can't learn hierarchical representations from raw data
- **Very large datasets**: Training time scales roughly as $O(B \cdot n \log n \cdot m)$ — can be slow for $n > 10^6$. Gradient boosted trees (with histogram methods) are faster at scale.
- **Memory**: Storing $B$ full trees can use significant memory. A forest of 500 deep trees on a large dataset can be gigabytes.

---

## 10. Random Forests vs Gradient Boosting

This comparison comes up constantly. Here's the honest picture:

|Property|Random Forest|Gradient Boosting (XGBoost, LightGBM)|
|---|---|---|
|Training|Parallel (trees independent)|Sequential (each tree uses previous)|
|Speed|Faster to train|Slower, but modern implementations are fast|
|Hyperparameter sensitivity|Low — robust defaults|High — learning rate, depth, subsampling all interact|
|Variance reduction|Primary mechanism|Secondary to bias reduction|
|Bias reduction|Limited (trees are deep)|Primary mechanism (trees are shallow)|
|Overfitting risk|Low — hard to overfit|Moderate — need early stopping|
|Performance on tabular data|Strong|Usually slightly better|
|Extrapolation|Poor|Poor (same issue)|
|Best use case|Quick strong baseline, interpretability, robust defaults|Maximum predictive performance on tabular data|

**Practical advice**: Start with a random forest. If you need more performance, switch to LightGBM or XGBoost with careful tuning. The random forest will rarely be far behind, and it requires almost no tuning.

---

## 11. Proximity Matrix and Other Outputs

A lesser-known capability: the proximity matrix.

For all pairs of training samples $(i, j)$, count the fraction of trees in which samples $i$ and $j$ end up in the **same leaf node**. This gives a pairwise similarity measure:

$$\text{Proximity}(i, j) = \frac{\text{ \#trees where } i \text{ and } j \text{ share a leaf}}{B}$$

**Uses**:

- Clustering: run hierarchical clustering or MDS on the proximity matrix to visualize the data structure
- Outlier detection: samples with low average proximity to all other samples are anomalies
- Missing value imputation: iteratively impute missing values using proximity-weighted averages

This is unique to random forests (and ensemble tree methods) — it's a data-adaptive similarity measure that captures complex, nonlinear relationships.

---

## 12. Handling Imbalanced Classes

Random forests, like most classifiers, tend to favor the majority class when classes are imbalanced. Several strategies:

### Class Weights (`class_weight`)

Weight each sample's contribution to impurity calculations inversely proportional to its class frequency. Common setting: `class_weight='balanced'` in sklearn, which sets weight of class $k$ to $n / (n_k \cdot K)$.

### Balanced Bootstrap Sampling

Instead of pure bootstrap sampling, sample each bootstrap sample to be class-balanced (e.g., equal numbers of each class). sklearn's `BalancedRandomForestClassifier` from `imbalanced-learn` does this.

### Threshold Adjustment

Random forests output class probabilities (fraction of trees voting for each class). Instead of defaulting to threshold 0.5 for binary classification, adjust the threshold based on the desired precision-recall tradeoff.

---

## 13. Random Forests for Unsupervised Learning

You can use random forests even without labels, through a trick:

1. Create a synthetic dataset by randomly shuffling each feature column in the original data (destroying all real structure, creating "fake" samples)
2. Label real samples as class 1, synthetic samples as class 0
3. Train a random forest to classify real vs synthetic
4. The proximity matrix from this forest captures the structure of the real data

This is called **Unsupervised Random Forests** or **Random Forest Kernel** and can be used for clustering, anomaly detection, and dimensionality reduction. The intuition: if the model can distinguish real from fake, it has learned what patterns make the real data real — and the proximity matrix encodes this.

---

## 14. Implementation: sklearn

```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import permutation_importance

# Classification
rf = RandomForestClassifier(
    n_estimators=200,       # number of trees
    max_features='sqrt',    # features per split: sqrt(p) for classification
    max_depth=None,         # grow full trees
    min_samples_leaf=1,
    bootstrap=True,
    oob_score=True,         # compute OOB error
    n_jobs=-1,              # use all cores
    random_state=42
)
rf.fit(X_train, y_train)

print(rf.oob_score_)        # OOB accuracy — free validation metric

# MDI feature importance
mdi_importances = rf.feature_importances_   # shape: (n_features,)

# Permutation importance (more reliable)
result = permutation_importance(rf, X_val, y_val, n_repeats=10, random_state=42)
mda_importances = result.importances_mean

# Probability estimates
proba = rf.predict_proba(X_test)  # shape: (n_samples, n_classes)
```

### Accessing Individual Trees

```python
# Access individual trees
tree = rf.estimators_[0]   # first tree — a DecisionTreeClassifier

# OOB indices for each tree
rf.estimators_samples_[0]  # indices of samples used in bootstrap for tree 0
```

---

## 15. Key Takeaways

- Random Forests = Bagging (bootstrap samples) + Random Feature Subsampling. Both mechanisms decorrelate trees; decorrelated errors cancel when averaged.
- Averaging $B$ trees reduces variance by a factor of roughly $1/B$ if trees are independent. Correlation $\rho$ between trees sets an irreducible floor: $\text{Var} \geq \rho \sigma^2$.
- Feature subsampling is the key innovation over plain bagging — it forces decorrelation even when one feature dominates.
- Each tree uses ~63.2% of the data; the other ~36.8% (OOB) gives a free, nearly unbiased estimate of generalization error.
- You cannot overfit by adding more trees. More trees = more stable, never worse.
- MDI (Gini) importance is biased toward high-cardinality features. Permutation importance (MDA) is more reliable but slower.
- Standard choices: $m = \sqrt{p}$ for classification, $m = p/3$ for regression. Treat as hyperparameter.
- Random forests cannot extrapolate — predictions are bounded by the range of training targets.
- No feature scaling needed — tree splits are invariant to monotonic transformations.
- Random forests are an excellent, robust baseline for tabular data. Gradient boosting usually wins on raw performance but needs more tuning.
- The proximity matrix is a powerful, underused feature of random forests for clustering, anomaly detection, and imputation.