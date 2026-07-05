---
title: "Alphazero Workflow"
lastmod: 2026-06-24
---

# MCTS Self-Play Walkthrough & Code Optimizations

---

## 🧠 Part 1: How the Naive Policy is Used in MCTS Self-Play

During self-play data generation (in `train_alphazero.py`), the agent uses MCTS to decide on moves. The **naive policy** output by the neural network acts as a **prior probability distribution** ($P(s, a)$) that guides search simulations toward promising actions.

Here is a detailed, step-by-step trace of how this happens over the first few search iterations (simulations) for a single move decision.

### The Baseline Setup
* **Search Budget**: We run $N$ simulations (e.g., `MCTS_SIMS = 10` or `800`) to decide a single move.
* **Root Node ($S_{root}$)**: The current game board state.
* **PUCT Selection Formula**: At any expanded node $s$, we choose the action $a$ maximizing:
  $$U(s, a) = Q(s, a) + c_{puct} \cdot P(s, a) \cdot \frac{\sqrt{\sum_b N(s, b)}}{1 + N(s, a)}$$
  * $Q(s, a)$ is the average value backpropagated for action $a$.
  * $P(s, a)$ is the **prior probability** (the network's naive policy).
  * $N(s, a)$ is the visit count for action $a$.

---

### Step-by-Step Walkthrough of the First 3 Simulations

#### 1️⃣ Simulation 1: Root Node Evaluation & Initial Expansion
* **Selection**:
  * We start at $S_{root}$. 
  * Initially, $S_{root}$ is not marked as expanded (`is_expanded = False`). The selection loop terminates immediately at the root.
* **Evaluation**:
  * The root state $S_{root}$ is treated as the leaf node.
  * The board state is preprocessed (and canonicalized if it is Player 2's turn) and sent through the neural network.
  * The network returns:
    1. **Naive Policy Logits**: `policy_logits`
    2. **Value Estimate** ($v$): A scalar in $[-1, 1]$ predicting the game outcome from the current player's perspective.
  * The policy logits are softmaxed to generate `policy_probs` (the naive policy).
* **Expansion**:
  * We retrieve the valid actions (empty hexes) for $S_{root}$.
  * The `policy_probs` for only these valid actions are extracted and renormalized so they sum to 1.
  * Children nodes are created for each valid action. The $P(s, a)$ (`prior_prob`) for each child is set to its renormalized network policy probability.
  * The root is marked as `is_expanded = True`.
* **Backpropagation**:
  * The value estimate $v$ is backpropagated up the path. The root's visit count $N(S_{root})$ becomes 1.

> [!NOTE]
> **Dirichlet Noise Placement Observation**
> In the current implementation of `mcts.py`, Dirichlet noise is added to the root children *before* Simulation 1 runs. However, during Simulation 1, `_evaluate_batched` overwrites the root's children priors directly with `valid_probs[j]`, discarding the noise. To fix this, Dirichlet noise should be applied *after* the network evaluation in the first simulation.

---

#### 2️⃣ Simulation 2: Selecting and Expanding a Child
* **Selection**:
  * We start at $S_{root}$. Now `is_expanded` is True.
  * We calculate the PUCT score for all children of $S_{root}$.
  * Since all children have 0 visits ($N(S_{root}, a) = 0$), $Q(S_{root}, a)$ defaults to 0.
  * The PUCT score is determined entirely by the prior probability:
    $$U(S_{root}, a) = c_{puct} \cdot P(s, a) \cdot \sqrt{N(S_{root})}$$
  * Therefore, the action $a_1$ with the **highest naive policy probability** (highest $P(s, a)$) is selected.
  * We traverse to the child node $S_1$ (corresponding to action $a_1$).
  * $S_1$ is not expanded yet, so selection stops here.
* **Evaluation**:
  * The game state at $S_1$ is sent to the neural network.
  * The network outputs the naive policy probabilities `policy_probs_S1` and value estimate $v_{S1}$ for $S_1$.
* **Expansion**:
  * We retrieve valid moves at $S_1$.
  * We create children nodes for $S_1$, initializing their prior probabilities using the renormalized `policy_probs_S1`.
  * $S_1$ is marked as expanded.
* **Backpropagation**:
  * $v_{S1}$ is backpropagated.
  * At $S_1$: $N(S_1)$ increases to 1. $Q(S_1)$ is updated.
  * At $S_{root}$: $N(S_{root})$ increases to 2. $Q(S_{root}, a_1)$ is updated to $-v_{S1}$ (since players alternate, a good state for Player 2 is a bad state for Player 1).

---

#### 3️⃣ Simulation 3: Deeper Selection vs. Breadth Search
* **Selection**:
  * We start at $S_{root}$.
  * We recalculate the PUCT score for all children of $S_{root}$:
    * Child $a_1$ now has $N(S_{root}, a_1) = 1$ and a non-zero $Q(S_{root}, a_1)$ value. Its exploration term decreases.
    * Other children $a_k$ still have $N(S_{root}, a_k) = 0$ and $Q = 0$.
  * The algorithm compares $Q(S_{root}, a_1) + U(S_{root}, a_1)$ against the purely prior-driven $U(S_{root}, a_k)$ of unvisited sibling nodes.
  * **Scenario A (Exploit)**: If the network evaluation of $S_1$ was highly favorable (large positive Q-value) and the prior $P(S_{root}, a_1)$ was very strong, $a_1$ might still have the highest PUCT score.
    * We select $a_1$, move to $S_1$.
    * Since $S_1$ is expanded, we evaluate the PUCT scores of $S_1$'s children (using the priors generated for $S_1$ in Simulation 2).
    * We select the best child $S_{1b}$ of $S_1$.
    * $S_{1b}$ is a leaf, so it is evaluated by the network, expanded, and backpropagated.
  * **Scenario B (Explore)**: If $S_1$ resulted in a poor evaluation (negative Q-value) or other actions had competitive priors, an unvisited sibling $a_2$ will have a higher PUCT score.
    * We select $a_2$, move to $S_2$.
    * $S_2$ is a leaf, so it is evaluated by the network, expanded, and backpropagated.

---

### Deciding the Move
After running all simulations (e.g. 10):
1. MCTS counts the visits $N(S_{root}, a)$ of all children of the root node.
2. The search policy $\pi(a | S_{root})$ is computed proportional to $N(S_{root}, a)^{1/\tau}$ (where $\tau$ is the temperature).
3. The actual move is sampled from $\pi$ during self-play. 
4. The network is then trained to predict $\pi$ rather than its own naive policy, making the model iteratively match the MCTS search.

---

## ⚡ Part 2: Codebase Improvements & Optimizations

Here is a summary of all key optimizations implemented in the repository to improve code design, training stability, and performance:

| Optimization / Improvement | Target Area | Description & Rationale |
| :--- | :--- | :--- |
| **Vectorized Environments** (`SyncVectorEnv`) | Speed | Runs 512 parallel game environments in `train_dqn_vector.py`. Allows the GPU to process transitions simultaneously in a single batched inference pass, bypassing Python's GIL constraints and loop overhead (speeding up collection by ~10–15x). |
| **Canonical Perspective Board Flipping** | Training Efficiency | When it is Player 2's turn, `SelfPlayWrapper` flips the board representation (swapping player 1 and 2 IDs). This enables a single model to always learn to play as "Player 1" (canonical perspective), effectively doubling training data density and eliminating the need for two separate networks. |
| **Flat ResNet Backbone (No Downsampling)** | Model Architecture | `AlphaBH` uses flat stride-1 ResNet blocks instead of stride-2 downscaling layers. Downsampling destroys fine spatial/coordinate precision (e.g., row 3 vs row 4). Maintaining board resolution ($L \times L$) retains precise coordinate relationships crucial for board games. |
| **Separated Validity Mask Inputs** | Numerical Stability | Splitting the network input into Channel 0 (signed tile values) and Channel 1 (binary valid board mask). This prevents large invalid penalties (like `-1000.0` on void grid locations) from inflating BatchNorm variance and destabilizing training. |
| **Winrate Streak Promotion** | Training Robustness | Promoting the self-play opponent model requires a consecutive evaluation win streak rather than a single victory threshold. This filters out variance/lucky runs and ensures only structurally stronger models are promoted. |
| **Batched MCTS Leaf Evaluation** | MCTS Speed | Instead of executing a separate PyTorch forward pass for every single MCTS simulation's leaf evaluation, `run_batched` aggregates leaf states across all active parallel games and performs a single batched inference pass. This dramatically reduces GPU launch overhead. |
| **Cyclic Epsilon Decay** | Exploration | Epsilon decreases linearly to prevent random moves, but restarts periodically (cosine annealing cycles). This prevents the agent from getting stuck in local optima during early stages of self-play. |
| **Adjacency Pre-Calculation** | Execution Speed | Triangular board adjacency list is generated once during environment initialization (`_build_adjacency`) rather than dynamically computed at every step, speeding up BFS ring calculations. |
