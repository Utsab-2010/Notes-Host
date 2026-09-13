---
title: "Gradient-Weight Alignment as a Train-Time Proxy for Generalization in Classification Tasks"
lastmod: 2026-09-05
---

#interpretebility #learning-theory 

### Background:
- Prior work indicates that robust generalization emerges when all training samples contribute coherently towards a shared learning goal, that is, their gradients are directionally well aligned
- Conflicting directions indicate potential failures to generalise
- the average gradient alignment over the dataset provides minimal insight into individual samples’ contribution to training e.g **GSNR and other pairwise gradient based metrics** 
	- They are also computationally and memory heavy to compute during train-time.
	- **GWA resolves these issues.**

## Contributions
- GWA as a novel proxy for generalization performance during training effectively replacing the need for withholding a separate validation set.  
- GWA reveals the influence of individual training samples on optimization, providing understanding for data quality issues like outliers and label errors.


### Main Theory
GWA is inspired by theoretical work on the **directional convergence** of model weights learned by gradient flow when minimizing the cross-entropy loss \[1]. Intuitive idea is, for perfectly classifiable data, the weights not only converge in direction, but moreover the corresponding gradients converge in direction to the weights, i.e., the gradient and weights align.

> \[1\] Ziwei Ji and Matus Telgarsky. “Directional convergence and alignment in deep learning”. In:  Advances in Neural Information Processing Systems 33 (2020), pp. 17176–17186.


## Results
- analysis of CIFAR-10 reveals that samples with high positive alignment scores tend to be visually simpler, while those with negative alignments are more cluttered and/or visually challenging.
- In a fine-tuning scenario, the GWA decreases to a minima and then starts rising again. The model must first adapt to dataset-specific details, temporarily disrupting the initially strong alignment. After a few epochs, this trend reverses.


### Relation to Gradient Norm
- we observe weak overall correlation between the per-sample gradient norms and our alignment scores **γi**
- We observe that particularly at the end of training, higher relative gradient norm correlate with lower alignment scores -- indicating orthogonal updates.
	- In the **ConvNeXt** exp: a group of samples exhibits the smallest gradient norm and low alignment at the end of training, suggesting these examples are well-learned with **remaining loss reduction being sample-specific, inherently orthogonal to general optimization**.