---
title: "New way of training small models?"
lastmod: 2026-05-21
---

#to_ponder 
What if you allot different parts of the parameter space to learning kinds of data in a somewhat explicit manner?
Then we use a smaller extractor layer to essentially only make use of the parameters of the required subspace for processing the given input to get the required output.

The architecture might be :
- A big network to store the representations in kinda well defined sub-param spaces for the input data distribution
- A smaller network which decides which subspace to extract the information from conditioned on the given input.

### Reading List
- [Matryoshka Representation Learning](/vault/deep-learning/matryoshka-representation-learning/)
- [Do We Really Need Parameter-Isolation to Protect Task Knowledge? \| OpenReview](https://openreview.net/forum?id=tVNZj27pb3)
- https://arxiv.org/pdf/2601.07372 - Deepseek Engrams - Memory Lookup  for LLMs
- 
- 