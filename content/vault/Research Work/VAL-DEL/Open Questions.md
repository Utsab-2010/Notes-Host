---
title: "Open Questions"
lastmod: 2026-06-12
---

- How much can a model actually learn? 
	- Do we address this?
	- Capacity of a model?
- Parameter-space alloted for different tasks? 
	- related works - 
- Look into Data Attribution?
	- Which data is important for which predictions.
	- Use cases of good DA methods??
- Does the assumption of neural networks being over-parameterised hold well in the context of CL? 
- Which area to target CIL, TIL, DIL, etc?
- how to extract juice from all the samples as quickly as possible w/o leading to overfitting / forgetting.
	- Does overfitting come first or forgetting occur first?
- Scaling Laws Hold after pruning??
	- Image data statistics
	- Intuition regarding why its not working
		- Then build math
- CL on a level beyond Cifar, Imgnet
- In the continual setup, does overfitting happen first or CF? What does it depends on ? 
- Do we want to prune with constant compute to achieve better scaling? 
	- We would first want to understand how scaling happens with data-pruning?
	- Different for different Datasets, but what causes this difference?
	- Can we derive any info like from the dataset properties like the language statistics paper?
- Is learning the "hard" samples good for generalisaion? For classification yes probably coz helps define the cluster boundaries of the representation.
- 