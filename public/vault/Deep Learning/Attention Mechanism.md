---
title: "Attention Mechanism"
lastmod: 2026-06-03
---

## Why Attention Exists

Before attention, sequence models (RNNs, LSTMs) processed tokens one by one and tried to compress the entire context into a single hidden state vector before producing an output. This bottleneck was brutal — by the time you're generating the 50th word, the information from the 1st word has been squeezed through 49 intermediate states and is largely gone.

Attention throws out the bottleneck. Instead of a single compressed state, every output position gets to **directly look at every input position** and decide what's relevant. No compression. No forgetting by design.

---

## The Setup: What Are We Working With?

Let's ground this concretely. Say you have a sequence of $n$ tokens. After an embedding layer, each token is represented as a vector of dimension $d_\text{model}$. So your input is a matrix:

$$X \in \mathbb{R}^{n \times d_\text{model}}$$

Each row is one token. This is what enters the attention block.

---

## Step 1: Project Into Three Spaces — Q, K, V

The first thing attention does is linearly project $X$ into three separate matrices: **Queries**, **Keys**, and **Values**.

$$Q = X W^Q, \quad K = X W^K, \quad V = X W^V$$

Where:

- $W^Q, W^K \in \mathbb{R}^{d_\text{model} \times d_k}$
- $W^V \in \mathbb{R}^{d_\text{model} \times d_v}$
- Typically $d_k = d_v = d_\text{model} / h$ where $h$ is the number of heads

So $Q, K \in \mathbb{R}^{n \times d_k}$ and $V \in \mathbb{R}^{n \times d_v}$.

These are learned projections — the weight matrices are trained. The model learns _what aspects of a token to use_ for querying, for matching, and for value retrieval.

### The Intuition for Q, K, V
Think of it like a soft lookup in a dictionary.
- **Query**: what this position is _looking for_
- **Key**: what each position _advertises about itself_
- **Value**: what each position _actually contributes_ if selected

A query and a key matching means: "position $i$ finds position $j$ relevant." The value of $j$ then flows into $i$'s output. The Q/K/V split lets the model decouple _what to look for_ from _what to retrieve_ — these don't have to be the same thing, and often shouldn't be.

---

## Step 2: Compute the Attention Matrix

Now compute the dot product between every query and every key:

$$A_\text{raw} = Q K^T \in \mathbb{R}^{n \times n}$$

Entry $(i, j)$ in this matrix is the dot product of query $i$ with key $j$ — a scalar measuring how much position $i$ should attend to position $j$.

Then scale and softmax:

$$A = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) \in \mathbb{R}^{n \times n}$$

Each row of $A$ is a probability distribution over all $n$ positions. Row $i$ says: "given query $i$, here's how much weight to put on each position."

### Why divide by $\sqrt{d_k}$?

Without scaling, dot products grow in magnitude as $d_k$ increases (the sum of $d_k$ multiplied terms). Large dot products push softmax into saturation — it becomes nearly one-hot, gradients vanish, and learning stalls. Dividing by $\sqrt{d_k}$ keeps the variance of the dot product at ~1 regardless of dimension, keeping softmax in a useful range.

### What is the attention matrix, intuitively?

$A$ is an $n \times n$ matrix where $A_{ij}$ says: _how much does token $i$ attend to token $j$?_

Each row sums to 1. Each row is a soft selection over the sequence — not hard retrieval, but a weighted blend. This is the "soft dictionary" in action. Rather than picking one entry, you take a weighted average of all entries.

---

## Step 3: Apply Attention to Values

$$\text{Attention}(Q, K, V) = A \cdot V \in \mathbb{R}^{n \times d_v}$$

This is the core operation. You're taking the attention weights $A$ (which tell you _how much_ to look at each position) and using them to take a **weighted sum of the value vectors**.

For position $i$, the output is:

$$\text{out}_i = \sum_{j=1}^{n} A_{ij} \cdot V_j$$

So the output at position $i$ is not just a function of token $i$ — it's a blend of _all tokens_, weighted by relevance. Tokens that are highly attended to contribute more. Tokens that are ignored contribute almost nothing.

Output shape: $\mathbb{R}^{n \times d_v}$. Each row is an updated representation of one token, enriched by context from the whole sequence.

---

## Step 4: The Output Projection (Multi-Head Case)

In practice, attention is always run in parallel across $h$ heads. Each head gets its own $W^Q_i, W^K_i, W^V_i$ and independently computes attention in its own subspace.

Each head produces an output of shape $\mathbb{R}^{n \times d_v}$. All $h$ heads are concatenated:

$$\text{MultiHead}(X) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) \in \mathbb{R}^{n \times (h \cdot d_v)}$$

Since $d_v = d_\text{model}/h$, this gives $\mathbb{R}^{n \times d_\text{model}}$ — back to the original dimension.

Then one final linear projection:

$$\text{Output} = \text{MultiHead}(X) \cdot W^O \in \mathbb{R}^{n \times d_\text{model}}$$

Where $W^O \in \mathbb{R}^{d_\text{model} \times d_\text{model}}$.

### Why the output projection?
Two reasons:
1. **Mixing heads**: concatenation stacks the heads but doesn't let them interact. $W^O$ lets information from different heads combine.
2. **Restoring representational capacity**: each head worked in a $d_k$-dimensional subspace. The output projection maps back to the full $d_\text{model}$ space, letting the model recombine what different heads found.

---

## Step 5: Residual Connection + Layer Norm

The attention output doesn't replace the input — it's _added_ back:

$$\text{out} = \text{LayerNorm}(X + \text{MultiHead}(X))$$

This is a residual connection. The attention block computes a _delta_ — what to add to each token's representation given the context it has gathered. The original token information is preserved and augmented, not overwritten.
This matters for stability: gradients can flow directly through the residual path, and in early training when attention hasn't learned anything useful yet, the residual ensures the layer doesn't destroy the signal.

---

## Putting It All Together: Shape Trace

For concreteness, with $n=10$ tokens, $d_\text{model}=512$, $h=8$ heads, so $d_k = d_v = 64$:

```
Input X:             [10 × 512]

Per head:
  Q = X @ W^Q:       [10 × 64]
  K = X @ W^K:       [10 × 64]
  V = X @ W^V:       [10 × 64]

  QK^T:              [10 × 10]   ← attention matrix
  softmax(QK^T/8):   [10 × 10]   ← normalized attention weights
  AV:                [10 × 64]   ← attended values per head

After 8 heads, concat: [10 × 512]
Output projection:     [10 × 512]
Add & LayerNorm:       [10 × 512]   ← same shape as input
```

The output has exactly the same shape as the input. The transformer block is a function $\mathbb{R}^{n \times d} \to \mathbb{R}^{n \times d}$. This is what allows stacking — you can pipe the output of one block straight into the next.

---

## Why Multiple Heads?

One head learns one way to attend. It might learn syntactic relationships, or semantic similarity, or positional proximity — it can only do one thing at a time.

Multiple heads run in parallel subspaces. One head might learn to track subject-verb agreement, another might track coreference, another might track local word order. The output projection then combines what each head found.

This is the representational diversity argument. A single head in the full $d_\text{model}$ space could theoretically do this too, but the subspace structure forces the model to find multiple _independent_ attention patterns rather than collapsing to one.

---

## Encoder vs. Decoder: How Attention Changes

**Encoder (self-attention):** every token can attend to every other token freely. Full $n \times n$ attention matrix, no restrictions. The goal is to build a rich representation of the input.

**Decoder (masked self-attention):** during training, when generating position $i$, you cannot attend to positions $j > i$ — you haven't generated those yet. This is implemented by masking: set the pre-softmax scores for future positions to $-\infty$ so they become 0 after softmax. Causality enforced.

**Cross-attention (encoder-decoder):** queries come from the decoder, keys and values come from the encoder output. The decoder is asking: "given what I'm generating right now, what part of the input should I look at?" This is where translation-like alignment happens.

---

## Ideas to Ponder

- The attention matrix is $n \times n$. For a sequence of length $n$, this costs $O(n^2)$ memory and compute. For $n = 10{,}000$ (long documents, high-res images), this becomes crippling. Almost all of the "efficient attention" literature (Linformer, Performer, FlashAttention) is attacking this quadratic cost from different angles.
    
- Each head produces a _distribution over positions_. After training, if you visualize these distributions, different heads pick up very different patterns — some attend locally (nearby tokens), some attend to specific syntactic roles, some scatter across the sequence. The model discovers these roles purely from the training objective.
    
- The Q/K/V decomposition means a token's "what I'm looking for" ($Q$) is different from "what I tell others about myself" ($K$) and "what I give when selected" ($V$). Is this decomposition necessary? What would break if $Q = K$? (Answer: it still works, and some architectures do this, but it reduces expressivity.)
    
- Attention has no notion of position built in — dot products are permutation-invariant. If you shuffled all tokens, the attention matrix would just permute accordingly. This is why positional encodings are added before attention — they inject order into what is otherwise a bag-of-tokens operation.
    
- The residual connection means each transformer layer is computing a _correction_, not a complete rewrite. A useful mental model: early layers do local, syntactic cleanup; middle layers do relational reasoning; late layers do task-specific prediction. But the original embedding signal threads through every layer via the residuals.