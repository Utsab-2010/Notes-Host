---
title: "Stable Coresets"
lastmod: 2026-09-05
---

#data-pruning #data-attribution #learning-theory #data-efficient-ml 

## Background
1. The curvature mismatch and loss landscape misalignment issue is a **general challenge inherent to any subset selection**, but it becomes **peculiarly catastrophic and pronounced in coreset methods that rely purely on first-order gradient matching**. 
2. While landscape misalignment is a general risk, standard gradient-matching coreset algorithms (such as _Craig_, _Grad-Match_, or _Glister_) suffer from two specific flaws that turn this minor warping into a catastrophic failure:
	1. gradient matching without curvature awareness
	2. outliers and noise can produce large gradient
3. Methods like CREST try to match both gradients and Hessians over time.
4. But hessians are expensive but we can't also ignore them


## Contributions
- They evaluate via gradient matching under Gaussian weight pertur\bations doing which they smooth out the high-frequency spikes and false flat basins. They do monte carlo smoothening over the loss objective.
- They show mathematically that the coreset's curvature remains tightly aligned with the full dataset curvature.
- 