---
title: "Curriculum Learning"
---

#curriculum_learning 

The original definition of **Curriculum Learning (CL)** was formally proposed by Bengio et al. in 2009. 
They defined a curriculum as a sequence of **training criteria** over $T$ training steps, denoted as:
$$\mathcal{C} = \langle Q_1, \dots, Q_t, \dots, Q_T \rangle$$
Each criterion $Q_t$ represents a reweighting of the target training distribution $P(z)$ at a specific step $t$. $Q_{t}(z) ∝ W_t(z)P (z) \quad ∀ example z ∈ training\, set\,  D$


To be considered a curriculum under the original definition, the sequence must satisfy three specific conditions:
1. **Increasing Entropy (Diversity):** The entropy of the distributions must gradually increase ($H(Q_t) < H(Q_{t+1})$). Ensuring that info and diversity in training data increases.
2. **Monotonic Weight Increase:** The weight assigned to any specific training example must increase or stay the same over time ($W_t(z) \leq W_{t+1}(z)$).  This weight is essentially applied on the loss from said data point.
3. **Target Distribution Convergence:** The final training criterion must be equal to the target training distribution ($Q_T(z) = P(z)$). This ensures that the model eventually trains on the full, original dataset with uniform weights for all examples.

*Why do Curriculum Learning?*
 - Speeds up convergence
 - improve model generalisation over unseen data
 - More stable training over the loss curvature. doesn't get stuck at poor local minima.



![](/vault/papers/attachments/pasted-image-20260507171317.png)


### Curriculum Design
1. Difficulty Measurer - What kind of data is easy or harder to learn?
2. Training Scheduler - When to present harder data and how much harder?

### Predefined CL
When both DM and TS are designed based on human's prior knowledge without involvement of any data-driven algorithms.
