---
title: "Emergent Properties with Repeated Examples"
lastmod: 2026-09-13
---

#scaling #llm #data-attribution 


## Two-set Training
- If TB = 600 M. they issue a fraction of the compute to only single view full data D and the remaining is given to a repeating random subset S. 


## Interesting Points
- The selected subset being repeated is chosen randomly without any curation. Curation doesn't seem to help with this and can also affect adversely.
- Mixing repeated and non-repeated examples in the same minibatches is required for two-set training to work. 
- Benefits of repetition are significant but come in different flavors.
	- Gcd - perf improve and acc learning
	- new task learning
	- accessible to smaller models
- training on the tiny sample alone (with large repetition), or oneset training on the same data budget, result in much lower performance than what two-set training provides by mixing them together

## Thoughts
- They mainly worked with controlled Arithmetic tasks. What other datasets does this behaviour extend to.
	- What is speicial about these setups which allows gains from repetition on smaller DB? Is this lacking in vision datasets?
	- The observed Synergeistic effect: Some cases training on single epoch unlimited data did not lead to any learning or repeted small set, however in vision models we have seen otherwise. However we never tested with $S<<N$ which might be something we need to look at. 
- Is this behaviour specific to the Architecture? - they used transformers
- Fig 2. Test loss and GCD predcited are not very correlated it seems
	- Things with high test loss seem to have better performance
	- Which is large ddiverse data pool or infinite data underperforming?
	- So their explaination is that GCD predicted and test loss are different metrics. GCD shows how many out of 100 GCD setups it gets correct.
- Can we fit a scaling law to this to find the optimal data budget and repetition number?
- We can run the two-set experiments on cifar100 and check once. How should we schedule it given that image datasets require must more repetititons compared to text data.
- How did they test the effect of data curation in the two-set training also matters, because it should help in learning intuitively.
	- They did based on the frequency of data. Representing underrepresented data points more.
	- They did not have any notion of easy, informative, or hard samples. So those can be tested.
- Fig. 5 - the Good region of hyper-params for two-set on Modular Mult is very low. 
- The two-set setup feels like training on a main representative set and introducing bits of diversity during each batch's training. This is similar to a form of regularisation, the extra diverse new data bits in the batch don't let the learning signal die down?
	- Allen-Zhu & Li (2024) undertake a controlled study on synthetic language data in the context of knowledge retrieval and find that knowledge augmentation - repeated inclusion of reformulated variants - of a small subset of the data leads to performance improvement; an effect somewhat akin to what we observe in two-set training.



- Data to model ratio.
- Are they overfitting?
- Fig 2 -
- Power of power law had compositional task.
- What are we knowing newly, someone in the field might infer?
- If the paper is just discussing this is task this is result. 
	- If they gave a proper motivation for this and all?
	  -  Is it good enoug~h?
	  - Main claims and what is interesting?
- Dive into 3-4 papers at once.
- Trends across papers find it.
	- If we see multiple papers talking about it.
	- Before going deep into one.
	- See trends across papers.