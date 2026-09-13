---
title: "Mechanistic Mode Connectivity"
lastmod: 2026-06-28
---

#interpretebility #continual_learning 

*Def: Mechanistic Similarity between two models*
(Mechanistic Similarity.) Consider a set of unit interventions Ab := {Ai}, where i ∈ [m]. For parameters θ, denote the subset of interventions that f (.; θ) is invariant to as I(θ) ⊂ Ab. Then, f (.; θ1) and f (.; θ2) are called mechanistically similar if I(θ1) = I(θ2).

Definition 5. *(Mechanistic Connectivity.)* Consider two minimizers θ1 and θ2 of loss L(f (D; θ)) on a dataset D.  Let$E(D) := {E(D; A^{α_i∼Z_i} )}^m  _{i=1}$ denote a set of counterfactual datasets designed by applying{ }unit interventions Ai o all points in dataset D, where intervention assignments αi are chosen uniformly from the respective range of values Zi. Then, θ1 and θ2 are called mechanistically connected along the path $γ_{θ_1→θ_2} (t)$ if, for all counterfactual datasets, they are minimizers that exhibit mode connectivity.
- two minimizers exhibit mechanistic connectivity, then there exists a path such that moving along it does not yield increase in loss on the counterfactual dataset described by any pre-defined intervention


They trained a ResNet18 on a synthetic dataset with cues correlation to the predict then finetuned it later on a non-cue dataset. Here are the eval results.
![](/vault/papers/attachments/pasted-image-20260628140459.png)
As you can see the *small lr* scenario - the model is still fixated on the previous learnings and focusing only on the cues. The fine-tuning did not help.
However for larger LRs , the the finetuning worked somewhat.
Using a large learning rate or enforcing perfect correlation between the cue and label induces loss barriers along the linear path, i.e., linear mode connectivity does not hold.

![](/vault/papers/attachments/pasted-image-20260628141746.png)

### Key Findings:
**1. Lack of Linear Connectivity Implies Mechanistic Dissimilarity** A central finding of the paper is the formalization of the relationship between linear connectivity and a model's underlying rules. The authors demonstrate that if two models cannot be connected via a straight linear path in the parameter space without encountering a "loss barrier" (a spike in error), they definitively rely on different predictive mechanisms. This holds true even after applying "activation matching" to align the models' hidden neurons and account for architectural permutation symmetries.

**2. Mechanistically Dissimilar Models Exhibit Non-Linear Connectivity** Even if two models use completely disparate mechanisms—such as one relying entirely on spurious background cues and another relying on natural object shapes—the researchers found they can still be easily connected via non-linear, quadratic paths. Moving along these curved paths does not yield a drop in performance on the original training data.

**3. "Mechanistic Connectivity" is Unfounded for Dissimilar Models** While you can draw a successful non-linear path between dissimilar models, the authors proved that the internal mechanisms are fundamentally unstable along that transition. When they tested intermediate models along the quadratic paths using counterfactual datasets (where specific attributes like cues were randomized or removed), performance dropped significantly. This means the continuous path alters the underlying predictive mechanisms, proving that true "mechanistic connectivity" between models with different invariances does not exist.

**4. Naïve Fine-Tuning Fails to Eliminate Pre-Trained Biases** The geometric findings above perfectly explain a major practical failure in modern deep learning: naïve fine-tuning often fails to fix models that learned bad habits. When a model that relies on spurious attributes is fine-tuned on a small "clean" dataset using standard low learning rates, it generally remains linearly connected to its pre-trained initialization. Because linear connectivity implies mechanistic similarity, the fine-tuned model retains the exact same flawed predictive mechanisms it had before

## Connectivity Based Fine-Tuning
- In order the change the model's rules learnt during pre-training, we have to break the linear connectivity to the Finetuned parameters from the pretrained parameters.
	![](/vault/papers/attachments/pasted-image-20260628142608.png)

### Major Implications of their contributions
- **Explaining the Failure of Naı̈ve Fine-Tuning:** A major practical takeaway is that naı̈ve fine-tuning on a small "clean" dataset is often insufficient to eliminate a model's reliance on spurious attributes (like background cues) learned during pre-training. Because standard optimization tends to find solutions that remain linearly connected to the pre-trained initialization, the fine-tuned model generally retains the exact same underlying predictive mechanisms, essentially failing to correct the bias
- **Sample-Efficient Targeted Model Alteration:** By understanding that linear connectivity must be broken to change a model's mechanisms, researchers can explicitly force a model to unlearn bad behaviors. The authors exploit this to create **Connectivity-Based Fine-Tuning (CBFT)**, a method that purposefully injects a "barrier loss" to push the model into a linearly disconnected region of the landscape. CBFT successfully alters the model's mechanisms (e.g., dropping reliance on spurious cues) using only a minimal amount of clean data, proving much more effective than standard fine-tuning or simply re-training the last layer



