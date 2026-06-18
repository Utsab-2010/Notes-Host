---
title: "Any other ways than deterministic and Probabilistic Modelling"
---

#to_ponder #ideas
<alphaxiv-thinking-title title="Reading papers on quantum cognition and evidence theory" />

While the deterministic and probabilistic paradigms dominate modern machine learning, several other frameworks exist that model uncertainty and logic in fundamentally different ways. These paradigms are often used when data is scarce, contradictory, or when researchers try to capture the "non-rational" nuances of human behavior.
## Alternative Modeling Paradigms in ML

Beyond the standard deterministic $f(x) = y$ and probabilistic $P(y|x)$ approaches, several specialized theories provide different mathematical structures for handling information:

*   **Evidence Theory (Dempster-Shafer Theory)**: Unlike probability, which must distribute a total "mass" of $1$ across all possible single outcomes, Evidence Theory allows for "ignorance." It distinguishes between **Belief** (the evidence supporting a specific claim) and **Plausibility** (the lack of evidence against it). The gap between the two represents the degree of uncertainty or "vacuity" of knowledge. [A Survey on Uncertainty Reasoning and Quantification for Decision Making: Belief Theory Meets Deep Learning](https://arxiv.org/abs/2206.05675)
*   **Possibilistic Modeling**: This framework, rooted in fuzzy logic, uses possibility distributions $\pi(x)$ to represent how "at ease" or "feasible" an outcome is, rather than how likely it is. It is particularly useful for modeling linguistic vagueness (e.g., what counts as "tall") where classical probability boundaries are too rigid. [Possibilistic inferential models: a review](https://arxiv.org/abs/2507.09007)
*   **Symbolic and Logical Modeling**: Traditional AI uses formal logic (if-then rules) and knowledge graphs. While "Neural-Symbolic" hybrids are popular now, pure symbolic models are strictly non-probabilistic; they focus on structured relationships and deductive reasoning rather than statistical correlation.

---

## Are Humans Probabilistic Models?

The question of whether humans are "probabilistic" is a major debate in cognitive science. For a long time, the **Bayesian Brain** hypothesis suggested that humans are essentially "optimal" probabilistic reasoners who update their internal models as they receive new data. However, humans frequently violate the axioms of classical probability.

### The Case Against Pure Probability
Researchers have found that human decision-making often follows **Quantum Cognition** principles rather than classical ones. Classical probability relies on the "Law of Total Probability," which assumes that the order of information doesn't change the underlying state. Humans, however, show "order effects"—where hearing option $A$ before $B$ changes the outcome in a way that classical probability cannot easily model.

> "Experiments in cognitive science and decision theory show that the ways in which people combine concepts and make decisions cannot be described by classical logic and probability theory." [Quantum Cognition](https://alphaxiv.org/abs/1104.3344v1?page=1)
### Quantum Structure in Human Thought
To resolve these paradoxes, some models use the mathematics of quantum mechanics—not because the brain is a quantum computer, but because quantum logic allows for **superposition** (being in multiple states at once) and **interference**. For instance, when humans combine two concepts (like "Pet" and "Fish"), they often assign higher typicality to a "Goldfish" than classical probability would predict. This "over-extension" is modeled better as a wave-like interference pattern in a Hilbert space. [Conceptual Structure](https://alphaxiv.org/abs/1104.3344v1?page=1)

In summary, while we can *approximate* human behavior with probabilistic models, we aren't "strictly" probabilistic in the classical sense. We are better described by more flexible frameworks that account for context, ambiguity, and the inherent contradictions of thought.