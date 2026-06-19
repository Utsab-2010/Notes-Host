---
title: "I-JEPA"
lastmod: 2026-05-21
---

Image Joint Embedding Predictive Architecture:
Paper: [\[2301.08243\] Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](http://arxiv.org/abs/2301.08243)

#deep_learning #representations #compvis


### Flaws in the older stuff
>  - Masked pretraining tasks require less prior knowledge than view-invariance approaches and easily generalize beyond the image modality [8]. However, the esulting representations are typically of a lower semantic level and underperform invariance-based pretraining in offthe-shelf evaluations (e.g., linear-probing) and in transfer settings with limited supervision for semantic classification tasks [4].
- Before Jepa there were two main methods of image self-supervised training
	- Fill in the blanks/gaps -  But in this method the model gets obsessed with pixel, trying to find the perfect combination to fill the gap but overlooks the deeper semantic meanings. It under performs in linear-probing evaluations where we freeze the encoder and train a linear layer taking those reps as inputs and then outputing a softmax over the given classes. If it learns well then means that the model captured the semantics correctly. 
	- View Invariance - This is basically what contrastive learning is. It requires prior human knowledge over the dataset which determines which data points are similar and which are different. It can't do that on its own.
- Jepa tries to improve upon both of these without using prior information.


*How does IJEPA prevent model Collapse?*
