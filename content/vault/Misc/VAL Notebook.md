---
title: "VAL Notebook"
lastmod: 2026-06-01
---

```
Author: Utsab Karan
Vision and AI Lab, IISc Bangalore
Summer Internship 2026
```
#### Current Work
1. Order-DP keep the same compute
	1. 20,50,100 epochs
	   2. Prune ratio = 0.3,0.5
	   3. imgnet
2.  When can pruning lead to gains? Can there be a theory behind it? Imgnet not much. At CLIP level some gains.
### Questions
1. Possible Directions for Lit Review
2. Possible set of experiments.

### To-Dos
1. 

### To Ponder
- What exactly are we looking for?
- Are we thinking about only the pre-training phase of image models?
	- No right? so the idea would also be to able to continually learn stuff for downsteam tasks without CF.
	- We want to answer the question of whether this is possible.
	- Prior work on data pruning just prunes out a coreset and trains on that without any concern for the able to learn further downstream tasks.
- But are we really trying to answer the question of future downstream task inc learning? like the TiC-CLIP paper.
- Are we trying to simply better utilise the static pruning methods?
	- But they seem to focus on the pretraining phase of models(training from scratch). Not sure if ResNets have any downstream fine-tuning cases.
- 

### Updates
- Saurabh Garg - Thinking Machines
- Pratyush Maini - Thinking Machines
- When Do curricula work?
- If you find any stuff specifically on LLMs but seems relevant as in it has potential to be translated to vision models then look into it
	- like attention based stuff might be translated to ViTs.


