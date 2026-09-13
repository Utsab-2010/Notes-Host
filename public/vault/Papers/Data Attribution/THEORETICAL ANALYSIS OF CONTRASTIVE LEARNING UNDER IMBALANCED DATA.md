---
title: "THEORETICAL ANALYSIS OF CONTRASTIVE LEARNING UNDER IMBALANCED DATA"
lastmod: 2026-09-05
---

#data-attribution #data-efficient-ml #learning-theory 


## Background
- CLIP is useful, but the theoretical understanding about it remains limited, for imbalanced data distributions which are most common in real world datasets.
- minority classes are underrepresented - hinders capture of discriminative features
## Setup
- Transformer MLP setup with ReLU activations with imbalanced data
- Structured data model where each input includes majority and minority features with different frequencies.

## Experiments
- Alignment of Neurons with the feature vectors:
	- Cosine sim between neuron weight vector and the feature vector
	- How the Two Things Are Correlated :
	$$ \text{Update Step} \propto \mathbb{E} \left[ h_i(Y_n) \langle \nabla_{w_i} h_i(X_n), M_j \rangle \right] $$
	$$ \mathbb{E} \left[ h_i(Y_n) \langle \nabla_{w_i} h_i(X_n), M_j \rangle \right] = \frac{1}{L^2} \langle w_i, M_j \rangle \mathbb{E} \left[ \hat{z}^+_{n, j} \hat{z}_{n, j} \right] $$
	This formula establishes a **direct, linear correlation** between the gradient update (the learning contribution) and two main factors2:
	
	1. **The Existing Alignment (($\langle w_i, M_j \rangle$)):** The gradient update is directly multiplied by the neuron's _current_ alignment with the feature $M_j$2. If a neuron already points slightly toward $M_j$, it receives a larger update in that direction5.
	2. **The Feature Frequency ($\mathbb{E} [ \hat{z}^+_{n, j} \hat{z}_{n, j} ] \propto \epsilon_j$):** The update is also scaled by how often that feature actually appears in positive training pairs ($\epsilon_j$)


## Main Results
- Neuron weights grow in feature directions while non-feature components are suppressed
- Lucky neurons then specialize in single features, and ordinary neurons learn a mix of features; finally, each neuron converges in a way that guarantees a small training loss, becoming strongly aligned with one or more features, weakly aligned with other features, and remaining small in non-feature directions.
- **Imbalance degrades representation performance** in multiple ways: it **slows the learning of minority features**, decreases the number of neurons that specialize in a single feature, and produces a chain effect that necessitates a more complex model to adequately capture all features
- Success of contrastive learning relies on neurons that specialize in a single feature.  In contrast, neurons that learn mixtures of features are useful only for a limited subset of downstream tasks.
- each underlying semantic feature is captured cleanly by a subset of lucky neurons.

---

## My thoughts 
What if we do an analysis of pruning methods by looking at the contributions of each feature to the learning process. Based on this, we can try to connect things to the power law type acceleration in the learning landscape and maybe even connect it formally to the volume hypothesis by showing that pruning while ensuring similar relative contribution of the features to the learning process would lead to .

But the entire paper has been written from the POV of CLIP based training and hence we have to look for similar feature learning math for normal encoder type setups too and see if neuron-feature alignment is the way to go.