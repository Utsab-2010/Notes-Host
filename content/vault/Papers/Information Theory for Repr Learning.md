---
title: "Information Theory for Repr Learning"
---

The weight of evidence regarding a particular hypothesis over the other(defined hre as prob distributiosns) is just log p/q. that is log of the ratios of the posteriors.

KL Divergence can be thought of as the expected weight of evidence

VAEs . world P is what we build, world Q is desirable. Taking kl divergence gives us just the VAE architecture
![](/vault/papers/attachments/pasted-image-20260403200028.png)

![](/vault/papers/attachments/pasted-image-20260403200142.png)

### Variational Information Bottleneck
![](/vault/papers/attachments/pasted-image-20260403201220.png)
repr without augmentated variations of inputs
![](/vault/papers/attachments/pasted-image-20260403201252.png)
if you express each input as a new random variatble you can encode a much richer set of relationships like heirarchies,etc.


So everythign is KL, it was always KL!
what about the other distances?
- Other distances like the Wasserstein distance are not reparameterisation invariant. KL is. so more convinient to think about.