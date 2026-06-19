---
title: "Data-Driven Inductive Bias"
lastmod: 2026-06-17
---

The word **Inductive** refers to a reasoning process that uses specific observations, evidence, or patterns to form broad, general conclusions or theories.

An **inductive bias** is the set of assumptions a model uses to predict outputs for inputs it hasn't seen yet.

- **Manual Bias:** A researcher decides, "I assume the important weights are the ones with low gradients," and writes an algorithm like EWC to enforce that.
- **Data-Driven Bias:** The model is "meta-trained" on various sequences of tasks. Through this process, it discovers for itself which types of internal representations or gradient updates lead to the least amount of interference across tasks.

It effectively builds its own "common sense" about how to handle task transitions based on its experience with previous task distributions.



The inductive bias refers to a set of assumptions and biases that determine the hypothesis space of a model before it is even exposed to data. Once it is exposed to data, the dataset then influences the decision boundary(or concrete hypothesis) selected from the models' hypothesis space.
