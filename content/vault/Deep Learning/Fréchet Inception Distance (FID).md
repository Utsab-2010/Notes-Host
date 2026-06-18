---
title: "Fréchet Inception Distance (FID)"
---

#compvis #diffusion 
## The Problem It Solves

You've trained a generative model — a GAN, a diffusion model, whatever — and it's producing images. How do you know if they're _good_? You can look at them, sure, but that doesn't scale. You need a number.

Early metrics like **Inception Score (IS)** tried to answer this, but they had a blind spot: they only looked at the _generated_ images. They had no idea what real images looked like. A model hallucinating sharp, confident-looking nonsense could still score well.

FID fixes this by comparing generated images _directly against real ones_.

---

## The Core Idea

FID asks: **how far apart are the distributions of real images and generated images?**

Not pixel-by-pixel. Not even image-by-image. It works at the level of _distributions_ — the statistical shape of where images tend to live in some feature space.

The pipeline is:
1. Take a large batch of **real images** and a large batch of **generated images**
2. Pass both through a pretrained **Inception v3** network, and extract activations from an intermediate layer (the pool3 layer, ~2048-dimensional)
3. Now you have two clouds of points in 2048-dimensional space — one for real, one for generated
4. Fit a **multivariate Gaussian** to each cloud: compute the mean $\mu$ and covariance matrix $\Sigma$
5. Measure the distance between the two Gaussians using the **Fréchet distance** (also called the Wasserstein-2 distance between Gaussians)

The formula:

$$ \text{FID} = |\mu_r - \mu_g|^2 + \text{Tr}\left(\Sigma_r + \Sigma_g - 2(\Sigma_r \Sigma_g)^{1/2}\right) $$

Where subscripts $r$ and $g$ denote real and generated distributions respectively.
**Lower FID = generated distribution closer to real = better model.**

---
## Why Inception Features?

*Raw pixels are a terrible space to measure distance in*. Two images that look nearly identical to a human can be far apart in pixel space (think: a tiny shift or brightness change). Inception features are a much better proxy for _perceptual_ similarity — the network has learned to encode semantically meaningful structure.

The choice of Inception v3 is somewhat arbitrary and historical — it was the standard image classifier when FID was introduced (2017). This is also one of FID's known weaknesses (more on that below).

---
## Why Gaussians?
Fitting a Gaussian to a cloud of 2048-dimensional points is a massive simplifying assumption. Real image distributions are almost certainly _not_ Gaussian. But:

- It makes the distance analytically tractable (there's a closed-form formula)
- In practice, it captures enough structure — mean captures the "average content," covariance captures the "variety and correlations"
- It's computationally feasible

The Fréchet distance between two Gaussians has this nice closed form precisely because of the Gaussian assumption. Without it, you'd need something like a full Wasserstein computation, which is intractable at this scale.

---

## What FID Captures
FID is sensitive to both:
- **Fidelity** — are generated images realistic? If the model generates blurry or incoherent images, the generated feature cloud will look different from the real one.
- **Diversity** — does the model cover the full distribution? If a model only generates one type of image (mode collapse), its covariance will be much smaller than the real covariance, and FID will penalize this.

This dual sensitivity is what makes FID better than Inception Score, which could be fooled by a model with high confidence but low diversity.

---
## Known Limitations

- **It assumes Gaussians.** The Gaussian approximation is a convenience, not a truth. For complex, multimodal distributions this can be a lossy summary.
- **It's tied to Inception v3.** The metric inherits whatever biases Inception has — it was trained on ImageNet, so it's best calibrated for natural images. For domains like medical imaging, satellite imagery, or abstract art, the features may not be meaningful.
- **It needs a lot of samples.** FID estimates are noisy with small sample sizes. You typically need at least 10k–50k images for stable estimates. This makes it expensive to compute frequently during training.
- **It's a scalar.** A single number collapses a lot of information. Two models with the same FID can have very different failure modes — one might be diverse but slightly blurry, another might be sharp but narrow.
- **It doesn't capture fine-grained structure.** FID can miss certain types of artifacts that are perceptually obvious to humans, because the Inception features aggregate information in ways that can obscure local structure.

---

## Ideas to Ponder

- FID measures distance between _summaries_ (Gaussians) of the distributions, not the distributions themselves. What are you losing in that compression? Is a model that has the right mean and covariance but wrong higher-order statistics actually good?
    
- The choice of which Inception layer to extract from matters. Pool3 is the standard, but earlier layers capture different granularities of features. Could layer-specific FID scores give you more diagnostic information?
    
- FID doesn't tell you _why_ a model is bad. A low-diversity model and a low-fidelity model might score similarly. How would you design a metric that decomposes these two failure modes cleanly?
    
- There's a philosophical question baked in here: should we evaluate generative models by how well they match the training distribution, or by some human preference measure? These can diverge — a model might match the distribution well but produce images humans find unsatisfying, or vice versa. FID assumes the former is the right target.
    

---

## Quick Reference

| Property          | Value                                                                   |
| ----------------- | ----------------------------------------------------------------------- |
| Introduced        | Heusel et al., 2017 ("GANs Trained by a Two Time-Scale Update Rule...") |
| Lower is better   | Yes                                                                     |
| Range             | $[0, \infty)$, perfect model = 0                                        |
| Typical compute   | 10k–50k samples per evaluation                                          |
| Feature extractor | Inception v3, pool3 layer (2048-dim)                                    |
| Sensitive to      | Both fidelity _and_ diversity                                           |
