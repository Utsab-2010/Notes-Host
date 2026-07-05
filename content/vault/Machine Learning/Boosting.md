---
title: "Boosting"
lastmod: 2026-06-24
---

## 1. Start Here: The Philosophy
In the Random Forests note, we saw that averaging many high-variance, low-bias models (deep trees) reduces variance. That's one way to build an ensemble.

Boosting takes the **opposite approach**.
> **Boosting = sequentially build many weak (high-bias, low-variance) models, each correcting the mistakes of the previous ones.**

Where random forests work by reducing variance through parallelism and decorrelation, boosting works by **reducing bias through sequential error correction**. Two completely different strategies to get to low total error.

The term "weak learner" has a precise definition: a model that does only slightly better than random guessing. In practice, this almost always means a **very shallow decision tree** — typically a stump (depth 1) or depth 2–5.

The question boosting answers:
> Can you combine many mediocre models, each barely better than chance, into one strong model?

The answer — proven theoretically and empirically — is yes.

---

## 2. The Core Idea: Learning From Mistakes
Before going into math, build the intuition with a story.

Imagine you're a teacher grading essays. After the first round of grading, you identify which students got questions wrong. In the next round, you focus more of your attention on those students — the ones who struggled before. After a few rounds of this focused attention, even the weakest students have improved.

This is exactly what boosting does:
1. Train a weak model on the data
2. Look at which examples the model got wrong
3. **Upweight those wrong examples** (pay more attention to them)
4. Train another weak model on the reweighted data
5. Repeat

At the end, combine all weak models with learned weights into one strong model.

Different boosting algorithms implement this idea differently. The three you need to know:
- **AdaBoost** (Adaptive Boosting) — the original, works by reweighting samples
- **Gradient Boosting** — the generalization, works by fitting residuals in function space
- **XGBoost / LightGBM / CatBoost** — highly optimized gradient boosting implementations that dominate tabular data competitions

---

## 3. AdaBoost: The Original

### Setup

- Training data: $(x_1, y_1), \ldots, (x_n, y_n)$ where $y_i \in {-1, +1}$ (binary classification)
- Weak learner: a decision stump (one-level decision tree — splits on one feature once)
- $T$ rounds of boosting

### The Algorithm

**Initialize**: Assign equal weight to every training sample: $$w_i^{(1)} = \frac{1}{n} \quad \text{for all } i$$

**For each round $t = 1, \ldots, T$:**

**Step 1**: Train a weak classifier $h_t(x)$ on the data using current weights $w^{(t)}$. The weak learner minimizes weighted classification error: $$\epsilon_t = \sum_{i : h_t(x_i) \neq y_i} w_i^{(t)}$$

**Step 2**: Compute the weight (voting power) of this weak classifier: $$\alpha_t = \frac{1}{2} \ln\left(\frac{1 - \epsilon_t}{\epsilon_t}\right)$$

**Step 3**: Update sample weights — **upweight misclassified examples, downweight correctly classified ones**: $$w_i^{(t+1)} = w_i^{(t)} \cdot \exp\left(-\alpha_t \cdot y_i \cdot h_t(x_i)\right)$$

Then normalize so weights sum to 1.

**Final prediction**: $$H(x) = \text{sign}\left(\sum_{t=1}^{T} \alpha_t \cdot h_t(x)\right)$$

A weighted vote of all weak classifiers.

### Unpacking the $\alpha_t$ Formula

$$\alpha_t = \frac{1}{2} \ln\left(\frac{1 - \epsilon_t}{\epsilon_t}\right)$$

- If $\epsilon_t = 0.5$ (random guessing): $\alpha_t = 0$ — this model gets zero vote
- If $\epsilon_t \to 0$ (perfect classifier): $\alpha_t \to \infty$ — this model gets huge vote
- If $\epsilon_t > 0.5$ (worse than random): $\alpha_t < 0$ — this model's vote is flipped

This is elegant: the algorithm automatically determines how much to trust each weak classifier based on its error rate.

### The Weight Update Intuition

$$w_i^{(t+1)} \propto w_i^{(t)} \cdot \exp\left(-\alpha_t \cdot y_i \cdot h_t(x_i)\right)$$

- Correctly classified: $y_i \cdot h_t(x_i) = +1$ → weight decreases by $e^{-\alpha_t}$ → easier examples get less focus
- Misclassified: $y_i \cdot h_t(x_i) = -1$ → weight increases by $e^{+\alpha_t}$ → harder examples get more focus

After each round, the model is forced to focus on what it got wrong.

### What AdaBoost is Minimizing

AdaBoost can be shown to minimize the **exponential loss**: $$L = \sum_{i=1}^{n} \exp\left(-y_i \cdot F(x_i)\right)$$

where $F(x) = \sum_t \alpha_t h_t(x)$ is the ensemble score. This connection to a specific loss function is what Friedman, Hastie, and Tibshirani (2000) showed — it opened the door to generalizing boosting to arbitrary differentiable loss functions.

---

## 4. Gradient Boosting: The Generalization

AdaBoost is limited to classification with exponential loss. **Gradient Boosting** (Friedman, 2001) generalizes boosting to any differentiable loss function — regression, classification, ranking, survival analysis — by reframing the problem in terms of gradients.

### The Key Reframe

In AdaBoost, we reweighted samples. In gradient boosting, we think about the problem differently:

> We're doing **gradient descent in function space** rather than parameter space.

Instead of finding parameters $\theta$ that minimize loss (parameter space gradient descent), we're building a function $F(x)$ step by step, where each step moves in the direction of the negative gradient of the loss with respect to the **function itself**.

### The Algorithm

**Initialize** with a constant prediction: $$F_0(x) = \arg\min_\gamma \sum_{i=1}^{n} L(y_i, \gamma)$$

For regression with MSE, this is just the mean of the targets: $F_0(x) = \bar{y}$.

**For each round $t = 1, \ldots, T$:**

**Step 1**: Compute **pseudo-residuals** — the negative gradient of the loss with respect to the current prediction $F_{t-1}(x_i)$:

$$r_i^{(t)} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F = F_{t-1}}$$

**Step 2**: Fit a weak learner $h_t(x)$ to predict these pseudo-residuals. The weak learner learns to approximate the gradient.

**Step 3**: Find the optimal step size: $$\gamma_t = \arg\min_\gamma \sum_{i=1}^{n} L\left(y_i, F_{t-1}(x_i) + \gamma \cdot h_t(x_i)\right)$$

**Step 4**: Update the model: $$F_t(x) = F_{t-1}(x) + \nu \cdot \gamma_t \cdot h_t(x)$$

where $\nu$ is the **learning rate** (shrinkage parameter), typically 0.01–0.3.

### The Pseudo-Residuals Are the Gradient

This is the central insight. For MSE loss $L(y, F) = \frac{1}{2}(y - F)^2$:

$$r_i = -\frac{\partial L}{\partial F} = -(F - y) = y - F$$

The pseudo-residuals are literally the residuals $y_i - F_{t-1}(x_i)$ — the errors the current model makes. Fitting a tree to the residuals is fitting a tree to the errors, then adding it to fix those errors.

For other loss functions, the pseudo-residuals are different:

- **Log-loss (binary classification)**: pseudo-residuals are $y_i - p_i$ (true label minus predicted probability) — which looks like residuals but technically they're gradient components
- **Absolute error (MAE)**: pseudo-residuals are $\text{sign}(y_i - F(x_i))$, just the direction of the error
- **Huber loss**: interpolates between MSE and MAE behavior

This is why gradient boosting generalizes: you can plug in any loss function, take its gradient, and run the same algorithm.

### Gradient Boosting as Gradient Descent

Normal gradient descent in parameter space: $$\theta \leftarrow \theta - \eta \cdot \nabla_\theta L$$

Gradient boosting in function space: $$F \leftarrow F - \nu \cdot \nabla_F L$$

The difference: normal gradient descent moves a parameter vector. Gradient boosting adds a _function_ (the weak learner) in the direction of the negative gradient. The weak learner is the gradient — it approximates the direction of steepest descent in the space of all functions.

---

## 5. Case Study: Gradient Boosting on a Regression Problem

**Setup**: Predict house prices. True relationship is roughly $y = 2x + \text{noise}$. You have 6 training points.

|$x$|True $y$|Initial prediction $F_0$|
|---|---|---|
|1|2.1|4.5 (mean)|
|2|4.2|4.5|
|3|5.9|4.5|
|4|8.1|4.5|
|5|10.0|4.5|
|6|11.8|4.5|

**Round 1**: Compute residuals $r_i = y_i - F_0(x_i)$:

|$x$|Residual|
|---|---|
|1|-2.4|
|2|-0.3|
|3|+1.4|
|4|+3.6|
|5|+5.5|
|6|+7.3|

Fit a shallow tree $h_1$ to predict these residuals. The tree learns that large $x$ → large positive residual, small $x$ → large negative residual.

Update: $F_1(x) = F_0(x) + 0.1 \cdot h_1(x)$ (with learning rate 0.1)

**Round 2**: Compute new residuals from $F_1$. These are smaller because $F_1$ already corrected some error. Fit $h_2$ to these new residuals. Update.

**Keep going**: Each round, the model gets closer to the true function by focusing on what's left unexplained. After 100 rounds, you have a very good fit.

**Key observation**: Each individual tree $h_t$ is terrible at predicting house prices — it's only predicting the _residuals_ of the current model, which are small numbers near zero. But the _sum_ of all these small corrections adds up to an accurate model.

This is what "reducing bias sequentially" means. Each step takes a small bite out of the remaining error.

---

## 6. Case Study: Why Boosting Beats a Single Deep Tree on Noisy Data

**Setup**: Binary classification. Features are 20 numeric variables, 5 are actually predictive, 15 are pure noise. Dataset has 1000 samples.

**Single deep tree**:

- Finds the 5 real features — great
- Also finds spurious patterns in the 15 noise features that happen to separate training points
- Overfits these noise patterns
- Test accuracy: 78%

**Gradient Boosting with stumps (depth 1)**:

- Round 1: A stump finds the single most predictive feature. Explains some variance.
- Round 2: A stump on the residuals finds the second most predictive feature.
- Rounds 3–5: Remaining real features are captured.
- Rounds 6+: Residuals become small and noisy. Stumps only find weak signal in them. With learning rate 0.1, each stump contributes very little. The noise features occasionally "win" a round but their contribution is tiny.
- After 100 rounds with early stopping: test accuracy 86%

**Why**: Each shallow tree has high bias (stumps can't overfit the noise features, they can only pick one split) and low variance. The boosting process selectively extracts signal across many rounds. The noise features occasionally win a round, but their cumulative contribution is dwarfed by the signal features. With early stopping (stop when validation loss stops improving), you prevent the model from overfitting.

---

## 7. The Learning Rate: The Most Important Hyperparameter

The learning rate $\nu$ (also called shrinkage) scales each tree's contribution:

$$F_t = F_{t-1} + \nu \cdot h_t$$

### Why Not $\nu = 1$?

With $\nu = 1$, each tree tries to fully correct the current residuals in one step. This is like taking enormous gradient descent steps — you overshoot, and the model overfits quickly.

With small $\nu$, each tree makes a tiny correction. You need many more trees, but:

- Each correction is conservative → less risk of overfitting
- More rounds means more chances to correct different aspects of the error
- The regularization effect is stronger

### The Learning Rate vs. Number of Trees Tradeoff

These two are coupled:

- Small $\nu$ → need more trees to achieve the same training loss reduction
- Large $\nu$ → fewer trees needed but worse generalization

**Empirical rule**: Smaller learning rate almost always gives better generalization, at the cost of needing more trees. The combination ($\nu = 0.01$, $T = 1000$) typically outperforms ($\nu = 0.1$, $T = 100$), even though both reduce training loss to the same point.

In practice:

- Set $\nu$ small (0.01–0.1)
- Set $T$ large (500–5000)
- Use early stopping to find the optimal $T$ automatically

---

## 8. XGBoost, LightGBM, CatBoost: The Modern Implementations

Friedman's original gradient boosting is elegant but slow. The modern implementations add critical engineering and algorithmic improvements.

### XGBoost (Chen & Guestrin, 2016)

**Second-order gradients**: Instead of just the gradient (first derivative), XGBoost uses both gradient $g_i$ and Hessian $h_i$ (second derivative) of the loss. This gives a better-quality approximation of the loss surface and allows for more principled regularization.

The tree split score in XGBoost is: $$\text{Gain} = \frac{1}{2}\left[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right] - \gamma$$

where $G, H$ are gradient/Hessian sums in left/right nodes, $\lambda$ regularizes leaf weights, and $\gamma$ regularizes tree complexity.

**Key additions over vanilla gradient boosting**:

- L1 and L2 regularization on leaf weights built into the objective
- Column (feature) subsampling — like random forests, random features per tree
- Row subsampling — random samples per tree
- Sparsity-aware split finding — handles missing values and sparse features natively
- Parallelization of the split-finding step

### LightGBM (Microsoft, 2017)

The key innovation: **Gradient-based One-Side Sampling (GOSS)** and **Exclusive Feature Bundling (EFB)**.

**GOSS**: Instead of using all training samples, keep samples with large gradients (they're harder, contribute more information) and randomly sample from the small-gradient instances. This dramatically reduces the number of samples used per iteration while retaining the most informative ones.

**EFB**: Sparse features often can't be nonzero simultaneously (mutually exclusive). Bundle such features together into a single feature, reducing effective feature count. This massively speeds up training on wide datasets.

**Leaf-wise tree growth** (vs. level-wise in XGBoost): LightGBM grows the leaf with the highest loss reduction at each step, rather than growing all leaves at the same depth level. This finds better trees faster but can overfit more — requires `max_depth` or `num_leaves` to control.

Result: LightGBM is **dramatically faster** than XGBoost on large datasets — often 10–20× with similar or better accuracy.

### CatBoost (Yandex, 2017)

Key innovation: **handling categorical features** natively without target encoding leakage.

Standard target encoding: replace category $c$ with $P(y | x = c)$ estimated from training data. The problem: this leaks target information, causing overfitting.

CatBoost uses **ordered target statistics** — for sample $i$, only use samples from a random permutation that appeared _before_ $i$ to compute target statistics. This prevents leakage while still providing useful categorical encodings.

Also introduces **ordered boosting** — a variant that computes gradients on a different subset of data than the one used to fit the tree, reducing overfitting.

### When to Use Which

||XGBoost|LightGBM|CatBoost|
|---|---|---|---|
|Many rows (>1M)|Slow|Fast|Medium|
|Many columns (>1000)|OK|Fast (EFB)|OK|
|Categorical features|Manual encoding|Manual encoding|Native|
|GPU support|Yes|Yes|Yes|
|Interpretability|Similar|Similar|Similar|
|Default behavior|Robust|Needs tuning|Robust|

**Practical starting point**: LightGBM for speed, CatBoost when you have lots of categoricals and want to avoid encoding headaches, XGBoost when you need maximum community support and documentation.

---

## 9. Key Hyperparameters (and What They Actually Control)

### Number of Trees / Estimators (`n_estimators`)

Unlike random forests (where more is always better), too many trees in boosting can overfit. The optimal number is found via early stopping.

### Learning Rate (`learning_rate`, `eta`)

Scales each tree's contribution. Lower = better generalization but needs more trees. Most important hyperparameter to get right. Don't tune trees and learning rate independently — they interact.

### Max Depth / Num Leaves

Controls how complex each individual tree is. Deeper trees capture more complex interactions but add variance:

- **Stumps (depth 1)**: Pure AdaBoost style, no feature interactions
- **Depth 3–6**: Standard for gradient boosting — captures pairwise and triple interactions
- **Depth > 8**: Usually overfits, rarely needed

In LightGBM, you tune `num_leaves` instead of `max_depth`. A depth-6 tree has at most 64 leaves.

### Subsampling (`subsample`, `bagging_fraction`)

Fraction of training samples used per tree. Introduces randomness (like random forests). Typically 0.6–0.9. Below 0.5 usually hurts.

### Column Subsampling (`colsample_bytree`, `feature_fraction`)

Fraction of features considered per tree. Same role as `max_features` in random forests. Decorrelates trees and reduces overfitting.

### Min Child Weight / Min Data in Leaf

Minimum sum of instance weights (or number of samples) in a leaf. Prevents the model from creating leaves based on very few samples. Important regularizer — increase when overfitting.

### Regularization Terms (`reg_alpha` L1, `reg_lambda` L2)

Penalize large leaf weights. L1 promotes sparsity in leaf values; L2 is the default. Usually modest values work (0.1–10). More important on noisy data.

---

## 10. Early Stopping: The Critical Technique

Without early stopping, boosting will eventually overfit — it keeps adding trees until it memorizes training data.

Early stopping: maintain a validation set. After each round, evaluate on validation data. Stop training when validation loss hasn't improved for $k$ consecutive rounds (patience).

```python
# XGBoost
model = xgb.XGBClassifier(n_estimators=5000, learning_rate=0.05)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=50,  # stop if no improvement for 50 rounds
    verbose=100
)
# model.best_iteration gives the optimal number of trees

# LightGBM
model = lgb.LGBMClassifier(n_estimators=5000, learning_rate=0.05)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    callbacks=[lgb.early_stopping(stopping_rounds=50)]
)
```

**Nuance**: Early stopping with a validation set means your final model uses fewer than `n_estimators` trees. Set `n_estimators` large (5000+), set learning rate small (0.01–0.1), and let early stopping find the right number of trees. Don't try to hand-tune the number of trees.

---

## 11. Bias-Variance Perspective on Boosting

Recall from the bias-variance note:

- **Boosting reduces bias** by sequential error correction (each tree corrects residuals of the previous)
- **Individual trees are shallow** → low variance per tree, high bias per tree
- **The ensemble** has low bias (residuals are corrected over many rounds) and manageable variance (each tree is shallow, each contributes little individually)

The learning rate controls the bias-variance tradeoff:

- Large $\nu$: each tree corrects a lot → fast bias reduction, but high variance risk
- Small $\nu$: each tree corrects a little → slow bias reduction, lower variance → need more trees

Subsampling adds randomness that further reduces variance (same mechanism as random forests), making boosting a hybrid that exploits both bias reduction (sequential residual fitting) and variance reduction (subsampling, column sampling).

---

## 12. Boosting vs Random Forests: The Real Comparison

|Property|Boosting|Random Forest|
|---|---|---|
|Primary mechanism|Bias reduction|Variance reduction|
|Tree depth|Shallow (depth 3–6)|Deep (max depth)|
|Tree training|Sequential|Parallel|
|Sensitive to noise/outliers|More sensitive|Less sensitive|
|Hyperparameter tuning|Essential|Robust to defaults|
|Training speed|Slower (sequential)|Faster (parallel)|
|Performance ceiling|Higher (usually)|Slightly lower|
|Risk of overfitting|Real — need early stopping|Low|
|Interpretability|Similar (SHAP available)|Similar (SHAP available)|

**When to use what**:

- You have time to tune and want maximum performance → Gradient Boosting (LightGBM/XGBoost)
- You want a strong, robust baseline with minimal tuning → Random Forest
- Data has lots of outliers or noisy labels → Random Forest (more robust)
- Data is clean, large, and tabular → Gradient Boosting

**The honest answer**: On clean tabular data, gradient boosting almost always wins. But the margin is often small and the tuning cost is real. For prototyping or when you need reliable defaults, start with random forest.

---

## 13. Feature Importance in Boosting

Boosting models provide the same two types of feature importance as random forests:

### Gain-Based Importance

Sum of the loss reduction achieved by splits on each feature across all trees. More informative than the count-based "split importance" because it weights by how useful each split actually was.

### Permutation Importance

Same as in random forests: permute feature, measure drop in performance.

### SHAP Values (The Right Way)

SHAP (SHapley Additive exPlanations) values give each feature a contribution to each individual prediction, not just a global importance score. This is both:

- More theoretically sound (rooted in cooperative game theory)
- More useful (tells you why the model made _this specific prediction_)

XGBoost and LightGBM have native SHAP support:

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Global importance
shap.summary_plot(shap_values, X_test)

# Individual prediction explanation
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

SHAP values are additive: $\hat{y} = \text{base value} + \sum_j \phi_j$ where $\phi_j$ is feature $j$'s SHAP contribution to this prediction.

---

## 14. What Boosting Can't Do

- **Extrapolate**: Same limitation as random forests — predictions are bounded by training target range. Tree-based models cannot predict values outside $[\min(y_{\text{train}}), \max(y_{\text{train}})]$ in regression.
- **Handle raw images/audio/text**: Needs engineered features; can't learn hierarchical representations
- **Sequential/temporal structure**: No native recurrence or attention — time series require careful feature engineering
- **Parallel training**: Sequential by nature — each tree needs the previous tree's residuals. Cannot trivially parallelize across trees (though the split-finding _within_ each tree can be parallelized)
- **Very noisy labels**: More sensitive to noise than random forests because it deliberately focuses on hard examples, which may just be noisy ones

---

## 15. Key Takeaways

- Boosting = sequentially train shallow weak learners, each correcting the mistakes of the previous ones. Primary mechanism: **bias reduction**.
- AdaBoost reweights training examples — misclassified examples get upweighted so the next model focuses on them. Each classifier gets a vote weighted by its accuracy.
- Gradient Boosting generalizes this to any loss function by casting boosting as **gradient descent in function space**. Each tree fits the pseudo-residuals (negative gradient of the loss).
- For MSE, pseudo-residuals are just regular residuals $y_i - F_{t-1}(x_i)$. For other losses, they're the gradient — same algorithm, different "errors" to fit.
- Learning rate is the most important hyperparameter. Small learning rate + many trees + early stopping is the standard recipe.
- XGBoost adds second-order gradients and regularization. LightGBM adds GOSS and EFB for speed. CatBoost handles categoricals natively without leakage.
- Subsampling (of rows and columns) introduces variance-reducing randomness, making gradient boosting a hybrid of bias reduction and variance reduction.
- Always use early stopping — without it, boosting will overfit.
- SHAP values are the right way to interpret boosting models — they give per-prediction, per-feature contributions grounded in game theory.
- Boosting typically outperforms random forests on clean tabular data, but requires more tuning and is more sensitive to noise.