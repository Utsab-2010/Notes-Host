---
title: "Mouse VS AI"
lastmod: 2026-07-30
---

## Paper Summary: What the Paper Is Trying to Do

The paper introduces the **Mouse vs. AI: Robust Foraging Competition**, a benchmark designed to jointly evaluate **visual robustness** and **neural alignment** in artificial agents using a shared active sensorimotor task.

### 1. Goal & Core Problem

Standard reinforcement learning and computer vision models are notoriously brittle to real-world visual variations (such as fog or occlusion), whereas biological systems like mice easily maintain stable performance under degraded visual inputs. Existing benchmarks often evaluate robustness (e.g., static image corruptions) or neural alignment (e.g., passive visual encoding) separately.

This paper bridges that gap by having both virtual RL agents and real mice perform the **exact same 3D visually guided foraging task** (navigating to a target in a Unity environment).

### 2. Competition Tracks

- **Track 1 (Visual Robustness):** Evaluates how well trained RL agents generalize to **unseen visual perturbations** (e.g., clutter, random dot motion overlays, contrast-modulated noise) beyond standard conditions and a single training perturbation (fog). Performance is scored based on target acquisition success rates.
    
- **Track 2 (Neural Alignment):** Evaluates how well the internal representations of the task-trained visual encoders predict actual **two-photon calcium imaging recordings** from $>50,000$ neurons across primary and higher visual cortical areas in mice performing the same task.
    

### 3. Key Findings

- **Weak Coupling:** Generalization under visual perturbations (Track 1) and neural alignment (Track 2) show only a weak positive correlation ($r = 0.352$). Highly robust models do not automatically yield brain-like representations, and vice versa.
    
- **Architectural Trade-offs:** Deeper architectures improve neural alignment by learning hierarchical representations, whereas task robustness often benefits more from targeted inductive biases (e.g., normalization, gating, scale-equivariance) than sheer depth or parameter size.
    

## 1st Place Solution for Track 1: `HCMUS_TheFangs`

The top-ranking solution for Track 1 achieved a winning score of **0.9540** (compared to baseline scores around 0.61–0.62).

### Key Architectural & Training Details:

- **Lightweight CNN Architecture:** Instead of using massive or deep networks, the team used a compact, shallow convolutional neural network.
    
- **Gated Linear Units (GLU) & Normalization:** The model was augmented with **Gated Linear Units (GLU)** and **observation normalization**.
    
- **Key Finding via Ablations:** Ablation studies showed that **observation normalization was the single largest contributor** to their generalization performance. Adding extra architectural complexity—such as deeper residual layers, recurrent modules, or heavy data augmentation—actually degraded held-out robustness.
    
- **Early Stopping / Training Dynamics:** They discovered that model performance was highly sensitive to training duration. Stopping training at **intermediate checkpoints** yielded optimal generalization, whereas overtraining on training conditions degraded performance under unseen perturbations.
    

_(Note: For Track 2, `HCMUS_TheFangs` adopted a completely separate, much deeper convolutional model with higher capacity to capture neural dynamics, reinforcing their finding that robustness and neural alignment favor distinct regions in the model design space.)_