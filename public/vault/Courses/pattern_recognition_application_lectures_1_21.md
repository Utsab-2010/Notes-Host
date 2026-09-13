---
title: "pattern_recognition_application_lectures_1_21"
lastmod: 2026-09-13
---

# Pattern Recognition and Application — Detailed Notes (Lectures 1–21)

**Course:** Pattern Recognition and Application  
**Instructor:** Prof. Prabir Kumar Biswas, IIT Kharagpur  
**Course code:** NPTEL 117105101  
**Coverage:** Lectures 1–21

> **Obsidian math notation:** all mathematical expressions in these notes use `$$ ... $$`. For equations intended as standalone display equations, the delimiters are placed on separate lines.

---

# Lecture 1 — Introduction

## 1. What is Pattern Recognition?

A **pattern** is an object, event, signal, image, or measurement that has properties which allow us to distinguish it from other patterns.

Examples:

- A handwritten digit is a pattern.
- A speech waveform is a pattern.
- A fingerprint is a pattern.
- A character in an OCR system is a pattern.
- A measured sensor signal is a pattern.
- A geometrical object such as a circle, ellipse, or arbitrary closed contour is a pattern.

The central problem is:

> Given an unknown pattern, determine which known class or category it belongs to.

Pattern recognition therefore involves **matching an unknown observation against learned models**.

A useful conceptual chain is

$$
\text{raw pattern}
\rightarrow
\text{feature extraction}
\rightarrow
\text{feature vector}
\rightarrow
\text{classifier/decision rule}
\rightarrow
\text{class label}.
$$

The raw pattern itself is often high-dimensional and contains much information that is irrelevant to the recognition task. The purpose of feature extraction is to retain information that is useful for discrimination.

---

## 2. Machine perception

A pattern-recognition system can be viewed as a machine-perception system:

1. The physical world produces some object or phenomenon.
2. A sensor measures it.
3. The measurement is represented numerically.
4. Useful features are extracted.
5. A learning or decision mechanism is used.
6. The system assigns the observation to a class.

The important point is that the **machine does not generally operate directly on the semantic identity of the object**. It operates on a numerical representation.

---

## 3. Pattern recognition as a matching problem

Suppose a knowledge base contains representative patterns or models for classes.

Given a new pattern $$x$$, the system has to decide whether it is similar to:

- class $$\omega_1$$,
- class $$\omega_2$$,
- etc.

Similarity can be defined directly in pattern space, but this is usually difficult.

Instead, we map the pattern into a feature space:

$$
x
\mapsto
\mathbf{z}
=
[z_1,z_2,\ldots,z_d]^T.
$$

The recognition problem then becomes a problem of **classification in feature space**.

---

## 4. Supervised versus unsupervised learning

### Supervised learning

In supervised learning, the class identity of training patterns is known.

Suppose the training set is

$$
\mathcal{D}
=
\{(\mathbf{x}_i,\omega_i)\}_{i=1}^{N}.
$$

The recognizer sees both:

- an input pattern,
- the desired class/label.

Training therefore tries to learn a mapping from feature vectors to known classes.

If a training feature vector is assigned the wrong class, the error is known. Learning algorithms can use this error to modify the classifier.

### Unsupervised learning

In unsupervised learning, the class labels are not supplied.

Instead, the system receives a mixture of feature vectors and has to discover natural groups.

Conceptually:

$$
\{\mathbf{z}_1,\mathbf{z}_2,\ldots,\mathbf{z}_N\}
\rightarrow
\text{partition into similar subsets}.
$$

After the partitioning, each subset can be treated as an emerging class or cluster.

The crucial difference is therefore:

- **supervised:** class association is known during learning;
- **unsupervised:** class association must be discovered from the data.

---

## 5. Why feature vectors?

Consider a circular arc.

A circle can be characterized by parameters such as:

- radius,
- center coordinates.

If translation is not important, the radius alone may be enough for the task. If location matters, the center must also be included.

For an ellipse, the corresponding description requires more parameters, for example:

$$
\frac{x^2}{a^2}+\frac{y^2}{b^2}=1.
$$

This illustrates an important principle:

> The useful features depend on the problem domain.

There is no universally optimal feature set.

---

## 6. Mapping between patterns and features

A feature-extraction procedure maps a pattern to a feature vector:

$$
f:\mathcal{X}\rightarrow\mathbb{R}^d.
$$

For a fixed deterministic feature extractor, the same pattern will produce the same feature vector.

But the reverse mapping generally is not unique:

$$
\mathbf{z}\not\rightarrow \text{unique pattern}.
$$

Many different patterns may produce identical or very similar feature vectors.

This is one reason why we normally use **multiple features together**.

---

## 7. Types of features

Broadly, features can describe:

### Shape features

These capture the geometry or form of an object:

- circular,
- rectangular,
- elliptical,
- boundary shape,
- symmetry,
- elongation,
- curvature.

### Region features

These describe properties of the region enclosed by the shape:

- intensity,
- color,
- texture,
- local variation.

For a color image, features may involve hue, saturation, and intensity. For a textured region, texture descriptors may be useful.

The feature vector is

$$
\mathbf{z}
=
[z_1,z_2,\ldots,z_d]^T,
$$

and the **ordering of the components matters**. The first component must always mean the same thing, the second component must always mean the same thing, etc.

---

## 8. Recognition system viewpoint

A generic recognition system can therefore be divided into:

1. Data acquisition.
2. Pre-processing.
3. Feature extraction.
4. Feature representation.
5. Learning/training.
6. Decision/classification.
7. Evaluation.

The later lectures focus primarily on statistical decision rules and learning algorithms operating in feature space.

---

# Lecture 2 — Feature Extraction I

## 1. Motivation

Feature extraction converts a raw pattern into a smaller, informative numerical representation.

The goal is not simply to describe everything about the pattern. The goal is to describe the aspects that matter for **recognition or classification**.

---

## 2. Circular-arc example

Suppose the pattern is a circular arc.

If the task is to determine which circle generated the arc, useful parameters include:

- center coordinates,
- radius.

A feature representation might be

$$
\mathbf{z}
=
[c_x,c_y,r]^T.
$$

If translation should be ignored, then the center may not be useful, and

$$
\mathbf{z}= [r]
$$

may be sufficient.

Thus feature design depends on the **invariances desired by the application**.

---

## 3. Similarity and dissimilarity in feature space

Once patterns are represented by feature vectors, they can be compared using distance or similarity measures.

For example, Euclidean distance is

$$
d(\mathbf{x},\mathbf{y})
=
\sqrt{
\sum_{j=1}^{d}(x_j-y_j)^2
}.
$$

If two feature vectors are close, the corresponding patterns may be considered similar.

A classifier can therefore operate on feature vectors rather than raw patterns.

---

## 4. Representative vectors

Suppose several training patterns belong to the same known class.

Their individual feature vectors may be

$$
\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_N.
$$

A simple representative feature vector is the mean:

$$
\boldsymbol{\mu}
=
\frac{1}{N}
\sum_{i=1}^{N}\mathbf{x}_i.
$$

The mean is a model of the center of a class in feature space.

This idea leads naturally to statistical classification, where classes are modeled by probability distributions.

---

## 5. Supervised feature learning

For a known class, we can collect many feature vectors and estimate a representative model.

The process is:

$$
\text{known patterns}
\rightarrow
\text{feature extraction}
\rightarrow
\text{class-specific feature statistics}
\rightarrow
\text{classifier}.
$$

The classifier then receives an unknown pattern, extracts the same features, and compares the resulting vector with the learned class models.

---

## 6. Unsupervised feature grouping

When labels are unavailable, the system receives a mixture of feature vectors.

The vectors have to be partitioned according to similarity.

Conceptually,

$$
\mathcal{X}
=
\mathcal{X}_1\cup\mathcal{X}_2\cup\cdots\cup\mathcal{X}_K.
$$

The individual clusters are not initially assigned semantic class names.

---

## 7. Feature extraction as information reduction

The original pattern may contain a huge number of measurements. A feature extractor maps it into a lower-dimensional vector.

For example,

$$
\mathbf{x}\in\mathbb{R}^{M}
\quad\rightarrow\quad
\mathbf{z}\in\mathbb{R}^{d},
\qquad d\ll M.
$$

A good feature representation should:

- preserve class-discriminative information,
- remove irrelevant variation,
- be robust to noise,
- ideally be compact.

This tension between preserving useful information and reducing dimension becomes important in later lectures.

---

# Lecture 3 — Feature Extraction II

## 1. Shape versus region information

A pattern may be represented using:

### Shape-based features

These are determined primarily by the boundary:

- perimeter,
- curvature,
- aspect ratio,
- compactness,
- symmetry,
- elongation,
- geometric moments.

### Region-based features

These characterize the contents of a region:

- gray-level distribution,
- average intensity,
- variance,
- color,
- texture.

A practical system often combines both.

---

## 2. Why a single feature is usually insufficient

Suppose two patterns have approximately identical area but very different shapes.

A single scalar feature such as area cannot distinguish them.

Likewise, two objects may have the same shape but different internal textures.

Hence a vector is preferred:

$$
\mathbf{z}
=
[z_1,z_2,\ldots,z_d]^T.
$$

Each component captures a different property.

The complete vector provides a richer description.

---

## 3. Feature vector dimensionality

The dimension of the feature vector determines the complexity of the feature space.

If the dimension is too low, different patterns may collapse onto the same representation.

If the dimension is very high, there may be:

- increased computation,
- increased storage,
- more difficult density estimation,
- sparse observations,
- poorer generalization.

The dimensionality problem becomes a major topic later.

---

## 4. Symmetry and ordering

For a machine system, consistency is essential.

Suppose

$$
\mathbf{x}=[x_1,x_2,x_3]^T.
$$

If $$x_1$$ means area during training but means perimeter during testing, the classifier is effectively operating on a different feature space.

Therefore:

> The semantic interpretation and ordering of feature components must remain fixed.

---

## 5. Properties of useful features

A desirable feature is:

- **discriminative:** different classes have different values;
- **stable:** small perturbations do not radically change the value;
- **compact:** it avoids unnecessary dimensions;
- **invariant:** it ignores nuisance transformations when appropriate;
- **computationally reasonable:** it can be extracted efficiently.

Feature extraction is therefore a form of **representation design**.

---

# Lecture 4 — Feature Extraction III

## 1. Feature design depends on the application

The lecturer emphasizes that there is no universally good feature.

A feature useful for one type of pattern may be useless for another.

For circles:

$$
\text{radius and center}
$$

are natural.

For ellipses, the two semi-axis lengths and orientation become important.

For arbitrary images, geometric parameters alone are not enough.

---

## 2. Shape and region descriptors

A recognition system can combine:

$$
\text{shape information}
+
\text{region information}.
$$

Region information may include:

- intensity,
- color,
- texture.

Texture itself can be described statistically through quantities such as mean intensity, variance, local contrast, or more complex descriptors.

---

## 3. Feature extraction versus feature selection

These are conceptually different:

### Feature extraction

Construct new features from the original measurements.

Example:

$$
\mathbf{x}\rightarrow\mathbf{z}.
$$

### Feature selection

Choose a subset of existing features.

Example:

$$
[x_1,x_2,x_3,x_4]
\rightarrow
[x_1,x_3].
$$

Both aim to produce a more useful representation.

---

## 4. One-to-many reverse mapping

A crucial observation is that several raw patterns may correspond to the same feature vector.

Thus:

$$
\text{pattern}\rightarrow\text{feature vector}
$$

can be deterministic while

$$
\text{feature vector}\rightarrow\text{pattern}
$$

is generally ambiguous.

As feature dimension is reduced, this ambiguity can become larger.

This gives the main tradeoff:

> Lower dimension reduces complexity, but may destroy discriminative information.

---

# Lecture 5 — Bayes Decision Theory

## 1. Why Bayesian decision theory?

Once every pattern is represented by a feature vector, the next task is classification.

Suppose there are two classes:

$$
\omega_1,\omega_2.
$$

For an observed feature vector $$\mathbf{x}$$, we wish to decide which class generated it.

Bayesian decision theory gives a principled answer using probabilities.

---

## 2. Prior probability

The prior probability of class $$\omega_i$$ is

$$
P(\omega_i).
$$

It represents how likely the class is before observing the particular feature vector.

If the classes occur equally often, the priors may satisfy

$$
P(\omega_1)=P(\omega_2)=\frac12.
$$

But unequal priors are common.

---

## 3. Class-conditional density

The probability density of observing feature vector $$\mathbf{x}$$ given class $$\omega_i$$ is

$$
p(\mathbf{x}\mid\omega_i).
$$

This describes how feature vectors are distributed within class $$\omega_i$$.

---

## 4. Posterior probability

Bayes' rule gives

$$
P(\omega_i\mid\mathbf{x})
=
\frac{
p(\mathbf{x}\mid\omega_i)P(\omega_i)
}{
p(\mathbf{x})
}.
$$

The evidence is

$$
p(\mathbf{x})
=
\sum_j
p(\mathbf{x}\mid\omega_j)P(\omega_j).
$$

The posterior expresses how likely the class is after observing the feature vector.

---

## 5. Minimum-error classification

Under a zero-one loss function, the optimal decision is to choose the class with the largest posterior probability:

$$
\text{decide }\omega_i
\quad\text{if}\quad
P(\omega_i\mid\mathbf{x})
>
P(\omega_j\mid\mathbf{x})
\;\;\forall j\neq i.
$$

Because $$p(\mathbf{x})$$ is common to all classes, this is equivalent to comparing

$$
p(\mathbf{x}\mid\omega_i)P(\omega_i).
$$

Thus:

$$
\boxed{
\text{decide }\omega_i
\text{ if }
p(\mathbf{x}\mid\omega_i)P(\omega_i)
>
p(\mathbf{x}\mid\omega_j)P(\omega_j)
}
$$

for all competing classes.

---

## 6. Loss function

Not all errors have equal consequences.

Let

$$
\lambda(\alpha_i\mid\omega_j)
$$

denote the loss incurred when action $$\alpha_i$$ is taken while the true class is $$\omega_j$$.

Then the conditional risk of action $$\alpha_i$$ is

$$
R(\alpha_i\mid\mathbf{x})
=
\sum_j
\lambda(\alpha_i\mid\omega_j)
P(\omega_j\mid\mathbf{x}).
$$

The Bayes decision rule selects the action with the smallest conditional risk.

---

## 7. Overall risk

If the decision rule is $$\alpha(\mathbf{x})$$, the overall risk is

$$
R
=
\int
R(\alpha(\mathbf{x})\mid\mathbf{x})
p(\mathbf{x})
\,d\mathbf{x}.
$$

If the conditional risk is minimized for every $$\mathbf{x}$$, the overall risk is minimized.

This gives the fundamental Bayesian decision principle.

---

# Lecture 6 — Bayes Decision Theory (Continued)

## 1. Two-category classification

For two classes, define the posterior probabilities

$$
P(\omega_1\mid\mathbf{x}),
\qquad
P(\omega_2\mid\mathbf{x}).
$$

Since the posteriors sum to one,

$$
P(\omega_1\mid\mathbf{x})
+
P(\omega_2\mid\mathbf{x})
=
1.
$$

Under minimum probability of error, decide class 1 if

$$
P(\omega_1\mid\mathbf{x})
>
P(\omega_2\mid\mathbf{x}).
$$

---

## 2. Decision boundary

The decision boundary occurs where the two alternatives are equally preferred:

$$
P(\omega_1\mid\mathbf{x})
=
P(\omega_2\mid\mathbf{x}).
$$

Using Bayes' theorem:

$$
p(\mathbf{x}\mid\omega_1)P(\omega_1)
=
p(\mathbf{x}\mid\omega_2)P(\omega_2).
$$

This defines the boundary in feature space.

The feature space is divided into **decision regions**.

---

## 3. Discriminant functions

Instead of explicitly writing posterior probabilities, define discriminant functions.

One convenient choice is

$$
g_i(\mathbf{x})
=
p(\mathbf{x}\mid\omega_i)P(\omega_i).
$$

Then choose the class with the largest discriminant.

An equivalent logarithmic form is often useful:

$$
g_i(\mathbf{x})
=
\ln p(\mathbf{x}\mid\omega_i)
+
\ln P(\omega_i).
$$

The logarithm preserves ordering because it is monotonic.

---

## 4. Decision surfaces

For classes $$\omega_i$$ and $$\omega_j$$, the decision surface satisfies

$$
g_i(\mathbf{x})=g_j(\mathbf{x}).
$$

In one dimension this is a point.

In two dimensions it is a curve.

In higher dimensions it is a hypersurface.

---

## 5. Effect of priors

The prior probability shifts the decision boundary.

If one class is much more common, the classifier should require stronger evidence before assigning a rare class.

Thus classification does not depend only on the likelihoods.

It depends on

$$
\text{likelihood}\times\text{prior}.
$$

---

## 6. Error regions

For a two-class problem, each decision region can contain samples from both classes.

Hence two kinds of mistakes are possible:

- samples from $$\omega_1$$ classified as $$\omega_2$$;
- samples from $$\omega_2$$ classified as $$\omega_1$$.

The total probability of error is the probability mass lying on the wrong side of the decision boundary.

---

# Lecture 7 — Normal Density and Discriminant Function

## 1. Gaussian model

A very important assumption in statistical pattern recognition is that class-conditional densities are Gaussian.

### Univariate Gaussian

For scalar $$x$$,

$$
p(x\mid\omega_i)
=
\frac{1}{
\sqrt{2\pi}\sigma_i
}
\exp
\left[
-\frac{
(x-\mu_i)^2
}{
2\sigma_i^2
}
\right].
$$

Here:

- $$\mu_i$$ is the mean;
- $$\sigma_i^2$$ is the variance.

---

## 2. Multivariate Gaussian

For a feature vector $$\mathbf{x}\in\mathbb{R}^d$$,

$$
p(\mathbf{x}\mid\omega_i)
=
\frac{1}{
(2\pi)^{d/2}
|\Sigma_i|^{1/2}
}
\exp
\left[
-\frac12
(\mathbf{x}-\boldsymbol{\mu}_i)^T
\Sigma_i^{-1}
(\mathbf{x}-\boldsymbol{\mu}_i)
\right].
$$

Here:

- $$\boldsymbol{\mu}_i$$ is the class mean vector;
- $$\Sigma_i$$ is the covariance matrix;
- $$|\Sigma_i|$$ is its determinant.

---

## 3. Gaussian discriminant function

Take the logarithm of the Gaussian density and add the log prior.

A convenient discriminant is

$$
g_i(\mathbf{x})
=
-\frac12\ln|\Sigma_i|
-\frac12
(\mathbf{x}-\boldsymbol{\mu}_i)^T
\Sigma_i^{-1}
(\mathbf{x}-\boldsymbol{\mu}_i)
+
\ln P(\omega_i),
$$

where terms common to all classes have been omitted.

The quadratic term measures the distance of $$\mathbf{x}$$ from the class mean while accounting for covariance.

---

## 4. Mahalanobis distance

The covariance-weighted squared distance is

$$
D_i^2(\mathbf{x})
=
(\mathbf{x}-\boldsymbol{\mu}_i)^T
\Sigma_i^{-1}
(\mathbf{x}-\boldsymbol{\mu}_i).
$$

This is the squared **Mahalanobis distance**.

Unlike Euclidean distance, it accounts for:

- different feature variances,
- correlations between features.

---

## 5. Equal covariance case

If all classes share the same covariance matrix,

$$
\Sigma_i=\Sigma,
$$

then the quadratic terms involving $$\mathbf{x}$$ cancel when comparing classes.

The discriminant becomes linear in $$\mathbf{x}$$:

$$
g_i(\mathbf{x})
=
\mathbf{w}_i^T\mathbf{x}
+
w_{i0}.
$$

Thus a Gaussian model with common covariance produces **linear decision boundaries**.

---

# Lecture 8 — Normal Density and Discriminant Function (Continued)

## 1. Different covariance cases

The form of the decision boundary depends strongly on the covariance matrices.

### Case 1: Equal covariance matrices

If

$$
\Sigma_1=\Sigma_2,
$$

the decision boundary is linear.

### Case 2: Different covariance matrices

If

$$
\Sigma_1\neq\Sigma_2,
$$

the quadratic terms do not cancel, producing a **quadratic decision boundary**.

Thus:

- shared covariance → linear discriminant;
- class-dependent covariance → quadratic discriminant.

---

## 2. Diagonal covariance

A diagonal covariance matrix has the form

$$
\Sigma
=
\begin{bmatrix}
\sigma_1^2 & 0 & \cdots & 0\\
0 & \sigma_2^2 & \cdots & 0\\
\vdots & \vdots & \ddots & \vdots\\
0 & 0 & \cdots & \sigma_d^2
\end{bmatrix}.
$$

This assumes feature components are uncorrelated.

The Gaussian density then factors into a product of one-dimensional Gaussian densities:

$$
p(\mathbf{x}\mid\omega_i)
=
\prod_{k=1}^{d}
p(x_k\mid\omega_i).
$$

---

## 3. Spherical covariance

If

$$
\Sigma_i
=
\sigma_i^2 I,
$$

all directions have equal variance and there are no correlations.

Then the Gaussian contours are spheres (circles in two dimensions).

If the variances are equal across classes, the decision boundaries become especially simple.

---

## 4. Geometric interpretation

For a multivariate Gaussian:

- the mean is the center of the distribution;
- covariance determines orientation and spread;
- determinant controls volume/spread;
- the inverse covariance weights deviations in different directions.

The constant-density surfaces satisfy

$$
(\mathbf{x}-\boldsymbol{\mu})^T
\Sigma^{-1}
(\mathbf{x}-\boldsymbol{\mu})
=
c,
$$

which describes ellipsoids in general.

---

# Lecture 9 — Bayes Decision Theory: Binary Features

## 1. Continuous versus discrete features

Earlier lectures considered continuous-valued feature vectors.

Now consider a binary feature representation:

$$
x_j\in\{0,1\}.
$$

For a vector of binary features,

$$
\mathbf{x}
=
[x_1,x_2,\ldots,x_d]^T.
$$

The probability model must now be a discrete probability model.

---

## 2. Binary probability distribution

For a single binary variable,

$$
P(x_j=1\mid\omega_i)=p_{ij}
$$

and

$$
P(x_j=0\mid\omega_i)=1-p_{ij}.
$$

If the features are conditionally independent given the class, then

$$
P(\mathbf{x}\mid\omega_i)
=
\prod_{j=1}^{d}
p_{ij}^{x_j}
(1-p_{ij})^{1-x_j}.
$$

This is the Bernoulli-product model.

---

## 3. Bayes classification with binary features

The Bayes rule remains:

$$
\text{decide }\omega_i
\quad\text{if}\quad
P(\mathbf{x}\mid\omega_i)P(\omega_i)
>
P(\mathbf{x}\mid\omega_j)P(\omega_j).
$$

Taking logarithms gives

$$
\ln P(\mathbf{x}\mid\omega_i)
+
\ln P(\omega_i).
$$

For the Bernoulli-product model:

$$
\ln P(\mathbf{x}\mid\omega_i)
=
\sum_j
\left[
x_j\ln p_{ij}
+
(1-x_j)\ln(1-p_{ij})
\right].
$$

The resulting discriminant is linear in the binary feature vector.

---

## 4. Important interpretation

Even when the raw observations are discrete, the Bayesian framework is unchanged:

1. model how each class generates observations;
2. incorporate the prior;
3. compute posterior evidence;
4. choose the minimum-risk decision.

The probability model simply changes from a continuous density to a discrete mass function.

---

# Lecture 10 — Maximum Likelihood Estimation

## 1. Why estimate parameters?

Bayesian classification assumes that class densities such as

$$
p(\mathbf{x}\mid\omega_i)
$$

are known.

In real applications they are unknown.

Instead, we have training data and must estimate their parameters.

Maximum likelihood estimation (MLE) is one of the central parameter-estimation techniques.

---

## 2. Likelihood

Suppose data

$$
\mathcal{D}
=
\{\mathbf{x}_1,\mathbf{x}_2,\ldots,\mathbf{x}_N\}
$$

are assumed independent and identically distributed according to a density

$$
p(\mathbf{x}\mid\boldsymbol{\theta}).
$$

The likelihood is

$$
L(\boldsymbol{\theta})
=
\prod_{n=1}^{N}
p(\mathbf{x}_n\mid\boldsymbol{\theta}).
$$

The MLE chooses parameters maximizing this likelihood:

$$
\hat{\boldsymbol{\theta}}_{\mathrm{ML}}
=
\arg\max_{\boldsymbol{\theta}}
L(\boldsymbol{\theta}).
$$

---

## 3. Log-likelihood

Because products can be numerically inconvenient, maximize the logarithm instead:

$$
\ell(\boldsymbol{\theta})
=
\ln L(\boldsymbol{\theta})
=
\sum_{n=1}^{N}
\ln p(\mathbf{x}_n\mid\boldsymbol{\theta}).
$$

Since logarithm is monotonic,

$$
\arg\max_{\boldsymbol{\theta}}L(\boldsymbol{\theta})
=
\arg\max_{\boldsymbol{\theta}}\ell(\boldsymbol{\theta}).
$$

---

## 4. MLE of Gaussian mean

For scalar Gaussian data with known variance, maximizing likelihood yields

$$
\hat{\mu}
=
\frac{1}{N}
\sum_{n=1}^{N}x_n.
$$

Thus the ML estimate of the Gaussian mean is the sample mean.

---

## 5. MLE of variance

For a Gaussian model, the ML variance estimate is

$$
\hat{\sigma}^2
=
\frac{1}{N}
\sum_{n=1}^{N}
(x_n-\hat{\mu})^2.
$$

The denominator is $$N$$ for the ML estimate.

This differs from the familiar unbiased sample-variance estimator that uses $$N-1$$.

The distinction comes from optimizing likelihood versus requiring unbiasedness.

---

## 6. Multivariate Gaussian MLE

The ML estimate of the mean vector is

$$
\hat{\boldsymbol{\mu}}
=
\frac{1}{N}
\sum_{n=1}^{N}\mathbf{x}_n.
$$

The covariance estimate is

$$
\hat{\Sigma}
=
\frac{1}{N}
\sum_{n=1}^{N}
(\mathbf{x}_n-\hat{\boldsymbol{\mu}})
(\mathbf{x}_n-\hat{\boldsymbol{\mu}})^T.
$$

These estimates directly connect training data to Gaussian Bayesian classifiers.

---

## 7. MLE assumptions

Maximum likelihood estimation depends on assumptions about the data-generating distribution.

If the chosen model is wrong, the resulting parameter estimates may not provide a good classifier.

Thus there are two distinct issues:

- estimating parameters accurately;
- choosing an appropriate model family.

---

# Lecture 11 — Probability Density Estimation

## 1. Parametric versus non-parametric estimation

In **parametric estimation**, we assume a density family and estimate a finite number of parameters.

Example:

$$
p(x\mid\theta)
$$

with Gaussian parameters $$\theta=(\mu,\sigma^2)$$.

In **non-parametric density estimation**, fewer assumptions are made about the form of the distribution.

The distribution is inferred more directly from the training samples.

---

## 2. Why density estimation matters

Bayesian classification requires

$$
p(\mathbf{x}\mid\omega_i).
$$

If this density is unknown, it must be estimated from data.

Thus density estimation provides the link:

$$
\text{training samples}
\rightarrow
\text{estimated density}
\rightarrow
\text{Bayes classifier}.
$$

---

## 3. Histogram estimation

The simplest non-parametric density estimator is a histogram.

The feature space is divided into bins.

For a one-dimensional variable, suppose a bin has width $$h$$ and contains $$k$$ samples out of $$N$$.

The density estimate in that bin is approximately

$$
\hat{p}(x)
=
\frac{k}{Nh}.
$$

The idea generalizes to multidimensional partitions.

---

## 4. Problems with histograms

Histograms have several disadvantages:

- they depend strongly on bin boundaries;
- results depend on bin width;
- they can become unreliable in high dimensions;
- they are not smooth.

This motivates kernel-based estimators.

---

# Lecture 12 — Probability Density Estimation (Continued.)

## 1. Parzen-window idea

Instead of assigning every observation to a hard histogram bin, place a smooth window around each sample.

The estimated density can be written as

$$
\hat{p}(\mathbf{x})
=
\frac{1}{Nh^d}
\sum_{n=1}^{N}
K
\left(
\frac{\mathbf{x}-\mathbf{x}_n}{h}
\right),
$$

where:

- $$N$$ is the number of samples;
- $$d$$ is the feature dimension;
- $$h$$ is the smoothing parameter or window width;
- $$K$$ is the kernel/window function.

---

## 2. Gaussian kernel

A common choice is a Gaussian kernel:

$$
K(\mathbf{u})
=
\frac{1}{(2\pi)^{d/2}}
\exp
\left(
-\frac12\|\mathbf{u}\|^2
\right).
$$

Then

$$
\hat{p}(\mathbf{x})
=
\frac{1}{N(2\pi)^{d/2}h^d}
\sum_{n=1}^{N}
\exp
\left[
-\frac{
\|\mathbf{x}-\mathbf{x}_n\|^2
}{
2h^2
}
\right].
$$

Each training point contributes a local bump to the estimated density.

---

## 3. Role of the smoothing parameter

The parameter $$h$$ controls the bias-variance tradeoff.

### Small $$h$$

The estimate is highly local:

- follows training samples closely;
- may become noisy;
- high variance.

### Large $$h$$

The estimate is smoother:

- less sensitive to individual samples;
- may oversmooth important structure;
- higher bias.

Hence choosing $$h$$ is crucial.

---

# Lecture 13 — Probability Density Estimation (Continued.)

## 1. Multidimensional Parzen estimation

In a $$d$$-dimensional feature space:

$$
\hat{p}(\mathbf{x})
=
\frac{1}{Nh^d}
\sum_{n=1}^{N}
K
\left(
\frac{\mathbf{x}-\mathbf{x}_n}{h}
\right).
$$

The factor $$h^d$$ is essential because the effective volume of a window scales with the dimension.

---

## 2. Curse of dimensionality

Suppose the window has side length proportional to $$h$$ in each dimension.

Its volume scales like

$$
h^d.
$$

As $$d$$ grows, the amount of data required to populate local neighborhoods grows rapidly.

This is a fundamental manifestation of the **curse of dimensionality**.

Even a large training set may become sparse in high-dimensional feature space.

---

## 3. Nearest-neighbor density estimation

A different approach is to choose a region around the query point that contains a specified number of samples.

Let the volume required to contain $$k$$ samples be $$V_k$$.

Then the density estimate is approximately

$$
\hat{p}(\mathbf{x})
=
\frac{k}{N V_k}.
$$

This method adapts the neighborhood size to local density.

Dense regions require small neighborhoods; sparse regions require large neighborhoods.

---

## 4. Parzen versus nearest-neighbor methods

### Parzen method

- Fix the neighborhood size/window;
- count or weight data points inside it.

### Nearest-neighbor method

- Fix the number of data points;
- let the neighborhood size vary.

Both are non-parametric techniques.

---

# Lecture 14 — Probability Density Estimation (Continued.)

## 1. Convergence intuition

A good density estimator should satisfy the intuition:

- as the amount of data grows, the estimated density should approach the true density;
- the window should shrink enough to resolve local structure;
- but not shrink so rapidly that each local estimate becomes dominated by noise.

Thus there is a balancing requirement between data size and smoothing.

---

## 2. Conditions on the window

For Parzen-type methods, a typical asymptotic intuition is:

$$
h_N\rightarrow 0
$$

as

$$
N\rightarrow\infty,
$$

so that local resolution increases.

At the same time, the effective number of samples in the window should grow sufficiently large.

This is captured by the qualitative condition

$$
Nh_N^d\rightarrow\infty.
$$

The two requirements pull in opposite directions:

- $$h_N\rightarrow 0$$ gives increasing resolution;
- $$Nh_N^d\rightarrow\infty$$ keeps enough samples in the effective neighborhood.

---

## 3. Density estimation and classification

For a classifier, we estimate one density for each class:

$$
\hat{p}(\mathbf{x}\mid\omega_1),
\ldots,
\hat{p}(\mathbf{x}\mid\omega_K).
$$

Then the Bayes rule uses

$$
\hat{p}(\mathbf{x}\mid\omega_i)P(\omega_i).
$$

Thus non-parametric density estimation can be inserted directly into Bayesian decision theory.

---

## 4. Practical issue

Non-parametric methods can become computationally expensive because every new test point may have to interact with many training samples.

This becomes especially important as:

- number of samples increases;
- feature dimension increases;
- number of classes increases.

---

# Lecture 15 — Probability Density Estimation (Continued.)

## 1. Choosing the smoothing parameter

The window parameter is central to Parzen estimation.

Conceptually:

- very small window → detailed but noisy estimate;
- very large window → smooth but potentially inaccurate estimate.

The choice of smoothing therefore controls recognition performance.

---

## 2. Density estimation and sample size

Increasing the training-set size allows smaller windows while preserving enough samples to estimate density.

This means that the same dimensionality can become easier to handle when more data are available.

However, increasing dimensionality can overwhelm this benefit.

---

## 3. Relation to the curse of dimensionality

If the feature dimension increases from $$d$$ to $$d+1$$, a local region of side length $$h$$ gains another factor of $$h$$ in volume.

Therefore data become rapidly sparse.

This explains why feature selection and dimensionality reduction are not merely computational conveniences.

They are often essential for reliable statistical learning.

---

# Lecture 16 — Dimensionality Problem

## 1. Why dimension is a problem

As feature dimension increases:

- feature space volume increases dramatically;
- data become sparse;
- density estimation becomes difficult;
- more training data are required;
- distances can become less informative;
- computational requirements increase.

This collection of problems is called the **curse of dimensionality**.

---

## 2. A geometric intuition

Suppose we want a neighborhood containing a fixed fraction of the total volume.

In one dimension, the neighborhood can be relatively large.

In high dimensions, to occupy the same fraction of the total space, the corresponding radius becomes much larger.

For example, for a unit hypercube, the volume is

$$
V=1.
$$

A centered hypercube of side length $$a$$ has volume

$$
V_a=a^d.
$$

For a fixed fraction $$\eta$$,

$$
a=\eta^{1/d}.
$$

As $$d$$ becomes large, the relationship between side length and volume becomes unintuitive.

---

## 3. Data sparsity

A classifier that relies on local neighborhoods needs enough data to populate those neighborhoods.

But the number of points required grows rapidly with dimension.

Hence:

$$
\text{higher dimension}
\Rightarrow
\text{more data required}.
$$

If data availability is fixed, adding irrelevant dimensions can make the classifier worse.

---

## 4. Irrelevant features

Suppose only a small subset of features contains class information.

Adding many irrelevant features increases dimension without improving separability.

For Euclidean distance,

$$
d^2(\mathbf{x},\mathbf{y})
=
\sum_{j=1}^{d}(x_j-y_j)^2.
$$

Noise dimensions add positive contributions to the distance.

This can obscure the informative components.

---

## 5. Need for dimensionality reduction

Possible strategies include:

- feature selection;
- feature extraction;
- principal component analysis;
- discriminant analysis.

The next lectures develop discriminant-based dimension reduction.

---

# Lecture 17 — Multiple Discriminant Analysis

## 1. Motivation

Suppose there are multiple classes and a high-dimensional feature vector.

We want to project the data onto a lower-dimensional subspace while preserving class separability.

This is the purpose of **Multiple Discriminant Analysis (MDA)**, closely related to Fisher's linear discriminant framework.

---

## 2. Linear transformation

We seek a projection matrix $$W$$ such that

$$
\mathbf{y}
=
W^T\mathbf{x}.
$$

If the original dimension is $$d$$ and the reduced dimension is $$r$$, then

$$
W\in\mathbb{R}^{d\times r},
\qquad
r<d.
$$

---

## 3. Within-class scatter

For each class $$\omega_i$$, let the class mean be $$\boldsymbol{\mu}_i$$
The within-class scatter measures variability inside each class.
For class $i$$:

$$
S_i
=
\sum_{\mathbf{x}\in\omega_i}
(\mathbf{x}-\boldsymbol{\mu}_i)
(\mathbf{x}-\boldsymbol{\mu}_i)^T.
$$

The total within-class scatter is

$$
S_W
=
\sum_i S_i.
$$

A small within-class scatter after projection means class members remain compact.

---

## 4. Between-class scatter

Let the overall mean be $$\boldsymbol{\mu}$$

The between-class scatter measures separation between class means:

$$
S_B
=
\sum_i
N_i
(\boldsymbol{\mu}_i-\boldsymbol{\mu})
(\boldsymbol{\mu}_i-\boldsymbol{\mu})^T.
$$

Here $$N_i$$ is the number of samples in class $$i$$.

A large between-class scatter means class means are well separated.

---

## 5. Fisher criterion

The basic idea is to maximize
$$
J(W)
=
\frac{
|W^TS_BW|
}{
|W^TS_WW|
}.
$$

For one projection direction $$\mathbf{w}$$ this reduces conceptually to

$$
J(\mathbf{w})
=
\frac{
\mathbf{w}^TS_B\mathbf{w}
}{
\mathbf{w}^TS_W\mathbf{w}
}.
$$

We want:

- large between-class variance;
- small within-class variance.

---

## 6. Generalized eigenvalue problem

The optimization leads to a generalized eigenvalue problem:

$$
S_B\mathbf{w}
=
\lambda S_W\mathbf{w}.
$$

Equivalently,

$$
S_W^{-1}S_B\mathbf{w}
=
\lambda\mathbf{w},
$$

when $$S_W$$ is invertible.

The eigenvectors corresponding to the largest eigenvalues provide discriminant directions.

---

## 7. Maximum useful dimension

For $$C$$ classes, the rank of the between-class scatter is at most

$$
C-1.
$$

Therefore there can be at most $$C-1$$ linearly independent discriminant directions.

This is a fundamental difference between discriminant analysis and generic variance-preserving dimensionality reduction.

---

# Lecture 18 — Multiple Discriminant Analysis (Tutorial)

## 1. Tutorial viewpoint

The practical objective is to compute the discriminant projection from data.

Typical workflow:

1. Separate training samples class-wise.
2. Compute each class mean.
3. Compute the overall mean.
4. Compute within-class scatter.
5. Compute between-class scatter.
6. Solve the generalized eigenvalue problem.
7. Select the leading eigenvectors.
8. Project the data.

---

## 2. Class means

For class $$i$$,

$$
\boldsymbol{\mu}_i
=
\frac{1}{N_i}
\sum_{\mathbf{x}\in\omega_i}
\mathbf{x}.
$$

The overall mean is

$$
\boldsymbol{\mu}
=
\frac{1}{N}
\sum_i
N_i\boldsymbol{\mu}_i.
$$

---

## 3. Within-class covariance/scatter

One can form covariance-like quantities

$$
\Sigma_i
=
\frac{1}{N_i}
\sum_{\mathbf{x}\in\omega_i}
(\mathbf{x}-\boldsymbol{\mu}_i)
(\mathbf{x}-\boldsymbol{\mu}_i)^T.
$$

Depending on convention, scatter matrices may omit normalization.

For discriminant directions, the relative scaling matters more than the particular normalization convention.

---

## 4. Interpretation of the generalized eigenvectors

Each eigenvector gives a direction in the original feature space.

Projection along that direction produces a scalar:

$$
y=\mathbf{w}^T\mathbf{x}.
$$

The leading directions are those that best trade off class separation against within-class spread.

---

## 5. Two-class special case

For two classes, only one independent discriminant direction is needed.

The direction is proportional to

$$
\mathbf{w}
\propto
S_W^{-1}
(\boldsymbol{\mu}_1-\boldsymbol{\mu}_2).
$$

Thus the projection effectively looks in the direction that best separates the class means after correcting for within-class covariance.

---

# Lecture 19 — Multiple Discriminant Analysis (Tutorial)

## 1. Multi-class projection

For more than two classes, several discriminant directions may be useful.

Collect the leading eigenvectors:

$$
W
=
[\mathbf{w}_1,\mathbf{w}_2,\ldots,\mathbf{w}_r].
$$

Then

$$
\mathbf{y}=W^T\mathbf{x}.
$$

This creates a lower-dimensional discriminant feature space.

---

## 2. Why this projection is supervised

MDA uses class labels in the construction of $$S_W$$ and $$S_B$$.

Therefore it is a supervised dimensionality-reduction method.

This contrasts with methods such as PCA, which primarily consider the total covariance of the data without using class identities.

---

## 3. Geometric interpretation

MDA attempts to rotate and project the original feature space so that:

- observations belonging to the same class become compact;
- observations belonging to different classes become separated.

Thus the reduced coordinates are explicitly chosen to support discrimination.

---

## 4. Classification after MDA

After projection, classification can be performed in the reduced space.

The complete pipeline becomes

$$
\mathbf{x}
\rightarrow
W^T\mathbf{x}
\rightarrow
\mathbf{y}
\rightarrow
\text{classifier}.
$$

The benefit is that the classifier operates in fewer dimensions while retaining class-discriminative structure.

---

# Lecture 20 — Perceptron Criterion

## 1. Linear discriminant functions

A linear classifier represents a discriminant function as

$$
g(\mathbf{x})
=
\mathbf{w}^T\mathbf{x}+b.
$$

Often a bias term is absorbed into an augmented vector:

$$
\tilde{\mathbf{x}}
=
\begin{bmatrix}
\mathbf{x}\\
1
\end{bmatrix},
\qquad
\tilde{\mathbf{w}}
=
\begin{bmatrix}
\mathbf{w}\\
b
\end{bmatrix}.
$$

Then

$$
g(\mathbf{x})
=
\tilde{\mathbf{w}}^T
\tilde{\mathbf{x}}.
$$

---

## 2. Two-class encoding

For convenience, encode classes using labels such as

$$
y_i\in\{+1,-1\}.
$$

A sample is correctly classified when

$$
y_i g(\mathbf{x}_i)>0.
$$

It is misclassified when

$$
y_i g(\mathbf{x}_i)<0.
$$

The quantity

$$
y_i g(\mathbf{x}_i)
$$

is therefore a signed measure of classification correctness.

---

## 3. Perceptron criterion

The perceptron criterion focuses on misclassified samples.

A standard form is

$$
J_P(\mathbf{w})
=
-\sum_{\mathbf{x}_i\in\mathcal{M}}
y_i\mathbf{w}^T\mathbf{x}_i,
$$

where $$\mathcal{M}$$ is the set of currently misclassified patterns.

For every misclassified point,

$$
y_i\mathbf{w}^T\mathbf{x}_i<0,
$$

so its contribution to the criterion is positive.

The objective is to find weights that make the criterion zero.

---

## 4. Gradient of the criterion

For a fixed set of misclassified samples,

$$
\nabla J_P(\mathbf{w})
=
-\sum_{\mathbf{x}_i\in\mathcal{M}}
y_i\mathbf{x}_i.
$$

A gradient-descent step is

$$
\mathbf{w}_{k+1}
=
\mathbf{w}_k
-
\eta
\nabla J_P(\mathbf{w}_k),
$$

which gives

$$
\mathbf{w}_{k+1}
=
\mathbf{w}_k
+
\eta
\sum_{\mathbf{x}_i\in\mathcal{M}}
y_i\mathbf{x}_i.
$$

This explains the classical perceptron correction rule.

---

## 5. Sequential perceptron update

For a single misclassified sample,

$$
\mathbf{w}_{k+1}
=
\mathbf{w}_k
+
\eta y_i\mathbf{x}_i.
$$

Thus:

- positive-class misclassification pushes the boundary toward classifying that point as positive;
- negative-class misclassification pushes it in the opposite direction.

---

## 6. Augmented representation

Bias can be included in the vector.

Let

$$
\tilde{\mathbf{x}}
=
[\mathbf{x}^T,1]^T.
$$

Then the decision is

$$
\operatorname{sign}
(
\tilde{\mathbf{w}}^T\tilde{\mathbf{x}}
).
$$

An update becomes

$$
\tilde{\mathbf{w}}_{k+1}
=
\tilde{\mathbf{w}}_k
+
\eta y_i\tilde{\mathbf{x}}_i.
$$

This is particularly convenient for derivations and implementations.

---

## 7. Separability

The perceptron algorithm is guaranteed to find a separating hyperplane if the training data are linearly separable.

If the data are not linearly separable, the plain perceptron can continue making updates without converging to zero training error.

Therefore the perceptron criterion is intimately connected with the geometry of linear separability.

---

# Lecture 21 — Perceptron Criterion (Continued.)

## 1. Criterion-based viewpoint

The perceptron is not merely an update rule.

It can be viewed as an optimization procedure for a criterion that penalizes misclassified samples.

This perspective is useful because many learning algorithms can be understood as:

$$
\text{define loss/criterion}
\rightarrow
\text{differentiate}
\rightarrow
\text{optimize parameters}.
$$

---

## 2. Why only misclassified patterns matter

For correctly classified points,

$$
y_i\mathbf{w}^T\mathbf{x}_i>0.
$$

The perceptron criterion does not need to penalize these points once they are on the correct side.

Therefore the learning signal comes from the mistakes.

This differs from objectives such as squared error, which typically continue assigning a numerical penalty even to correctly classified but imperfectly fitted samples.

---

## 3. Batch and sequential forms

### Batch update

Collect all misclassified samples:

$$
\mathcal{M}
=
\{i:y_i\mathbf{w}^T\mathbf{x}_i\leq0\}.
$$

Then update:

$$
\mathbf{w}_{k+1}
=
\mathbf{w}_k
+
\eta
\sum_{i\in\mathcal{M}}
y_i\mathbf{x}_i.
$$

### Sequential update

Process one pattern at a time:

$$
\mathbf{w}_{k+1}
=
\mathbf{w}_k
+
\eta y_i\mathbf{x}_i
$$

only when sample $$i$$ is misclassified.

The sequential form is the classic perceptron learning rule.

---

## 4. Geometric interpretation of the update

Consider a positive sample that is incorrectly classified:

$$
\mathbf{w}^T\mathbf{x}<0,
\qquad y=+1.
$$

The update is

$$
\mathbf{w}'=\mathbf{w}+\eta\mathbf{x}.
$$

Then

$$
\mathbf{w}'^T\mathbf{x}
=
\mathbf{w}^T\mathbf{x}
+
\eta\|\mathbf{x}\|^2.
$$

The score of the misclassified point therefore increases.

For a negative misclassification,

$$
y=-1,
$$

and the update is

$$
\mathbf{w}'=\mathbf{w}-\eta\mathbf{x},
$$

which decreases the score of that point.

Thus the update directly tries to push each error across the decision boundary.

---

## 5. Perceptron convergence intuition

For linearly separable data, suppose there exists a vector $$\mathbf{w}^*$$ satisfying

$$
y_i{\mathbf{w}^*}^T\mathbf{x}_i>0
$$

for every training sample.

Under the standard perceptron assumptions, repeated updates eventually stop making mistakes.

The convergence result depends on linear separability. It does **not** say that perceptron necessarily converges for arbitrary data.

---

## 6. What the perceptron does not optimize

The perceptron criterion is fundamentally concerned with classification correctness.

It is not directly minimizing:

- squared reconstruction error,
- posterior probability error,
- margin maximization,
- probabilistic negative log-likelihood.

Those correspond to different learning criteria.

This distinction is important because changing the criterion changes the learning behavior.

---

# Cross-Lecture Connections

## 1. The complete statistical pattern-recognition pipeline

The first 21 lectures develop a coherent progression:

$$
\boxed{
\text{Pattern}
\rightarrow
\text{Features}
\rightarrow
\text{Feature vector}
\rightarrow
\text{Probability model}
\rightarrow
\text{Bayesian decision}
\rightarrow
\text{Dimensionality reduction}
\rightarrow
\text{Linear classifier}
}
$$

The course is therefore not presenting disconnected algorithms. Each topic solves a limitation introduced by the previous stage.

---

## 2. Features create the space in which classification happens

Raw data are usually difficult to classify directly.

Feature extraction creates

$$
\mathbf{x}
\rightarrow
\mathbf{z}.
$$

All subsequent statistical operations act on $$\mathbf{z}$$.

Therefore a bad feature representation can limit any classifier, regardless of how sophisticated the classifier is.

---

## 3. Bayesian classification requires a density model

Once feature vectors are available, Bayesian classification asks:

$$
\text{Which class most likely generated this feature vector?}
$$

That requires

$$
p(\mathbf{x}\mid\omega_i)
$$

and

$$
P(\omega_i).
$$

When the density is assumed Gaussian, the problem becomes a parametric estimation problem.

When the density is unknown, non-parametric estimation is introduced.

---

## 4. Density estimation creates the dimensionality problem

Non-parametric methods rely on local neighborhoods.

But the number of samples needed to represent local neighborhoods grows rapidly with dimensionality.

This leads naturally to:

$$
\text{density estimation}
\rightarrow
\text{curse of dimensionality}
\rightarrow
\text{dimensionality reduction}.
$$

---

## 5. MDA attacks dimensionality using class information

MDA uses:

$$
S_W
$$

to measure within-class spread and

$$
S_B
$$

to measure between-class separation.

The goal is therefore not simply to preserve arbitrary variance.

It is to preserve **discriminative information**.

---

## 6. Perceptron shifts the focus from probabilistic modeling to discriminative learning

Bayesian methods model how data are generated by each class.

The perceptron instead directly learns a decision boundary:

$$
\mathbf{w}^T\mathbf{x}+b=0.
$$

So there is a conceptual transition:

$$
\text{generative/statistical modeling}
\rightarrow
\text{direct discriminative classification}.
$$

---

# Important Formula Sheet

## Bayes theorem

$$
P(\omega_i\mid\mathbf{x})
=
\frac{
p(\mathbf{x}\mid\omega_i)P(\omega_i)
}{
\sum_j p(\mathbf{x}\mid\omega_j)P(\omega_j)
}.
$$

## Minimum-error Bayes rule

$$
\text{decide }\omega_i
\quad\text{if}\quad
p(\mathbf{x}\mid\omega_i)P(\omega_i)
>
p(\mathbf{x}\mid\omega_j)P(\omega_j)
\quad\forall j\neq i.
$$

## Conditional risk

$$
R(\alpha_i\mid\mathbf{x})
=
\sum_j
\lambda(\alpha_i\mid\omega_j)
P(\omega_j\mid\mathbf{x}).
$$

## Multivariate Gaussian density

$$
p(\mathbf{x}\mid\omega_i)
=
\frac{1}{
(2\pi)^{d/2}|\Sigma_i|^{1/2}
}
\exp
\left[
-\frac12
(\mathbf{x}-\boldsymbol{\mu}_i)^T
\Sigma_i^{-1}
(\mathbf{x}-\boldsymbol{\mu}_i)
\right].
$$

## Gaussian discriminant

$$
g_i(\mathbf{x})
=
-\frac12\ln|\Sigma_i|
-\frac12
(\mathbf{x}-\boldsymbol{\mu}_i)^T
\Sigma_i^{-1}
(\mathbf{x}-\boldsymbol{\mu}_i)
+
\ln P(\omega_i).
$$

## Mahalanobis distance

$$
D_i^2(\mathbf{x})
=
(\mathbf{x}-\boldsymbol{\mu}_i)^T
\Sigma_i^{-1}
(\mathbf{x}-\boldsymbol{\mu}_i).
$$

## MLE

$$
\hat{\boldsymbol{\theta}}
=
\arg\max_{\boldsymbol{\theta}}
\prod_{n=1}^{N}
p(\mathbf{x}_n\mid\boldsymbol{\theta}).
$$

## Log-likelihood

$$
\ell(\boldsymbol{\theta})
=
\sum_{n=1}^{N}
\ln p(\mathbf{x}_n\mid\boldsymbol{\theta}).
$$

## Gaussian mean MLE

$$
\hat{\boldsymbol{\mu}}
=
\frac1N
\sum_{n=1}^{N}\mathbf{x}_n.
$$

## Gaussian covariance MLE

$$
\hat{\Sigma}
=
\frac1N
\sum_{n=1}^{N}
(\mathbf{x}_n-\hat{\boldsymbol{\mu}})
(\mathbf{x}_n-\hat{\boldsymbol{\mu}})^T.
$$

## Parzen-window density estimate

$$
\hat{p}(\mathbf{x})
=
\frac{1}{Nh^d}
\sum_{n=1}^{N}
K
\left(
\frac{\mathbf{x}-\mathbf{x}_n}{h}
\right).
$$

## Nearest-neighbor density estimate

$$
\hat{p}(\mathbf{x})
=
\frac{k}{NV_k}.
$$

## MDA projection

$$
\mathbf{y}
=
W^T\mathbf{x}.
$$

## Within-class scatter

$$
S_W
=
\sum_i
\sum_{\mathbf{x}\in\omega_i}
(\mathbf{x}-\boldsymbol{\mu}_i)
(\mathbf{x}-\boldsymbol{\mu}_i)^T.
$$

## Between-class scatter

$$
S_B
=
\sum_i
N_i
(\boldsymbol{\mu}_i-\boldsymbol{\mu})
(\boldsymbol{\mu}_i-\boldsymbol{\mu})^T.
$$

## Fisher criterion

$$
J(\mathbf{w})
=
\frac{
\mathbf{w}^TS_B\mathbf{w}
}{
\mathbf{w}^TS_W\mathbf{w}
}.
$$

## Generalized eigenvalue equation

$$
S_B\mathbf{w}
=
\lambda S_W\mathbf{w}.
$$

## Perceptron discriminant

$$
g(\mathbf{x})
=
\mathbf{w}^T\mathbf{x}+b.
$$

## Correct-classification condition

$$
y_i g(\mathbf{x}_i)>0.
$$

## Perceptron update

$$
\mathbf{w}_{k+1}
=
\mathbf{w}_k
+
\eta y_i\mathbf{x}_i
$$

for a misclassified sample.

---

# Conceptual Map for Revision

### Stage 1: Representation

**Lectures 1–4**

$$
\text{raw pattern}
\rightarrow
\text{features}
\rightarrow
\text{feature vector}.
$$

Key questions:

- What information should be retained?
- What should be invariant?
- How many features are needed?
- Which properties distinguish the classes?

### Stage 2: Statistical decision theory

**Lectures 5–9**

$$
p(\mathbf{x}\mid\omega_i),\quad P(\omega_i)
\rightarrow
P(\omega_i\mid\mathbf{x})
\rightarrow
\text{decision}.
$$

Key questions:

- What is the probability a class generated the observation?
- How should priors affect the decision?
- How does the shape of a Gaussian density influence the boundary?
- What changes when features are binary?

### Stage 3: Estimating the unknown distribution

**Lectures 10–15**

$$
\text{training data}
\rightarrow
\text{density/parameter estimation}.
$$

Key questions:

- What if the class distributions are unknown?
- How can their parameters be estimated?
- How can a density be estimated without assuming a parametric form?
- Why does high dimension make local density estimation difficult?

### Stage 4: Reducing dimensionality using class information

**Lectures 16–19**

$$
\mathbf{x}
\rightarrow
W^T\mathbf{x}.
$$

Key questions:

- How can dimension be reduced?
- What is the difference between within-class and between-class variation?
- Why can the discriminant subspace have at most $$C-1$$ dimensions?

### Stage 5: Direct discriminative learning

**Lectures 20–21**

$$
\mathbf{w}^T\mathbf{x}+b=0.
$$

Key questions:

- How can a linear classifier be learned directly?
- What criterion should be optimized?
- Why do perceptron updates only respond to misclassified points?
- Under what condition does perceptron converge?

---

# Lecture-to-Lecture Dependency Graph

$$
\text{Feature Extraction}
\rightarrow
\text{Bayes Decision Theory}
\rightarrow
\text{Gaussian Models}
\rightarrow
\text{Parameter Estimation}
\rightarrow
\text{Non-parametric Density Estimation}
\rightarrow
\text{Curse of Dimensionality}
\rightarrow
\text{MDA}
\rightarrow
\text{Perceptron}.
$$

A useful way to remember the logic is:

> First decide **how to represent** a pattern.  
> Then decide **how to classify** it.  
> Then ask **how to learn the unknown probability model**.  
> Then ask **how to deal with high dimensionality**.  
> Finally, learn a classifier **directly from classification errors**.

---

# Source / Course Reference

These notes are based on the NPTEL **Pattern Recognition and Application** course by Prof. Prabir Kumar Biswas, IIT Kharagpur, course code **117105101**. The official NPTEL lecture listing identifies Lectures 1–21 as:

1. Introduction
2. Feature Extraction - I
3. Feature Extraction - II
4. Feature Extraction - III
5. Bayes Decision Theory
6. Bayes Decision Theory (Continued.)
7. Normal Density and Discriminant Function
8. Normal Density and Discriminant Function (Continued.)
9. Bayes Decision Theory - Binary Features
10. Maximum Likelihood Estimation
11. Probability Density Estimation
12. Probability Density Estimation (Continued.)
13. Probability Density Estimation (Continued.)
14. Probability Density Estimation (Continued.)
15. Probability Density Estimation (Continued.)
16. Dimensionality Problem
17. Multiple Discriminant Analysis
18. Multiple Discriminant Analysis (Tutorial)
19. Multiple Discriminant Analysis (Tutorial)
20. Perceptron Criterion
21. Perceptron Criterion (Continued.)

The official course syllabus groups these topics into feature extraction, Bayes decision theory, density estimation, dimensionality reduction, and perceptron criteria.

