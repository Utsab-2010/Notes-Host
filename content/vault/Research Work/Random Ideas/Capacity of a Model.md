---
title: "Capacity of a Model"
lastmod: 2026-05-22
---

#to_ponder 
To learn information, to hold information

### The Gap You're Pointing At

What doesn't exist is a **per-model, per-task characterization** of the generalization ceiling — something like: "a transformer of this size, trained optimally, can generalize to functions of at most this complexity, this frequency content, with this many tasks." The pieces are there — information-theoretic bounds, spectral bias analysis, Kolmogorov complexity arguments, scaling law empirics — but they haven't been assembled into a coherent framework that gives you the equivalent of Shannon capacity for a specific architecture on a specific task class.

The reason is probably that the problem is genuinely hard: the effective capacity interacts with the task distribution, th