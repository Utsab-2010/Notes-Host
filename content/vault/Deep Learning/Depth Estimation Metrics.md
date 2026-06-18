---
title: "Depth Estimation Metrics"
---

To evaluate the accuracy of the predicted depth maps against the "ground truth" (the actual measured distance), the **InfiniDepth** paper utilizes a standard set of error and accuracy metrics common in monocular depth estimation research.

These metrics compare the predicted depth $d$ with the ground-truth depth $d^*$ for $N$ total pixels.

### 1. Error Metrics (Lower is Better)

These metrics quantify the average distance or deviation between the prediction and the truth.
- **Absolute Relative Error (Abs Rel):**
    Calculates the average percentage error relative to the ground truth depth.$$\text{Abs Rel} = \frac{1}{N} \sum \frac{|d - d^*|}{d^*}$$
- **Squared Relative Error (Sq Rel):**
    Similar to Abs Rel but squares the error term to penalize larger outliers more heavily.
    $$\text{Sq Rel} = \frac{1}{N} \sum \frac{\|d - d^*\|^2}{d^*}$$
    
- **Root Mean Squared Error (RMSE):**
    
    Measures the average magnitude of the error in the same units as the depth (e.g., meters). It is very sensitive to large errors.
    
    $$\text{RMSE} = \sqrt{\frac{1}{N} \sum (d - d^*)^2}$$
    
- **RMSE log:**
    
    Calculates the RMSE in log space, which helps account for the fact that depth errors naturally increase as objects get farther away.
    
    $$\text{RMSE log} = \sqrt{\frac{1}{N} \sum (\log d - \log d^*)^2}$$
    

---

### 2. Accuracy Metrics (Higher is Better)

These metrics, often denoted as **$\delta < 1.25^n$**, measure the percentage of pixels where the ratio of the predicted depth to the ground truth (or vice versa) is within a certain threshold.

The threshold is defined as:

$$\max \left( \frac{d}{d^*}, \frac{d^*}{d} \right) = \delta < 1.25^n$$

The paper typically reports three levels of strictness:

- **$\delta_1$**: Threshold is $1.25$
    
- **$\delta_2$**: Threshold is $1.25^2 = 1.5625$
    
- **$\delta_3$**: Threshold is $1.25^3 \approx 1.95$
    

---

### 3. Log10 Error

This is the mean absolute error calculated using base-10 logarithms, providing a different perspective on the scale-invariant accuracy of the model.

$$\text{Log10} = \frac{1}{N} \sum |\log_{10} d - \log_{10} d^*|$$

### 4. Why these matter for InfiniDepth

Because InfiniDepth focuses on **fine-grained geometry**, the authors look closely at how these metrics behave at high resolutions. Standard metrics can sometimes "hide" errors in thin structures (like a power line) because those structures only occupy a few pixels. By evaluating on their new **Synth4K** dataset, they demonstrate that their model maintains high $\delta_1$ accuracy even when rendering at 4K, where traditional models often see a significant performance drop.

Since you've worked with **Structure from Motion (SfM)**, you'll know that high RMSE can lead to "warped" 3D reconstructions, while poor $\delta_1$ accuracy usually results in "noisy" or "floating" artifacts in the point cloud.

