---
title: "Need for score networks"
lastmod: 2026-09-06
---

Start with langevin dynamics and why we need it?
Why given a score network we need the dynamics to sample p(x)?
- we talk about the interplay of drift due to score and the randomness due to the brownian motion in the reverse SDE.
- We show that given only the score of a dist, we can effectively sample from it even though the score only leads us to a mode of the distribution.

Now we talk about how we don't even have access to the score of the true data distribution and only the samples of data. So what do we do?
- Enters the score matching(with trace - [Estimation of Non-Normalized Statistical Models by Score Matching](https://jmlr.org/papers/v6/hyvarinen05a.html))
- But this fails for higher dimensions.
- Enter denoising score matching
- NCSNs
- I can learn the score of every smoothed distribution, and the smoothed distributions form a path whose endpoint approaches the distribution I actually care about
- ![](/vault/blogs/attachments/need-for-score-networks-1788690760743.webp)
- NCSN learns the score fields of a hierarchy of Gaussian-smoothed KDEs.

Next question would be: Why does following these learned score fields from large $\sigma$ down to small $\sigma$ actually give a good approximation to sampling from the underlying $p_{\rm data}$, especially in high dimensions where KDE itself is notoriously problematic? This is the main principle behind why Diffusion iterative process works.
 - [Why Iterative Reverse Sampling Recovers the Data Distribution?](/vault/blogs/why-iterative-reverse-sampling-recovers-the-data-distribution/)

