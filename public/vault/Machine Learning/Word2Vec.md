---
title: "Word2Vec"
lastmod: 2026-06-26
---

## 1. The Problem: Words Need to Mean Something to a Machine

Before Word2Vec, the standard way to represent words for machine learning was **one-hot encoding**: a vector of zeros with a single 1 at the index corresponding to that word.

For a vocabulary of size $V$:

- "cat" → $[0, 0, 1, 0, \ldots, 0]$
- "dog" → $[0, 0, 0, 1, \ldots, 0]$
- "king" → $[1, 0, 0, 0, \ldots, 0]$

### Why One-Hot Fails

**Every word is equidistant from every other word.** The dot product between any two one-hot vectors is 0. Cosine similarity is 0. There is no notion of "cat" and "dog" being more similar to each other than "cat" and "democracy."

The representation is also enormous ($V$-dimensional, where $V$ can be 50k–1M), and almost entirely zeros — high-dimensional, sparse, and semantically empty.

What we actually want: a **dense, low-dimensional vector** where geometric proximity reflects semantic similarity. A representation where:

- "cat" and "dog" are close together
- "king" and "queen" are close together
- "king − man + woman ≈ queen" (linear relationships capture analogies)

Word2Vec (Mikolov et al., 2013) gave us this. The insight driving it:

> **The meaning of a word is defined by the company it keeps.**

This is the **distributional hypothesis**, attributed to linguist John Firth (1957): words that appear in similar contexts have similar meanings. Word2Vec operationalizes this into a learning objective.

---

## 2. The Core Idea: Predict Context from Word (or Vice Versa)

Word2Vec doesn't try to do anything sophisticated. It trains a **shallow neural network** on a **self-supervised prediction task** using raw text — no labels needed. The learned weights of this network become the word embeddings.

There are two variants, which are mirror images of each other:

### Skip-Gram: Predict Context from Center Word

Given a center word, predict the surrounding context words.

Input: "cat"  
Predict: "the", "sat", "on", "mat" (words within a window around "cat")

### CBOW (Continuous Bag of Words): Predict Center from Context

Given the surrounding context words, predict the center word.

Input: "the", "sat", "on", "mat"  
Predict: "cat"

**Which to use?**

- Skip-gram: better for rare words, better on smaller datasets, more commonly used in practice
- CBOW: faster to train, slightly better for frequent words, averages context signal

Most discussions and implementations default to Skip-gram. We'll focus on it and note CBOW differences where relevant.

---

## 3. Skip-Gram: The Architecture

### The Setup

- Vocabulary size: $V$
- Embedding dimension: $d$ (typically 100–300)
- Context window size: $c$ (typically 2–5 words on each side)

### The Two Weight Matrices

The network has:

- **Input embedding matrix** $W \in \mathbb{R}^{V \times d}$: each row $W_i$ is the embedding of word $i$ as a center word
- **Output embedding matrix** $W' \in \mathbb{R}^{V \times d}$: each row $W'_j$ is the embedding of word $j$ as a context word

Two matrices for the same vocabulary. This is a nuance that gets skipped: every word has **two** embeddings — one when it's the center word, one when it's a context word. After training, you typically use only $W$ (the input matrix) and discard $W'$, or average the two.

### The Forward Pass

Given center word $w_c$ (one-hot vector $\mathbf{x}$):

1. **Lookup**: $\mathbf{v}_{w_c} = W^T \mathbf{x}$ — extract the row of $W$ corresponding to $w_c$. This is just an embedding lookup, not a matrix-vector product in any meaningful computation sense.
    
2. **Score each context word**: Compute dot product of center embedding with each output embedding: $$s_j = \mathbf{v}_{w_c}^T \mathbf{v}'_{w_j}$$
    
3. **Softmax**: Convert scores to probabilities over the vocabulary: $$P(w_j | w_c) = \frac{\exp(s_j)}{\sum_{k=1}^{V} \exp(s_k)} = \frac{\exp(\mathbf{v}_{w_c}^T \mathbf{v}'_{w_j})}{\sum_{k=1}^{V} \exp(\mathbf{v}_{w_c}^T \mathbf{v}'_{w_k})}$$
    
4. **Loss**: Cross-entropy loss for each context word $w_o$ in the window: $$L = -\log P(w_o | w_c) = -\mathbf{v}_{w_c}^T \mathbf{v}'_{w_o} + \log \sum_{k=1}^{V} \exp(\mathbf{v}_{w_c}^T \mathbf{v}'_{w_k})$$
    

Sum this over all (center, context) pairs in the corpus.

### The Bottleneck: The Softmax Denominator

Computing $\sum_{k=1}^{V} \exp(\mathbf{v}_{w_c}^T \mathbf{v}'_{w_k})$ requires a dot product with **every word in the vocabulary** for every single training pair. With $V = 100{,}000$, this is 100,000 dot products per gradient step — completely infeasible on a billion-word corpus.

This is the fundamental computational problem of Word2Vec, and it's what the two approximation methods (Hierarchical Softmax and Negative Sampling) solve.

---

## 4. Negative Sampling: The Key Approximation

Negative Sampling (NEG) replaces the full softmax with a much simpler objective. Instead of asking "what is the probability of this context word over all $V$ words?", it reframes the problem as **binary classification**:

> For each (center, context) pair, can you distinguish the real context word from randomly sampled "noise" words?

### The Objective

For a (center word $w_c$, context word $w_o$) pair, sample $k$ **negative samples** $w_1^-, \ldots, w_k^-$ from a noise distribution $P_n(w)$.

The objective becomes:

$$L = \log \sigma(\mathbf{v}_{w_c}^T \mathbf{v}'_{w_o}) + \sum_{i=1}^{k} \log \sigma(-\mathbf{v}_{w_c}^T \mathbf{v}'_{w_i^-})$$

Where $\sigma$ is the sigmoid function. Maximize this (or minimize its negative).

- First term: push the dot product of the real (center, context) pair **up** → make them likely under sigmoid
- Second term: push the dot product of (center, negative) pairs **down** → make them unlikely

### The Noise Distribution

Negative samples are drawn from $P_n(w) \propto f(w)^{3/4}$ where $f(w)$ is the unigram frequency of word $w$.

Why $3/4$? It's empirical — found to work better than plain unigram ($f(w)$) or uniform ($1/V$). The $3/4$ power smooths the distribution: common words are still sampled more than rare words, but the gap is reduced. This gives rare words a fairer chance of being used as negative samples.

For $V = 100{,}000$, a word appearing 1000× more than another would appear $1000^{0.75} \approx 178\times$ more under $P_n$ than under plain unigram.

### Why This Works

Negative sampling is an approximation to Noise Contrastive Estimation (NCE), which is a statistically principled method for training unnormalized models. NCE replaces the intractable partition function (the softmax denominator) with a classification task against noise.

Negative sampling simplifies NCE further (it's not exactly NCE) but retains the key property: the gradient update only involves the center word, the real context word, and $k$ noise words — not all $V$ words. With $k = 5$–$15$, you do $6$–$16$ dot products instead of $V = 100{,}000$.

### How Many Negative Samples?

- $k = 2$–$5$ for large corpora
- $k = 5$–$20$ for smaller corpora
- More negative samples → better approximation of true softmax gradient, but slower training

In practice $k = 5$ is the standard choice.

---

## 5. Hierarchical Softmax: The Other Approximation

The alternative to negative sampling. Instead of the flat softmax over $V$ words, organize the vocabulary in a **binary tree** (a Huffman tree, where frequent words are near the root).

Each word corresponds to a leaf. The probability of a word is the product of sigmoid probabilities at each node along the path from root to that leaf.

For a path of length $L$: $$P(w | w_c) = \prod_{l=1}^{L} \sigma\left(\text{direction}_l \cdot \mathbf{v}_{w_c}^T \mathbf{v}'_{\text{node}_l}\right)$$

where direction$_l \in {+1, -1}$ indicates whether you go left or right at each node.

**Complexity**: $O(\log V)$ instead of $O(V)$ — for $V = 100{,}000$, that's 17 operations instead of 100,000.

**In practice**: Negative sampling is preferred because it's simpler to implement, works better empirically for most tasks, and negative sampling's hyperparameter $k$ is easier to tune than the tree structure.

---

## 6. Subsampling of Frequent Words

Extremely common words ("the", "a", "is", "of") appear in almost every context window but carry very little semantic information. They dilute training by creating many (center, context) pairs where the context word is uninformative.

Word2Vec discards frequent words during training with probability:

$$P(\text{discard } w) = 1 - \sqrt{\frac{t}{f(w)}}$$

where $f(w)$ is the word's frequency in the corpus and $t$ is a threshold (typically $t = 10^{-5}$).

- Very frequent words ($f(w) \gg t$): high discard probability
- Rare words ($f(w) \ll t$): near-zero discard probability

**Effect**: Words like "the" might be discarded 99% of the time. This:

1. Speeds up training (fewer pairs to process)
2. Improves embeddings for content words (they're no longer pulled toward function words)
3. Effectively increases the context window for content words — when "the" is discarded, neighboring content words become "closer" in the subsampled text

This is a small but important detail. Subsampling is not the same as removing stop words — the words remain in the vocabulary and can still appear as targets; they're just rarely used as training examples.

---

## 7. The Training Loop: What Actually Happens

For a corpus of $T$ words:

1. Slide a window of size $c$ over each position
2. For each center word $w_c$ and each context word $w_o$ in the window:
    - (Optionally skip $w_c$ or $w_o$ based on subsampling probability)
    - Sample $k$ negative words from $P_n$
    - Compute the negative sampling loss
    - Backpropagate: update $\mathbf{v}_{w_c}$ (row of $W$) and $\mathbf{v}'_{w_o}, \mathbf{v}'_{w_1^-}, \ldots, \mathbf{v}'_{w_k^-}$ (rows of $W'$)

**Key observation**: Each gradient update only touches:

- 1 row of $W$ (the center word)
- $(1 + k)$ rows of $W'$ (the context word + $k$ negatives)

With $V = 100{,}000$ and $d = 300$, the full embedding matrix has 30M parameters. But each update only touches $\sim (1+k) \times d \approx 1{,}800$ parameters. This sparsity is what makes Word2Vec fast.

---

## 8. CBOW: The Mirror Image

CBOW predicts the center word from the context words. The architecture:

1. Average the input embeddings of all context words: $$\bar{\mathbf{v}} = \frac{1}{2c} \sum_{-c \leq j \leq c, j \neq 0} \mathbf{v}_{w_{t+j}}$$
    
2. Use $\bar{\mathbf{v}}$ to predict the center word $w_t$ via softmax (or negative sampling)
    

**Difference from Skip-gram**: Skip-gram generates one prediction per context word (multiple targets per center). CBOW averages all context vectors and generates one prediction (one target per center). CBOW trains faster because it generates fewer gradient updates.

**Why Skip-gram handles rare words better**: In Skip-gram, a rare center word generates many training pairs (one per context word in the window). This gives the rare word's embedding many gradient updates — it gets trained on directly each time it appears. In CBOW, a rare word only appears as a context word (averaged into $\bar{\mathbf{v}}$, diluting its contribution) or as the center word (but rare center words rarely appear). Skip-gram is more data-efficient for rare words.

---

## 9. What the Embeddings Learn

After training on a large corpus, the embedding matrix $W$ has remarkable properties.

### Semantic Similarity

Words with similar meanings end up close in embedding space:

- cosine("cat", "dog") ≫ cosine("cat", "democracy")
- Synonyms cluster together
- Words with similar syntactic roles cluster together

### Linear Structure: The Analogy Property

The most famous property:

$$\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}} \approx \mathbf{v}_{\text{queen}}$$

More generally:

- $\mathbf{v}_{\text{Paris}} - \mathbf{v}_{\text{France}} + \mathbf{v}_{\text{Italy}} \approx \mathbf{v}_{\text{Rome}}$ (capital cities)
- $\mathbf{v}_{\text{walking}} - \mathbf{v}_{\text{walk}} \approx \mathbf{v}_{\text{swimming}} - \mathbf{v}_{\text{swim}}$ (verb tenses)
- $\mathbf{v}_{\text{biggest}} - \mathbf{v}_{\text{big}} \approx \mathbf{v}_{\text{coldest}} - \mathbf{v}_{\text{cold}}$ (superlatives)

These relationships emerge without any explicit supervision about grammar or semantics — purely from co-occurrence statistics.

### Why Does Linear Structure Emerge?

This is not fully understood theoretically, but the intuition is:

If "king" and "queen" appear in similar contexts except that "king" co-occurs with male-gendered words and "queen" with female-gendered words, then their embeddings will differ primarily in the "gender" direction. The same "gender" direction that separates "man" from "woman". So:

$$\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{queen}} \approx \mathbf{v}_{\text{man}} - \mathbf{v}_{\text{woman}}$$

Rearranging: $\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}} \approx \mathbf{v}_{\text{queen}}$.

The linear structure is a consequence of the distributional structure of language: if relationships between words manifest as consistent differences in context distributions, they manifest as consistent differences in embedding vectors.

### What Dimensions Encode

Individual dimensions of a Word2Vec embedding are not interpretable in isolation — the model doesn't assign "dimension 42 = gender." The meaningful structure is in **directions** (combinations of dimensions), not individual axes. This is why PCA on word embeddings often reveals interpretable axes.

---

## 10. The Relationship to Matrix Factorization

This is a deep connection that was discovered after Word2Vec was published.

Levy & Goldberg (2014) showed that **Skip-gram with Negative Sampling (SGNS) implicitly factorizes a shifted PMI matrix**:

$$W \cdot W'^T \approx M \quad \text{where } M_{ij} = \text{PMI}(w_i, w_j) - \log k$$

**PMI (Pointwise Mutual Information)**: $$\text{PMI}(w, c) = \log \frac{P(w, c)}{P(w)P(c)} = \log \frac{\text{count}(w,c) \cdot |D|}{\text{count}(w) \cdot \text{count}(c)}$$

PMI measures how much more often two words co-occur than you'd expect by chance. High PMI = words appear together much more than random; low PMI = words appear independently.

So Word2Vec, which looks like a neural network, is actually doing **low-rank factorization of the PMI co-occurrence matrix** — the same thing classical methods like LSA (Latent Semantic Analysis) do, just with a different objective and a nonlinear pathway to get there.

**Why this matters**:

1. It connects Word2Vec to a long tradition of count-based distributional semantics
2. It explains _why_ the method works — you're compressing co-occurrence statistics into a dense representation
3. It implies that methods like GloVe (which explicitly factorizes a co-occurrence matrix) are doing something very similar to Word2Vec

---

## 11. GloVe: The Explicit Co-occurrence Approach

GloVe (Global Vectors for Word Representation, Pennington et al., 2014) makes the matrix factorization explicit.

**Step 1**: Build a co-occurrence matrix $X$ where $X_{ij}$ = number of times word $j$ appears in the context of word $i$ (over the whole corpus, with distance weighting).

**Step 2**: Minimize: $$J = \sum_{i,j=1}^{V} f(X_{ij})\left(\mathbf{v}_i^T \mathbf{v}'_j + b_i + b'_j - \log X_{ij}\right)^2$$

where $f(X_{ij})$ is a weighting function that downweights very frequent co-occurrences:

$$f(x) = \begin{cases} (x/x_{\max})^\alpha & \text{if } x < x_{\max} \ 1 & \text{otherwise} \end{cases}$$

with $\alpha = 3/4$ and $x_{\max} = 100$ typically.

### Word2Vec vs GloVe

||Word2Vec (SGNS)|GloVe|
|---|---|---|
|Training data|Raw text, online|Pre-computed co-occurrence matrix|
|Objective|Predict context (implicit PMI)|Explicitly factorize log co-occurrence|
|Memory|Low (streaming)|High (full co-occurrence matrix)|
|Speed|Fast on large corpora|Faster on smaller corpora|
|Performance|Similar|Similar|

In practice, performance on downstream tasks is similar between the two. Choice often comes down to implementation preference and corpus size. For very large corpora, Word2Vec's streaming nature is an advantage.

---

## 12. Failure Modes and Limitations

### One Vector Per Word: The Polysemy Problem

Word2Vec assigns one embedding per word form. "Bank" (financial institution) and "bank" (river bank) get a single embedding — the average of all their usages. In a corpus where "bank" appears in both senses roughly equally, the embedding lands somewhere between both meanings, capturing neither well.

This is a fundamental limitation. Contextual embeddings (ELMo, BERT) solve this by producing different representations for the same word depending on its context.

### Bias Encoded from Corpus

Word2Vec faithfully encodes the statistical patterns of its training corpus — including human biases. Famous examples:

- "man is to doctor as woman is to nurse"
- "he" closer to "programmer", "she" closer to "homemaker"

These are real, measured results from Word2Vec trained on large corpora. The model doesn't create bias — it reflects and compresses the biases present in the text. This matters practically: using Word2Vec embeddings in downstream systems can propagate societal biases into predictions.

### Out-of-Vocabulary Words

Standard Word2Vec has a fixed vocabulary. Any word not seen during training has no embedding. "Unhappiness" might not be in the vocabulary even if "happy" and "unhappy" are.

**FastText** (Bojanowski et al., 2017, also from Facebook) extends Word2Vec by representing words as bags of character n-grams:

$$\mathbf{v}_{\text{unhappy}} = \mathbf{v}_{\text{<un}} + \mathbf{v}_{\text{unh}} + \mathbf{v}_{\text{nha}} + \mathbf{v}_{\text{hap}} + \cdots + \mathbf{v}_{\text{py>}}$$

This allows embeddings for unseen words (composed from their n-grams) and better handles morphologically rich languages (Turkish, Finnish, Arabic) and misspellings. For these cases, FastText substantially outperforms Word2Vec.

### No Sentence-Level Representation

Word2Vec produces word embeddings. Getting sentence or document embeddings requires averaging (Bag of Words with embeddings), or other methods (Doc2Vec, which extends Word2Vec with a paragraph vector; or more modern approaches like sentence-BERT).

Averaging word vectors is surprisingly competitive for many tasks but loses word order entirely.

### Context Window is Flat

Within the context window, all words are treated equally regardless of distance. A word 1 position away from the center contributes the same as a word $c$ positions away. GloVe addresses this with distance weighting ($1/d$ for distance $d$). Word2Vec's subsampling partially compensates but doesn't explicitly distance-weight.

---

## 13. Evaluating Word Embeddings

### Intrinsic Evaluation

**Word similarity tasks**: Given pairs like (cat, dog), (cat, television), human judges rate semantic similarity. Compare cosine similarity of embeddings to human ratings. Datasets: WordSim-353, SimLex-999.

**Analogy tasks**: For "king : man :: ? : woman", find the word closest to $\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}}$. Dataset: Google analogy dataset (Mikolov et al., 2013), contains 19,544 analogies covering semantic (capital cities, currencies) and syntactic (verb tenses, plurals) relationships.

**Nuance about analogy evaluation**: The standard evaluation method (find the nearest vector) excludes the input words from the answer. This is important — otherwise "king" would always be the nearest to $\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}}$ and the metric would be trivial.

### Extrinsic Evaluation

Use embeddings as features in a downstream task: text classification, NER, sentiment analysis, machine translation. This is what actually matters — intrinsic scores don't always correlate with downstream performance.

**The right evaluation principle**: Always prefer extrinsic evaluation. High analogy scores don't guarantee better NER performance.

---

## 14. From Word2Vec to Contextual Embeddings

Word2Vec produces **static embeddings** — one vector per word regardless of context. The evolution:

### ELMo (2018, Peters et al.)

Run a bidirectional LSTM over the full sentence. The embedding for a word is a learned combination of all LSTM layer outputs — it changes based on the sentence. "Bank" in a financial context gets a different vector than "bank" in a river context.

### BERT (2018, Devlin et al.)

Transformer encoder pretrained on Masked Language Modeling (predict masked tokens) and Next Sentence Prediction. The [CLS] token embedding or token-level embeddings are contextual. "Bank" in context of "loans" vs. "river" produces very different embeddings.

### The Conceptual Continuity

Word2Vec: predict context word from center word → train on co-occurrence statistics → compress into dense vectors.

BERT: predict masked words from context → train on co-occurrence statistics → compress into contextual dense vectors via attention.

The objective is related (both exploit the distributional hypothesis). The key difference: BERT's Transformer can condition on the entire sentence, not just a window. Each token's representation is a function of all other tokens.

Word2Vec can be seen as the degenerate case: a single-layer "attention" where the query is the center word and the keys/values are context words in a flat window, with no context-dependence in the representations themselves.

---

## 15. Practical Training Details

### Hyperparameters That Matter

**Embedding dimension $d$**: 100–300 for Word2Vec on standard corpora. Larger $d$ captures more information but needs more data and is slower. For very large corpora (billions of words), 300 is standard.

**Context window $c$**: Larger windows capture more topical/semantic similarity (words that appear in similar documents); smaller windows capture more syntactic/functional similarity (words that substitute for each other in sentences). $c = 5$ is standard.

**Negative samples $k$**: 5–15. Diminishing returns above 15.

**Subsampling threshold $t$**: $10^{-5}$ for large corpora, $10^{-4}$ for smaller.

**Epochs**: Typically 1–5 passes over the corpus for very large corpora; more for smaller ones. The original paper used a single pass for billion-word corpora.

**Learning rate**: Usually linearly decayed from 0.025 to 0.0001 over training.

### Corpus Size Matters

Word2Vec is data-hungry. Embeddings trained on:

- < 1M words: poor quality
- 10M–100M words: decent, usable
- 1B+ words: good quality (Google's original Word2Vec was trained on 100B words from Google News)

Training on domain-specific text (medical, legal, code) is often better than using general-purpose pre-trained embeddings when your application domain differs significantly from web text.

---

## 16. Implementation

### Using Pretrained Embeddings (Recommended Starting Point)

```python
import gensim.downloader as api

# Load pretrained Word2Vec (Google News, 300d, 3M vocab)
model = api.load("word2vec-google-news-300")

# Word vector
vec = model["king"]  # shape: (300,)

# Similarity
model.similarity("cat", "dog")    # cosine similarity
model.most_similar("king", topn=10)

# Analogy: king - man + woman = ?
model.most_similar(positive=["king", "woman"], negative=["man"])
```

### Training Your Own

```python
from gensim.models import Word2Vec

# Sentences: list of lists of words
sentences = [["the", "cat", "sat"], ["dogs", "run", "fast"], ...]

model = Word2Vec(
    sentences=sentences,
    vector_size=300,     # embedding dimension
    window=5,            # context window size
    min_count=5,         # ignore words appearing < 5 times
    sg=1,                # 1 = Skip-gram, 0 = CBOW
    negative=5,          # number of negative samples
    sample=1e-5,         # subsampling threshold
    workers=4,           # parallel threads
    epochs=5
)

model.wv["cat"]                          # get vector
model.wv.most_similar("cat")             # nearest neighbors
model.wv.save("word2vec.wordvectors")    # save embeddings
```

### Using as Features in Downstream Models

```python
import numpy as np

def sentence_embedding(sentence, model, dim=300):
    """Average word vectors — simple but effective baseline."""
    vectors = []
    for word in sentence:
        if word in model.wv:
            vectors.append(model.wv[word])
    if not vectors:
        return np.zeros(dim)
    return np.mean(vectors, axis=0)
```

---

## 17. Key Takeaways

- Word2Vec learns **dense, low-dimensional word embeddings** by training a shallow network to predict context words from center words (Skip-gram) or vice versa (CBOW).
- The **distributional hypothesis** is the foundation: words that appear in similar contexts have similar meanings. Word2Vec operationalizes this as a prediction task.
- The full softmax over $V$ words is intractable. **Negative sampling** replaces it with binary classification against $k$ random noise words — cheap, effective, and the standard approach.
- SGNS implicitly factorizes a **shifted PMI matrix** — Word2Vec is low-rank matrix factorization in disguise. This connects it to classical distributional semantics.
- **Every word has two embeddings**: one in the input matrix $W$ (center word) and one in the output matrix $W'$ (context word). You typically use $W$ after training.
- **Subsampling** discards frequent words during training with probability proportional to their frequency — speeds up training and improves content word embeddings.
- K-means++ uses $D(x)^{3/4}$ sampling; **the noise distribution for negative sampling uses $f(w)^{3/4}$** — both are $3/4$-power smoothed frequency distributions. Coincidence of the same trick in two different contexts.
- Word2Vec produces **static embeddings** — one vector per word type regardless of context. This is the core limitation: polysemous words get one averaged representation.
- Linear structure (king − man + woman ≈ queen) emerges from the distributional structure of language, not from explicit supervision.
- **FastText** extends Word2Vec with character n-grams to handle OOV words and morphologically rich languages.
- The path from Word2Vec → ELMo → BERT is conceptually continuous: all exploit the distributional hypothesis, but BERT's Transformer conditions each word's representation on the full sentence context.