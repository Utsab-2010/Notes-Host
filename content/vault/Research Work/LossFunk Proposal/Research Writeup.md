---
title: "Research Writeup"
lastmod: 2026-04-05
---



**Target Problem**: How do we learn representations that help with out of distribution generalization? Do they need to be disentangled? How do we learn that?
- *Create learning algorithms that are as sample efficient as humans*- What can we study from the nature of data to drive sample efficiency? How can we use data to create new data (are world models involved?) ? What kinds of abstractions lead to sample efficient learning?Explore tradeoff between compute, parameters and data samples.
- 


## Resources
- [Causal Representation Learning for Out-of-Distribution Recommendation](https://dl.acm.org/doi/epdf/10.1145/3485447.3512251)
- [\[2108.13624\] Towards Out-Of-Distribution Generalization: A Survey](https://arxiv.org/abs/2108.13624)
- [\[2103.03097\] Generalizing to Unseen Domains: A Survey on Domain Generalization](https://arxiv.org/abs/2103.03097)
- [\[2111.13839\] Towards Principled Disentanglement for Domain Generalization](https://arxiv.org/abs/2111.13839)
- [A Survey on Evaluation of Out-of-Distribution Generalization \| alphaXiv](https://www.alphaxiv.org/abs/2403.01874?chatId=019d4c56-173d-75f6-8d1f-f70f59e3cfa8)
- [\[2103.02503\] Domain Generalization: A Survey](https://arxiv.org/abs/2103.02503)

#### Random Ideas
- Loss based on different metrics of seperation between 2 distributions
- Guiding adversarial data points back to learnt manifold for OOD functionality
- 


### OOD Gen : Survey
- Unsupervised generalisaiton:
	- Learning discriminitive robust representations across diverse distributions, particularly with limited data.
	- - **Unsupervised Domain Generalization**: Techniques like DARLING that learn domain-invariant features without using domain labels
	- **Disentangled representation learning** aims to learn representations where distinct and informative factors of data variation are separate. It aims to separate data into its *underlying, independent causal factors* (e.g., shape, color, and background).
		- No Additional Information β-VAE [101] introduces an extra hyperparameter β into vanilla VAE objective function, making a trade-off between latent bottleneck capacity and independence constraints, thus encouraging the model to learn more efficient representations. The objective function of β-VAE is as follows: ![](/vault/research-work/lossfunk-proposal/attachments/pasted-image-20260402104905.png)
		- FactorVAE [121] adds the term of Total Correlation into the objective function, which is formulated as the KL-divergence between marginal posterior q(z) and its corresponding factorized distribution ¯q(z):![](/vault/research-work/lossfunk-proposal/attachments/pasted-image-20260402104935.png)
- #### Optimisation method for OOD
	-  Apart for USL and SL , robust optimization methods with theoretical guarantees have recently aroused much attention, which is both model agnostic and data structure agnostic, and therefore could be incorporated with various approaches.
	- The fundamental goal of OOD optimization is expressed as: argminf​maxe∈supp(Eall​)​L(f∣e). In simple terms, we want to find a prediction model (f) that minimizes (argmin) the absolute highest loss (L) it could possibly experience across any potential test environment (e) from the set of all possible environments (Eall​).
	- **Distributionally Robust Optimisation** - 


### Evaluation of OOD Generalisation
