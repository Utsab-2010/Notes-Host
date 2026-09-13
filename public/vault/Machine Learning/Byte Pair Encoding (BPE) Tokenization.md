---
title: "Byte Pair Encoding (BPE) Tokenization"
lastmod: 2026-06-26
---

## 1. The Problem: Why Not Just Use Words or Characters?

Before diving into BPE, understand the landscape of tokenization choices and why each has problems.

### Word-level Tokenization
Split text on whitespace/punctuation. "running" → `["running"]`

**Problems**:
- Huge vocabulary (50k–100k+ unique words in natural language)
- *Out-of-vocabulary (OOV*) problem: unseen words at inference get mapped to `<UNK>`, losing all information
- Morphological variants treated as completely different tokens: "run", "runs", "running", "runner" have no shared representation
- Languages like German (compound words: _Donaudampfschifffahrtsgesellschaft_) or Turkish (agglutinative morphology) blow up vocabulary size even further

### Character-level Tokenization
"running" → `["r", "u", "n", "n", "i", "n", "g"]`

**Problems**:
- Very long sequences — each word becomes many tokens, making attention over long documents extremely expensive
- Individual characters carry little semantic meaning; the model must learn to compose them from scratch
- Much harder to learn (the model needs more parameters and data to reconstruct word-level semantics from characters)

### What We Actually Want
A tokenization scheme that:
- Has a **bounded vocabulary** (controllable size, typically 30k–100k)
- **Shares subword units** across related words ("run", "running", "runner" share "run")
- **Handles rare and unseen words** gracefully by decomposing into known subpieces
- Produces **shorter sequences** than character-level
- Is **deterministic and lossless** — no information is lost
*BPE achieves all of this.*

---
## 2. The Origin of BPE
BPE was originally a **data compression algorithm** introduced by Philip Gage in 1994. The idea: find the most frequent pair of bytes in a sequence, replace them with a single new symbol, and repeat. This compresses the data by representing frequent patterns with fewer symbols.

Sennrich, Haddow & Birch (2016) adapted this for NLP in their paper _"Neural Machine Translation of Rare Words with Subword Units"_ — the foundational paper for modern BPE tokenization.

The key adaptation: instead of compressing bytes for storage, they use it to learn a **subword vocabulary** from a text corpus that balances vocabulary size with sequence length.

---
## 3. The BPE Algorithm: Training

### Input
- A text corpus
- A target vocabulary size $V$ (e.g., 32,000)

### Step 0: Initialize the Vocabulary

Start with a character-level vocabulary. Every word in the corpus is represented as a sequence of characters, with a special end-of-word token appended (commonly `</w>` or `Ġ` depending on implementation):

```
"low"     → l o w </w>
"lower"   → l o w e r </w>
"newest"  → n e w e s t </w>
"widest"  → w i d e s t </w>
```

The initial vocabulary is just the set of all unique characters (plus `</w>`).

Count the frequency of each word in the corpus:

```
"low </w>"     → 5 times
"lower </w>"   → 2 times
"newest </w>"  → 6 times
"widest </w>"  → 3 times
```

### Step 1: Count All Adjacent Pairs

Count how often each consecutive pair of symbols appears across all word occurrences (weighted by word frequency):

```
(l, o): 5 + 2 = 7
(o, w): 5 + 2 = 7
(w, </w>): 5
(w, e): 2 + 6 = 8       ← most frequent
(e, r): 2
(e, s): 6 + 3 = 9       ← actually most frequent
...
```

### Step 2: Merge the Most Frequent Pair

Take the pair with the highest count, merge it into a single new symbol, and add it to the vocabulary.

Say `(e, s)` is most frequent with count 9. Merge → new symbol `es`.

Update the corpus representation:

```
"newest </w>" → n e w es t </w>
"widest </w>" → w i d es t </w>
```

### Step 3: Repeat

Recount pairs with the updated corpus. Next most frequent pair might be `(es, t)` → merge to `est`:

```
"newest </w>" → n e w est </w>
"widest </w>" → w i d est </w>
```

Continue until the vocabulary reaches size $V$ or until no more merges are beneficial.

### What You End Up With

A **merge table**: an ordered list of merge rules, e.g.:

```
Merge 1: (e, s) → es
Merge 2: (es, t) → est
Merge 3: (l, o) → lo
Merge 4: (lo, w) → low
...
```

The order matters — these rules are applied in sequence during tokenization.

---

## 4. BPE Tokenization: Inference

Given a new word (or piece of text), tokenize by:
1. Split into characters (+ `</w>` or space prefix)
2. Apply merge rules **in the order they were learned**, greedily

Example: tokenize "lowest" with the merge table above.

Start: `l o w e s t </w>`

- Apply merge `(e, s) → es`: `l o w es t </w>`
- Apply merge `(es, t) → est`: `l o w est </w>`
- Apply merge `(l, o) → lo`: `lo w est </w>`
- Apply merge `(lo, w) → low`: `low est </w>`

Result: `["low", "est", "</w>"]` or equivalently `["low", "est"]` (dropping the end marker)

**The word "lowest" was never seen in training** but is correctly decomposed into known subwords.

---

## 5. The End-of-Word Marker: A Critical Nuance

The `</w>` marker (or its equivalent) is essential and frequently misunderstood.

Without it, "low" appearing at the start of a word and "low" appearing standalone would be indistinguishable. The marker distinguishes:

- `low</w>` → the complete word "low"
- `low` (without marker) → the prefix "low" in words like "lower", "lowest"

In practice the marker placement varies by implementation:

- **Sennrich et al. original**: append `</w>` after the last character of each word
- **GPT-2 / Tiktoken**: prepend `Ġ` (a special space character) to mark the _start_ of a new word (e.g., `Ġrunning` means "running" preceded by a space)
- **SentencePiece**: uses `▁` (underscore) to mark word boundaries

This affects how the vocabulary and merge rules look but is functionally equivalent.

---

## 6. Byte-Level BPE

Standard BPE operates on Unicode characters. This *still has OOV issues for rare Unicode characters — emojis, rare scripts, math symbols.*

**GPT-2** introduced **Byte-Level BPE**: operate on raw bytes (0–255) instead of Unicode characters.
- The base vocabulary is exactly 256 symbols (all possible bytes)
- Every possible string can be represented without OOV, since any string is a sequence of bytes
- Merges then combine frequent byte sequences into larger tokens

**Consequence**: No `<UNK>` token is needed — every possible input can be encoded. This is why GPT models have no unknown token in their vocabulary.

**Tradeoff**: For common scripts (ASCII text), byte-level BPE is essentially the same as character-level BPE since each character is one byte. For rare scripts or emoji, you may need 3–4 bytes per character, making sequences longer.

---

## 7. Vocabulary Size: How to Choose

The vocabulary size $V$ is a hyperparameter set before training BPE.

|Model|Vocab Size|
|---|---|
|Original BPE (Sennrich 2016)|10k–40k|
|GPT-2|50,257|
|GPT-3 / GPT-4 (tiktoken)|100,277|
|BERT (WordPiece)|30,522|
|LLaMA 2|32,000|
|LLaMA 3|128,256|

**Larger vocab**:

- Fewer tokens per sequence → shorter sequences → cheaper attention
- Each token carries more meaning
- Larger embedding matrix (more parameters)
- Rarer tokens seen less during training — weaker representations

**Smaller vocab**:

- More tokens per sequence → longer sequences → more expensive
- Each token is more atomic and seen more often
- Handles morphological variation worse

**Rule of thumb**: LLMs today trend toward larger vocabularies (100k+) because the embedding matrix cost is relatively small compared to the rest of the model, and shorter sequences are more efficient for attention.

---

## 8. Tokenization Is Not Splitting on Spaces

A widespread misconception: that tokenization just splits on whitespace and maybe punctuation.

BPE produces tokens that can be:

- Multi-character subwords: `"ing"`, `"tion"`, `"##er"`
- Complete common words: `"the"`, `"and"`, `"is"`
- Partial words (prefixes/suffixes): `"un"`, `"##able"`, `"pre"`
- Numbers (often split digit by digit): `"2024"` → `["20", "24"]` or `["2", "0", "2", "4"]`
- Punctuation (often its own token)
- Whitespace (in some tokenizers, the space is attached to the following token)

**Important implication for LLMs**: Token boundaries do not align with word boundaries. This creates well-known failure modes:

- Counting letters: "How many 'r's in 'strawberry'?" — the model sees `["st", "raw", "ber", "ry"]`, not individual characters
- Arithmetic: numbers may be split arbitrarily, making digit-level computation hard
- Spelling tasks: the model doesn't naturally "see" individual characters

---

## 9. BPE vs WordPiece vs SentencePiece vs Unigram

BPE is not the only subword tokenization algorithm. Here's how they compare:

### WordPiece (used in BERT)

Similar to BPE but uses a different merge criterion. Instead of merging the most frequent pair, it merges the pair that **maximizes the likelihood of the training data** given the current vocabulary:

$$\text{score}(A, B) = \frac{\text{count}(AB)}{\text{count}(A) \times \text{count}(B)}$$

This is essentially pointwise mutual information (PMI). It prefers merges where the pair co-occurs more than chance, not just the raw most frequent pair.

**Difference in practice**: WordPiece tends to produce slightly different splits but is empirically similar to BPE. BERT uses `##` to mark that a token is a continuation (not a word start): "running" → `["run", "##ning"]`.

### SentencePiece (used in T5, LLaMA, Mistral)

A library (not just an algorithm) that implements both BPE and Unigram LM tokenization. Key difference from standard BPE:

- Treats whitespace as a regular character (using `▁`)
- Operates directly on raw text without pre-tokenization (no whitespace split first)
- Fully language-agnostic: works on Chinese, Japanese, Arabic, etc. without special handling

**Why this matters**: Standard BPE first splits on spaces (pre-tokenization), then applies BPE within each word. SentencePiece sees the entire text as a character sequence and lets BPE/Unigram decide where word boundaries should be. This makes it better for languages without explicit word separators.

### Unigram Language Model Tokenization

A fundamentally different approach. Instead of bottom-up merging, start with a **large** vocabulary and iteratively **remove** tokens that least harm the overall corpus likelihood under a unigram language model:

$$P(\text{sequence}) = \prod_i P(t_i)$$

The final vocabulary is whichever set of subwords maximizes coverage of the corpus under this model.

**Key difference from BPE**: Unigram is **probabilistic** — at inference time, a word can be tokenized in multiple ways, and the tokenizer samples from or picks the most likely segmentation. BPE is deterministic (always applies merges in the same order, same result).

### Summary Table

|Algorithm|Training Criterion|Inference|Deterministic?|Used By|
|---|---|---|---|---|
|BPE|Most frequent pair merge|Apply merges in order|Yes|GPT-2/3/4, RoBERTa|
|WordPiece|Maximize corpus likelihood (PMI-like)|Apply merges in order|Yes|BERT, DistilBERT|
|Unigram LM|Maximize corpus likelihood under unigram|Viterbi / sampling|No (probabilistic)|T5, ALBERT|
|SentencePiece|Implements BPE or Unigram|Depends on algorithm|Depends|LLaMA, Mistral, T5|

---

## 10. Pre-tokenization: The Hidden Step Before BPE

Standard BPE doesn't run on raw text directly. There's a **pre-tokenization** step first.

GPT-2, for example, uses a regex to split text into chunks before applying BPE. The regex roughly splits on:

- Contractions (`'s`, `'t`, `'re`, ...)
- Words
- Numbers
- Punctuation
- Whitespace

This ensures that "don't" is always split into `["don", "'t"]` before BPE, so BPE never merges across these boundaries. Without pre-tokenization, BPE might learn that `"n't"` should merge with the preceding word, leading to inconsistent tokenization.

**The implication**: The tokenizer for a model is a combination of (pre-tokenizer + BPE vocabulary + merge rules). You can't just swap one component without retraining.

---

## 11. Special Tokens

Every modern tokenizer includes special tokens with reserved IDs outside the normal BPE vocabulary:

|Token|Symbol|Purpose|
|---|---|---|
|Beginning of sequence|`<s>`, `[CLS]`, `<BOS>`|Marks start of input|
|End of sequence|`</s>`, `[SEP]`, `<EOS>`|Marks end / separator|
|Padding|`[PAD]`, `<pad>`|Fills shorter sequences in a batch|
|Unknown|`[UNK]`|Rare in BPE (especially byte-level)|
|Mask|`[MASK]`|Used in BERT-style masked LM training|

In GPT-style models, `<EOS>` doubles as the separator — multiple documents in a sequence are separated by `<EOS>` tokens, and generation stops when the model produces one.

These special tokens are **always added to the vocabulary** before BPE training starts, and their embeddings are learned normally.

---

## 12. Tokenization Artifacts and Failure Modes

### Token Fertility

The number of tokens a sentence produces depends on the language and domain. English Wikipedia text tokenizes at ~1.3 tokens/word with GPT-2's tokenizer. Code tokenizes at higher fertility (more tokens per "word"). Non-English text, especially non-Latin scripts, tokenizes at much higher fertility:

- English: ~1.3 tokens/word
- German: ~1.5 tokens/word
- Russian (Cyrillic): ~2–4 tokens/word
- Thai: ~5–10 tokens/character sequence
- Emoji: ~2–4 tokens per emoji (in byte-level BPE)

This means **multilingual models are at a disadvantage for non-English languages** — they use more tokens per unit of meaning, effectively seeing less semantic content per context window.

### Tokenization of Numbers

Numbers are particularly poorly handled. "42" might be one token, but "4200000" might be split as `["42", "000", "00"]` or `["4", "200", "000"]` — inconsistently, depending on what the training corpus contained frequently. This is a fundamental reason why LLMs struggle with arithmetic.

### The "Token Healing" Problem

When you prompt a model and it continues generation, the split between your prompt and the continuation occurs at a token boundary. But the natural continuation might start mid-token. This is called the "prompt boundary problem" and is why some generation libraries implement **token healing**: backtrack by one token at the end of the prompt and let the model re-predict it as part of generation.

### Capitalization

"Hello" and "hello" often tokenize differently. Many tokenizers have separate tokens for capitalized versions of common words, which doubles (or more) the effective vocabulary needed for case-insensitive semantic content.

---

## 13. BPE and the Embedding Matrix

After tokenization, each token ID is mapped to a dense embedding vector. The **embedding matrix** has shape $V \times d$ where $V$ is vocab size and $d$ is the model's hidden dimension.

For GPT-3 with $V = 50{,}257$ and $d = 12{,}288$: the embedding matrix has $~617M$ parameters — about 15% of total model parameters just for the embedding lookup.

For LLaMA 3 with $V = 128{,}256$ and $d = 4{,}096$: the embedding matrix has $~525M$ parameters, but the vocabulary is 4× larger so rare tokens get fewer gradient updates during training.

**Tied embeddings**: In many language models, the input embedding matrix and the output projection matrix (the one that maps from hidden states back to logits over vocabulary) are **shared** (weight tying). This halves the parameter count for these matrices and often improves performance because the model must learn representations that work for both encoding and decoding.

---

## 14. Training a BPE Tokenizer in Practice (HuggingFace)

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# Initialize
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

# Train
trainer = BpeTrainer(
    vocab_size=30000,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
    min_frequency=2     # pair must appear at least 2x to be merged
)
tokenizer.train(files=["corpus.txt"], trainer=trainer)

# Save
tokenizer.save("tokenizer.json")

# Use
output = tokenizer.encode("Hello, world!")
print(output.tokens)   # ['Hello', ',', 'world', '!']
print(output.ids)      # [234, 15, 8923, 5]
```

### The `min_frequency` Parameter

Pairs that appear only once or twice are likely noise. `min_frequency=2` ensures merges are statistically meaningful. For large corpora this barely matters; for small corpora it's important.

---

## 15. Domain Mismatch in Tokenization

The BPE vocabulary is learned from the training corpus. If you apply a model to a very different domain, tokenization degrades:

- A BPE trained on web text will inefficiently tokenize medical text (many rare medical terms get split into many subwords)
- A BPE trained on English text will tokenize code poorly (tokens like `__init__`, `->`, `//` might not be in vocabulary as units)
- This is why code-specialized models (CodeLlama, StarCoder) sometimes retrain the tokenizer on code corpora or extend the vocabulary with code-specific tokens

**Added tokens**: You can add new tokens to an existing tokenizer and expand the embedding matrix. Common for domain adaptation (e.g., adding `[TABLE]`, `[CELL]` for structured data tasks). The new token embeddings need to be initialized — a good practice is to initialize them as the mean of similar existing token embeddings rather than random.

---

## 16. Decoding: Tokens Back to Text

Encoding: text → token IDs. Decoding: token IDs → text.

BPE decoding is straightforward: look up each token ID in the vocabulary, concatenate the strings, handle the word boundary markers (remove `</w>`, or handle `Ġ` as a space prefix).

**Nuance**: Byte-level BPE decoding needs to convert bytes back to Unicode. Some byte sequences are invalid UTF-8 (e.g., a lone continuation byte). Robust decoders handle this with error-replacement modes.

---

## 17. Key Takeaways

- BPE is a **greedy, bottom-up** algorithm: start with characters, iteratively merge the most frequent adjacent pair, stop at target vocabulary size.
- The output of BPE training is a **merge table** (ordered list of rules) + a vocabulary. Both are needed for tokenization.
- The end-of-word marker distinguishes complete words from prefixes — critical for correct tokenization.
- **Byte-level BPE** (GPT-2+) operates on raw bytes, eliminating OOV entirely. Every string is encodable.
- BPE is deterministic at inference — apply merge rules in order, greedily.
- WordPiece uses PMI-like scoring instead of raw frequency. Unigram LM is probabilistic. SentencePiece is a library that can do either.
- Pre-tokenization (regex splitting before BPE) is a hidden but important step in most production tokenizers.
- Tokenization artifacts (number splitting, multilingual fertility disparity, capitalization sensitivity) directly cause LLM failure modes — they're not bugs, they're consequences of how BPE works.
- Vocabulary size is a tradeoff: larger vocab = shorter sequences, rarer tokens; smaller vocab = longer sequences, more uniform token frequency.
- Input and output embedding matrices are often tied (shared weights) to save parameters and improve performance.