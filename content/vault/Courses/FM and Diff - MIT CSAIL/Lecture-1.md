---
title: "Lecture-1"
---

## Flow and Diffusion Models
*We start by defining a trajectory.*

**Ordinary Differential Equations (ODEs):** The mathematical foundation for flow models.

**Trajectory:** The solution to an ODE. It is a function that maps time $t$ to a specific location in a $d$-dimensional space.
    - **Function:** $X : [0, 1] \to \mathbb{R}^d, \quad t \mapsto X_t$

**Vector Field ($u$):** The rule that defines an ODE. It assigns a specific velocity vector to every point in space at any given time
    - **Function:** $u : \mathbb{R}^d \times [0, 1] \to \mathbb{R}^d, \quad (x, t) \mapsto u_t(x)$

### The ODE System
An ODE requires that a trajectory $X$ "follows along the lines" of the vector field $u_t$, beginning at a specific starting point.

This is formalized by a system of two equations:

- **The ODE (Direction):**
    
    $$\frac{d}{dt}X_t = u_t(X_t)$$
    
    _(Meaning: The derivative/velocity of $X_t$ is determined by the vector field $u_t$.)_
    
- **Initial Conditions (Starting Point):**
    
    $$X_0 = x_0$$
    
    _(Meaning: At time $t=0$, we start at location $x_0$.)_
    

### 3. Flow

**The Core Question:** If we start at $X_0 = x_0$ at $t = 0$, where exactly are we at time $t$ (what is $X_t$)?

**The Answer:** A function called the **flow** ($\psi$). The flow is the mathematical solution to the ODE.

- **Flow Function:** $\psi : \mathbb{R}^d \times [0, 1] \to \mathbb{R}^d, \quad (x_0, t) \mapsto \psi_t(x_0)$
    
- **Governing Equations for Flow:**
    
    - **Flow ODE:** $\frac{d}{dt}\psi_t(x_0) = u_t(\psi_t(x_0))$
        
    - **Flow Initial Conditions:** $\psi_0(x_0) = x_0$
        

### 4. Key Takeaway & Intuition

If you know the initial condition ($X_0 = x_0$), you can find the entire trajectory using the flow: $X_t = \psi_t(X_0)$.

Because of this relationship, you can think of vector fields, ODEs, and flows as three different ways to describe the exact same object:

> **Golden Rule: Vector fields define ODEs whose solutions are flows.**

- unqiue soln to an SDE means the distribution over trajectories is constant with time