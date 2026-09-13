---
title: "Polygenic Voting Toy Test"
lastmod: 2026-06-15
---

Read [](file:///raid2/priyam/utsab/new-quantisation-tests/polygenic_voting.ipynb#91-91), lines 91 to 175

Here's a complete breakdown of the data generation process with your current config (`n_tasks=500`, `num_classes=100`, `max_poly=1`, `max_quanta_classes=5`, `alpha=1.44`, `weighted_votes=False`):

---

### Phase 1: Setup (once at dataset creation)
**Step 1 — Zipf probabilities**
```
probs[q] = q^(-alpha) / sum(i^(-alpha))
```
This gives a descending probability distribution: quantum 0 is ~140× more likely to be sampled than quantum 499.

**Step 2 — Class votes per quantum**
For each quantum `q` (0 to 499):
- Pick a random integer `k` between **1 and 5**
- Randomly choose `k` distinct classes from {0, ..., 99} without replacement

Example: `class_vote[42] = [7, 33, 81]` (size 3), `class_vote[7] = [12]` (size 1)

So a quantum can influence anywhere from 1 to 5 different classes. With 500 quanta and 100 classes, each class gets votes from roughly `500 × 2.5 / 100 ≈ 12.5` quanta on average.

**Step 3 — Quantum strengths** _(skipped since `weighted_votes=False`)_

---

### Phase 2: Per-sample generation (D = 100,000 samples)

**For each sample `i`:**

1. **Sample `m`** — number of active quanta. With `max_poly=1` and `poly_dist="normal"`, `mu = (1+1)/2 = 1`, `sigma = (1-1)/4 = 0`, so `m` is always exactly **1**. (Each sample has exactly one active quantum.)

2. **Pick the active quantum** — randomly choose 1 quantum index from the Zipf distribution. Quantum 0 gets picked most often, quantum 499 gets picked least often.

3. **Build the input** — `X[i]` is a 500-dimensional binary vector:
   ```
   X[i] = [0, 0, ..., 1 at position q, ..., 0]
   ```
   A single `1` at the index of the chosen quantum.

4. **Vote** — let `q` be the active quantum with `class_vote[q] = [c₁, c₂, ..., cₖ]`. Create a length-100 vote vector:
   ```
   votes = [0, 0, ..., 0]
   for each class c in class_vote[q]:
       votes[c] += 1
   ```
   So 1–5 classes each get +1 vote.

5. **Label** — `y = argmax(votes)`. Since there's only one quantum active (m=1), if `class_vote[q]` has size 3, three classes tie at 1 vote each. `argmax` breaks ties to the **lowest-index class**, so the label is `min(class_vote[q])`.

---

### What the model sees

**Input:** A sparse 500-bit vector with exactly one `1` — a one-hot encoding of which quantum is active in this sample.

**Target:** One of 100 classes — the lowest-indexed class that the active quantum votes for.

### What the model must learn

A mapping from 500 input bits → 100 output classes:
- **Common quanta** (low index, e.g. q=0 with ~3000+ samples) → model learns their class vote quickly, high accuracy on those samples
- **Rare quanta** (high index, e.g. q=499 with ~20 samples) → model may never see enough examples to learn their vote, so those samples get misclassified

With `max_poly > 1`, each sample would activate multiple quanta, and the votes would accumulate — making the label depend on the *combination* of which quanta appear, which is harder and more image-like.

Created 6 todos


### Some Observations
- Dynamic Unc Seems to have the same effect as EL2n
- Difference in observation for the mutli-hot vector input and fixed random vector input setups.
	- Pruning seems to have the opposite effect on the latter one.
		- samples with less no. of quanta get pruned out first.
		- el2n avg scores across samples is lower for the lower ranked quantas
	- These are opposite for the mult-hot vector type inputs.
		
### Further Points to Ponder
- Implicit Curricula
	- There might be chunks of quanta that need to be in a region for the implicit curricula to work. Basically, implicit might not learn single quanta at a time but through chunks of quanta  at time. This is also more relevant due to the fact that mostly the tail quanta seem to change their rank with pruning and also the tail quantas tend to have close enough frequencies, so a chunk of consecutive quantas being learnt together, makes sense since the model sees them the same number of times.
	- For each such chunk there is probably a threshold region a deviate of rank beyond which the curricula is fully ruined . That threshold probably increases with the number of quanta and the no. of chunks  or size of chunks might also be dependent on the total number of quanta types.
	- Fat tail is main thing affecting it. More the std. dev in the fat tail, more loss of implicit quanta.