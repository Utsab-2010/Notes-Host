---
title: "Recurrent Neural Netoworks(RNNs)"
lastmod: 2026-06-23
---

## 1. The Core Idea: Why Not Just Use Feedforward Networks?

A standard MLP or CNN processes a fixed-size input and produces a fixed-size output. Each input is treated **independently** — the network has no memory of what it saw before.

But many real-world problems are **sequential**: the meaning of a word depends on previous words; the next stock price depends on past prices; a music note makes sense only in context.

The key insight behind RNNs:
> **Process sequences by maintaining a hidden state — a "memory" — that gets updated at each step.**

---
## 2. The Basic RNN: Architecture
At each timestep $t$, the RNN takes:
- $x_t$: the current input
- $h_{t-1}$: the hidden state from the previous timestep ("memory")

And produces:
- $h_t$: the updated hidden state
- $y_t$: an output (optional, depending on the task)

### The Equations
$$h_t = \tanh(W_{hh} \cdot h_{t-1} + W_{xh} \cdot x_t + b_h)$$
$$y_t = W_{hy} \cdot h_t + b_y$$
Where:
- $W_{hh}$: hidden-to-hidden weight matrix (how much the previous memory matters)
- $W_{xh}$: input-to-hidden weight matrix (how much the current input matters)
- $W_{hy}$: hidden-to-output weight matrix
- $b_h, b_y$: biases

**Key nuance**: The weight matrices $W_{hh}$, $W_{xh}$, $W_{hy}$ are **shared across all timesteps**. This is what makes an RNN an RNN — the same function is applied repeatedly, just with evolving state.

### The "Unrolled" View
If you unroll an RNN across time, it looks like a very deep feedforward network where each "layer" is a timestep, and the layers all share weights. This framing is important for understanding backpropagation through it.

```
x_1 → [RNN] → h_1 → [RNN] → h_2 → [RNN] → h_3
         ↑              ↑              ↑
        y_1            y_2            y_3
```
---

## 3. Input/Output Configurations
RNNs are extremely flexible in their I/O structure. All of these are valid:

|Mode|Description|Example|
|---|---|---|
|**Many-to-many (same length)**|Output at every step|POS tagging, NER|
|**Many-to-many (diff length)**|Encoder-decoder / seq2seq|Machine translation|
|**Many-to-one**|Read sequence, output once|Sentiment classification|
|**One-to-many**|Single input, output sequence|Image captioning|
|**One-to-one**|Same as MLP (degenerate case)|N/A|

**Nuance**: In the many-to-many different-length case, you typically run one RNN (encoder) over the input to get a context vector, then feed that into another RNN (decoder) that generates outputs one by one — this is the **seq2seq** architecture. The context vector is the bottleneck: it must compress the entire input sequence.

---

## 4. Training: Backpropagation Through Time (BPTT)

Since an unrolled RNN is just a deep network, you can run standard backpropagation through it. But because the network is unrolled _through time_, this is called **Backpropagation Through Time (BPTT)**.

### How BPTT Works

1. Forward pass: compute $h_1, h_2, \ldots, h_T$ and all outputs
2. Compute loss at each step (or at the final step, depending on the task)
3. Backward pass: backpropagate gradients from $h_T$ all the way back to $h_1$

The gradient of the loss with respect to an early hidden state $h_k$ requires multiplying many Jacobian matrices:

$$\frac{\partial h_T}{\partial h_k} = \prod_{t=k+1}^{T} \frac{\partial h_t}{\partial h_{t-1}} = \prod_{t=k+1}^{T} W_{hh}^T \cdot \text{diag}(\tanh'(\cdot))$$

This product of matrices is the root of two major problems.

### Truncated BPTT

For very long sequences, unrolling all the way back is computationally expensive and memory-intensive. **Truncated BPTT** backpropagates only through the last $k$ steps instead of the full sequence. This is a practical compromise — you sacrifice some gradient quality for tractability.

---

## 5. The Vanishing and Exploding Gradient Problems

### Vanishing Gradients

If the singular values of $W_{hh}$ are less than 1, the repeated multiplication makes gradients exponentially shrink:

$$\left|\frac{\partial h_T}{\partial h_k}\right| \sim \lambda^{T-k}$$

where $\lambda < 1$. After even 10-20 timesteps, the gradient from an early input is essentially zero. The network **cannot learn long-range dependencies**.

**Practical consequence**: A vanilla RNN reading a long sentence will effectively "forget" what it saw at the beginning by the time it reaches the end.

### Exploding Gradients

If singular values of $W_{hh}$ are greater than 1, gradients grow exponentially. This causes instability during training — weights update by huge amounts and the loss diverges.

**Fix for exploding gradients: Gradient Clipping**  
Before the update step, if the gradient norm exceeds a threshold $\theta$:

$$g \leftarrow \frac{\theta}{|g|} \cdot g$$

This is a standard, universally-used trick. It's simple and effective.

**Fix for vanishing gradients**: Requires architectural changes — LSTMs and GRUs (see below).

---

## 6. Long Short-Term Memory (LSTM)

The LSTM was designed specifically to address the vanishing gradient problem. The key idea: give the network an explicit **cell state** $c_t$ that acts as a "highway" for gradients to flow through time without repeated multiplication by the same matrix.

### The Four Gates

LSTMs have four learned "gates" — each is a sigmoid or tanh applied to the concatenation of $[h_{t-1}, x_t]$:
**Forget Gate** — what to erase from cell state: $$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$**Input Gate** — what new info to write: $$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$
**Candidate Cell State** — what to potentially write: $$\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$
**Output Gate** — what to expose as hidden state: $$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$

### Cell State and Hidden State Update
$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

$$h_t = o_t \odot \tanh(c_t)$$

Where $\odot$ is elementwise multiplication.

### Why Does This Fix Vanishing Gradients?

The cell state update is **additive** (not multiplicative by a weight matrix):

$$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$

The gradient can flow from $c_T$ back to $c_k$ through the $f_t$ gates without going through repeated matrix multiplications. If the forget gate is close to 1, the gradient passes through nearly unchanged. This is the "constant error carousel" intuition from the original LSTM paper.

### Nuances Often Skipped

- LSTMs have **two** hidden states per timestep: $h_t$ (the "exposed" output) and $c_t$ (the "internal" memory). They serve different roles.
- The forget gate was **not in the original 1997 LSTM** — it was added by Gers et al. (2000). Before that, LSTMs had a persistent memory with no way to clear it, which was problematic.
- Peephole connections (making the gates also look at $c_{t-1}$ directly) exist as an LSTM variant but are rarely used today.
- In practice, LSTMs have roughly **4x** the parameters of a vanilla RNN for the same hidden size, because of the four gate matrices.

---

## 7. Gated Recurrent Unit (GRU)

The GRU (Cho et al., 2014) is a simplified version of the LSTM. It merges the cell state and hidden state into a single $h_t$, and uses only two gates:

**Reset Gate** — how much of the old state to forget: $$r_t = \sigma(W_r \cdot [h_{t-1}, x_t])$$

**Update Gate** — how much to update vs. keep: $$z_t = \sigma(W_z \cdot [h_{t-1}, x_t])$$

**Candidate hidden state**: $$\tilde{h}_t = \tanh(W_h \cdot [r_t \odot h_{t-1}, x_t])$$

**Final update**: $$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$$

### LSTM vs GRU

||LSTM|GRU|
|---|---|---|
|Gates|3 (forget, input, output)|2 (reset, update)|
|States|$h_t$ and $c_t$|only $h_t$|
|Parameters|~4x vanilla RNN|~3x vanilla RNN|
|Performance|Usually slightly better on long sequences|Faster, roughly comparable|

**Practical rule of thumb**: GRU trains faster and is easier to tune. Start with GRU; switch to LSTM if you need better long-range memory.

---

## 8. Bidirectional RNNs

A standard RNN only has access to the **past** when processing $x_t$. But for many tasks (e.g., text classification, named entity recognition), the future context also matters — you want to know what comes _after_ a word to understand it.

A **Bidirectional RNN** runs two RNNs:

- One forward: $\overrightarrow{h_t}$ reading left-to-right
- One backward: $\overleftarrow{h_t}$ reading right-to-left

The final representation at each step is the concatenation: $$h_t = [\overrightarrow{h_t}; \overleftarrow{h_t}]$$

**Nuance**: Bidirectional RNNs only make sense when you have access to the **full sequence** at inference time. They cannot be used for autoregressive generation (e.g., language modeling step by step), since the backward pass requires seeing the future.

---

## 9. Deep (Stacked) RNNs

You can stack multiple RNN layers, where the output of one layer becomes the input to the next:

```
x_t → [RNN Layer 1] → h_t^(1) → [RNN Layer 2] → h_t^(2) → ... → output
```

Empirically, 2-4 layers is the sweet spot. More layers help capture increasingly abstract temporal patterns, but also make training harder (deeper = more gradient issues) and slower.

**Nuance**: Stacking RNN layers is not the same as unrolling through time. Depth through layers = richer representation at each step. Depth through time = capturing long-range dependencies.

---

## 10. Dropout in RNNs

Standard dropout (randomly zeroing activations) applied to RNN hidden states at each timestep causes issues — you're corrupting the memory signal at every step, which disrupts temporal learning.

### Variational Dropout (Correct approach)
Sample the dropout mask **once per sequence** and apply it consistently at every timestep. This way, the mask doesn't interfere with temporal dependencies.

### Zoneout
An alternative to dropout specifically for RNNs: instead of zeroing units, randomly **copy** the previous hidden state value forward. This acts as a form of regularization that respects the recurrent nature.

---

## 11. Teacher Forcing
During training of sequence-to-sequence models, you have a choice:

- **Teacher forcing**: At each decoding step, feed the **ground truth** previous token as input (even if the model predicted wrong)
- **Free running (exposure bias)**: Feed the model's **own prediction** at each step

Teacher forcing trains faster and more stably. But at inference time, the model must use its own predictions. This mismatch between training and inference is called **exposure bias** and is a fundamental tension in RNN-based seq2seq training.

**Scheduled sampling** (Bengio et al., 2015) addresses this by gradually transitioning from teacher forcing to free running during training.

---

## 12. The Hidden State as a Bottleneck (and Attention as the Fix)

In a classic seq2seq encoder-decoder, the entire input sequence must be compressed into a single fixed-size vector $h_T$ (the final encoder hidden state). For long sequences, this bottleneck severely limits performance.

**Attention mechanisms** (Bahdanau et al., 2014) were introduced specifically to fix this. Instead of using only $h_T$, the decoder at each step computes a weighted sum over **all encoder hidden states**:

$$c_t = \sum_k \alpha_{tk} h_k$$

where $\alpha_{tk}$ are learned attention weights. This lets the decoder "look back" at any part of the input as needed.

This is the direct predecessor to the Transformer — the Transformer essentially replaces the RNN entirely with self-attention, discarding the recurrence.

---

## 13. Practical Training Tips and Nuances

### Initialization
- $W_{hh}$ initialized as an orthogonal matrix — orthogonal initialization helps preserve gradient norms through BPTT.
- Forget gate biases initialized to **1.0** in LSTMs — this encourages the network to remember by default at the start of training. This is a well-known empirical trick.

### Gradient Clipping
Always use gradient clipping with RNNs. A typical threshold is 1.0 or 5.0 on the global gradient norm. Without it, a single bad batch can destroy training.

### Sequence Padding and Packing
When batching sequences of different lengths, you pad shorter sequences with zeros. But running the RNN over padding is wasteful and pollutes the hidden state. In PyTorch, `pack_padded_sequence` and `pad_packed_sequence` handle this efficiently by skipping padded positions.

### Stateful vs Stateless Inference

- **Stateless**: Reset $h_0 = 0$ at the start of each new sequence. Most common.
- **Stateful**: Carry $h_T$ of one batch as $h_0$ of the next. Useful when a single long document is split into chunks.

### Vanishing Gradient Diagnostic

If your loss plateaus early or the model ignores early inputs, suspect vanishing gradients. A quick test: visualize gradient norms across timesteps during backprop. If early timestep gradients are near zero, vanilla RNNs won't work — switch to LSTM/GRU.

---

## 14. When to Use RNNs vs Alternatives

|Scenario|Recommendation|
|---|---|
|Short sequences (<100 steps)|Vanilla RNN may work; LSTM/GRU safer|
|Long sequences (>500 steps)|Transformer preferred (attention doesn't decay with distance)|
|Streaming / online inference|RNN (processes one token at a time, O(1) memory)|
|Parallel training at scale|Transformer (can parallelize; RNNs are inherently sequential)|
|Very small data|RNN (fewer parameters than Transformer)|
|Variable-length, real-time|RNN natural fit|

The Transformer has largely displaced RNNs for NLP, but RNNs remain competitive for:

- Time series forecasting
- Real-time sequential control (robotics, audio)
- Tasks with strict memory/compute budgets
- Streaming applications where you cannot wait for the full input

---

## 15. Summary of Equations

| Model       | Hidden State Update                                                              |
| ----------- | -------------------------------------------------------------------------------- |
| Vanilla RNN | $h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b)$                                   |
| LSTM        | $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ ; $h_t = o_t \odot \tanh(c_t)$ |
| GRU         | $h_t = (1-z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$                            |

---

## Key Takeaways
- Vanilla RNNs work in theory but fail in practice for long sequences due to vanishing gradients.
- LSTMs solve this with an additive cell state update and three learned gates. The forget gate (added later, not in the original) is critical.
- GRUs are a simpler, faster alternative to LSTMs with comparable performance on most tasks.
- BPTT is just backprop through an unrolled network; truncated BPTT is the practical version.
- Gradient clipping is non-negotiable when training RNNs.
- Forget gate bias initialized to 1.0 and orthogonal weight initialization are two important engineering tricks.
- The fixed-size bottleneck in seq2seq is what motivated attention mechanisms, which then led directly to Transformers.
- RNNs are still relevant for streaming and compute-constrained settings, but Transformers dominate NLP.