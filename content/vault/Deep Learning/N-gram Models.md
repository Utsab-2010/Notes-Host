---
title: "N-gram Models"
---

#deep_learning #nlp 
An **n-gram model** is a classical, statistically driven approach used in Natural Language Processing (NLP) to predict the next item in a sequence (typically words or characters) based on the history of the preceding items.

Unlike modern Large Language Models that process long paragraphs of text simultaneously using self-attention mechanisms, an n-gram model operates on a strict, local window of text.

## 1. Breaking Down the Term "n-gram"

In this context, the **"n"** represents a fixed number, and a **"gram"** represents a unit of text (usually a word). An n-gram is simply a contiguous sequence of $n$ items from a given sample of text.

Depending on the size of the window ($n$), these sequences have specific names:

- **1-gram (Unigram):** Looks at words in complete isolation.
    
    - _Example:_ "The", "dog", "barked"
        
- **2-gram (Bigram):** Looks at pairs of consecutive words.
    
    - _Example:_ "The dog", "dog barked"
        
- **3-gram (Trigram):** Looks at triplets of consecutive words.
    
    - _Example:_ "The dog barked"
        
- **4-gram (Quadgram):** Looks at four consecutive words.
    
    - _Example:_ "The dog barked loudly"
        

## 2. How the Prediction Math Works

An n-gram model calculates the probability of a word occurring based entirely on the $n-1$ words that came immediately before it. This relies on what mathematicians call the **Markov Assumption**—the idea that you don't need the entire history of a system to predict its future state; a brief snapshot of the recent past is enough.

For a **Bigram model ($n=2$)**, the probability of a word depends only on the _one_ single word before it:

$$P(\text{word} \mid \text{previous word}) = \frac{\text{Count}(\text{previous word}, \text{word})}{\text{Count}(\text{previous word})}$$

### Real-World Example:

Imagine training a bigram model on a small collection of text, and you want to predict what follows the word **"artificial"**.

1. The model counts how many times **"artificial"** appears in the training text (let's say 100 times).
    
2. It counts how many times the phrase **"artificial intelligence"** appears (say 60 times).
    
3. It counts how many times **"artificial sweetener"** appears (say 20 times).
    

Using these raw frequency counts, the model calculates the probabilities:

- $P(\text{intelligence} \mid \text{artificial}) = \frac{60}{100} = 60\%$
    
- $P(\text{sweetener} \mid \text{artificial}) = \frac{20}{100} = 20\%$
    

If asked to autocomplete, the model picks "intelligence" because it has the highest statistical probability based on the training data.

## 3. The Major Bottleneck: The Curse of Dimensionality

While n-gram models are fast to compute for small sequences, they fall apart completely when you try to scale them up to handle longer contexts (making $n$ larger to remember more history). This limitation is highly relevant to the paper discussed earlier:

- **Exponential Memory Explosion:** As $n$ grows, the number of possible word combinations explodes exponentially. If your vocabulary size ($V$) is 50,000 words, a bigram model ($n=2$) has $50,000^2 = 2.5 \text{ billion}$ possible combinations. A trigram model ($n=3$) has $50,000^3 = 125 \text{ trillion}$ combinations.
    
- **The Sparsity Problem (Zero Probabilities):** Because the space of possibilities grows so fast, your training data will never contain every logical combination. If a model encounters a phrase it hasn't seen before during testing—even if it makes perfect sense to a human—the count will be 0, yielding a probability of 0% and breaking the system.
    
- **Lack of Deep Understanding:** N-gram models look up raw frequencies; they do not map words to a continuous vector space (embeddings). They don't know that "cat" and "kitten" are similar concepts, so learning a pattern for "the cat sat" tells the model absolutely nothing about "the kitten sat."
    

This is exactly why the paper's authors emphasize that classical n-gram models lie outside the fast-learning "universality class" of modern deep neural networks. Because n-gram models lack compositional shortcuts, they suffer heavily from this curse of dimensionality, rendering them incapable of efficiently scaling past a few tokens of history.