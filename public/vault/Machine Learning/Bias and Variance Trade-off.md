---
title: "Bias and Variance Trade-off"
lastmod: 2026-06-24
---

## 1. Start Here: The Core Question
Every time you train a model, you're trying to answer one question:

> **Why is my model making mistakes, and what kind of mistakes are they?**

The bias-variance framework is a precise way to decompose the sources of error. It tells you _why_ your model is wrong, which tells you _what to do about it_.

There are only three fundamental sources of error in any model:

1. **Bias** — the model is systematically wrong (wrong on average)
2. **Variance** — the model is inconsistent (sensitive to which data it saw)
3. **Irreducible noise** — randomness in the data itself that no model can capture

Understanding which of these is hurting you determines everything: whether to get more data, make your model bigger, add regularization, or accept the limitation.

---

## 2. A Concrete Setup: What We're Decomposing

Suppose the true relationship between input $x$ and output $y$ is:

$$y = f(x) + \epsilon$$

where $f(x)$ is the true (unknown) function and $\epsilon$ is noise with mean 0 and variance $\sigma^2_\epsilon$.

You train a model $\hat{f}(x)$ on a dataset $D$ sampled from this distribution. The expected squared error of your model at a point $x$ is:

$$\mathbb{E}_D\left[(y - \hat{f}(x))^2\right] = \underbrace{\left(\mathbb{E}_D[\hat{f}(x)] - f(x)\right)^2}_{\text{Bias}^2} + \underbrace{\mathbb{E}_D\left[\left(\hat{f}(x) - \mathbb{E}_D[\hat{f}(x)]\right)^2\right]}_{\text{Variance}} + \underbrace{\sigma^2_\epsilon}_{\text{Irreducible noise}}$$

The expectation $\mathbb{E}_D$ is over all possible training datasets you could have drawn. This is important — bias and variance are defined across many possible training runs, not a single one.

Let's unpack each term.

---

## 3. Bias: Being Systematically Wrong
**Bias** measures how far your model's average prediction is from the truth.

$$\text{Bias} = \mathbb{E}_D[\hat{f}(x)] - f(x)$$

Imagine training your model 1000 times on 1000 different datasets drawn from the same distribution. What is the average prediction your model makes at a given point $x$? If that average is far from the true value $f(x)$, you have high bias.

High bias means the model is **systematically wrong** — not just noisy, but consistently off in the same direction, no matter how much data you give it.
### The Root Cause of High Bias
High bias almost always comes from **the model being too simple to capture the true structure** of the data.
- A linear model trying to fit a quadratic relationship: it will always underfit, no matter how many samples you give it
- A shallow decision tree trying to learn a complex boundary
- A small neural network trying to model a highly nonlinear function

The model's hypothesis class — the set of functions it can possibly represent — doesn't include the true function. This is called **model misspecification**.

### Important Nuance: Bias is Not About One Training Run
A common misconception: "my model has high bias because it got the training examples wrong." No. Bias is about the _average behavior_ of the model across many training sets. A model can have high bias even if it perfectly fits one particular training set — if it does so by memorizing rather than generalizing.

---

## 4. Variance: Being Inconsistently Right
**Variance** measures how much your model's predictions change depending on which training data it happened to see.
$$\text{Variance} = \mathbb{E}_D\left[\left(\hat{f}(x) - \mathbb{E}_D[\hat{f}(x)]\right)^2\right]$$

Again imagine 1000 training runs. High variance means the predictions scatter widely around their average — each training set produced a very different model. The model is **sensitive to the particular sample of data it was trained on**.

### The Root Cause of High Variance
High variance almost always comes from **the model being too complex relative to the amount of data**.
- A very deep decision tree that carves out tiny regions of feature space
- A high-degree polynomial that wiggles through every training point
- A large neural network trained on very little data

The model has enough capacity to memorize the training data, including all the noise in it. Change the training set slightly and you get a very different model.

---
## 5. The Tradeoff: Why You Can't Win Both

Simplicity → Low variance, High bias  
Complexity → Low bias, High variance

This is the tradeoff. As you increase model complexity:

- Bias decreases: the model can represent more functions, getting closer to the true one
- Variance increases: the model is more sensitive to training data fluctuations

The **optimal** model sits at the sweet spot where total error $= \text{Bias}^2 + \text{Variance} + \text{Noise}$ is minimized.

```
Error
  |
  |  \          /  ← Total error (U-shaped)
  |   \        /
  |    \      /   ← Variance (increases with complexity)
  |     \    /
  |      \  /
  |       \/  ← Sweet spot
  |      / \______________  ← Bias² (decreases with complexity)
  |_________________________
            Model Complexity →
```

The noise floor $\sigma^2_\epsilon$ is always present regardless of complexity — no model, no matter how perfect, can do better than this.

---

## 6. Overfitting and Underfitting: The Practical Language
Here's where terminology gets confusing. People use "overfitting" and "underfitting" colloquially, and it often obscures what's actually happening.

### Underfitting ↔ High Bias
Your model is too simple. It performs badly on **both training and test data**. The model hasn't captured the actual signal in the data.

Diagnostic:
- High training error
- High test error
- Training error ≈ test error (the gap is small, both are bad)

### Overfitting ↔ High Variance
Your model is too complex. It performs well on training data but badly on test data. It has learned the noise in the training set as if it were signal.

Diagnostic:
- Low training error
- High test error
- Large gap between training and test error

### The Confusing Part: Overfitting ≠ Zero Training Error
A model can overfit without achieving zero training loss. Any time there's a large gap between training and test performance, variance is the likely culprit — even if training accuracy is only 85%, not 100%.

Similarly, "underfitting" doesn't mean the model is bad in absolute terms — it means the model is **capacity-limited** relative to the problem. A linear model on MNIST might hit 90% accuracy but still underfit, because a CNN can hit 99.5%.

### The Sneaky Third Case: Fitting the Wrong Thing
A model can have low training error and low test error but still be wrong — if the test distribution is the same as training but the true function is different from what's being measured. This is a **data problem**, not a bias-variance problem. No decomposition framework saves you from measuring the wrong thing.

---

## 7. Case Study 1: Polynomial Regression
This is the cleanest illustration.
**Setup**: True function is $f(x) = \sin(2\pi x)$, with Gaussian noise $\epsilon \sim \mathcal{N}(0, 0.1)$. You have 15 training points and fit polynomials of degree 1, 4, and 14.

### Degree 1 (Linear): High Bias, Low Variance

The model: $\hat{f}(x) = w_0 + w_1 x$
- Cannot capture the sine wave — it's a straight line
- Train 1000 times on different 15-point samples: the lines are all roughly the same (low variance), but they're all wrong (high bias)
- High training error, high test error, small gap

The model isn't sensitive to which 15 points you saw — any 15 points give you roughly the same slope. But the slope is a poor approximation of a sine wave.

### Degree 4: Low Bias, Low Variance (Sweet Spot)
The model can represent smooth curves. With 15 points:
- It captures the rough shape of the sine wave
- Different training sets give somewhat different but all reasonable curves
- Low training error, low test error, small gap

### Degree 14: Low Bias, High Variance (Overfit)
The model can pass exactly through all 15 training points (15 parameters, 15 points).
- Each training set gives a _wildly_ different polynomial — huge swings between data points
- Training error near zero, test error catastrophically high
- The model has memorized noise as signal

**The key insight**: The degree-14 polynomial has zero training error on any given dataset, but if you average its predictions over 1000 training sets, the average prediction is still roughly the right shape (low bias!). The problem is the enormous variance — each individual fit is terrible on new data.

This is why **bias and variance are population-level concepts**, not single-run concepts.

---
## 8. Case Study 2: k-Nearest Neighbors
kNN is perfect for building intuition because the bias-variance behavior is unusually transparent.

**Prediction**: For a new point $x$, find the $k$ nearest training points and average their labels.
### k = 1: Lowest Bias, Highest Variance
With $k=1$, the prediction at $x$ is exactly the label of its single nearest training neighbor. This means:
- Training error is exactly **zero** (each point is its own nearest neighbor)
- The decision boundary is extremely jagged and irregular
- Change one training point and the boundary can change dramatically near that point
- On test data: high error from high variance

### k = n (All Points): Highest Bias, Lowest Variance
With $k = n$, the prediction for every point is the mean of all training labels — a constant.
- The model ignores $x$ entirely
- Variance is zero (same prediction always, regardless of training set)
- Bias is the difference between the global mean and the true function — usually very large

### k = Moderate: Sweet Spot
Somewhere in between, you get a smooth enough boundary to generalize without throwing away local structure.

**Nuance**: In kNN, bias and variance are controlled by a single hyperparameter ($k$), which is unusually clean. Most real models have multiple hyperparameters that each pull on bias and variance in different ways.

---
## 9. Case Study 3: Random Forests vs Single Decision Tree

This is a real-world example that directly demonstrates variance reduction via ensembling.
**Single deep decision tree**:
- Grows until leaves are pure → zero training error → high variance
- On different bootstrap samples of the same dataset, you get very different trees
- Individual tree test accuracy might be 75%

**Random Forest (200 trees)**:
- Each tree has the same high variance as the single tree
- But the trees are uncorrelated (different bootstrap samples + random feature subsampling)
- Average their predictions → variance cancels → test accuracy might jump to 88%

**What changed?** Not bias — the average prediction of the forest is about the same as the average prediction of a single deep tree. What changed is variance, which was cut drastically by averaging 200 independent noisy predictions.

This is why random forests work. They don't make each tree better — they make the ensemble of trees better by averaging out the variance.

**Contrast with boosting** (XGBoost, LightGBM):
- Uses shallow trees (stumps or depth-3 trees): individually high bias, low variance
- Sequentially reduces bias: each tree corrects the residuals of the previous
- The ensemble ends up with low bias (from boosting) and manageable variance (from shallow base learners)

Two entirely different strategies to reach the same destination: low total error.

---

## 10. Case Study 4: Neural Networks — Where the Classical Picture Breaks Down
*Deep learning breaks the traditional bias-variance story* in important ways. This is crucial to understand.

### The Classical Expectation
The classical picture says: as you increase model size, at some point variance grows faster than bias decreases, and test error starts rising. You should stop there.
### What Actually Happens with Deep Networks
With neural networks trained on real data, the curve looks different:

```
Error
  |
  |  \         /\
  |   \       /  \_______________  ← Test error (double descent)
  |    \     /
  |     \   /
  |      \_/  ← "Classical" regime
  |
  |____________________________________________
           Model Size / # Parameters →
              ↑
          Interpolation threshold
          (model can fit training data perfectly)
```

This is the **double descent** phenomenon (Belkin et al., 2019). At the interpolation threshold — where the model just barely has enough parameters to fit the training data — test error peaks. But as you continue increasing model size _beyond_ this threshold, test error starts decreasing again.

Very large, heavily overparameterized neural networks can simultaneously:
- Achieve near-zero training loss (interpolate the training data)
- Generalize well to test data

>This seems to violate the bias-variance tradeoff. It doesn't — but it requires rethinking what "variance" means for neural networks:
- The implicit bias of SGD: neural networks trained with gradient descent don't just find _any_ interpolating solution — they tend to find **low-complexity, smooth interpolating solutions** due to the implicit regularization of the optimizer
- Overparameterized networks have "extra" parameters that smooth out predictions between data points rather than overfitting sharply to noise

### The Practical Implication
For deep learning:
- **Don't be afraid of large models** — more parameters with appropriate regularization often generalizes better
- The classical "find the optimal model size" advice is less relevant — you often want the largest model you can afford
- The risk control shifts from model size to regularization techniques (dropout, weight decay, early stopping, data augmentation)

### High Bias in Deep Learning
High bias still exists and shows up when:
- Architecture is too small for the task (a 2-layer MLP on ImageNet)
- Training is stopped too early (training loss hasn't converged)
- Learning rate is too high (model never finds a good minimum)
- Task is genuinely hard and the architecture doesn't match the inductive bias needed

### High Variance in Deep Learning
High variance shows up when:
- Training set is small relative to model size (and no regularization)
- Data augmentation is absent for vision tasks
- Dropout is not used
- Training for too long without early stopping on a small dataset

---

## 11. The Diagnostic Framework: What Do You Actually Do?
Given training and validation/test error, here's how to diagnose and respond:
### Scenario A: High Training Error + High Test Error
**Diagnosis**: High bias (underfitting)  
**What to do**:
- Use a more complex model (deeper network, higher-degree polynomial, more trees)
- Add more features or engineer better features
- Train longer (for neural networks)
- Reduce regularization (L2 weight decay, dropout rate)
- **Getting more data will NOT help** — the model can't capture the signal it already has

### Scenario B: Low Training Error + High Test Error
**Diagnosis**: High variance (overfitting)  
**What to do**:
- Get more training data (this directly reduces variance)
- Add regularization (L2/L1 penalty, dropout, early stopping)
- Use a simpler model / reduce model capacity
- Data augmentation (for vision/audio tasks)
- Ensemble methods (average multiple models)
- **Making the model bigger may or may not help** — depends on whether you're in the classical or modern regime

### Scenario C: Low Training Error + Low Test Error
**Diagnosis**: Well-generalized — you're done  
Check: is the absolute performance level acceptable? If not, you need a better model or more data, not a bias-variance intervention.

### Scenario D: High Training Error + Low Test Error
**Diagnosis**: This shouldn't happen if test distribution = training distribution. If it does, suspect:
- Train/test distribution mismatch
- Bugs in evaluation code (different preprocessing)
- Leakage in test labels

### Nuance: The Bayes Error Rate
All of the above assumes you know what "good" performance looks like. In practice, you need an estimate of the **Bayes error rate** — the best possible error achievable, given the irreducible noise in the data.

For human-level tasks, human performance is often a proxy for Bayes error. If:
- Human error: 5%, Training error: 6%, Test error: 6% → Minimal bias and variance, near-optimal
- Human error: 5%, Training error: 6%, Test error: 20% → Low bias, high variance
- Human error: 5%, Training error: 30%, Test error: 31% → High bias, low variance (train longer, bigger model)
- Human error: 5%, Training error: 15%, Test error: 30% → Both bias and variance problems

This framing (from Andrew Ng's course) is extremely useful in practice.

---

## 12. Regularization as Bias-Variance Control

Every regularization technique is, at its core, a tool to increase bias slightly in exchange for a larger decrease in variance.

### L2 Regularization (Weight Decay)

Adds $\lambda |w|^2$ to the loss. Shrinks weights toward zero. Prevents any single weight from becoming too large → prevents overfitting to individual training examples. Increases bias slightly (prevents the model from fitting extreme cases), reduces variance significantly.

### L1 Regularization (Lasso)

Adds $\lambda |w|_1$. Encourages sparsity — drives unimportant weights to exactly zero. Implicit feature selection. Same bias-variance effect as L2 but with the added benefit of producing sparse solutions.

### Dropout

At each training step, randomly zero out a fraction of neurons. Equivalent to training an exponential number of different network architectures and averaging them (model ensembling). Directly reduces variance without dramatically increasing bias.

### Early Stopping

Stop training before the model fully converges on training data. As training continues past the point of minimum validation loss, the model starts memorizing noise → variance increases. Early stopping is equivalent to L2 regularization in certain settings (not exactly, but the intuition is right).

### Data Augmentation

Artificially increases training set size by creating new examples (flipping, rotating, cropping images; paraphrasing text). Directly reduces variance because the model sees more diverse examples. Does not increase bias (the augmented data is still drawn from (approximately) the same distribution).

### Batch Normalization

Reduces internal covariate shift, but also has a regularizing effect — the noise introduced by computing statistics over mini-batches acts like dropout. Primarily addresses optimization but incidentally reduces variance.

---

## 13. The Terminology Problem: A Direct Address

There are several places where the vocabulary used in practice doesn't cleanly map to the formal framework. Let's address them explicitly.

### "Overfitting" is used too loosely

In practice, people say "the model is overfitting" to mean "test performance is worse than training performance." This is correct in spirit but hides important nuance:

- A model can overfit (high train-test gap) while still being the best available model if the dataset is small and the problem is hard
- "Overfitting" doesn't necessarily mean the model is bad — maybe the training set is simply too small
- Fixing "overfitting" might not mean adding regularization — it might mean getting more data

The formal term is **high variance**, which is more precise: the model's predictions are too sensitive to the specific training data it saw.

### "Underfitting" is even more misused

People often say "the model underfits" to mean "training loss is high" or "the model is dumb." The formal meaning is specific: the model's hypothesis class cannot represent the true function. A huge neural network can underfit if trained for too few epochs (the capacity exists but wasn't used) — that's an optimization problem, not a bias problem. Genuine underfitting means you need a structurally different, more expressive model.

### "Generalization gap" ≠ "variance"

The generalization gap (test error − training error) is a symptom of high variance, but the two are not the same thing. Variance is defined across multiple training sets; the generalization gap is measured on one. A large gap on one run is evidence of high variance, not proof.

### "Model complexity" is not one-dimensional

The bias-variance curves drawn in textbooks use "model complexity" on the x-axis as if it's a single number. In reality:

- For neural networks, "complexity" could mean depth, width, number of parameters, training time, or the degree of regularization
- You can have a very deep network with low variance (if heavily regularized) or a small network with high variance (if trained on tiny data)

The relevant quantity is **effective complexity** — how many degrees of freedom the model is actually using given the data and regularization.

### "Bias" in the social/statistical vs. ML sense

"Bias" in ML's bias-variance decomposition means systematic prediction error. "Bias" in fairness/ethics means discriminatory behavior. "Bias" in statistics sometimes means estimator bias ($\mathbb{E}[\hat{\theta}] - \theta$). These are different uses of the same word. The bias-variance tradeoff is about the first one only.

---

## 14. Bias-Variance in the Real World: What Actually Matters

In practice, the formal decomposition is less important than the diagnostic skill. Here's what experienced practitioners actually think about:

**Question 1: Do I have enough data?**  
If no → variance is likely the problem. More data, regularization, or ensembling.  
If yes → bias might be the problem. Bigger model, more features, longer training.

**Question 2: Is my model big enough for the problem?**  
If the task requires complex representations and the model is small → high bias. Think: using logistic regression for image classification.

**Question 3: Am I comparing to the right baseline?**  
Before diagnosing bias vs variance, know what "good" looks like. Human performance, or the best published result, is your reference. Without this, "my model is 80% accurate" is uninterpretable.

**Question 4: Is the train-test gap large?**  
The train-test gap is the fastest practical diagnostic. Large gap → variance. Small gap with bad absolute performance → bias.

**Question 5: Is my data distribution right?**  
A model that generalizes poorly might not have a bias-variance problem at all — it might have a distribution shift problem. The framework assumes train and test are from the same distribution. If they're not, all bets are off.

---

## 15. Key Takeaways

- Error = Bias² + Variance + Irreducible Noise. These are the only three sources.
- **Bias**: systematic error from a model too simple to capture the truth. Doesn't improve with more data.
- **Variance**: inconsistency from a model too sensitive to training data. Improves with more data, regularization, or ensembling.
- Underfitting = high bias. High training error AND high test error. Cure: bigger model, more features, less regularization.
- Overfitting = high variance. Low training error, high test error. Cure: more data, regularization, ensembling, simpler model.
- Bias and variance are population-level concepts — defined across many training sets, not a single run.
- The classical U-shaped tradeoff curve is correct for classical models. Deep neural networks exhibit **double descent** — very large models can generalize well even while interpolating the training data.
- Regularization trades a small increase in bias for a larger decrease in variance — that's always the deal.
- The generalization gap (train error vs. test error) is the fastest practical diagnostic, but it's not the whole story.
- Always estimate Bayes error (e.g., human performance) before diagnosing. Knowing where the floor is tells you how much room there is to improve and which direction to push.