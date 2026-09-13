---
title: "Prof. Subhadip"
lastmod: 2026-06-21
---

@Utsab: Can you read the following two papers?
1. https://arxiv.org/abs/2304.14762: they show that hand-crafted perturbation kernels improve KSD power, so the natural next question is whether you can do strictly better by learning the perturbation...diffusion models give you a principled, expressive family of perturbation kernels (one per noise scale) with pretrained scores already attached. The main idea is: stop choosing the kernel by hand, learn it jointly with the mixture weights to maximize power directly.
2. https://arxiv.org/abs/2209.14687: This paper shows a posterior sampling strategy for inverse problems using a score model. Can we using the residual that they use for guiding the posterior sampling to generate a principled test statistic so that we can do anomaly detection using y-samples...which could be useful for inverse problems when the images are observed through a forward op.


Just to clarify, we have two problems here: 1. learn a kernel and optimal aggregation of scores at different noise levels to maximize the power of KSD 2. Do KSD in the inverse problems setting, where you have samples from y and not from x...but you want to do anomaly detection on x