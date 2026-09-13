---
title: "Reason Behind the Creativity of Diffusion Models"
lastmod: 2026-08-18
---


Diffusion based generation process works on the principle of guiding functions called score functions. Think of these score functions as force fields which push samples in the data space towards the data manifold.

The goal of Diffusion training is to learn this score function but not perfectly. Why? A perfect replication of the score function would lead to exact generation of the training samples and won't serve our goal of sensible novel generations. Hence while training due to both implicit and explicit regularisation of the neural networks , a smoother estimate of the score function is learnt. This is called **Score Smoothening**.


Real and useful data in the high dimensional space has been hypothesised to lie of manifolds and the training data are essentially sampled points from that manifold. The diffusion process essentially learns a score function which exerts lesser force along the direction parallel/tangetial to the data manifold(compared to the ideal score for perfect training data recovery) and in the direction perpendicular to the manifold it stays similar to the normal score only.

That is, the learnt score function should be able to push the noisy intial points to the data manifold but doesn't exert too much force along the manifold to lead them to the exact training data samples. The final position of the tranformed points on the manifold is essentially an well interpolated point from the training samples and hence the generated sample is also sensible and recognisable.