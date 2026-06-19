---
title: "Predicting Next Word with GPT-2"
lastmod: 2026-03-20
---

### GPT-2 Inference Pipeline and Tensor Transformations

The following report outlines the sequential transformation of data through the GPT-2 architecture, tracking the tensor shapes from input tokens to the final vocabulary distribution.
## 1. Input Processing

The process begins with a sequence of $T$ tokens for a batch of $B$ sequences.
- **Input Sequence:** $(B, T,1)$
    - The input consists of integer indices representing words/sub-words from the vocabulary.
- **Token & Positional Encoding:** $(B, T, C)$
    - The model performs a lookup in the Word Token Embedding (WTE) matrix.
    - Simultaneously, a Word Positional Embedding (WPE) is added to provide sequence order information(usually a sinosoid encoding).
    - _Operation:_ `x = self.transformer.wte(input_ids) + self.transformer.wpe(pos)`

## 2. The Transformer Block Stack
The combined embedding passes through $N$ successive transformer layers (Blocks).
- **Hidden State Representation:** $(B, T, C)$
    - Each block consists of **Causal Self-Attention** and a **Feed-Forward Network (MLP)**.
	    - Might have multi head attention - parallel processing of $(B,T,c_{i})$ and then finally concatenation of all $c_i$'s into C. 
    - **Self-Attention:** Each token at position $t$ updates its embedding vector(C or $c_i$) by attending to all previous tokens $[0, \dots, t]$.
    - **Normalization:** A LayerNorm (`ln_f`) is applied after the final block to stabilize the activations before the head.
    - _Result:_ The final tensor $(B, T, C)$ now contains contextualized "features" rather than static word meanings.

##  The Language Modeling Head
The high-dimensional features are mapped back into the vocabulary space to produce predictions.
- **Linear Projection (Logits):** $(B, T, V)$
    - The `lm_head` (a linear layer) projects the sequence from embedding dimension $C$ to vocabulary size $V$.
    - _Operation:_ `logits = self.lm_head(x)`
- **Target Selection:** $(B, 1, V)$
    - For next-word prediction, we specifically extract the last index of the sequence i.e $(T-1)$.
    - This slice represents the model's belief about what follows the current input.

### Output: Probability Distribution
To convert raw scores (logits) into interpretable data, a Softmax function is typically applied.
- **Softmax Layer:** $(B, 1, V)$
    - The values are squeezed between $0$ and $1$, summing to $1.0$.
    - Each index in the $V$ dimension corresponds to a specific word in the vocabulary, with its value representing the probability of being the next token.
