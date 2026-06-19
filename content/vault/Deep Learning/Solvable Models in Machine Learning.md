---
title: "Solvable Models in Machine Learning"
lastmod: 2026-06-04
---

#deep_learning 

In physics and mathematics, a **solvable model** (or exactly integrable system) is a theoretical system that can be solved analytically from first principles without relying on approximations, trial-and-error simulations, or heuristic guesswork.

In Machine Learning, we rarely have solvable models. Most modern neural networks are "black boxes"—we optimize them using gradients, but we cannot write down a clean, exact mathematical formula for the final weights or the exact shape of the loss landscape. However, studying highly simplified, mathematically solvable models is the bedrock of **Deep Learning Theory**. They allow us to understand _why_ and _how_ optimization and generalization work.

## Key Examples of Solvable Models in ML

To make an ML model mathematically solvable, theorists usually strip away non-linearities or assume the network is infinitely wide.

### 1. Deep Linear Networks

A deep linear network looks like a standard deep neural network, but it has **no activation functions** (no ReLU, no Sigmoid).

- **The Setup:** The output is just a chain of matrix multiplications: $\hat{y} = W_L W_{L-1} \dots W_1 x$.
    
- **Why it's solvable:** Mathematically, this entire chain collapses into a single linear transformation, meaning the model can only learn linear relationships.
    
- **What it teaches us:** Even though the function it computes is simple, the _loss landscape_ of deep linear networks is non-convex and looks surprisingly like a deep non-linear network. Solving the equations of gradient descent exactly on this model allowed researchers to prove that deep networks naturally learn features in a hierarchical, "coarse-to-fine" order.
    

### 2. The Neural Tangent Kernel (NTK) / Infinite-Width Regime

If you make a standard non-linear network infinitely wide (meaning the number of hidden neurons in a layer approaches infinity), a mathematical miracle occurs.

- **The Setup:** As the width goes to infinity, the individual weights change by an infinitesimally small amount during training, yet their collective shift alters the output.
- **Why it's solvable:** In this limit, the network's training dynamics freeze into a linear system governed by a fixed matrix called the **Neural Tangent Kernel (NTK)**. The training trajectory can be solved exactly using standard linear differential equations.
- **What it teaches us:** It provides a rigorous proof that gradient descent can find global minima on complex training data, giving us a mathematical baseline for how networks overparameterize and generalize.    

### 3. Matrix Completion and Two-Layer Matrix Factorization

Used to understand low-rank structures (like recommendation systems or token embeddings). By analyzing gradient descent on a matrix decomposition problem ($M = U V^T$), theorists can track the exact trajectory of eigenvalues over time. This solved model proved that gradient descent has an **implicit bias** toward choosing low-rank, simpler solutions, explaining why models generalize even without explicit regularization.

## Why Do Theorists Study Solvable Models?

Real-world models like GPT-4 or ResNets are too complex for exact mathematics. We look at solvable models for three main reasons:

- **Isolating Phenomena:** They allow us to isolate a single variable (like depth, width, or data noise) and see its exact impact on learning dynamics without confounding variables.    
- **Sanity Checks for Scaling:** Before spending millions of dollars scaling up an architecture, solvable toy models help verify if the underlying optimization algorithms behave predictably as size approaches infinity.
- **Uncovering Implicit Biases:** They help answer the fundamental mystery of deep learning: _Why do overparameterized models find solutions that generalize well instead of just memorizing the training noise?_ Solvable models let us mathematically trace the path gradient descent takes through the landscape.