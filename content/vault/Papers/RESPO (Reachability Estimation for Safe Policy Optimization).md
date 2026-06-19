---
title: "RESPO (Reachability Estimation for Safe Policy Optimization)"
lastmod: 2026-05-19
---

#robotics #controls
The framework is inspired by **Hamilton-Jacobi (HJ) reachability analysis**, a control-theoretic approach that rigorously verifies safety by finding the set of states from which an agent can avoid obstacles. RESPO was specifically developed to address the limitations of prior reachability-based methods, like RCRL, which struggled with **stochasticity** and lacked guarantees for **recovery** (re-entering safe zones) once a violation occurred.

### Contributions
- Addresses the stochasticity of real world 
- Address the weak safety guarantees of other methods
- Makes it such that an agent can go back to the safe region from a danger zone.
- Use **Reachability Analysis** but adapt it for unpredictable general RL.
- Created a REF(reachability estimation function) - gives probablility that the agent will ever hit a violation in the future starting from current state. 
- Optimises the Agent's behaviour
	- Safe Zone: if ref is low focus on maxing rewards
	- Danger Zone : if ref is high, focus on returning to safe. 

### 1. The Math of Reachability (REF)
The core of the method is the **Reachability Estimation Function (REF)**, denoted as $\phi^{\pi}(s)$.
- **Bellman Recursion**: The authors prove that this probability can be learned iteratively using a **recursive Bellman formulation**: $$\large \phi^{\pi}(s) = \max\{\mathbb{I}_{s \in \mathcal{S}_v}, \mathbb{E}_{s' \sim \pi, P(s)} \phi^{\pi}(s')\}$$where $\mathbb{I}_{s \in \mathcal{S}_v}$ is $1$ if the current state is unsafe and $0$ otherwise. This "max" operator is critical: it says your risk is either your current violation or the maximum risk you face in the next step.
- **Unified Objective**: The full optimization objective (Equation 4) combines reward and safety:$$\min_{\pi} \max_{\lambda} \mathbb{E}_{s \sim d_0} [([-V^{\pi}(s) + \lambda \cdot V_c^{\pi}(s)] \cdot (1 - p(s)) + V_c^{\pi}(s) \cdot p(s))]$$
	- If $p(s) = 0$ (Safe Zone), it maximizes rewards while keeping costs at zero.
    - If $p(s) = 1$ (Danger Zone), it ignores rewards and focuses solely on minimizing costs ($V_c$) to get back to safety.

---

### 2. Implementation Details
The researchers implemented RESPO as an **Actor-Critic** algorithm. Below is the technical setup used to turn the theory into a working agent:
#### Architecture & Hyperparameters
- **Neural Networks**: They used Multi-Layer Perceptrons (MLP) for the Actor (policy), the Critics (reward and cost), and the REF ($p(s)$).
- **Network Size**: 2 hidden layers with 256 units each.
- **Activations**: `tanh` for hidden layers, `sigmoid` for the REF output (to keep it between 0 and 1), and `softplus` for the Lagrange multiplier ($\lambda$).
- **Learning Rates**: A **multi-timescale schedule** was used where critics learn fastest ($1\times 10^{-3}$), the actor is middle ($3\times 10^{-4}$), the REF is second slowest ($1\times 10^{-4}$), and the Lagrange multiplier is slowest ($5\times 10^{-5}$).

## Training Process
1. **Sampling**: The agent collects trajectories by interacting with the environment.    
2. **Updating Critics**: The reward and cost critics are updated using standard Temporal Difference (TD) learning.
3. **Updating REF**: The $p(s)$ network is updated to minimize the difference between its current guess and the recursive Bellman value.
4. **Updating Policy**: The actor’s weights are adjusted in a direction that lowers the combined objective, guided by the REF's "safety probability".
---
### 3. Experiments and Testing

To prove the theory works, they tested RESPO across three major high-dimensional benchmarks:

|**Benchmark**|**Environments**|**Key Challenge**|
|---|---|---|
|**Safety Gym**|PointButton, CarGoal|Avoiding moving obstacles and hazards while reaching goal buttons.|
|**Safety PyBullet**|DroneCircle, BallRun|Keeping a quadcopter in a safety zone with 5% gaussian noise (stochasticity).|
|**Safety MuJoCo**|HalfCheetah, Reacher|Managing complex physics without "cheating" (e.g., running backward to avoid a forward limit).|

####  Primary Findings:
- **Balance**: RESPO consistently achieved higher rewards than other safe algorithms (like FAC or CBF) while maintaining near-zero violations.
- **Recovery**: In the **Double Integrator** test, they showed that RESPO is one of the few algorithms that can actually "re-enter" the safe set after wandering out, whereas others (like RCRL) stayed failed indefinitely.
- **Prioritization**: In a multi-drone tunnel test, RESPO successfully prioritized "Wall Avoidance" over "Staying Close," showing it can manage hierarchical safety rules.
- 
