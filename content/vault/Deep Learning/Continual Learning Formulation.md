---
title: "Continual Learning Formulation"
---

Continual learning is defined as learning from dynamic data distributions. Unlike standard machine learning, where data is often static, here training samples from different distributions arrive in a sequence.

A model (parameterized by $\theta$) must learn new tasks ($t$) under two main constraints:
1. Limited Memory: No or very limited access to previous training data.
2. Performance: The model must still perform well on the test sets of those old tasks.

## Formal Notation
- Task $t$: Defined by its data distribution $\mathbb{D}_t := p(\mathcal{X}_t, \mathcal{Y}_t)$.
- Training Batch ($\mathcal{D}_{t,b}$): Represented as $\{\mathcal{X}_{t,b}, \mathcal{Y}_{t,b}\}$, where:
    - $\mathcal{X}_{t,b}$: Input data.
    - $\mathcal{Y}_{t,b}$: Data labels.
    - $t \in \mathcal{T} = \{1, \dots, k\}$: Task identity.
    - $b \in \mathcal{B}_t$: Batch index.

Key Assumptions & Realistic Constraints

- Distribution Consistency: It is generally assumed there is no difference between the training and testing distributions for a specific task.
- Missing Information: In real-world scenarios, the task identity ($t$) and labels ($\mathcal{Y}_t$) might not always be provided.
- Data Arrival: Samples can arrive in two ways:
    
    - Incrementally: In sequential batches $(\{\mathcal{D}_{t,b}\}_{b \in \mathcal{B}_t})_{t \in \mathcal{T}}$.
    - Simultaneously: All data for a specific task arrives at once $(\{\mathcal{D}_t\}_{t \in \mathcal{T}})$.
    

Do you want to add the five groups of continual learning we discussed earlier to this note to make it a complete summary?