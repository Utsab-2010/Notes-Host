---
title: "Why do Diffusion Models Generalise So Well?"
---

#to_ponder #diffusion #compvis 

- Can we somehow use properties of this to improve OOD Generalisation in other non-genrative vision models?
- It seems the iterative nature of these models lead to learning of the low level features for better generalisation. If we design the non-generative framework in a similar iterative manner would that lead to OOD Gen??
- Models can do two things depending on the regime(needs to be studied):
	- Gen -> overfit
	- Overfit -> gen (grokking)

## Geminis' version on Gen vs Non-Gen Vis Generalisation Ability!!
This is one of the most fascinating asymmetries in modern deep learning. The short answer comes down to **what** the models are forced to learn first: non-generative models optimize for low-dimensional, high-frequency shortcuts (labels) to drop information quickly, while diffusion models are forced to reconstruct the entire data distribution layer by layer, starting with the coarsest, low-frequency structures.

Let’s break down exactly why this happens from first principles.

## 1. Non-Generative Vision Models: The Race to Forget

Discriminative models (like ResNets or ViTs trained on ImageNet) map a high-dimensional image $X \in \mathbb{R}^{C \times H \times W}$ to a tiny, low-dimensional label space $Y \in \mathbb{R}^K$.

According to the **Information Bottleneck Theory**, the model's goal is to maximize its predictive power while minimizing the information it retains about the input image.

### Why they memorize first:

- **The Shortcut Principle:** Images contain millions of pixels, but the label "cat" depends on a fraction of them. Early in training, the network finds high-frequency, superficial shortcuts (like a specific pixel texture, a background color, or noise patterns unique to the training set) to drive the cross-entropy loss to zero as fast as possible.
    
- **Overfitting to the Sample:** This reliance on brittle, dataset-specific features is essentially memorization. The network quickly memorizes the exact mapping of training samples to labels.
    
- **The Generalization Delay:** Only after the training loss is minimized does the optimizer (like SGD with weight decay) begin to smooth out the decision boundaries. It slowly prunes away these brittle, high-frequency shortcuts and forces the network to learn more robust, invariant semantic features (shapes, structures) that generalise to unseen data.
    

## 2. Diffusion Models: The Coarse-to-Fine Trajectory

Diffusion models reverse this entire dynamic because of their objective function. A denoiser $e_\theta(x_t, t)$ doesn't compress an image into a single token; it must predict the noise added to an image across varying timesteps $t \in [0, T]$.

The key here is the **Signal-to-Noise Ratio (SNR)** across the diffusion trajectory.

### Why they generalise first:

- **The Macroscopic Geometry ($t \to T$):** Early in training (and at high noise levels $t$), the image is mostly pure Gaussian noise. The fine-grained details (exact pixel values, sharp edges, textures) are completely obliterated by the noise. The only thing the model can possibly learn to predict at this stage is the global, low-frequency structure—the coarse layout, dominant color blobs, and overall data geometry.
    
- **Generalization as Geometry:** Because these low-frequency structures are shared across many images in the dataset (e.g., "clouds are at the top," "faces are roughly oval"), learning them first means the model learns the _general manifold_ of the data distribution before it knows anything about individual images.
    
- **Memorization as Finetuning ($t \to 0$):** Only late in training, once the model has mastered the global structure, does it start optimizing for low noise levels ($t \approx 0$). Here, the noise is subtle, and the model learns high-frequency details—sharp textures, exact lines, and ultimately, the specific idiosyncratic details of individual training images (memorization).
    

## Summarizing the Asymmetry

|**Feature**|**Non-Generative (Discriminative) Models**|**Generative Diffusion Models**|
|---|---|---|
|**Objective**|Compress input $X$ to label $Y$ (Information Bottleneck).|Reconstruct input $X$ by reversing noise injection.|
|**Early Training Focus**|High-frequency shortcuts & pixel-level correlations (Memorization).|Low-frequency global structures & data manifold layout (Generalization).|
|**Late Training Focus**|Smoothing decision boundaries to capture invariant semantics (Generalization).|High-frequency details, exact textures, and sample specificities (Memorization).|
|**Spectral Bias**|Biased toward fitting sharp, high-frequency functions first.|Explicitly forced by noise scheduling to fit low-frequency functions first.|

Essentially, a classifier tries to discard as much of the image as possible to find the label, accidentally memorizing the easiest pixel patterns first. A diffusion model is forced to rebuild the universe from a cloud of dust; it has no choice but to learn the layout of that universe before it can paint the individual grains of sand.
