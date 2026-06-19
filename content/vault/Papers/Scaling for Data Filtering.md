---
title: "Scaling for Data Filtering"
lastmod: 2026-05-11
---

#data_efficient_ml 
*Data curation cannot be compute-agnostic!*

Paper: [IEEE Xplore - Unable to Load Page](https://ieeexplore.ieee.org/document/10656415/)

### Brief
- presents a methodical study on how "quality" of data is not fixed and is actually compute dependent(how long you train the model).
- Past research considered web-data to be homogeneous(belonging to the same distribution) which they haven't assumed in their work.
- filtering metrics must be designed by assessing the trade-off between the diminishing utility of a small pool of ‘high-quality’ data, and the initially lower but slowly diminishing utility of a larger pool that includes ‘lower-quality’ data.
- To circumvent this, we **leverage scaling laws to predict** the performance of models trained with optimal filtering strategies(tailored for heterogeneous datasets).
- Focus is on scaling laws for large scale contrastive training of VLMs like CLIP.
- 

### Existing Scaling Laws
- LLMs: Training on tokens **beyond four epochs** yields negligible gains compared to training on new language data due to diminishing utility. However they don't consider different data quality pools.
- CLIP: Contrary to language models which are rarely trained with more than 3-4 epochs, **CLIP training invovles upto 30-40** epochs even at the largest data scale

### Datasets:
- LAION dataset only has the top 10% "high quality" data points based on the highest CLIP similarity scores. Points with similarity less than 0.28 are filtered out.
- 

### Conclusions and Contributions
- When training for large compute(more no. of repetitions possible), the filtering/selection of the subset needs to be less aggressive.
	- After multiple repetitions , the high quality data loses its utility.
- ![](/vault/papers/attachments/pasted-image-20260507175337.png)
	- Advantages of data filtering decreases with increase in compute amount.



## Scaling Laws:
### Utility
CLIP style pre-training is done by repeating multiple epochs of training on the same data. It is a metric which determines how useful a data sample is for training a model(increasing its accuracy). Obviously as training goes on an a sample is seen multiple times, its utility diminishes. The instantaneous utility is defined by the following
![](/vault/papers/attachments/pasted-image-20260510213228.png)
y = the error/loss of a model
n = no. of samples seen so far.

#### **Utility Under Repetition**
![](/vault/papers/attachments/pasted-image-20260510213430.png)
![](/vault/papers/attachments/pasted-image-20260510213510.png)
- assumes that utility decreases exponentially with repetitions
#### **Heterogeneous Web Data**
- presence of data pools of different quality is overlooked
- *how can we estimate the loss and thus the scaling curves for a mixture of pools effectively?*
	![](/vault/papers/attachments/pasted-image-20260510213835.png)

## Experimental Setup
- **DataComp medium scale** pool which consists of **128M** image-caption pairs
- T-MARS score and CLIP score as the two data utility estimates and rank the webdata based on them.
![](/vault/papers/attachments/pasted-image-20260511075127.png)

## Questions
*How are these scaling laws useful?*
- we can train and get the params(via curve fitting) for many different pools of data
- then using theorem 1 we can find the pareto optimal data mixture for training
- **Pareto Optimal** refers to the best possible trade-off between model accuracy and cost of compute.

![](/vault/papers/attachments/pasted-image-20260511080608.png)
- The scatter points are the real points evaluated on the real models and the lines are the plots predicted by their scaling laws
- the authors used publicly available checkpoints of models already trained at massive scales at the given pool sizes to get the scatter points. 

- Take a look at the citations
	- follow-up works- maybe LLMs?
- - review ICLR openreview
- continual works?
- 