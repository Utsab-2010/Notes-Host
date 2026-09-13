---
title: "Scaling laws with rep"
lastmod: 2026-06-12
---

### 1. The Core Premise: What Must $\delta$ Measure?

When a model processes a dataset of size $P_0$ tokens for the first time, it uses those samples to resolve the true underlying distribution rules of the language. When it reads the exact same sequence a second time, no new tokens are added. The _only_ reason the second pass contains non-zero utility is if the model failed to fully extract the statistical relationships during the first pass.

In standard statistical estimation, if you sample with replacement from a finite pool, the rate at which new information saturates depends on the **entropy of the sequence choices** and the **rank of the correlation space**. If a corpus is highly redundant, a single pass extracts everything. If a corpus is highly complex, the patterns are undersampled after one pass, meaning full utility is retained on the next loops.

### 2. The Information-Theoretic Derivation: Backward Conditional Entropy

For a context window of length $n$, Cagnetta et al. focuses on the forward conditional entropy—the uncertainty of the _next_ token given the past:

$$H_{\text{forward}}(n) = H(X_{n+1} \mid X_{1:n})$$

However, to model why repeating a sequence provides new value, we must look backward. When the model encounters a familiar $n$-gram context $X_{1:n}$ during epoch 2, that context only provides new structural signal if it is connected to multiple semantic pathways across the wider corpus. We measure this using the **Backward Conditional Entropy**:
$$H_{\text{backward}}(n) = H(X_0 \mid X_{1:n})$$

This tracks the uncertainty of the token _preceding_ the current context window.

- **Rigid Contexts ($\delta \to 0$):** If $H_{\text{backward}}(n) \approx 0$, it means whenever the sequence $X_{1:n}$ appears in the language, it is always preceded by the exact same token $X_0$. It is a locked, boilerplate phrase. Once the model learns this single rigid chain in Epoch 1, re-reading it provides zero new topological context.
    
- **Fluid Contexts ($\delta \to 1$):** If $H_{\text{backward}}(n)$ is high, the sequence $X_{1:n}$ is highly promiscuous—it acts as a landing point for many completely different sentences, topics, and ideas.
    

We define the **Contextual Ambidexterity Ratio ($A_n$)** at the data-dependent horizon scale $n^*$:

$$A_{n^*} = \frac{H(X_0 \mid X_{1:n^*})}{H(X_{n^*+1} \mid X_{1:n^*})}$$

If $A_{n^*}$ is high, the contexts are fluidly branching in both directions. The model requires multiple exposure loops to properly map how these central structural nodes connect to the rest of the language graph, which keeps $\delta$ close to 1.

### The Geometric Derivation: Covariance Spectral Entropy
We can make this even more mathematically precise by extending Cagnetta’s core engine: the token-token covariance matrix $C(n)$.
Cagnetta’s data-limited scaling law only tracks the _operator norm_ (the maximum singular value) of this matrix to see if the strongest signal crosses the noise floor:
$$\|C(n)\|_{\text{op}} \sim n^{-\beta}$$
*But a model's capacity to absorb information over multiple epochs depends on the **entire spectrum** of that covariance matrix.* Let $\sigma_1, \sigma_2, \dots, \sigma_V$ be the singular values of the token-token covariance matrix $C(n)$ calculated at the maximum resolvable context horizon $n^* = P_0^{1/2\beta}$.

We normalize this spectrum to turn the singular values into a probability distribution of correlation energy:
$$\tilde{\sigma}_i = \frac{\sigma_i}{\sum_{j=1}^{V} \sigma_j}$$
Now, we compute the **Spectral Entropy ($H_{\text{spec}}$)** of the correlation space:

$$H_{\text{spec}}(n^*) = -\sum_{i=1}^{V} \tilde{\sigma}_i \log \tilde{\sigma}_i$$
#### How Spectral Entropy Controls $\delta$:
1. **Low Spectral Entropy (Low Effective Rank):** The covariance spectrum is sharply skewed. A few dominant singular values contain all the energy, while the rest drop to zero. This means the tokens relate to each other in only a few simple ways. During the first pass ($Epoch 1$), the model's gradients easily capture these giant structural peaks. Because there are no orthogonal feature directions left to learn, the utility of a second pass drops to zero ($\delta \to 0$).
2. **High Spectral Entropy :** The covariance spectrum is flat and distributed across hundreds of orthogonal dimensions. In a single pass, a finite dataset $P_0$ only provides enough statistical resolution to clear the noise floor for the top few dimensions. The lower, flatter parts of the spectrum remain unresolved. Pushing into subsequent epochs allows the gradient step(High Effective Rank)s to steadily resolve these subtle, orthogonal structural directions without drowning in sampling noise. The dataset retains its utility across many passes ($\delta \to 1$).
### 4. The Unified Structural Formulation
To tie Goyal's repetition decay parameter directly to this measurable corpus statistic, we scale the spectral entropy by the maximum possible entropy of the vocabulary space ($\log V$), clamping $\delta$ cleanly between 0 and 1:
$$\delta = \frac{H_{\text{spec}}(n^*)}{ \log V } = -\frac{1}{\log V} \sum_{i=1}^{V} \tilde{\sigma}_i \log \tilde{\sigma}_i \quad \text{where} \quad n^* = P_0^{\frac{1}{2\beta}}$$
Substituting this pure linguistic statistic back into the unified scaling law yields the complete, parameter-free expression for multi-epoch test loss:
$$\mathcal{L}_{AR}(P_0, k) - H_\infty \sim \left[ P_0 \cdot \frac{1 - \left(-\frac{1}{\log V} \sum_{i=1}^{V} \tilde{\sigma}_i \log \tilde{\sigma}_i\right)^k}{1 - \left(-\frac{1}{\log V} \sum_{i=1}^{V} \tilde{\sigma}_i \log \tilde{\sigma}_i\right)} \right]^{-\frac{\gamma}{2\beta}}$$

Every variable on the right side of this equation—$\gamma$ (forward entropy decay), $\beta$ (correlation decay), and $H_{\text{spec}}$ (spectral covariance entropy)—can be computed directly via token counts on a static text file before a single model parameter is ever initialized.

## Why does this make Sense?
The empirical covariance matrix $C(P)_n$ is a frozen, static property of the specific dataset $P$ you hand to the model.  $C(P)_n$ does not change by a single decimal point between Epoch 1 and Epoch 10.
##### The Mechanism: Projection and Satiation
Think of $C(P)_n$ as a multi-dimensional structural landscape defined entirely by the dataset's token-token statistics. When a model trains, its weights are updated via gradients that try to match this landscape.
Mathematically, we decompose this static matrix $C(P)_n$ into its singular values (its spectrum):
$$C(P)_n = \sum_{i=1}^{V} \sigma_i u_i v_i^T$$

- **Epoch 1:** The network looks at the data for the first time. The gradients are overwhelmingly driven by the largest singular values ($\sigma_1, \sigma_2$, etc.)—the most massive, dominant statistical correlations in the dataset (like basic grammar structures or highly frequent phrases). By the end of the first pass, the model has successfully absorbed these high-energy dimensions.
- **Epoch 2:** The model reads the exact same sequence. Because $C(P)_n$ is static, it doesn't offer any new major directional hills to climb. The model already perfectly predicts the dominant components it learned in Epoch 1, so the gradient updates along those directions drop to zero.
	- The _only_ thing left for the model to learn from this static matrix are the remaining lower-energy, orthogonal dimensions (the smaller singular values) that it didn't have enough time or resolution to fully capture in pass one.

### Why $\delta$ is a Direct Function of $C(P)_n$
This is why Goyal's decay parameter $\delta$ is fundamentally dictated by the shape of the dataset's static spectrum:
1. **If $C(P)_n$ has Low Spectral Entropy (Low Rank):** The probability mass of the correlations is concentrated almost entirely in the top few singular values. Once Epoch 1 finishes, the model has completely cleaned out the signal. Because $C(P)_n$ is static and has nothing else to offer in its lower dimensions, the *utility of the second pass completely tanks*. **Result: $\delta \to 0$.**
2. **If $C(P)_n$ has High Spectral Entropy (High Rank):** The correlation energy is spread out evenly across hundreds of orthogonal, subtle dimensions. In a single pass, a finite dataset doesn't give the model enough gradient steps to resolve all these quiet, complex directions from the random sampling noise floor. When Epoch 2 begins, even though the big structures are satiated, there is still a massive reservoir of unlearned, lower-level orthogonal signals waiting to be resolved. **Result: $\delta \to 1$.**

It is precisely because $C(P)_n$ is static that the model drains its informative value layer by layer, and the rate at which that value is drained ($\delta$) depends entirely on how many hidden, orthogonal layers the matrix spectrum possessed in the first place.

If $\delta$ is determined by $n^*$, and $n^*$ is driven by $P_{\text{eff}}$, which itself is calculated using $\delta$, you get stuck in an endless loop:

$$\delta \implies P_{\text{eff}} \implies n^* \implies \delta$$

To break this cycle and keep the math rigorous, we have to look at the physics of how a training run actually starts. The resolution lies in **anchoring $\delta$ strictly to the initial unique data pool.**
### Step 1: Freeze $\delta$ at the Starting Line ($n^*_0$)
Goyal et al. define $\delta$ as a constant parameter for a given data pool. It represents the penalty for re-reading _that specific pool_. Therefore, we do not calculate $\delta$ on a moving context horizon. We evaluate it exactly once at the **initial baseline horizon ($n^*_0$)** before any repetitions occur.
When you hand a model a unique dataset of size $P_0$, it establishes a fixed starting frontier:
$$n^*_0 \approx P_0^{\frac{1}{2\beta}}$$
We analyze the static token-token covariance matrix $C(P_0)$ specifically at this length scale $n^*_0$. We extract its singular values and compute the Spectral Entropy:
$$H_{\text{spec}}(n^*_0) = -\sum_{i=1}^{V} \tilde{\sigma}_i \log \tilde{\sigma}_i$$
This gives us a fixed, unchanging scalar value for the decay parameter:
$$\delta = \frac{H_{\text{spec}}(n^*_0)}{\log V}$$

By tying $\delta$ entirely to the baseline properties of the unique data pool ($P_0$), we instantly break the cycle. $\delta$ is now a frozen constant.

$$P_{\text{eff}}(k) = P_0 \cdot \frac{1 - \delta^k}{1 - \delta}$$

As $P_{\text{eff}}(k)$ grows with each epoch, it drives the expansion of the **moving context horizon $n^*_k$**:

$$n^*_k \approx \left[ P_{\text{eff}}(k) \right]^{\frac{1}{2\beta}} = \left[ P_0 \cdot \frac{1 - \delta^k}{1 - \delta} \right]^{\frac{1}{2\beta}}$$

Because $\delta$ is an anchor behind the system, the moving horizon $n^*_k$ creeps forward smoothly epoch by epoch, pulling back deeper layers of the static data matrix without any circular feedback loops.


## How much with $n^*(k)$ grow?
When a model processes a frozen dataset file of size $P_0$ for the first time, it doesn't have enough gradient steps or optimization capacity to absorb every ounce of statistical signal present in that file. It prioritizes the loudest, highest-energy patterns (short-range correlations).
When you loop back for subsequent epochs, the model doesn't see fresh text, but it _does_ get more optimization cycles. Because it has already mastered the easy, dominant structures, the gradients for those structures drop to zero. This frees up the model's parameters to start resolving the quieter, lower-energy orthogonal dimensions in the data's static covariance spectrum that it was forced to ignore during the first pass.

Because the model is steadily resolving these subtler, lower-energy correlation paths, its effective analytical resolution capacity expands. In the math, this is exactly what happens when we swap the raw token count $P_0$ for the **Effective Dataset Size** ($P_{\text{eff}}$).

As a direct consequence of this increased resolution, the maximum context length where the model can successfully distinguish real linguistic signal from background noise—the **moving horizon $n^*_k$**—is pushed outward:
$$n^*_k \approx \left[ P_{\text{eff}}(k) \right]^{\frac{1}{2\beta}} = \left[ P_0 \cdot \frac{1 - \delta^k}{1 - \delta} \right]^{\frac{1}{2\beta}}$$
With each pass, the model gains the statistical clarity required to look further back into its context window and extract meaningful semantic dependencies that originally looked like pure noise.
As the number of epochs $k$ approaches infinity, the marginal information gain from re-reading the data decays exponentially to zero ($\delta^k \to 0$). The model completely exhausts the file's information reservoir and achieves perfect saturation on that specific pool. At this point, the moving horizon hits the exact mathematical ceiling you predicted:
$$n^*_{\max} \approx \left( \frac{P_0}{1 - \delta} \right)^{\frac{1}{2\beta}}$$
This maximum achievable horizon is governed strictly by the unique token volume ($P_0$) and the intrinsic structural diversity of the text corpus ($\delta$, derived from its baseline spectral covariance entropy). Your intuition captures the entire physical reality of the integrated theory.

[Initial Tests for the Scaling Law](/vault/research-work/val-del/initial-tests-for-the-scaling-law/)



## Questions
*But $n^*$ should increase with epochs till some asymptote, so based on that we should have a decreasing $\delta$ value with each epoch **k** right? *
- While this extension can also be tested out, I do think that the spectral entropy would not change much with increasing n* value. Intuitively also kinda makes sense, if the initial spectral entropy kindof gives you the idea of the information distribution of P. Now since model is kinda better, it is able to understand into the noisy domains more but doesn't mean that the information distribution of P has changed.
- Should we condition the information distribution to be condtioned on the model's current understanding of P? Will that be helpful?
	- This can be emperically tested ig. We can assume the first hypothesis and get the spectral entropy and then via the second hypothesis we can use P_eff in epoch 2 and get the new 
Quantisation + vq+vae + random projections.
vision space + projection to random vectors. Use 5 vectors to discretize