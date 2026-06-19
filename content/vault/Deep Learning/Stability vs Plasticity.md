---
title: "Stability vs Plasticity"
lastmod: 2026-05-05
---

#continual_learning 

This section describes the **Bayesian approach to [Continual Learning](/vault/deep-learning/continual-learning/)**, which is a more mathematically rigorous alternative to just storing old images in a buffer (replay-based methods).

Think of it as trying to turn the model's "memory" into a probability distribution rather than a hard drive of raw data.

### 1. How is the Posterior being defined?

In this context, the posterior $p(\theta | \mathcal{D}_{1:k})$ represents the **probability of the model parameters $\theta$ being correct**, given that you have observed all the datasets from Task 1 up to Task $k$ ($\mathcal{D}_{1:k}$).
The paper defines it recursively using Bayes' Rule:
$$p(\theta | \mathcal{D}_{1:k}) \propto p(\theta | \mathcal{D}_{1:k-1}) p(\mathcal{D}_k | \theta)$$

Breaking this down:
- **$p(\theta | \mathcal{D}_{1:k-1})$ (The Prior):** This is what the model learned from all previous tasks. It acts as the "starting point" or prior knowledge before seeing the current task.
- **$p(\mathcal{D}_k | \theta)$ (The Likelihood):** This is how well the current parameters $\theta$ explain the new data from Task $k$.
- **$p(\theta | \mathcal{D}_{1:k})$ (The New Posterior):** The updated belief about the parameters after merging old knowledge with the new data.

## Posterior is Intractable
To understand why the posterior is intractable, we have to look at the "math tax" imposed by Bayes' Rule.  the posterior for task $k$ is defined as:

$$p(\theta | \mathcal{D}_{1:k}) = \frac{p(\mathcal{D}_k | \theta) p(\theta | \mathcal{D}_{1:k-1})}{p(\mathcal{D}_k)}$$
 $p(\mathcal{D}_k)$, also known as the **Evidence** or **Marginal Likelihood**. *The above expression is written assuming conditional independence between the task datasets given parameter $\theta$.*

To calculate the denominator exactly, we must account for every possible configuration of the model parameters $\theta$ that could have produced the data $\mathcal{D}_k$. This requires solving an integral over the entire parameter space:
$$p(\mathcal{D}_k) = \int_{\Theta} p(\mathcal{D}_k | \theta) p(\theta | \mathcal{D}_{1:k-1}) d\theta$$

- Modern Neural Networks (NNs) have millions or even billions of parameters. Integrating over a million-dimensional space is computationally impossible; numerical integration techniques (like grid search) scale exponentially with the number of dimensions.
- The term $p(\mathcal{D}_k | \theta)$ is defined by the neural network itself. "probability landscape" is incredibly jagged and non-convex. There is no "closed-form" solution to solve this integral.
## Hence we use NNs to approximate it?

Since we can't solve the integral, we turn the problem from **Integration** into **Optimization**. the introduction of $q_k(\theta) \approx p(\theta | \mathcal{D}_{1:k})$.

### What is the significance of the Posterior?
The posterior is essentially the **"Elastic Memory"** of the network.
In standard Deep Learning, we usually only care about the **point estimate** (the specific values of the weights). But in [Continual Learning](/vault/deep-learning/continual-learning/), the *posterior tells us which weights are "flexible" and which are "rigid."*
- If the *posterior distribution for a specific weight is very narrow* (low variance), it means that weight is critical for a previous task. Moving it will cause **catastrophic forgetting**.
- If the distribution is wide (high variance), that weight isn't doing much for old tasks, and the model can safely change it to learn the new task.
By propagating the posterior, the model "remembers" not just the performance, but the **importance** of every single parameter in the network across all tasks seen so far.

### How would it be used if it were not intractable?
If we could actually compute this exactly (which we can't for deep neural networks because the parameter space is too high-dimensional and the integrals are impossible), the "perfect" continual learning algorithm would look like this:

1. **Zero Data Storage:** You would never need to store a single image from Task 1 once you move to Task 2. The posterior $p(\theta | \mathcal{D}_1)$ captures _everything_ useful about the data.
2. **Perfect Regularization:** When training on Task $k$, you would use the old posterior as a "penalty" term. A*ny time you try to change a weight that was important for Task $k-1$, the posterior would create a massive mathematical "cost,"* forcing the optimizer to find a solution that works for both tasks.
3. **Optimal Learning:** You would essentially be performing a running update of your knowledge. Instead of "retraining," you are "refining" your belief about the world.
