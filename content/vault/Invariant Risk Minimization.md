---
title: "Invariant Risk Minimization"
lastmod: 2026-05-23
---

> *Main Issue*
> ML models learn complex prediction rules by minimizing the training error. But while doing so they often overloop the proper features and get marred by selection biases. They essentially cheat by absorbing irrelevant correlations that are found in the training data and lead to a lower loss but not the intended correlation we would want.

A very simple example would be the following.
Imagine the problem of classifying images of cows and camels. To address this task, we label images of both types of animals. Due to a selection bias, most pictures of cows are taken in green pastures, while most pictures of camels happen to be in deserts. After training a convolutional neural network on this dataset, we observe that the model fails to classify easy examples of images of cows when they are taken on sandy beaches. It minimised its training error using a simple cheat: classify green landscapes as cows, and beige landscapes as camels.

We need to identify properties of the data:
- spurious correlations(landscape and contexts)
- phenomenon of interest(animal shapes for this e.g

*wdym by spurious?* - correlation is spurious when we do not expect it to hold in the future in the same manner as it held in the past. These are NOT **stable** properties.

### Why Shuffling data leads to SpurCorr
When we build machine learning datasets (like the famous MNIST dataset of handwritten digits), the original data often comes from completely different sources—like different people writing under different conditions.

Naturally, every person has a unique style: some press hard with the pen, some slant their letters, and some write larger. These unique quirks are **spurious features**—they don't actually define what a "7" or a "3" is.

Instead of keeping this data organized by writer, standard machine learning practice tells us to **throw all the data into a blender and shuffle it randomly** before splitting it into "train" and "test" sets.

*Why do we shuffle?*
We shuffle because standard machine learning algorithms rely on a fundamental assumption called **i.i.d.** (Independent and Identically Distributed). Shuffling forces the training set and the testing set to look identical. Because the mixes of writers are now perfectly balanced between the two sets, the model can exploit those unique writer quirks to get a near-perfect score on the test set. It makes our accuracy metrics look fantastic.

But as the authors point out- *"Shuffling is something that we do, not something that Nature does for us."*

When you blend all the data together, you destroy the information about _how_ the data changes from person to person. By destroying these boundaries, you deny the model the ability to learn the difference between what is **spurious** and what is **stable**:
- **Spurious (Destroyed by environments):** If the model could see the data grouped by writer, it would notice that a specific pen thickness or slant _only_ appears for one writer and completely vanishes for the next. It would realize, _"Ah, this thickness isn't part of what makes a number 7."
- **Stable (Invariant across environments):** The model would see that no matter who is writing, a "7" always consists of a horizontal top bar and a slanting down stroke. That is the universal truth.

> When we shuffle our data into a uniform soup, every single mini-batch inherits the global dataset's flaws, consistently presenting a 90% false correlation that the model greedily exploits across the entire training run. 
> However, when we preserve the boundaries of individual environments(say train one env at a time), we expose the shortcut. 
> 
> While a spurious correlation might be incredibly strong and high-valued in one or two specific environments, it completely vanishes or flips in the rest. As the model trains across these distinct environments sequentially, it is hit with a harsh reality check. The shortcut that worked flawlessly in Environment A suddenly causes catastrophic errors in Environment B. This localized failure generates massive gradient penalties, forcing the optimization algorithm to hunt for features that remain consistent across every single domain.


*invariant descriptions of objects relate to the causal explanation of the object itself (“Why is it a cow? ”)*
- Invariant descriptions refer to those which remain same across different settings and environments.
- Causal explaination refers to how humans would describe an object. They describe a cow to be something that stands on grass but based on its physical features.

They Propose IRM - a novel learning paradigm that estimates nonlinear, invariant, causal predictors from multiple training environments, to enable out-of-distribution (OOD) generalization.






