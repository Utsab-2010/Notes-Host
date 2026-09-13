---
title: "Kernel Density Estimation"
lastmod: 2026-07-27
---



Good blog: [Kernel Density Estimation](https://mathisonian.github.io/kde/)

# Definition
KDE stands for Kernel Density Estimation, a way to estimate the probability density function of a continuous random variable from a finite sample of data points.

**The core idea**: instead of binning data into discrete buckets like a histogram, you place a smooth "kernel" (usually a Gaussian) at each data point and sum them up. The result is a smooth curve estimating the underlying density, rather than a blocky, bin-dependent shape.

![](/vault/machine-learning/attachments/pasted-image-20260727184131.png)

Formally, given data points $x_1, \dots, x_n$, the KDE at a point $x$ is:

$$\hat{f}(x) = \frac{1}{nh} \sum_{i=1}^n K\left(\frac{x - x_i}{h}\right)$$

where $K$ is the kernel function (Gaussian is standard, but Epanechnikov, uniform, etc. are also used) and $h$ is the bandwidth, controlling how much each point's contribution spreads out.

![](/vault/machine-learning/attachments/pasted-image-20260727184023.png)
This is the KDE with the standard gaussian function.

# **Why it's preferred over histograms for visualization?**

![](/vault/machine-learning/attachments/pasted-image-20260727184055.png)
- No arbitrary bin edges or bin width choices that can distort the visual (histograms are sensitive to where bins start and how wide they are)
- The result is smooth and differentiable, which makes shape (modes, skew, tails) easier to read
- Assuming a good bandwidth choice, it's a more faithful estimate of the true underlying density than a histogram

**The bandwidth $h$ is the key hyperparameter**: too small and you overfit to individual points (spiky, noisy estimate), too large and you oversmooth and blur out real structure (like separate modes). Rules like Scott's rule or Silverman's rule give reasonable defaults, but for anything non-trivial it's worth eyeballing a few bandwidths.
