---
title: "Information Theory on Repr Learning"
lastmod: 2026-03-27
---

[NeurIPS Information Theory for Representation Learning](https://neurips.cc/virtual/2023/73986)

To Compress or Not to Compress- Self-Supervised Learning and Information Theory: A Review
- builds upon the info bottleneck principle![](/vault/research-work/attachments/pasted-image-20260327201523.png)
- They use a two-channel setup with the inputs to study a multiviewed system. They are essentially trying to understand what makes models learn implicitely through self-supervision without supervised labels. So they have two different channels for the input X to flow through and get encoded to Z. Then they use cross-decoders to predict one representation from the other.  It should learn to ignore the noisy extra info and only focus on the core information shared by both the view.
	- e.g looking at a cat from different angle and lighting but still inferring it to be the same cat.
- They label this setup as the **Multiview assumption** - states that relevant information for downstream tasks is primarily shared between different views of the same input, while non-shared information is largely irrelevant.
- 