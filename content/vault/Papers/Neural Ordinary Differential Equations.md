---
title: "Neural Ordinary Differential Equations"
lastmod: 2026-05-03
---

#flows
continuous normalizing flows

### **Continuous-Depth Residual Models**

In traditional **Residual Networks (ResNets)**, the model is built from a sequence of layers that make discrete jumps. Each layer transforms the data by adding a small change to it: $h_{t+1} = h_t + f(h_t, \theta_t)$.

- **From Jumps to Flow**: 
	- As you add more layers and make the steps smaller, this process starts to look like a continuous flow.
- **Neural ODEs**: 
	- Instead of specifying a fixed number of layers, a **Neural Ordinary Differential Equation (ODE)** defines the _rate of change_ of the hidden state using a neural network:$$\large 
		  \frac{dh(t)}{dt} = f(h(t), t, \theta)$$
- **Depth as Time**: 
	- In this view, the "depth" of the model is like "time." To get the final output, you don't pass through layers; you use an **ODE solver** to calculate the state of the data at the final "time" or depth.


> [!NOTE] Note
> They treat the ODE solver as a black box, and compute gradients using the adjoint sensitivity method (Pontryagin et al., 1962).

