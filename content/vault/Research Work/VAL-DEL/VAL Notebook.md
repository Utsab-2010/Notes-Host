---
title: "VAL Notebook"
lastmod: 2026-09-03
---

```
Author: Utsab Karan
Vision and AI Lab, IISc Bangalore
Summer Internship 2026
```
#### Current Work
1. 

### To Ponder
- Are we thinking about only the pre-training phase of image models?
	- No right? so the idea would also be to able to continually learn stuff for downsteam tasks without CF.
	- We want to answer the question of whether this is possible.
	- Prior work on data pruning just prunes out a coreset and trains on that without any concern for the able to learn further downstream tasks.
- But are we really trying to answer the question of future downstream task inc learning? like the TiC-CLIP paper.
- Are we trying to simply better utilise the static pruning methods?
	- But they seem to focus on the pretraining phase of models(training from scratch). Not sure if ResNets have any downstream fine-tuning cases.


### Updates
- If you find any stuff specifically on LLMs but seems relevant as in it has p- 
- They also suggest that towards the end of training, we should use a bigger batch size. I think maybe this can be true for pruning as well? Since the gradient variance is most likely increasing after pruning, higher batch size can be better for more signal? And for pruning to work, do we just need better hyperparameters? otential to be translated to vision models then look into it
	- like attention based stuff might be translated to ViTs.

## To be discussed:
- SGD implicit bias is not relevant for large datasets. We should focus wrt the volume hypothesis.
	- Claim supported by the Sharp Minima, Revisiting Vol Hyp paper, and Loss landscaper are all you need.
	- Sharp Minima paper has an empirical approximator for the Volume calculation. requiring a lot of forward runs of the model only.
- Stable coresets presents a kind of normalising/regularing effect during pruning and performs well.
- My hypothesis is that smth similar might be happening things like Random and OrderDP which leads to preservation of the Loss landscape even after pruning. 
	- For OrderDP though , although the overall loss landscape will be different, it is proven that it converges well to the full dataset Loss.
- Data mixing induces this kind of normalisation which helps maintain the loss landscape?
- Checking the behaviour of the Loss Landscape
	- Maybe using Gradient or Hessian based metrics
- How does a power law distribution in the dataset affect the loss landscape?
- If normalising/smoothening effect based pruning
- ![](/vault/research-work/val-del/attachments/val-notebook-1788411243434.webp)
- orderdp train accs increase much slower compared to the static pruning ones, I believe this implies that they explore the training landscape much more and hence more regularised to overfitting.