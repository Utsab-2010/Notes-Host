---
title: "Diffusion Posterior Sampling for General Noisy Problems"
lastmod: 2026-07-23
---

#diffusion #inverse-problems 

## Main Contributions
- we extend diffusion solvers to efficiently handle general noisy (non)linear inverse problems via approximation of the posterior sampling.
- incorporate various measurement noise statistics such as Gaussian and Poisson, and also efficiently handle noisy nonlinear inverse problems such as Fourier phase retrieval and non-uniform deblurring.


![](/vault/attachments/pasted-image-20260720164258.png)
Some inverse problems and their solved results.

### Notes:
- In this work, they have considered the variance preserving (VP) form of the SDE (Song et al., 2021b) which is equivalent to Denoising Diffusion Probabilistic Models

# Background
![](/vault/attachments/pasted-image-20260720113203.png)
This the typical conditional score matching loss, optimising which also leads to minimization of the unconditional score matching loss. Once $θ^{*}$  is acquired through (3), one can use the approximation$\nabla _{x_t}\log p_{t}(x_t) ≃ s_{θ^∗} (x_{t}, t)$ as a plug-in estimate to replace the score function in the reverse SDE to sample from the original distribution.

we have a partial measurement y that is derived from x. When the mapping x 7→ y is many-to-one, we arrive at an ill-posed inverse problem, where we cannot exactly retrieve x. In the Bayesian framework, one utilizes p(x) as the prior, and samples from the posterior p(x|y).

![](/vault/attachments/pasted-image-20260720170339.png)
The above equation is the reverse SDE used to sample from the posterior distribution by considering the posterior of each intermediate step $x_t| y$ , which is typical of a inverse problem setting.

![](/vault/attachments/pasted-image-20260720170742.png)
Consider the above measurement model. It is clear that y and x_t do not have any explicit dependency as given in the probabiltiy graph below.
 ![](/vault/attachments/pasted-image-20260720170827.png)



![](/vault/research-work/btp/attachments/pasted-image-20260723011523.png)