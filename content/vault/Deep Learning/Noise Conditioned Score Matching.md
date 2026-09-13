---
title: "Noise Conditioned Score Matching"
lastmod: 2026-09-06
---

Refer: [Noise Conditional Score Networks (NCSN)](https://www.emergentmind.com/topics/noise-conditional-score-networks-ncsn)

Noise Conditional Score Networks (NCSN) are generative models that approximate the gradient of the log density of noise-perturbed data using denoising score matching.


NCSN is **not trying to approximate the true data score with a noisy, arbitrarily blurred approximation and then hoping it works**. It is deliberately learning the exact score of a family of smoothed distributions $p_\sigma$, and the iterative procedure is designed to move through that family back toward $p_{\text{data}}$.