---
title: "Learned Representation are path dependent"
---

#to_ponder 
- Ekdeep Singh Lubana, Eric J Bigelow, Robert P Dick, David Krueger, and Hidenori Tanaka. Mechanistic mode connectivity. In International Conference on Machine Learning, pp. 22965–23004. PMLR, 2023.

Learned representations are substantially path-dependent (cf. Lubana et al., 2023)—if a model is pretrained to compute feature A, then trained to additionally compute feature B, it will have different representations than if it was trained on feature B before feature A, or if it was trained on both A and B simultaneously—even with similar behavior on train and test sets.



### Questions:
1. How much does the implicit curricula matter?
2. Is the implicit curricula also not the true implicit curricula?
	1. Probably not coz different curricula other than random seems to improve it.
3. Easy feature occupies substantially more of the penultimate layer representation variance than the hard feature. *More variance means more of the representation subspace is being occupied by the easy representation.* This is quite interesting, if this subspace is reduced (by some architectural design?) then seems to have several downstream benefits for continual and curriculum learning.