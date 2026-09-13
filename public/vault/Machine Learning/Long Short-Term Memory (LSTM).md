---
title: "Long Short-Term Memory (LSTM)"
lastmod: 2026-06-23
---

## 1. Motivation: What Problem Does the LSTM Solve?

Vanilla RNNs update their hidden state as:

$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b)$$

When you backpropagate through this over $T$ timesteps, the gradient of an early state involves a product of $T$ Jacobians — each involving $W_{hh}$. If the singular values of $W_{hh}$ are less than 1, gradients vanish exponentially. If greater than 1, they explode.

This means vanilla RNNs cannot reliably learn dependencies that span more than ~10–20 steps. An RNN reading a paragraph effectively forgets its first sentence by the time it reaches the last.

The LSTM (Hochreiter & Schmidhuber, 1997) was designed with one central goal:

> **Allow gradients to flow backward across arbitrarily long sequences without vanishing.**

The mechanism: replace the single hidden state with a **cell state** that is updated **additively**, not through repeated matrix multiplication.

---

## 2. The Two States: $h_t$ vs $c_t$

This is the most fundamental thing to understand about LSTMs and one of the most commonly glossed over points.

An LSTM maintains **two vectors** at each timestep:

|State|Symbol|Role|
|---|---|---|
|Hidden state|$h_t$|The "output" — what gets passed to the next layer or used for prediction|
|Cell state|$c_t$|The "memory highway" — the internal long-term memory, not directly exposed|

Think of $c_t$ as the LSTM's internal notebook — it can write to it, erase from it, or leave it unchanged. $h_t$ is what it decides to show to the outside world.

At $t=0$: both $h_0$ and $c_0$ are typically initialized to zero vectors.

---

## 3. The Four Gates

At each timestep, the LSTM computes four quantities from the concatenation of the previous hidden state and current input: $[h_{t-1}, x_t]$.

Let's denote this concatenation as $z_t = [h_{t-1}; x_t]$ for brevity.

### Gate 1: Forget Gate ($f_t$)

$$f_t = \sigma(W_f \cdot z_t + b_f)$$

- Output range: $(0, 1)$ elementwise (sigmoid)
- **Meaning**: How much of the previous cell state $c_{t-1}$ to keep.
    - $f_t \approx 1$ → keep this memory dimension
    - $f_t \approx 0$ → erase this memory dimension
- Applied to $c_{t-1}$ elementwise: $f_t \odot c_{t-1}$

**Historical note**: The forget gate was **not in the original 1997 LSTM**. It was introduced by Gers, Schmidhuber & Cummins (2000). The original LSTM had no mechanism to clear the cell state — memory only accumulated. This caused issues with tasks requiring the network to reset. The forget gate fixed this.

---

### Gate 2: Input Gate ($i_t$)

$$i_t = \sigma(W_i \cdot z_t + b_i)$$

- Output range: $(0, 1)$ elementwise
- **Meaning**: Which dimensions of the new candidate memory to actually write.
    - $i_t \approx 1$ → write this
    - $i_t \approx 0$ → ignore this

---

### Gate 3: Candidate Cell State ($\tilde{c}_t$)

$$\tilde{c}_t = \tanh(W_c \cdot z_t + b_c)$$

- Output range: $(-1, 1)$ elementwise (tanh)
- **Meaning**: What values we _want_ to potentially write to the cell state
- Not a gate — it's the actual content being written (gated by $i_t$)

The combination of $i_t$ and $\tilde{c}_t$ is the "input gate + candidate" pair: the gate decides _where_ to write, the candidate decides _what_ to write.

---

### Gate 4: Output Gate ($o_t$)

$$o_t = \sigma(W_o \cdot z_t + b_o)$$

- Output range: $(0, 1)$ elementwise
- **Meaning**: Which parts of the updated cell state $c_t$ to expose as the hidden state $h_t$

---

## 4. The Full Update Equations

### Step 1: Update the Cell State

$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

This is the heart of the LSTM. It's **additive**: the new cell state is a weighted blend of the old cell state (scaled by forget gate) and new candidate content (scaled by input gate).

### Step 2: Compute the Hidden State

$$h_t = o_t \odot \tanh(c_t)$$

The tanh squashes $c_t$ to $(-1, 1)$, then the output gate selects which parts to expose.

### Full Picture at Once

$$f_t = \sigma(W_f [h_{t-1}, x_t] + b_f) \quad \text{(forget)}$$ $$i_t = \sigma(W_i [h_{t-1}, x_t] + b_i) \quad \text{(input)}$$ $$\tilde{c}_t = \tanh(W_c [h_{t-1}, x_t] + b_c) \quad \text{(candidate)}$$ $$o_t = \sigma(W_o [h_{t-1}, x_t] + b_o) \quad \text{(output)}$$ $$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$ $$h_t = o_t \odot \tanh(c_t)$$

---

## 5. Why the LSTM Solves Vanishing Gradients

The gradient of the loss with respect to an earlier cell state $c_k$:

$$\frac{\partial L}{\partial c_k} = \frac{\partial L}{\partial c_T} \cdot \prod_{t=k+1}^{T} \frac{\partial c_t}{\partial c_{t-1}}$$

Now, the key: $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$, so:

$$\frac{\partial c_t}{\partial c_{t-1}} = \text{diag}(f_t)$$

The gradient flows back through **elementwise multiplication by the forget gate values** — not through a full weight matrix multiplication. This is the "Constant Error Carousel" from the original paper.

If the forget gate stays near 1, the gradient passes through largely unchanged — no vanishing. The LSTM learns _when_ to open or close the forget gate, giving it control over gradient flow.

**Compare to vanilla RNN**:

- Vanilla RNN: $\frac{\partial h_t}{\partial h_{t-1}} = \text{diag}(\tanh'(\cdot)) \cdot W_{hh}^T$ — a matrix multiplication at every step, leading to exponential decay or explosion.
- LSTM: $\frac{\partial c_t}{\partial c_{t-1}} = \text{diag}(f_t)$ — an elementwise scale, learned to be near 1 when memory should persist.

**Nuance**: This doesn't completely eliminate vanishing gradients — the gradient through $h_t$ (not $c_t$) still passes through weight matrices. But the cell state provides a "shortcut" highway that mitigates the problem significantly for the information that matters most.

---

## 6. Parameter Count

For hidden size $H$ and input size $D$, each gate has a weight matrix of size $H \times (H + D)$ and a bias of size $H$.

Total parameters per LSTM layer:

$$4 \times [H \times (H + D) + H] = 4H(H + D + 1)$$

This is roughly **4× more parameters** than a vanilla RNN with the same hidden size, which has $H(H + D + 1)$ parameters.

The four matrices $W_f, W_i, W_c, W_o$ are often concatenated into a single large matrix for efficient computation:

$$W = [W_f; W_i; W_c; W_o] \in \mathbb{R}^{4H \times (H+D)}$$

This is how most implementations (PyTorch, TensorFlow) do it internally — one large matrix multiply, then split into four.

---

## 7. Initialization Tricks

### Forget Gate Bias = 1.0

One of the most important practical tricks: initialize the forget gate bias $b_f$ to **1.0** (or sometimes 2.0).

Why? At the start of training, you want the LSTM to **default to remembering**. If $b_f = 0$, the forget gate starts at $\sigma(0) = 0.5$, meaning half the cell state is erased at each step. This makes learning long-range dependencies much harder early in training.

Setting $b_f = 1.0$ means $f_t \approx \sigma(1) \approx 0.73$ initially — the network leans toward keeping memory. As training progresses, the network learns to override this default when appropriate.

This was proposed by Gers et al. and later empirically validated by Jozefowicz et al. (2015) in "An Empirical Exploration of Recurrent Network Architectures."

### Orthogonal Initialization for Recurrent Weights

The recurrent weight matrices (portions of $W_f, W_i, W_c, W_o$ corresponding to $h_{t-1}$) should be initialized **orthogonally**. An orthogonal matrix has singular values all equal to 1, which means it doesn't shrink or explode norms of the hidden state on the first forward pass.

Xavier/Glorot initialization (for feedforward portions) + orthogonal (for recurrent portions) is the standard recipe.

---

## 8. Variants and Extensions

### Peephole Connections (Gers & Schmidhuber, 2000)

The standard LSTM gates look only at $h_{t-1}$ and $x_t$ — they don't see the cell state $c_{t-1}$ directly. Peephole connections add $c_{t-1}$ as an additional input to the gates:

$$f_t = \sigma(W_f [h_{t-1}, x_t, c_{t-1}] + b_f)$$ $$i_t = \sigma(W_i [h_{t-1}, x_t, c_{t-1}] + b_i)$$ $$o_t = \sigma(W_o [h_{t-1}, x_t, c_t] + b_o) \quad \text{(note: } c_t \text{ for output gate)}$$

This lets the gates make decisions based on the exact memory content. Useful for tasks requiring precise timing (e.g., counting, rhythm). In practice, rarely improves over standard LSTM enough to justify the added complexity.

### Coupled Input and Forget Gates

A simplification: instead of independent $f_t$ and $i_t$, couple them so that what you forget = what you write:

$$c_t = f_t \odot c_{t-1} + (1 - f_t) \odot \tilde{c}_t$$

This reduces parameters and enforces that you can only write new information where you've erased old information. This coupling is one of the simplifications that leads to the GRU.

### Depth Variants

- **Stacked LSTM**: Multiple LSTM layers where $h_t^{(l)}$ feeds into the next layer as input
- **Deep Transition RNN**: Multiple nonlinear layers _between_ timesteps (not just between layers)
- **Grid LSTM**: LSTMs arranged in a multidimensional grid — depth and time both handled with LSTM cells

---

## 9. Bidirectional LSTM (BiLSTM)

Run two LSTMs:

- Forward LSTM: reads $x_1 \to x_T$, produces $\overrightarrow{h_t}$
- Backward LSTM: reads $x_T \to x_1$, produces $\overleftarrow{h_t}$

Final representation: $h_t = [\overrightarrow{h_t}; \overleftarrow{h_t}]$ (concatenation, doubling the hidden size)

**When to use**: Classification tasks, tagging (NER, POS), any task where the full sequence is available at inference. Do **not** use for autoregressive generation — you can't run the backward LSTM without seeing the future.

**Nuance about parameter count**: A BiLSTM with hidden size $H$ has two separate LSTM networks, each with hidden size $H$. The output has dimension $2H$. The total parameter count is double that of a unidirectional LSTM.

---

## 10. Stacked (Deep) LSTMs

Multiple LSTM layers stacked:

$$h_t^{(1)} = \text{LSTM}_1(x_t, h_{t-1}^{(1)}, c_{t-1}^{(1)})$$ $$h_t^{(2)} = \text{LSTM}_2(h_t^{(1)}, h_{t-1}^{(2)}, c_{t-1}^{(2)})$$

The idea: lower layers capture local/syntactic patterns, higher layers capture more abstract/semantic patterns — analogous to depth in CNNs.

**Empirical sweet spot**: 2–4 layers. Beyond that, training becomes unstable and performance often degrades.

**Residual connections in stacked LSTMs**: For deeper stacks (3+ layers), adding skip connections $h_t^{(l)} = \text{LSTM}_l(\cdot) + h_t^{(l-1)}$ (when dimensions match) helps gradient flow and is common in production systems like Google's NMT architecture.

---

## 11. Dropout in LSTMs (Correctly)

### What NOT to Do

Applying standard dropout to $h_t$ at every timestep independently corrupts the memory signal at each step, making temporal learning very difficult.

### Variational Dropout (Gal & Ghahramani, 2016)

Sample a single binary dropout mask for $h_t$ and apply it **consistently at every timestep**:

$$h_t^{\text{dropped}} = h_t \odot m, \quad m \sim \text{Bernoulli}(1-p) \text{ (sampled once per sequence)}$$

This respects the sequential structure — the same units are dropped throughout the sequence, rather than introducing noise at every step.

**In PyTorch**: The `dropout` parameter in `nn.LSTM` applies dropout between LSTM layers (to $h_t^{(l)}$ before it enters the next layer), not within the recurrent connections. For intra-recurrent dropout you need a custom implementation or a library like AWD-LSTM.

### Zoneout (Krueger et al., 2016)

Rather than zeroing activations, randomly preserve the **previous** value:

$$h_t = \begin{cases} h_{t-1} & \text{with probability } p \ \text{LSTM}(h_{t-1}, x_t) & \text{with probability } 1-p \end{cases}$$

Applied elementwise. This acts as a regularizer that encourages the LSTM to maintain information across timesteps, and is particularly effective for the cell state.

### Weight Dropout / DropConnect (Merity et al. — AWD-LSTM)

Drop the weight matrices of the recurrent connections (not the activations) at each forward pass. This is the approach used in AWD-LSTM (ASGD Weight-Dropped LSTM), which was state-of-the-art for language modeling before Transformers took over. The key: drop $W_{hh}$ once per forward pass, not per timestep.

---

## 12. Gradient Flow: Detailed Analysis

Let $L$ be the total loss. During BPTT, we need $\frac{\partial L}{\partial h_k}$ for all $k$.

For the **cell state pathway**:

$$\frac{\partial L}{\partial c_k} = \frac{\partial L}{\partial c_T} \prod_{t=k+1}^{T} f_t$$

Since $f_t \in (0,1)$ and the product is elementwise, each $c_k$ dimension independently has its gradient scaled by the product of forget gate values along that dimension. If the forget gate is near 1 (remember), gradient is near 1. If near 0 (forget), gradient vanishes — but appropriately, since we intentionally forgot that memory.

For the **hidden state pathway** (through $h_t = o_t \odot \tanh(c_t)$):

Gradients through $h_t$ still go through weight matrices, so they can still vanish over long distances. But the cell state provides the primary long-distance gradient highway.

**Key insight**: The LSTM doesn't eliminate vanishing gradients — it provides an optional gradient highway through the cell state. The network learns to route important information through this highway.

---

## 13. Practical Notes for PyTorch

```python
import torch
import torch.nn as nn

# Single-layer LSTM
lstm = nn.LSTM(
    input_size=D,       # input feature dimension
    hidden_size=H,      # hidden state dimension
    num_layers=2,       # number of stacked layers
    batch_first=True,   # input shape: (batch, seq_len, input_size)
    bidirectional=False,
    dropout=0.3         # dropout between layers (not within recurrent connections)
)

# Initial states
h0 = torch.zeros(num_layers, batch_size, H)
c0 = torch.zeros(num_layers, batch_size, H)

output, (hn, cn) = lstm(x, (h0, c0))
# output: (batch, seq_len, H) — h_t at every timestep
# hn: (num_layers, batch, H) — final hidden state per layer
# cn: (num_layers, batch, H) — final cell state per layer
```

### Important Implementation Details

- **`batch_first=True`**: Makes the input shape `(batch, seq_len, features)`. Default is `(seq_len, batch, features)`. Choose consistently.
- **Packing sequences**: For variable-length sequences in a batch, use `nn.utils.rnn.pack_padded_sequence` before the LSTM and `pad_packed_sequence` after. This skips computation on padding tokens and prevents padding from affecting hidden states.
- **Accessing cell state**: `hn` gives you the final hidden state. `cn` gives you the final cell state. If you need $c_t$ at every step (not just $c_T$), you need a custom loop.
- **Gradient clipping**: Always clip before the optimizer step:
    
    ```python
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)optimizer.step()
    ```
    

---

## 14. The Forget Gate: Its Centrality and Its Limits

The forget gate is arguably the most important gate in the LSTM. Some observations:

- **Ablation studies** have shown that removing the forget gate degrades LSTM performance significantly on most tasks, more so than removing other gates.
- **Jozefowicz et al. (2015)** ran a large-scale architecture search and found that the forget gate was the single most critical component. They also found that initializing $b_f$ to 1 or 2 consistently helped.
- **The forget gate enables task switching**: If the input indicates a context change (e.g., start of a new sentence), the forget gate can clear irrelevant memory all at once.

**Limit**: The forget gate applies the same scalar per memory dimension — it can't do complex transformations of memory (e.g., it can't rotate, combine, or redistribute information across memory dimensions). This is a fundamental limitation compared to attention mechanisms, which can perform arbitrary reweighting.

---

## 15. LSTM vs Transformer: What LSTMs Can't Do

|Property|LSTM|Transformer|
|---|---|---|
|Long-range dependency|Good, not perfect|Excellent (direct attention)|
|Parallelizable over time|No (sequential by nature)|Yes|
|Constant-time access to past|No (must propagate through states)|Yes (direct attention)|
|Memory footprint at inference|O(1) per step|O(T) (must store all past KV)|
|Performance on long sequences|Degrades|Largely constant|
|Good for streaming|Yes|Harder (needs full context)|

The core limitation of LSTMs is that accessing a memory from 500 timesteps ago requires that information to have been **propagated forward through 500 cell state updates** without being overwritten. Attention bypasses this entirely by directly looking back.

This is why Transformers replaced LSTMs for NLP. But at inference time, LSTMs run in $O(1)$ memory per step, while Transformers require storing the entire KV cache — making LSTMs still relevant for edge/streaming use cases.

---

## 16. Summary: The Core Loop

At every timestep $t$:

1. **Forget**: Decide what to erase from memory → $f_t$
2. **Propose**: Compute what new content to write → $\tilde{c}_t$
3. **Gate the write**: Decide how much to actually write → $i_t$
4. **Update memory**: $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$
5. **Expose**: Decide what to share with the outside world → $o_t$
6. **Output**: $h_t = o_t \odot \tanh(c_t)$

The elegance of the LSTM is that each of these decisions is learned end-to-end from data, with no hand-tuning.

---

## Key Takeaways

- The LSTM maintains two states: $h_t$ (output/hidden) and $c_t$ (internal cell memory).
- The cell state update is additive, giving gradients a highway to flow through without vanishing.
- The forget gate (added in 2000, not the original 1997 design) is the most critical gate — initialize its bias to 1.0.
- Four gates total: forget, input, candidate (not a gate technically), output. Each is a learned sigmoid/tanh applied to $[h_{t-1}, x_t]$.
- LSTMs have ~4× the parameters of a vanilla RNN for the same hidden size.
- Use variational dropout or zoneout, not standard per-step dropout.
- Always use gradient clipping and orthogonal recurrent weight initialization.
- LSTMs don't fully solve vanishing gradients — they mitigate it via the cell state highway.
- Transformers have displaced LSTMs for most NLP tasks, but LSTMs remain relevant for streaming, edge, and time-series applications due to their O(1) inference memory footprint.