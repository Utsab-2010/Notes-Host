---
title: "Learning Deep Kernels for Non-Parametric Two-Sample Tests"
lastmod: 2026-08-11
---

#statistics

# Problem Addressed
A popular way to solve two sample tests is using a metric called Maximum Mean Discrepancy (MMD), which measures the distance between the two datasets using a "kernel" (a mathematical function that measures how similar data points are to each other).
- **The problem:** Traditional kernels (like the standard Gaussian kernel) are "spatially homogeneous" or translation-invariant >> **k(x, y) = k(x−t, y −t)**. This means they apply the exact same mathematical lens everywhere across the data.
- If your data is highly complex—like images, or multi-modal data where the sub-structures change shape—these simple, rigid kernels often fail to notice the intricate differences between the two datasets, confusing them as the same. A learned deep kernel uses a neural network to extract features first, allowing the kernel to **behave differently in different parts of the space**

![840x289](/vault/research-work/btp/attachments/pasted-image-20260723004837.png)
The above contour lines show that the deep kernel treats different regions of space differently unlike the symmetric gaussian kernels. 

## What is a feature map mentioned here?
### Example 1: The Geometric 2D-to-3D Map (The Intuition)

Imagine you have data points on a 2D flat sheet of paper. Your data points are blue dots inside a circle and red dots outside the circle. You cannot draw a straight line to separate them (they are not "linearly separable").

To solve this, we can define a **feature map** (let's call it $\Phi$) that takes a 2D point $x = (x_1, x_2)$ and maps it into a 3D space: $$\Phi(x) = \left(x_1^2, \sqrt{2}x_1x_2, x_2^2\right)$$
- **How it works:** If you apply this map to all your points, it effectively bends the flat sheet of paper into a 3D bowl shape.
- **The result:** In this new 3D space, the blue points (which were in the center) are now at the bottom of the bowl, and the red points (which were on the outside) are high up on the sides. You can now easily slide a flat, 2D sheet (a hyperplane) right through the middle of the bowl to perfectly separate the red and blue points.

---
### Example 2: The Linear Logit Feature Map (From the Paper)

In the paper's ablation studies (Section 4), the authors analyze a simpler classifier-based test that uses a linear kernel defined as $k_f^{(L)}(x, y) = f(x)f(y)$.

The authors explicitly point out the feature map for this kernel: $$k_f^{(L)}(x, \cdot) = f(x)$$

- **How to read this:** The input is a raw data point $x$. **The feature map centers the kernel at $x$, transforming that data point into its corresponding classification score $f(x)$.**

---

### Example 3: The Gaussian (RBF) Feature Map (From the Paper)

The paper frequently utilizes the **Gaussian (or RBF) kernel**. For a Gaussian kernel, the feature map maps a single point $x$ into an **infinite-dimensional** function space (the RKHS): $$\Phi(x) = k(\cdot, x) = \exp\left(-\frac{1}{2\sigma^2} |\cdot - x|^2\right)$$

- **How to read this:** The dot ($\cdot$) is a placeholder waiting for an input. Basically we get a function corresponding to an input point x.
- The "feature representation" of your data point $x$ is no longer a list of numbers; **it is a continuous bell-curve (a "bump" function) centered exactly at $x$**.
    - If `your data point is x = 3, its feature representation is a Gaussian curve peaking at 3.`
    - If your data point is $x = 10$, its feature representation is a Gaussian curve peaking at 10.
    - To find the similarity between these two points in the feature space, you multiply their curves together and calculate the area of overlap.

---
### Example 4: The Deep Learning Feature Map (From the Paper)

This is the core proposal of the paper. Instead of using a fixed math formula, they use a deep neural network, **$\phi_\omega(x)$**, as a highly flexible, learned feature map.

- **How it works:** If your raw input $x$ is a complex $32 \times 32 \times 3$ image from the CIFAR dataset (which is a 3,072-dimensional vector of raw pixel values), the neural network $\phi_\omega(x)$ acts as a feature map that processes the image through convolutional layers.
- **The output:** It maps that complex image into a dense, lower-dimensional vector (for example, a 300-dimensional vector of extracted high-level features). The simple Gaussian kernel then evaluates those 300-dimensional "deep embeddings" to easily compare the images.

---
### Summary Table

|Input ($x$)|Feature Map ($\Phi$)|Feature Representation ($\Phi(x)$)|Space Dimension|
|:--|:--|:--|:--|
|**2D Point** $(x_1, x_2)$|Geometric Polynomial Map|$(x_1^2, \sqrt{2}x_1x_2, x_2^2)$|3D (Finite)|
|**Data Point** $x$|Linear Logit Map|$f(x)$|1D (Finite)|
|**Data Point** $x$|Gaussian Kernel Map|A Gaussian curve centered at $x$|Infinite|
|**CIFAR Image** $x$|Deep Neural Network $\phi_\omega$|300-dimensional feature vector|300D (Finite)|


---
In the provided paper, **$S_P$ and $S_Q$ refer to sets of independent identically distributed (i.i.d.) observed samples** drawn from two specific probability distributions, $P$ and $Q$.

Specifically:
- **$S_P = {x_i}_{i=1}^n$** represents a set of $n$ samples drawn from the distribution $P$.
- **$S_Q = {y_j}_{j=1}^m$** represents a set of $m$ samples drawn from the distribution $Q$.

These sample sets act as the fundamental data inputs used to conduct the non-parametric two-sample tests. The goal of the test is to use the samples in $S_P$ and $S_Q$ to compute an empirical test statistic—such as the empirical Maximum Mean Discrepancy (MMD)—to check the hypothesis.


# MMD
In the context of the **MMD two-sample test** described in the sources, you use a resampling method—specifically a **permutation test**—to determine whether to reject the null hypothesis ($(H_0$)) or accept the alternative ($(H_1$)).

Here is the step-by-step process:
### 1. Compute the Observed Statistic

First, you calculate your "actual" test statistic, denoted as $est$, using the **$U$-statistic estimator** on your original two datasets, $S_P$ and $S_Q$. This value represents the measured difference (discrepancy) between the two sets of samples in the feature space.

### 2. Estimate the Null Distribution (Permutation/Bootstrap)
` You assume that the null is true.`
Because the **null hypothesis** assumes the two distributions are identical ($P=Q$), the specific labels "P" and "Q" shouldn't matter; the samples are essentially **interchangeable**.
- You combine all samples from S_P and S_Q into one pool.
- You **shuffle** this pool and randomly re-assign the samples into two new "fake" datasets, $X$ and $Y$.
- You re-calculate the MMD $U$-statistic on these shuffled sets to get a "permuted" value ($permi$).
- By repeating this many times (e.g., $n_{perm} = 500$), you build a histogram that represents what the MMD value **would look like just by random chance** if the distributions were actually the same.

### 3. Calculate the p-value
You then compare your original observed statistic ($est$) against this generated distribution of permuted statistics. The **p-value** is the fraction of times a permuted statistic was greater than or equal to your original observed statistic: $$\text{p-value} = \frac{1}{n_{perm}} \sum_{i=1}^{n_{perm}} \mathbb{1}(permi \geq est)$$
### 4. The Decision Rule
To determine if you stay with the **null** or move to the **alternative**, you compare your calculated p-value to a pre-selected **significance level ($\alpha$)**, which is typically set to 0.05:
- **Reject the Null ($\implies H_1$):** If the **p-value < $\alpha$**, it means the MMD value you measured in your real data is so large that it is highly unlikely to have happened by random chance (it occurred in less than 5% of the shuffles). You conclude that the two datasets are statistically different ($P \neq Q$).
- **Fail to Reject the Null ($\implies H_0$):** If the **p-value $\geq \alpha$**, the measured difference is considered "within the realm of random noise." You do not have enough evidence to claim the distributions are different, so you stick with the assumption that they are the same ($P = Q$).


# Deep Kernel Design
Instead of looking at every part of the data space in the same uniform way, the design allows the kernel to **adapt to local structures** and variations in complex, high-dimensional datasets,.

The mathematical design of this deep kernel is built in three main layers:
- **Deep Feature Extraction:** First, raw data points ($x$ and $y$) are passed through a neural network, denoted as **$\phi_\omega$**, which extracts the most important high-level features,.
- **Feature Similarity:** A simple, standard kernel (like a **Gaussian kernel** $\kappa$) then compares these high-level features to see how similar they are,.
- **The Statistical Safeguard:** To ensure the test is always mathematically reliable, the authors add a small amount of a known **characteristic kernel** ($q$) on the raw input space as a "safeguard",.

The full formula for this design is **$k_\omega(x, y) = [(1 - \epsilon)\kappa(\phi_\omega(x), \phi_\omega(y)) + \epsilon] q(x, y)$**, where $\epsilon$ is a small weight. This specific structure ensures that the kernel is **characteristic**, meaning it is guaranteed to land on a unique "mean embedding" for every distinct probability distribution,.


# Training
![621](/vault/research-work/btp/attachments/learning-deep-kernels-for-non-parametric-two-sample-tests-1786437630257.webp)
Designed to **maximize the power of the test** by learning a feature representation that pulls the distributions apart in the feature space. The process is divided into a training phase and a testing phase to ensure the statistical validity of the results.
### Step 0: Data Splitting
Before training begins, the provided sample sets $S_P$ and $S_Q$ are split into two disjoint parts: **training sets** ($S_{tr}^P, S_{tr}^Q$) and **testing sets** ($S_{te}^P, S_{te}^Q$). This split is crucial because using the same samples to both learn the kernel and perform the test would violate the asymptotic assumptions required for a valid p-value.

### Phase 1: Training the Kernel Parameters
The goal of this phase is to optimize the parameters $\omega$, which include the neural network weights ($\phi_\omega$), the kernel lengthscales ($\sigma_\phi, \sigma_q$), and the safeguard weight ($\epsilon$).

For a specified number of iterations ($T_{max}$), the algorithm performs the following steps:
1. **Minibatch Sampling:** Draw a minibatch of samples $X$ from the training set $S_{tr}^P$ and a minibatch $Y$ from $S_{tr}^Q$.
2. **Kernel Definition:** Define the current deep kernel $k_\omega$ using the form:  
    $k_\omega(x, y) = [(1 - \epsilon)\kappa(\phi_\omega(x), \phi_\omega(y)) + \epsilon] q(x, y)$.
3. **Compute the MMD Estimator:** Calculate $M(\omega)$, the **$U$-statistic estimator** of the squared MMD between the minibatches $X$ and $Y$ using the current kernel.
4. **Compute the Variance Estimator:** Calculate $V_\lambda(\omega)$, the **regularized estimator of the MMD variance** ($\sigma_{H_1}^2$). The regularization parameter $\lambda$ is typically set to a small constant like $10^{-8}$ to ensure numerical stability.
5. **Calculate the Training Objective:** Compute the ratio:  
    **$\hat{J}_\lambda(\omega) = M(\omega) / \sqrt{V_\lambda(\omega)}$**.  
    This specific ratio (MMD over its standard deviation) is the **approximate test power**. Maximizing this ratio ensures that the learned kernel is as sensitive as possible to the differences between $P$ and $Q$.
6. **Parameter Update:** Use the **Adam optimizer** to update the parameters $\omega$ in the direction that maximizes $\hat{J}_\lambda(\omega)$.

### Phase 2: The Final Test (Testing Phase)
The learned kernel $k_\omega$ is fixed (frozen) and used to perform the actual hypothesis test on the held-out test data:
1. **Observed Statistic:** Compute the final MMD test statistic ($est$) using $k_\omega$ on the test sets $S_{te}^P$ and $S_{te}^Q$.
2. **Permutation Testing:** To determine the significance, shuffle the combined test samples repeatedly ($n_{perm}$ times) to generate a **null distribution** and calculate the final **p-value**.
3. **Decision:** If the p-value is less than the significance level $\alpha$, the null hypothesis is rejected.


