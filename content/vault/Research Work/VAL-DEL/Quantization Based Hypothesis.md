---
title: "Quantization Based Hypothesis"
---

Quantisation Modelling paper states that the datasets comprise of different quantas of information corresponding to different characteristic features.
And that the distribution of said quanta is spread according to the Zipf distribution throughout the dataset.
Now based on the frequency of occurrence of a quanta we can create a descending sequence called the Q-sequence.
Some points: 
- Each quanta needs to be seen for a threshold $\tau$ number of times to get learnt. This tau may be quanta dependent but they took it to be same.

### Prior Knowledge and Expectations
- Hard samples help determine the boundary for classes but doesn't generalise well to complex datasets like Imagenet which are already human curated and hence our definition of the "hardness" is biased probably.

## Analysis
- based on the normal Q - sequence , there is a order in which the Quanta is learnt if trained on the full dataset. Statistically, higher frequency quanta should be learn't first according to their model.
- Pruning policy changes the quanta distribution and hence this Q-sequence which might be leading to low generalisation/test scores.
	- There might be some *underlying implicit curricula* corresponding to the original Q-sequence which is getting ruined. Model is learning concepts in a different order which might be detrimental to how effectively it is able to learn other concepts further into the training.
	- This implicit curricula may or may not correlation with the curricula of quanta given by the Q-sequence.

## Toy Experiment to Analyse.
- We can use a modified version the binary xor toy exp that they used.
- Input data = zipf dist. based control signals  + (uniform) random data 
- control signals determine the xor combo over the random data.
- Two classes 0 and 1 but we can expand to more classes and use modulo logic then instead of xor.
- We generate a lot of data based on these combos.
	- We have more polygenic control signals instead of just monogenic ones coz images should be polygenic in nature. (evidence is intrinsic patterns of CNNs)
- We then use pruning strategies that we know for this dataset.
- We can maybe vary the amount of polygeneity in the dataset and see.
## Observations:
- we know the original Q-sequence from the control signal distribution. We note the new Q-sequence from the pruned datset and check for differences.
- How amount of polygeneity affects observations?
	- More complex data should be highly polygenic
- Prune only on monogenic and see the changes.


*Need to maintain diversity and also most information*