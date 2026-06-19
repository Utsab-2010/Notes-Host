---
title: "Learning Stable Normalizing-Flow Control for Robotic Manipulation"
lastmod: 2026-02-04
---

This paper maps the real system X of the manipulator(end-effector) to a simpler spring mass types control system Y.
- This transformation is given by a learnable invertible flow network.
- The optimal control $u_y$ is found from the equation an we can get the optimal control for the manipulator state $u_x$ using the inverse jacobian matrix (using the concept of **virtual work**)
- They also show safety guarantees in their framework

In **Normalizing Flows**, complex probability distributions are models are constructed by learning a sequence of convertible and differential neural network transformations that map the simple prior distribution to the required complex ones.
![](/vault/assets/images/pasted-image-20260204023452.png)
![](/vault/assets/images/pasted-image-20260204023611.png)
### Training Details
- 