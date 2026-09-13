---
title: "BTP Notebook"
lastmod: 2026-09-06
---

# To-Dos
- [ ] Investigate Scenarios where a learnt kernel would boost the results of the pooled KSD thing with the learnt score function. 
	- Intuition is that is that for simpler distributions pooled KSD already does a lot of the heavy lifting and hence having a learnt kernel would not lead to that much noticeable benefit.
	- Also learnt kernel helped with MMD only.
- [ ] Create experiment setup with Cifar10,cifar100,svhn and their score models
	- [ ] Compute the histogram of ID and OOD sampels's test statistic using the KSD 
## Ideas
- Maybe we can do an simple ID vs OOD metric value histogram(normalised)
	- We can do it over Cifar10,  cifar100 and svhn using learnt score functions checkpoints (ref. Eigenscore paper) and check where the histograms are separable or not for our discrepancy metric.
- [\[1707.06626\] Learning to Draw Samples with Amortized Stein Variational Gradient Descent](https://arxiv.org/abs/1707.06626) - check the KL to KSD defintion here
	- Maybe we can use this to connect the KLIP paper's time integral to the KSD's pooling idea?
## Reading List
- [\[2605.31596\] KLIP: localized distribution shift detection via KL-divergence with diffusion priors in Inverse Problems](https://arxiv.org/abs/2605.31596)
- [\[2510.07206\] EigenScore: OOD Detection using Covariance in Diffusion Models](https://arxiv.org/abs/2510.07206)
- [GitHub - MuserHao/Kernel-stein-discrepancy-for-energy-based-model · GitHub](https://github.com/MuserHao/Kernel-stein-discrepancy-for-energy-based-model)
- [GitHub - Lornatang/PyTorch-NCSN: This is the best GAN method to generate cifar-10 · GitHub](https://github.com/Lornatang/PyTorch-NCSN)
- [GitHub - yang-song/score\_sde\_pytorch: PyTorch implementation for Score-Based Generative Modeling through Stochastic Differential Equations (ICLR 2021, Oral) · GitHub](https://github.com/yang-song/score_sde_pytorch)
- [\[2202.00824\] KSD Aggregated Goodness-of-fit Test](https://arxiv.org/abs/2202.00824)
- [1906.08283](https://arxiv.org/pdf/1906.08283)