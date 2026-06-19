---
title: "Deep Learning on a Data Diet"
lastmod: 2026-04-03
---

#data_efficient_ml 

## Proposed Ideas
- Compared to recent work that prunes data by discarding examples that are rarely forgotten over the  course of training, our scores use only local information early in training
- a scoring method to identify diff and important samples early on in training
- identify how this score pruned sub-population affect loss surface and the training dynamics

## Imp Results
- we can prune 25% of CIFAR-100 (verified by IISc task results) compared to 50% of CIFAR-10 due to difficulty in learning more variety.
- Performance drops at very high pruning levels. They have hypothesised that this might be due to a significant sub-population being excluded from the training dataset.
- EL2N scores is a property of the dataset and not specific to a network. They show that a ResNet18 and a ResNet50 trained on CIFAR-10 have similar performance curves and the same amount of data can be pruned,.
	- E2LN scores calculated for one set of networks and hyp-param config can be used to pruned for different architectures and configs.
- They also found that the very high scored data points  tend to be either unrepresentative outliers of a class, have non standard backgrounds or odd angles, are subject to label noise, or are otherwise difficult.
- 
## Proposed Ideas
- #### **GraNd Score (Gradient Normed)**
	- The GraNd score of a training example $(x, y)$ at a specific training time $t$ is defined as the **expected L2-norm of the loss gradient**. It measures how much an individual example influences the change in training loss for the rest of the dataset.$$\chi_{t}(x,y)=\mathbb{E}_{w_{t}}||g_{t}(x,y)||_{2}$$
	- **Components:** $g_{t}(x,y)$ is the gradient of the loss with respect to the weights $w_t$.
	- **Expectation:** The L2 norm  is calculated over the vector of all model weight gradients. It is also averaged over multiple random weight initializations (different seeds)to remove dependence on specific initial weights.
	- Often calculated very early or at initialisation. But since the model hasn't learnt the data structure yet, its not that effective for pruning. Warmup epochs + EL2n performs better
	
- #### **EL2N Score (Error L2-Norm)** 
	- The EL2N score is a simplified approximation of the GraNd score that becomes accurate after a few epochs of training. It measures the **expected L2-norm of the error vector**, which is the difference between the model's predicted probabilities and the actual label.$$EL2N\space Score=\mathbb{E}||p(w_{t},x)-y||_{2}$$
    - **Components:** $p(w_t, x)$ is the network's output probability vector and $y$ is the one-hot encoded label.
    - **Utility:** It is computationally cheaper than GraNd because it does not require calculating gradients through the entire network, yet it *often provides an even stronger signal* for data pruning.


### Related Work
- [Large-Scale Pruning using Dyna Uncertainty](/vault/papers/large-scale-pruning-using-dyna-uncertainty/)