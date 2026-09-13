---
title: "IVP Lectures 38-49"
lastmod: 2026-09-07
---

# Digital Image Processing — Lectures 38–49
## Detailed Speedrun Notes — Obsidian Version

> **Course:** NPTEL Digital Image Processing, IIT Kharagpur  
> **Instructor:** Prof. Prabir Kumar Biswas  
> **Coverage:** Lectures 38–49  
>
> The official NPTEL sequence places L38–40 under mask-processing enhancement, L41 under frequency-domain processing, L42–47 under image restoration, and L48–49 under image registration. citeturn2search2

---

# 0. Big Picture

This block moves from **enhancement** to **restoration** and then to **registration**:

1. **L38–40:** spatial/mask processing — improve an image using local neighborhoods.
2. **L41:** frequency-domain enhancement — manipulate Fourier coefficients instead of pixels directly.
3. **L42–47:** restoration — explicitly model degradation and invert/estimate the degradation.
4. **L48–49:** registration — geometrically align two images acquired from different viewpoints, times, sensors, etc.

The key distinction is:

- **Enhancement:** "Make the image look/usefully better." The desired result is often subjective or application-dependent.
- **Restoration:** "Estimate the original image from a mathematically modeled degradation process."
- **Registration:** "Find the geometric transformation that makes two images correspond."

---

# 1. L38–40 — Image Enhancement: Mask Processing Techniques

## 1.1 The central idea

Point processing from L32–37 changed a pixel using only its own intensity:

$$
g(x,y)=T[f(x,y)].
$$

Mask processing instead uses a **local neighborhood** around $(x,y)$:

$$
g(x,y)=T\left(\{f(x+i,y+j)\}\right).
$$

A small matrix of coefficients is called a **mask**, **kernel**, or **filter**.

For a $3\times3$ mask,

$$
w=
\begin{bmatrix}
w_{-1,-1} & w_{-1,0} & w_{-1,1}\\
w_{0,-1} & w_{0,0} & w_{0,1}\\
w_{1,-1} & w_{1,0} & w_{1,1}
\end{bmatrix},
$$

the linear filtered output is

$$
g(x,y)=
\sum_{i=-1}^{1}\sum_{j=-1}^{1}
w_{i,j}f(x-i,y-j).
$$

Depending on the convention, the operation may be described as **correlation** or **convolution**. In convolution the mask is flipped before applying it; in correlation it is not.

### Why use masks?

A pixel by itself tells us only local intensity. A neighborhood tells us about:

- smooth regions,
- local averages,
- edges,
- noise,
- local contrast,
- directional structure.

Thus mask processing is the basic mechanism behind many spatial filters.

---

## 1.2 L38 — Smoothing / low-pass spatial filtering

### Mean filter

The simplest smoothing mask is

$$
w=\frac{1}{9}
\begin{bmatrix}
1&1&1\\
1&1&1\\
1&1&1
\end{bmatrix}.
$$

Then

$$
g(x,y)=\frac{1}{9}
\sum_{i=-1}^{1}\sum_{j=-1}^{1}f(x+i,y+j).
$$

It replaces each pixel by the local average.

### Effect

- suppresses random fluctuations,
- reduces high-frequency detail,
- smooths edges,
- can reduce noise,
- but can also blur important boundaries.

The larger the mask, the stronger the smoothing but generally the greater the loss of detail.

---

## 1.3 Weighted averaging / Gaussian-like smoothing

Instead of giving every neighbor equal importance, assign larger weights near the center.

A typical $3\times3$ mask is

$$
\frac{1}{16}
\begin{bmatrix}
1&2&1\\
2&4&2\\
1&2&1
\end{bmatrix}.
$$

The weights sum to $1$, so a constant image remains constant.

This is conceptually closer to Gaussian smoothing: nearby pixels contribute more strongly than distant pixels.

### Important property

For smoothing masks, normalization is usually chosen so that

$$
\sum_{i,j}w_{i,j}=1.
$$

Otherwise the overall brightness can be changed.

---

## 1.4 Median filtering

Median filtering is **nonlinear**.

For every neighborhood:

1. collect all pixel values,
2. sort them,
3. replace the center pixel by the median.

For a $3\times3$ neighborhood there are $9$ values, and the fifth value after sorting is the output.

### Why median filtering is useful

It is especially effective against **salt-and-pepper noise** because isolated extreme values do not strongly influence the median.

Example:

$$
[10,10,11,10,255,9,11,10,10]
$$

The value $255$ is an impulse. The median remains around $10$.

By contrast, the mean would be pulled upward substantially.

### Mean vs median

| Filter | Linear? | Good for | Main problem |
|---|---|---|---|
| Mean | Yes | Gaussian-like/random noise | Blurs edges |
| Median | No | Salt-and-pepper noise | Can remove fine structures |

---

## 1.5 L39 — Sharpening through spatial masks

Smoothing suppresses rapid intensity changes. Sharpening does the opposite: it emphasizes high-frequency components such as edges and fine detail.

The fundamental idea is:

$$
\text{Sharpened image}
=
\text{Original image}
+
\text{High-frequency component}.
$$

A common route is the Laplacian.

### Laplacian operator

For a continuous image,

$$
\nabla^2f=
\frac{\partial^2f}{\partial x^2}
+
\frac{\partial^2f}{\partial y^2}.
$$

A common discrete 4-neighbor approximation is

$$
\nabla^2f(x,y)
=
f(x+1,y)+f(x-1,y)+f(x,y+1)+f(x,y-1)-4f(x,y).
$$

Corresponding mask:

$$
\begin{bmatrix}
0&1&0\\
1&-4&1\\
0&1&0
\end{bmatrix}.
$$

Another 8-neighbor version is

$$
\begin{bmatrix}
1&1&1\\
1&-8&1\\
1&1&1
\end{bmatrix}.
$$

The sign convention may be reversed depending on the chosen mask.

### Sharpening from the Laplacian

One common formulation is

$$
g=f-\nabla^2f.
$$

If the opposite Laplacian convention is used, the corresponding formula becomes

$$
g=f+\nabla^2f.
$$

The essential idea is unchanged: add an appropriately signed second-derivative response to emphasize rapid transitions.

---

## 1.6 Unsharp masking

A second important sharpening idea is **unsharp masking**.

First blur the image:

$$
f_{\text{blur}}=f*h.
$$

Then form the detail/high-frequency component:

$$
m=f-f_{\text{blur}}.
$$

Finally sharpen:

$$
g=f+k\,m.
$$

Equivalently,

$$
g=(1+k)f-kf_{\text{blur}}.
$$

For $k=1$,

$$
g=2f-f_{\text{blur}}.
$$

This is called unsharp masking because the blurred version is subtracted from the original.

### High-boost filtering

If the original image is multiplied more strongly,

$$
g=A f-f_{\text{blur}},
$$

with $A>1$, the method is called **high-boost filtering**.

Using

$$
A=1+k
$$

connects the two formulations.

---

## 1.7 First derivative vs second derivative

This distinction is worth remembering.

### First derivative

Edges correspond to large changes in intensity, so the gradient is useful:

$$
\nabla f=
\begin{bmatrix}
\frac{\partial f}{\partial x}\\
\frac{\partial f}{\partial y}
\end{bmatrix}.
$$

Magnitude:

$$
|\nabla f|
=
\sqrt{
\left(\frac{\partial f}{\partial x}\right)^2+
\left(\frac{\partial f}{\partial y}\right)^2
}.
$$

Approximation:

$$
|\nabla f|
\approx
|G_x|+|G_y|.
$$

### Second derivative

The Laplacian detects rapid changes and is often used for sharpening:

$$
\nabla^2f=f_{xx}+f_{yy}.
$$

---

## 1.8 Gradient masks

Typical masks for approximating derivatives include Roberts, Prewitt, and Sobel operators.

### Prewitt

Horizontal:

$$
G_x=
\begin{bmatrix}
-1&0&1\\
-1&0&1\\
-1&0&1
\end{bmatrix}.
$$

Vertical:

$$
G_y=
\begin{bmatrix}
-1&-1&-1\\
0&0&0\\
1&1&1
\end{bmatrix}.
$$

### Sobel

Horizontal:

$$
G_x=
\begin{bmatrix}
-1&0&1\\
-2&0&2\\
-1&0&1
\end{bmatrix}.
$$

Vertical:

$$
G_y=
\begin{bmatrix}
-1&-2&-1\\
0&0&0\\
1&2&1
\end{bmatrix}.
$$

Sobel gives extra weight to the center row/column, making it somewhat less sensitive to noise than the simplest derivative masks.

---

## 1.9 L40 — Combining enhancement operations

Mask processing is not restricted to one filter.

A typical pipeline can be:

$$
\text{noisy image}
\rightarrow
\text{smoothing}
\rightarrow
\text{edge/sharpening operation}
\rightarrow
\text{enhanced image}.
$$

The order matters.

For example, applying a derivative directly to a heavily noisy image can amplify noise because differentiation emphasizes high frequencies. A common strategy is therefore:

$$
\text{smooth first}
\rightarrow
\text{differentiate/sharpen}.
$$

This leads naturally toward frequency-domain processing in L41.

---

# 2. L41 — Frequency Domain Processing Techniques

## 2.1 Why move to the frequency domain?

Spatial filtering manipulates neighborhoods directly.

Frequency-domain filtering instead transforms the image into its Fourier representation:

$$
F(u,v)=\mathcal{F}\{f(x,y)\}.
$$

Then modify the spectrum using a transfer function $H(u,v)$:

$$
G(u,v)=H(u,v)F(u,v).
$$

Finally,

$$
g(x,y)=\mathcal{F}^{-1}\{G(u,v)\}.
$$

This is the central frequency-domain filtering equation.

---

## 2.2 Low-pass filtering

Low frequencies correspond broadly to slowly varying intensity structures. High frequencies correspond to rapid changes such as edges, fine details, and much noise.

A low-pass filter preserves low frequencies and suppresses high frequencies:

$$
H(u,v)\approx1
\quad\text{near the origin},
$$

and

$$
H(u,v)\approx0
\quad\text{far from the origin}.
$$

Effect:

- smoothing,
- noise reduction,
- loss of sharp edges/details.

---

## 2.3 High-pass filtering

A high-pass filter does the opposite:

$$
H(u,v)\approx0
\quad\text{near the origin},
$$

and

$$
H(u,v)\approx1
\quad\text{for high frequencies}.
$$

Effect:

- edge enhancement,
- detail extraction,
- removal of slowly varying background.

A high-pass result often needs to be combined with the original image to obtain a visually useful sharpened image.

---

## 2.4 Ideal low-pass filter

Let

$$
D(u,v)=
\sqrt{(u-u_0)^2+(v-v_0)^2}
$$

be the distance from the frequency origin.

The ideal low-pass filter is

$$
H(u,v)=
\begin{cases}
1,&D(u,v)\le D_0,\\
0,&D(u,v)>D_0.
\end{cases}
$$

Its abrupt cutoff creates ringing artifacts in the spatial domain.

---

## 2.5 Butterworth low-pass filter

A smoother transition is obtained with the Butterworth filter:

$$
H(u,v)=
\frac{1}
{1+\left[\frac{D(u,v)}{D_0}\right]^{2n}}.
$$

Here:

- $D_0$ = cutoff frequency,
- $n$ = filter order.

As $n$ increases, the transition becomes sharper.

The Butterworth filter gives a compromise between the abrupt ideal filter and a very smooth Gaussian filter.

---

## 2.6 Gaussian low-pass filter

A Gaussian low-pass filter has the form

$$
H(u,v)=
e^{-D^2(u,v)/(2D_0^2)}.
$$

It has a smooth spectral roll-off and avoids the strong ringing associated with a sharp ideal cutoff.

---

## 2.7 Corresponding high-pass filters

A simple way to construct a high-pass filter from a low-pass filter is

$$
H_{HP}(u,v)=1-H_{LP}(u,v).
$$

Thus:

- ideal HP = complement of ideal LP,
- Butterworth HP = complement of Butterworth LP,
- Gaussian HP = complement of Gaussian LP.

---

## 2.8 Frequency-domain sharpening

High-pass filtering can isolate detail:

$$
f_{HP}=\mathcal{F}^{-1}\{H_{HP}F\}.
$$

Then sharpen using

$$
g=f+kf_{HP}.
$$

This is the frequency-domain analogue of adding a high-frequency component in spatial filtering.

---

# 3. L42–43 — Image Restoration: The Degradation Model

## 3.1 Enhancement vs restoration

Restoration starts from an explicit model of how the image was degraded.

The standard model is

$$
g(x,y)=h(x,y)*f(x,y)+\eta(x,y),
$$

where:

- $f(x,y)$ = original image,
- $h(x,y)$ = degradation/blur function,
- $*$ = convolution,
- $\eta(x,y)$ = additive noise,
- $g(x,y)$ = observed degraded image.

In the frequency domain:

$$
G(u,v)=H(u,v)F(u,v)+N(u,v).
$$

This equation is the foundation of classical image restoration.

---

## 3.2 What can cause degradation?

Examples include:

- defocus,
- motion blur,
- atmospheric turbulence,
- optical limitations,
- sensor noise,
- transmission noise,
- acquisition errors.

The restoration problem is to estimate $F$ from $G$.

---

## 3.3 Inverse filtering

Ignoring noise for the moment,

$$
G=HF.
$$

Therefore,

$$
\hat F=\frac{G}{H}.
$$

In spatial-frequency notation,

$$
\hat F(u,v)
=
\frac{G(u,v)}{H(u,v)}.
$$

This is the **inverse filter**.

### Why inverse filtering fails with noise

With noise,

$$
G=HF+N.
$$

Then

$$
\hat F
=
\frac{G}{H}
=
F+\frac{N}{H}.
$$

If $H$ is very small at some frequencies, then

$$
\left|\frac{N}{H}\right|
$$

can become extremely large.

Thus inverse filtering can massively amplify noise.

This is the key reason we need more sophisticated restoration methods.

---

## 3.4 Noise models

Common noise models include:

### Gaussian noise

A Gaussian random variable has density

$$
p(z)=
\frac{1}{\sqrt{2\pi}\sigma}
e^{-(z-\mu)^2/(2\sigma^2)}.
$$

It is often used as a model for electronic/sensor noise.

### Salt-and-pepper noise

The image contains pixels with unusually low or high intensities.

It is impulsive and is often better handled by nonlinear spatial methods such as the median filter.

### Poisson noise

Common in photon-limited imaging. The variance depends on the signal level.

---

## 3.5 Mean and variance for restoration

For additive noise,

$$
g=f+\eta,
$$

if the noise has

$$
E[\eta]=0,
$$

then

$$
E[g]=f.
$$

Thus averaging independent observations can reduce the effect of noise.

For independent zero-mean noise samples with variance $\sigma^2$, averaging $K$ observations gives variance

$$
\frac{\sigma^2}{K}.
$$

Hence repeated measurements can improve SNR.

---

# 4. L44–45 — Estimation of the Degradation Model and Restoration

## 4.1 The central problem

Restoration requires knowledge of $H(u,v)$ and the noise statistics.

In practice, the degradation function may not be known exactly.

Therefore we may need to **estimate the degradation model** from:

1. calibration/experimental information,
2. the observed image itself,
3. assumptions about the imaging system.

---

## 4.2 Estimating blur from known patterns

A practical strategy is to image a known object containing sharp features.

If the original pattern $f$ is known and the observed image is $g$, then

$$
G=HF+N.
$$

Ignoring noise,

$$
H\approx\frac{G}{F}.
$$

Thus a known calibration target can reveal the system's frequency response.

---

## 4.3 Motion blur

Motion during exposure produces directional blur.

A simplified degradation model can be represented by a point-spread function describing the path traveled by the image during exposure.

The corresponding $H(u,v)$ contains characteristic zeros/low-response regions. These are dangerous for inverse filtering because dividing by small values amplifies noise.

The restoration problem therefore becomes a balance:

- recover lost high-frequency information,
- avoid excessive noise amplification.

---

## 4.4 Wiener filtering

The Wiener filter explicitly considers both degradation and noise.

A standard form is

$$
\hat F(u,v)
=
\left[
\frac{H^*(u,v)}
{|H(u,v)|^2+\frac{S_N(u,v)}{S_F(u,v)}}
\right]
G(u,v),
$$

where:

- $H^*$ is the complex conjugate of $H$,
- $S_N$ is the noise power spectral density,
- $S_F$ is the original-image power spectral density.

The term

$$
\frac{S_N}{S_F}
$$

controls how aggressively the filter avoids noise amplification.

### Interpretation

If noise is negligible,

$$
\frac{S_N}{S_F}\rightarrow0,
$$

and the Wiener filter approaches inverse filtering:

$$
\hat F\approx\frac{G}{H}.
$$

If noise is significant, the denominator prevents division by very small $H$ from becoming catastrophic.

---

## 4.5 Minimum mean-square-error viewpoint

The Wiener filter is associated with minimizing mean-square restoration error:

$$
E\left\{|F-\hat F|^2\right\}.
$$

The idea is not to recover the mathematically exact inverse at every frequency. Instead, it finds the estimate that gives the best average squared error under the assumed statistical model.

This is why restoration is fundamentally different from simply "undoing blur."

---

# 5. L46–47 — Other Restoration Techniques

## 5.1 Constrained least squares restoration

Another approach is to solve a regularized optimization problem.

A typical objective is

$$
\hat f
=
\arg\min_f
\left\{
\|g-Hf\|^2
+
\gamma\|Cf\|^2
\right\}.
$$

Interpretation:

- first term: fit the observed degraded image,
- second term: penalize undesirable/unstable solutions,
- $\gamma$: regularization parameter,
- $C$: regularization operator.

The second term encodes a prior preference, often for smoothness.

---

## 5.2 Why regularization is needed

The direct inverse problem may be ill-conditioned.

If some frequencies satisfy

$$
|H(u,v)|\approx0,
$$

then many candidate original images can produce nearly the same observation.

Regularization prevents the solution from exploding in those unstable directions.

This is the broader principle:

$$
\text{data fidelity}
+
\text{prior/regularization}.
$$

---

## 5.3 Constrained least-squares solution

In matrix notation, let

$$
g=Hf+n.
$$

Consider

$$
J(f)=
(g-Hf)^T(g-Hf)
+
\gamma(Cf)^T(Cf).
$$

Setting the derivative to zero gives

$$
H^T(Hf-g)+\gamma C^TCf=0.
$$

Therefore,

$$
(H^TH+\gamma C^TC)\hat f=H^Tg.
$$

Hence,

$$
\boxed{
\hat f=
(H^TH+\gamma C^TC)^{-1}H^Tg
}
$$

when the inverse exists.

This is the core regularized restoration formula.

---

## 5.4 Geometric/iterative viewpoint

Restoration can also be formulated as an iterative optimization problem.

The recurring structure is:

1. start with an initial estimate,
2. compare its degraded version with the observed image,
3. compute an error/residual,
4. update the estimate,
5. repeat until the restoration criterion is satisfied.

This viewpoint is important because many modern inverse problems follow exactly this template, even when the model is no longer a simple convolution.

---

## 5.5 Direct comparison of classical restoration methods

| Method | Uses degradation model? | Uses noise/statistics? | Main idea |
|---|---:|---:|---|
| Inverse filter | Yes | Weakly/no | Direct inversion |
| Wiener filter | Yes | Yes | MMSE/statistical compromise |
| Constrained least squares | Yes | Indirectly | Data fit + regularization |
| Median filter | No explicit blur model | No | Nonlinear local denoising |

The first three are **restoration** methods. Median filtering is primarily an **enhancement/denoising** technique.

---

# 6. L48–49 — Image Registration

## 6.1 What is registration?

Suppose we have two images of the same scene:

- reference image $I_R$,
- sensed/moving image $I_S$.

They may differ because of:

- camera position,
- scale,
- rotation,
- translation,
- viewpoint,
- acquisition time,
- sensor type.

Registration finds a transformation $T$ such that

$$
I_S(T(x,y))
\approx
I_R(x,y).
$$

In words: find the geometric transformation that aligns corresponding structures.

---

## 6.2 Why registration is important

Applications include:

- medical image fusion,
- satellite-image comparison,
- multi-temporal remote sensing,
- panorama construction,
- change detection,
- multi-sensor fusion,
- object tracking,
- image mosaicing.

---

## 6.3 Transformation models

### Translation

$$
x'=x+t_x,\qquad
y'=y+t_y.
$$

Only position changes.

### Rotation

About the origin:

$$
\begin{bmatrix}
x'\\
y'
\end{bmatrix}
=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}.
$$

### Scaling

$$
x'=s_xx,\qquad y'=s_yy.
$$

### Affine transformation

Combines translation, rotation, scaling, shear:

$$
\begin{bmatrix}
x'\\
y'
\end{bmatrix}
=
\begin{bmatrix}
a&b\\
c&d
\end{bmatrix}
\begin{bmatrix}
x\\
y
\end{bmatrix}
+
\begin{bmatrix}
t_x\\
t_y
\end{bmatrix}.
$$

In homogeneous coordinates:

$$
\begin{bmatrix}
x'\\
y'\\
1
\end{bmatrix}
=
\begin{bmatrix}
a&b&t_x\\
c&d&t_y\\
0&0&1
\end{bmatrix}
\begin{bmatrix}
x\\
y\\
1
\end{bmatrix}.
$$

### Projective transformation / homography

For planar scenes or perspective changes,

$$
\begin{bmatrix}
x'\\
y'\\
w'
\end{bmatrix}
=
H
\begin{bmatrix}
x\\
y\\
1
\end{bmatrix}.
$$

After homogeneous normalization,

$$
x_{\text{image}}=\frac{x'}{w'},
\qquad
y_{\text{image}}=\frac{y'}{w'}.
$$

The choice of model is crucial: using a transformation that is too simple cannot align the images; one that is unnecessarily flexible may overfit.

---

## 6.4 Registration pipeline

A useful conceptual pipeline is:

$$
\boxed{
\text{Feature detection}
\rightarrow
\text{Feature correspondence}
\rightarrow
\text{Transformation estimation}
\rightarrow
\text{Image warping}
\rightarrow
\text{Verification}
}
$$

### Step 1 — Detect corresponding structures

Possible features:

- corners,
- edges,
- blobs,
- distinctive local patterns.

### Step 2 — Establish correspondences

Find pairs

$$
p_i\leftrightarrow q_i
$$

that are believed to represent the same physical point.

### Step 3 — Estimate transformation

Find parameters $\theta$ minimizing a correspondence error such as

$$
E(\theta)
=
\sum_i
\|q_i-T_\theta(p_i)\|^2.
$$

### Step 4 — Warp the sensed image

Apply the estimated transformation.

### Step 5 — Verify

Check whether structures, edges, or intensities now agree.

---

## 6.5 Intensity-based registration

Instead of explicitly matching features, optimize an image similarity measure.

For example, one can minimize

$$
E(T)=
\sum_{x,y}
\left[
I_R(x,y)-I_S(T(x,y))
\right]^2.
$$

This is appropriate when corresponding images have sufficiently similar intensities.

For multi-modal images, intensity values may not correspond directly. Measures such as correlation or mutual information can be more appropriate.

---

## 6.6 Geometric transformation vs intensity interpolation

Registration requires two separate ideas:

1. **Estimate the geometric mapping.**
2. **Resample the image after mapping.**

The second step uses interpolation methods from L16–19.

For example, after transforming coordinates, the requested location may fall between pixels. Then use:

- nearest-neighbor interpolation,
- bilinear interpolation,
- higher-order interpolation.

So the earlier interpolation lectures are directly reused here.

---

# 7. How L38–49 Fit Together

The conceptual progression is:

### L38–40: Spatial enhancement

Work directly on local neighborhoods:

$$
g=\text{spatial filter}(f).
$$

Goal: improve appearance or emphasize useful structures.

### L41: Frequency enhancement

Transform:

$$
f
\rightarrow F
\rightarrow H F
\rightarrow g.
$$

Goal: manipulate low/high-frequency components.

### L42–47: Restoration

Model the acquisition process:

$$
g=Hf+n.
$$

Then estimate $f$ using:

- inverse filtering,
- Wiener filtering,
- regularized/constrained least squares,
- other model-based approaches.

Goal: recover the likely original image.

### L48–49: Registration

Model geometric mismatch:

$$
q\approx T(p).
$$

Estimate $T$, warp one image, and align it with the reference.

---

# 8. Essential Equations

## Spatial mask

$$
g(x,y)=
\sum_{i,j}w(i,j)f(x-i,y-j).
$$

## Mean filter

$$
g(x,y)=
\frac{1}{mn}
\sum_{i,j}f(x-i,y-j).
$$

## Laplacian

$$
\nabla^2f=f_{xx}+f_{yy}.
$$

## Unsharp masking

$$
m=f-f_{\text{blur}},
\qquad
g=f+km.
$$

## High-boost filtering

$$
g=Af-f_{\text{blur}}.
$$

## Frequency filtering

$$
G(u,v)=H(u,v)F(u,v).
$$

## Gaussian LPF

$$
H(u,v)=e^{-D^2(u,v)/(2D_0^2)}.
$$

## Degradation model

$$
g=h*f+\eta.
$$

## Frequency-domain degradation

$$
G=HF+N.
$$

## Inverse filter

$$
\hat F=\frac{G}{H}.
$$

## Wiener filter

$$
\hat F=
\frac{H^*}
{|H|^2+S_N/S_F}G.
$$

## Regularized least squares

$$
\hat f=
(H^TH+\gamma C^TC)^{-1}H^Tg.
$$

## Affine registration

$$
\begin{bmatrix}
x'\\y'\\1
\end{bmatrix}
=
\begin{bmatrix}
a&b&t_x\\
c&d&t_y\\
0&0&1
\end{bmatrix}
\begin{bmatrix}
x\\y\\1
\end{bmatrix}.
$$

## Registration objective

$$
E(\theta)=
\sum_i\|q_i-T_\theta(p_i)\|^2.
$$

---

# 9. What to Remember for Exams / Speedrunning

- **Mask processing = local neighborhood processing.**
- Mean/weighted averaging smooths but blurs edges.
- Median filtering is nonlinear and is particularly useful for impulse noise.
- **Gradient/first derivative → edge detection.**
- **Laplacian/second derivative → sharpening.**
- Unsharp masking = original minus blurred image, then add the detail back.
- High-boost filtering is a stronger/generalized unsharp-mask formulation.
- **Low-pass → smoothing.**
- **High-pass → detail/edge emphasis.**
- Ideal frequency filters have abrupt transitions and can cause ringing.
- Butterworth gives a controllable transition.
- Gaussian gives a very smooth transition.
- Restoration starts from a **degradation model**, not merely a visual preference.
- Core model:

$$
g=h*f+\eta.
$$

- Inverse filtering is unstable when $H$ is small.
- Wiener filtering trades inverse recovery against noise amplification using statistical information.
- Constrained least squares adds a regularization/prior term.
- Registration estimates a **geometric transformation**, not merely a denoising filter.
- Registration can use features or direct intensity-based similarity.
- After geometric mapping, interpolation is needed to obtain pixel values at non-grid locations.

---

# 10. Lecture-by-Lecture Coverage Checklist

- [x] **L38 — Image Enhancement: Mask Processing Techniques - I**
  - Local masks, linear spatial filtering, smoothing, averaging, weighted masks.
- [x] **L39 — Image Enhancement: Mask Processing Techniques - II**
  - Sharpening, Laplacian, gradient/derivative masks, unsharp masking.
- [x] **L40 — Image Enhancement: Mask Processing Techniques - III**
  - Combined spatial enhancement, high-boost filtering, practical filter behavior.
- [x] **L41 — Frequency Domain Processing Techniques**
  - Fourier-domain filtering, LPF/HPF, ideal/Butterworth/Gaussian filters.
- [x] **L42 — Image Restoration Techniques - I**
  - Degradation model, blur + noise, inverse restoration.
- [x] **L43 — Image Restoration Techniques - II**
  - Noise models, inverse-filter instability, statistical restoration motivation.
- [x] **L44 — Estimation of Degradation Model and Restoration Techniques - I**
  - Degradation-model estimation, calibration, blur estimation.
- [x] **L45 — Estimation of Degradation Model and Restoration Techniques - II**
  - Wiener restoration and MMSE interpretation.
- [x] **L46 — Other Restoration Techniques - I**
  - Regularized/constrained least-squares restoration.
- [x] **L47 — Other Restoration Techniques - II**
  - Regularization, iterative/inverse-problem viewpoint, method comparison.
- [x] **L48 — Image Registration - I**
  - Registration problem, geometric transformations, correspondences.
- [x] **L49 — Image Registration - II**
  - Registration pipeline, transformation estimation, warping/resampling, similarity-based registration.

---

# 11. Final Mental Model

If you see an image-processing problem, ask:

**1. Do I merely want to improve the image?**

Use enhancement.

- Pixel-wise → point processing.
- Neighborhood-wise → spatial masks.
- Frequency-wise → Fourier filtering.

**2. Do I know how the image became degraded?**

Use restoration.

$$
g=Hf+n.
$$

Then choose inverse, Wiener, or regularized restoration.

**3. Do I have two images that should depict the same scene but don't line up?**

Use registration.

$$
q\approx T(p).
$$

Estimate $T$, warp, interpolate, and verify alignment.

That is the conceptual bridge from L38 through L49.
