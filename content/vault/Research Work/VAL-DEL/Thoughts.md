---
title: "Thoughts"
lastmod: 2026-09-09
---

- small model -> shuffled data is confusing. Mainly coz the model doesn't have enough representational capacity to seperate both properly
	- for large models even junk data like random strings is well-separated and barely affects performance , whereas for smaller models they are pretty bad.
- So data curation can't be both model size and compute agnostic it seems.
- Keeping valid but low quality samples during training can also lead to better results. Low information but valid , not the mislabelled or noisy samples.
- So the tradeoff is between repeating high  quality or introducing low quality new information.
- I just read about the long tailed nature of SGD noise. Maybe this sort of data-mixing (in apt scenarios) leads to the SGD noise which improves the model's performance. Being very aligned to the direction of the good samples might be kind of overfitting.

- I saw that during the basic experiments like using 0.2 of the data budget, the time to max test accuracy also reduced , basically a lot of capacity seems to have opened up in the model and could easily fit to the required data. If compute is the main concern then , we can maybe start mixing medium informative samples too into this


- Things to think
	- Heavy tailed nature
	- Effect of data mixing on optimisation?
	- How much compute is enough for optimal data-budget based best performance/gains?
	- Task conditioned level of information per sample is different ig depending on the context? I would assume Cifar100 to have low informative images given the classification task since they are low resolution. So pruning in this kind of a setup is not exactly useful. Compared to something like ImageNet CLIP setting or webcrawl or textual data, the amount of information per task/ classificatin might be high. But then again the complexity needed to learn that task is  more , and to get that complex the model's training needs to have more dynamicity?(more exposure to different things, hence the role of data mixing?)
- There are methods which showed that regularisation can lead to the extraction of more generalisability in LLMs in a data-constrained but enough compute scenario.
	- This seems to be doing the same thing on the loss landscape, a regularising effect helps guide the training to flatter minimas.
	- My previous claim of random being good was also wrong, random biases the data distribution and hence the grad updates.
	- Dynamic pruning seems to endorse this regularising effect by adding more noise to the optimisation process given by the varying subset of data seen every cycle.
	- So is the result finally that data mixing leads to more regularisation and to better minimas? Not always as stated previously by Goyal et al, that filtered data is good when compute is low but bad for high compute scenarios compared to introducing more of the unseen data.
	- Basically there needs to be a schedule of learning over the data, curriculum which must again respect the true loss landscape.


#### GPT Discussions
- Given what the model already knows, what is the marginal value of spending one more training step on x?
- Increasing batchsize to learning ratio leads to more sharper minimas, lowering it leads to more flatter minimas.
- An interesting question will be , can we prune while preserving the low dimensional eigenvalue structure of the full-data hessian. That is maintaining the top-k eigenvalues(relative) which hold the most important information regarding the curvature. - very similar in idea to the gradient-matching and hessian-aware coreset selection papers from pre-2023-24.
	- But then again the groups of low value eigenvalues might hold significant information regarding the loss landscape
- We see that regularisation methods lead to better quality extraction out of data corpus. But more regularation should in theory lead to more flatter minima. Then certain high generalisation sharp minimas will obviously be avoided.
	- Can we do an experiment to show how likely it is to land on sharp minimas, Obviously less regularisation leads to sharper minimas e.g with larger batchsizes. But for that we will be needing a guiding signal which might be very difficult.
- We can maybe study in what kinds of scenarios regularisaiton methods fail - like data augmentations, or changing the hyperparams.
- We should also check 