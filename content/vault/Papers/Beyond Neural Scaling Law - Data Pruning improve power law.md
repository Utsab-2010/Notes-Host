---
title: "Beyond Neural Scaling Law - Data Pruning improve power law"
lastmod: 2026-06-09
---

#scaling_laws 
paper: [\[2206.14486\] Beyond neural scaling laws: beating power law scaling via data pruning](https://arxiv.org/abs/2206.14486)
## Main Points
- They are NOT focusing on trainining/compute efficiency in this work even though they are working with data pruning methods
- They try to show that use of data pruning can lead to the creation of better datasets which can help scale up performance beyond the traditional power law trend.
- They tested with a toy model and designed a scoring metric to score samples based on their quality.
- Now if this metric is imperfect, it will lead to more mixture of different quality data during fitlering. This mixture will try to force the scaling law back towards the power law trend.
- If the metric is ideal, then the pareto optimal scaling trend observed from the graph is exponential which gives you different values of pruning metrics for different levels of pruning that you need.

*note* - As mentioned, they are not focusing on data quality, Hence in their plots, they have plots of different pruning ratios for the same datasize, implying for the lower pruning ratios  we will have to start with a larger initial dataset. Basically, for the same dataset size, if we were to use only the "good" samples found by some ideal pruning metric then it will lead to exponential gains.

![](/vault/papers/attachments/pasted-image-20260609152926.png)
- Now while each of the plots will have different initial dataset sizes for a parcular value of training parameters per param. What might be more interesting to see is the individual plots  of the higher pruning ratios(low kept values). As the dataset size increases for a fixed low kept value, we don't see power scaling but sort of and S shape.
- *This implies that power scaling is probably due to the presence of redundant diversity in the dataset.* as stated in the paper as "..that power law scaling of error with respect to data suggests that many training examples are highly redundant."

## Questions:
#to_ponder 
1. Does the power law imply that a dataset HAS redundant samples that can be removed?'
2. 