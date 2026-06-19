---
title: "KSD for Goodness-of-fit Tests"
lastmod: 2026-06-11
---

[Reproducing Kernel Hilbert Space (RKHS)](/vault/research-work/btp/reproducing-kernel-hilbert-space-rkhs/)
### What is a Goodness of Fit Test?
The **goodness of fit** of a [statistical model](https://en.wikipedia.org/wiki/Statistical_model "Statistical model") describes how well it fits a set of observations. Measures of goodness of fit typically summarize the discrepancy between observed values and the values expected under the model in question.


## Contributions
- New discrepancy statistic  for measuring differences between two distribution.
- derive a new class of powerful goodness-of-fit tests that are widely applicable for complex and high dimensional distributions, even for those with computationally intractable normalization constants. other traditional goodness-of-fit tests, such as χ2test and Kolmogorov-Smirnov test, can not be applied.
- likehood free 

### Problems
- Traditional approaches often involve calculating or comparing the likelihoods or cumulative distribution functions (CDF) of the models.
- Computationally intractable likelihoods or CDFs coz Z(normalisation constant is intractable) for these high dim models. Approx methods lead to large errors which make it difficult to give results with statistical significance.


![](/vault/research-work/btp/attachments/pasted-image-20260611015745.png)

The paper proposes an alternative that does not care about $Z$. Instead of using the absolute likelihood, it uses the **Stein score function**:

$$s_q(x) = \nabla_x \log q(x)$$

Because the score function takes the derivative of a logarithm, the constant scales drop out entirely ($s_q = \nabla_x \log f(x)$), making it highly efficient to calculate even when the likelihood itself cannot be computed.

## 3. Combining Stein's Identity with RKHS
The mathematical machinery relies on combining two advanced concepts:
### Stein’s Identity
Two smooth probability densities $p$ (your data) and $q$ (your model) are identical if and only if the expectation of the Stein operator equals zero for smooth functions with proper boundary conditions:
$$\mathbb{E}_p[s_q(x)f(x) + \nabla_x f(x)] = 0$$
Using this, you can create a **Stein Discrepancy**. The problem is that searching for the optimal function $f(x)$ normally requires an impossible variational optimization.

#### The Classical Stein Discrepancy
Using integration by parts, we can verify Stein's identity. Consequently, we can formally define a **Stein discrepancy measure** between an observed data distribution $p$ and a target model distribution $q$ as follows:
$$\mathbb{S}(p,q) = \max_{f \in \mathcal{F}} \left( \mathbb{E}_p \left[ s_q(x)f(x) + \nabla_x f(x) \right] \right)^2 \qquad (2)$$
Here, $\mathcal{F}$ represents a functional family composed of smooth functions that strictly satisfy the zero-boundary conditions required by Stein's identity. To serve as a valid statistical distance metric, this function class $\mathcal{F}$ must also be mathematically **rich enough** to guarantee that the resulting discrepancy score is strictly positive ($\mathbb{S}(p,q) > 0$) whenever the actual data distribution deviates from the model ($p \neq q$).
### The RKHS Solution
The authors elegantly solve this optimization bottleneck by restricting the search function $f(x)$ to a unit ball within a [Reproducing Kernel Hilbert Space (RKHS)](/vault/research-work/btp/reproducing-kernel-hilbert-space-rkhs/) associated with a smooth positive definite kernel $k(x, x')$.

By enforcing this boundary, the infinite mathematical optimization completely collapses into a clean, closed-form expectation of a single function, **$u_q(x, x')$**:

$$\mathbb{S}(p, q) = \mathbb{E}_{x, x' \sim p}[u_q(x, x')]$$




## 4. Practical Execution via U-Statistics

Because the final metric relies entirely on the expectation of $u_q(x, x')$, it can be efficiently estimated from real-world data samples using a **U-statistic**:

$$\hat{\mathbb{S}}_u(p,q) = \frac{1}{n(n-1)}\sum_{i\neq j}u_q(x_i, x_j)$$

The paper notes that under the null hypothesis ($H_0: p=q$), this statistic is degenerate. To determine the classification threshold without analytical limits, the paper introduces a **Bootstrap Goodness-of-fit Test** (Algorithm 1) to simulate the ideal distribution and establish strict confidence controls.








> **Definition 3.4**. A kernel k(x, x′) is said to be in the Stein class of p if k(x, x′) has continuous second order partial derivatives, and both k(x, ·) and k(·, x) are in the Stein class of p for any fixed x


*what is the $u_{q}$ function?*
The "$u$ function" you are referring to—written in the paper as $u_q(x, x')$—is the **core mathematical engine** of the Kernelized Stein Discrepancy (KSD).
The function $u_q(x, x')$ is a **pairwise discrepancy evaluator**. It takes two separate transaction data points, $x$ and $x'$, and measures how much their joint behavior conflicts with your target model $q$.
According to **Theorem 3.6** in the paper, the $u$ function is explicitly defined as:
$$u_q(x,x') = s_q(x)^\top k(x,x') s_q(x') + s_q(x)^\top \nabla_{x'} k(x,x') + \nabla_x k(x,x')^\top s_q(x') + \text{trace}(\nabla_{x,x'} k(x,x'))$$

This looks intimidating, but it breaks down into four intuitive, computable parts:

| **Part**                       | **Formula Component**                 | **What it Measures in Layman Terms**                                                                                                                |
| ------------------------------ | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Score-Score Interaction** | $s_q(x)^\top k(x,x') s_q(x')$         | Scales the directional probability changes (scores) of both transactions by how geometrically similar ($k$) the two transactions are to each other. |
| **2. Cross-Gradient (Left)**   | $s_q(x)^\top \nabla_{x'} k(x,x')$     | Checks how the model's score at transaction $x$ aligns with the direction you need to move transaction $x'$ to make them more similar.              |
| **3. Cross-Gradient (Right)**  | $\nabla_x k(x,x')^\top s_q(x')$       | The exact symmetric mirror of Part 2 (swapping the roles of $x$ and $x'$).                                                                          |
| **4. Kernel Hessian Trace**    | $\text{trace}(\nabla_{x,x'} k(x,x'))$ | Measures the pure architectural smoothness of your chosen kernel function across the two data coordinates, completely independent of your model.    |


# Main GoF Part
**Theorem 4.1** is the mathematical foundation for how you actually make a "True" vs. "False" decision in your fraud detection project.
It tells us exactly what the calculated fraud score ($\hat{\mathbb{S}}_u$) will look like under two different scenarios: when the transactions are **Fake/Fraudulent** ($p \neq q$) , and when the transactions are **Legitimate/True** ($p = q$).
### Step 1: The Conditions (The Setup)
Before diving into the two cases, the theorem states the ground rules:
- You are using a valid, smooth similarity metric (the kernel $k(x,x')$).
- The expected variance of your pairwise score ($u_q$) is finite, meaning your data isn't so wild and infinite that it breaks standard math rules.
### Step 2: Case 1 — When the Data is FRAUD ($p \neq q$)

> _"If $p \neq q$, then $\hat{\mathbb{S}}_u(p,q)$ is asymptotically normal..."_

If the incoming transactions ($p$) do not match your model of legitimate behavior ($q$), it means you are looking at fraud.

$$\sqrt{n}(\hat{\mathbb{S}}_u(p,q) - \mathbb{S}(p,q)) \xrightarrow{d} \mathcal{N}(0, \sigma_u^2)$$

- **The Shape:** As you collect more transactions ($n$ grows), your calculated fraud score behaves beautifully like a standard **Normal Distribution (a Bell Curve)**.
    
- **The Average:** The score will center around the _true theoretical discrepancy_ $\mathbb{S}(p,q)$. Because the data is fraudulent, this value is guaranteed to be a solid, positive number significantly higher than zero.
    
- **The Variance ($\sigma_u^2 \neq 0$):** The score has a regular, measurable amount of spread or variance.
    

**What this means for your project:** Fraudulent transactions are predictable. They will reliably produce high, positive scores that sit neatly on a standard bell curve far away from zero, making them easy to spot if you have a decent sample size.

### Step 3: Case 2 — When the Data is LEGITIMATE ($p = q$)

> _"If $p = q$, then we have $\sigma_u^2 = 0$ (the U-statistics is degenerate)..."_

This is where the math gets fascinating. If the incoming transactions are perfectly clean and match your legitimate model ($p=q$), the regular variance collapses to absolute zero ($\sigma_u^2 = 0$). In statistics, this is called a **degenerate** state.

Because the standard bell curve collapses, the formula changes entirely:

$$n\hat{\mathbb{S}}_u(p,q) \xrightarrow{d} \sum_{j=1}^{\infty} c_j(Z_j^2 - 1)$$

- **$Z_j^2 - 1$:** The letter $Z$ represents standard normal variables. When you square them ($Z^2$), they form a **Chi-squared ($\chi^2$) distribution**.
    
- **The Sum ($\sum$):** Instead of a neat bell curve, your clean data forms an infinite, weighted sum of these shifted Chi-squared distributions.
    
- **The Weights ($c_j$):** The values $c_j$ are eigenvalues that depend on your specific transaction model and kernel. They act as weights, determining how heavily each piece of random noise skews the final score.
    

**What this means for your project:** Clean data does _not_ look like a normal bell curve. It produces very small numbers that bunch up close to zero with a skewed, long tail on the right side.

### Step 4: The Core Problem This Creates

Because Case 2 results in that nasty, infinite sum of Chi-squared variables ($\sum c_j(Z_j^2 - 1)$), **you cannot look up a threshold in a standard math textbook table** to say "any score above 2.5 is fraud". The shape changes depending on your exact data types and your model's parameters ($c_j$).

### Step 5: How Algorithm 1 Fixes It

This exact theorem is the entire reason the authors invented the **Bootstrap test (Algorithm 1)** later in the paper.

Since you can't calculate that infinite sum of Chi-squared shapes analytically, you use the bootstrap weights to simulate that exact formula ($n\hat{\mathbb{S}}_u^*$) directly on your computer. This lets you generate an empirical "cutoff line" customized perfectly to your legitimate transaction data.




# Figures
![](/vault/papers/attachments/pasted-image-20260525004130.png)
