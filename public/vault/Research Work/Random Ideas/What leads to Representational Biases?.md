---
title: "What leads to Representational Biases?"
lastmod: 2026-07-07
---

#to-ponder 

- [\[2507.22216\] Representation biases: will we achieve complete understanding by analyzing representations?](https://arxiv.org/abs/2507.22216)
- [\[2405.05847\] Learned feature representations are biased by complexity, learning order, position, and more](http://arxiv.org/abs/2405.05847)
- [\[2407.06076\] Understanding Visual Feature Reliance through the Lens of Complexity](http://arxiv.org/abs/2407.06076)


The above paper show that neural network representations are more skewed towards learning the easier features than the harder features. Why is this observed? There is intuitive explainations so far but not much that discusses it in depth.

## Hypothesis
It might be due to how we are framing the optimisation problem, designing the loss, updating the weights and all that. Maybe check the results over non-gradient based solvers can be a way to look into it.

Inspect the training dynamics: [Position: Don't Just "Fix it in Post": A Science of AI Must Study Training Dynamics](https://arxiv.org/abs/2606.06533)

## Setup to Get started.
- Do lit review on what causes this bias at the math level, preference for easy(linear) features over non-linear ones.
	- Even among the non-linear features , is there a level of non-linearity that is being prioritised?
- Start with the toy setups given in the paper.
- Setup a few non-gradient based solvers.
- Check a few other optimisation paradigms.