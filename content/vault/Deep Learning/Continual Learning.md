---
title: "Continual Learning"
---

#continual_learning

It is an AI learning approach which seeks to sequentially train a model for new tasks while retaining concepts and knowledge regarding previous tasks. That is , we need it to learn new things while retaining already learned info and the number of tasks is not fixed. ^e662de

#### Keywords
- Catastrophic Forgetting
- Stability-Plasticity Trade-off
- Inter/intra task generalizability

## Papers
- [Survey on Continual Learning](https://arxiv.org/pdf/2302.00487)
- 

These five categories represent different strategies for solving catastrophic forgetting
* **Regularization-based**: When learning a new task, it penalizes the model for changing the specific weights that were important for previous tasks. Basically adds an appropriate regularization term to the loss for the current task which ensures less divergence from older tasks.
* **Replay-based**:  The model either stores a few real examples from old tasks or uses a second model to generate "fake" versions of old data. It mixes these old examples with the new ones so it doesn't lose its original skills.
* **Optimization-based**:  Instead of just following the fastest path to learn the new task, the optimization algorithm is tweaked to ensure the "direction" of learning doesn't collide with or overwrite the logic needed for old tasks. It basically messes with the gradients such that learning is non-destructive wrt the older data.
* Representation-based: This focuses on building a very solid, flexible foundation. The goal is to learn features that are "robust" enough to work across many different tasks. If the underlying way the model "sees" data is high-quality, it doesn't need to change much to handle new information.
* Architecture-based: This is like "adding a new room to a house." Instead of trying to cram everything into the same space, the model allocates specific neurons or layers for specific tasks. This prevents new information from physically overwriting the old because they live in different parts of the network. [1, 2, 3, 4, 5] 

[Continual Learning Formulation](/vault/deep-learning/continual-learning-formulation/)
[Stability vs Plasticity](/vault/deep-learning/stability-vs-plasticity/)
[Continual Learning - Eval Metrics](/vault/deep-learning/continual-learning-eval-metrics/)
