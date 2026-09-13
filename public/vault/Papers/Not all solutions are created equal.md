---
title: "Not all solutions are created equal"
lastmod: 2026-07-23
---

[Not all solutions are created equal: An analytical dissociation of functional and representational similarity in deep linear neural networks](https://proceedings.mlr.press/v267/braun25a.html)
New terms - respresentational alignment, functional alignment

## Background
There is limited analytical understanding of how a network’s representation and function relate, despite this being essential to any quantitative notion of underlying function or functional similarity.
- The structure of artificial and biological networks is often non-identifiable in the sense that networks can be structurally distinct, yet implement the same input-output mapping.


### Definitions
**Functional alignment** (or functional similarity) occurs when different neural networks—whether artificial or biological—implement the exact same input-output mapping

**Representational alignment** (or representational similarity) occurs when networks share similar internal neural codes, such as matching hidden-layer activation patterns. This is commonly quantified using a Representational Similarity Matrix (RSM), which captures the pairwise similarities between different inputs within the network's hidden representational space