---
title: "Learned feature representations are biased by complexity, learning order, position, and more"
lastmod: 2026-07-08
---

#data-efficient-ml #interpretebility #curriculum_learning #representations 

[\[2405.05847\] Learned feature representations are biased by complexity, learning order, position, and more](http://arxiv.org/abs/2405.05847)
## Core Claim
- Surprising dissociations between representation and computation
- Learned feature representations are systematically biased towards some features over others
- Bias depends on: feature complexity, learning order, feature distribution over inputs
- "using representations to understand or improve computation depends fundamentally on the linking assumptions we make about their relationship"

---

# Definitions

**Feature** — abstract, task-relevant property of an input; result of applying some function f(I). Generally, features the model is explicitly trained to output.

**Computational role** — downstream contribution of a feature to the desired output behavior, once that feature's value has been computed.

**Representation** — does *not* stipulate causal implication in model behavior. Finding a pattern of neurons correlated with a feature ≠ the model uses those neurons for its final prediction.

#### Representational Variance
- It is a measure of how much the presence of a particular feature has on the representation vector of the model. The higher the value, the stronger the influence.
- Here is the formal calculation algorithm and mathematical expressions for the representation variance explained by a feature:
	1. **Define Variables** Let $\phi(I_i)$ denote the mean-centered representation vector produced by the model for a given input $I_i$, and let $f(I_i)$ be the corresponding feature value.
	2. **Fit the Linear Predictor (on Validation Set $V$)** Find the optimal linear predictor weight matrix $W^*_f$ that predicts the neural representations solely from the feature values by minimizing the squared error on a validation set:$$W^*_f = \arg\min_W \mathbb{E}_{I_i \in V} \left[ ||W f(I_i) - \phi(I_i)||^2 \right]$$
	3. **Calculate the Variance Explained (on Test Set $T$)** Calculate the $R^2_f$ score on a held-out test dataset by measuring the prediction error relative to the total variance of the representations:
	$$R^2_f = \mathbb{E}_{I_i \in T} \left[ 1 - \frac{||W^*_f f(I_i) - \phi(I_i)||^2}{||\phi(I_i)||^2} \right]$$

	(i.e., in the equation above, we replace the total variance term $||\phi(I_i) ||^2$ in the denominator with the final value $||\phi_{final} (I_i) ||_2$ at all timepoints), to plot all values on a consistent scale.
	
	#### Limitations:
	- This kind of probing based feature extraction and variance quantification only works in this toy setup where we have explicit knowledge regarding the features present and have confirmed them to be statistically independent. We can't exactly do this variance based analysis on a real-world model.
	#### Importance of Repr. Variance:
	- It can show causality and not only correlation

#### Checking for Causality:
- They took the trained MLP from the binary toy setup. Then they got the representations corresponding to when the feature is present and for when the feature is absent.
- A feature being present means that the feature probe's output is 1. If not present, output = 0.
	- A feature can either exist or not exist. If it had more classes, we can decompose it into a collection of other features. So features in itself are(safe to assume) binary classes.
- the difference of the present vs absent repr vectors was found
- Scalar multiple of this difference vector was added to repr of different test inputs to see if it would reverse the feature output corresponding to that feature. AND IT DID!
- The causality of the repr variance analysis is that - it takes much s*maller strength of the difference vector to change the difficult features outputs* than it takes for easier features
	- Difficult features have smaller variance in representation space, hence more sensitive to noise in representation space?? 
- This shows that the repr subspace that the difference vector is on, determines the existance of the feature and more simpler features get alloted more tolerate to this difference vector.

---

## Key Findings

### Representational Simplicity Bias
- Features simpler to compute (e.g. linearly computable) are more strongly represented than complex (e.g. nonlinear) features playing an equivalent computational role
- Features learned earlier → represented more strongly
- Long after the easy feature is mastered, its representation variance *continues to grow*, especially while the hard feature is being actively learned — some cooperative pressure inflating it
- Easy feature dominates top PCs; hard feature barely impacts them

### Complexity vs. Learning Order
- Pretraining the hard feature closes the gap somewhat, but easy feature still dominates → learning order alone doesn't explain it
- "there are more ways to represent harder features" → harder features produce sparser representations
- Could it be that components of the hard feature are strongly represented even if the hard feature itself isn't? → Yes, measuring sub-components of XOR reveals stronger representation

### Feature Prevalence
- More frequent features → more gradient updates → learned earlier → more strongly represented
- This may not be visible from behavior: "not immediately obvious from the model's behavior that one feature should be represented more strongly than another because of a frequency artifact"

### Architecture & Optimizer Effects
- Deeper MLPs → larger representational gaps; width has little effect
- Adam + dropout → can reverse the bias (slight hard feature preference at moderate dropout)
- Non-residual CNNs → strong color (easy) bias at spatial pooling layer
- ResNets → strong *shape* (hard) bias — opposite of expected
  - *Personal note: so is learning order the true defining cause? Especially for ResNets*
- Transformers: encoders with residual connections to input show stronger bias toward features requiring integration over larger input areas

---

## Causal Validation
- Analyses above are correlational
- Used causal interventions (equivalent to steering vectors) to verify representations are causally implicated
- Intervening along easy feature subspace flips easy feature labels without affecting hard feature labels → causally sufficient and specific
- Smaller interventions needed to flip hard feature labels (less representational variance)
- Top-k PCA: easy feature preserved with smaller k than hard feature

---

## Downstream Effect on Classifiers
- When both features are highly predictive, linear classifiers trained on representations are strongly biased toward relying on the easier feature
- Tested via decorrelated samples: easy=1, hard=0, label=1 → if classifier gets it right, it's relying on easy feature

---

## Personal Notes
- Causality check is strong — for data pruning work, showing causal relation between pruning and representational skew would be stronger than correlation alone
- Feature biases may be stronger with larger output spaces


>[!Note] Counter-intuitive: Why are easy features taking up more space within the repr space?
> **1. Learning Order (The "Head Start" Effect):** Simpler features are mathematically easier for the network to solve, meaning the AI figures them out much faster. Because the process of deep learning is highly "path-dependent," the things an AI learns first get to establish themselves and "hog" the majority of the available neural space before the harder, slower features have a chance to fully develop. - *This ain't the main reason* as shown my hard-first learning, it still happens.
> **2. "More Ways to Represent" (Fragmentation):** A simple feature has only one straightforward mathematical path. However, a complex "hard" feature can be broken down into many different intermediate steps or sub-equations and AI naturally scatters and fragments its processing across the network.  makes the hard feature's physical footprint much weaker and sparser compared to the highly concentrated, singular signal of the easy feature. - *still feels counterintuitive but was shown to work*
**3. The Network's Built-In "Simplicity Bias":** The researchers also link this phenomenon to a known concept called the "implicit inductive bias for simplicity". By their very mathematical nature, deep neural networks (even when they are just randomly initialized at the start of training) are biased toward computing simple functions. This inherent architectural bias makes simpler features naturally easier for the network to latch onto, resulting in them taking up a denser, more prominent space, while squeezing complex features into sparser, quieter corners of the network.
