---
title: "IVP Lectures 16-37"
lastmod: 2026-09-07
---

# Digital Image Processing — Detailed Speedrun Notes
## Prof. P. K. Biswas, IIT Kharagpur
### Lectures 16–37

> **Purpose:** detailed notes for speedrunning the lectures later.  
> Closely related lectures are grouped into conceptual blocks, but every lecture is covered in sequence.

The official NPTEL course sequence for Lectures 16–37 is:

- 16 — Interpolation and Resampling
- 17 — Interpolation Techniques
- 18 — Interpolation with examples – I
- 19 — Interpolation with Examples – II
- 20 — Image Transformation – I
- 21 — Image Transformation – II
- 22 — Separable Transformation
- 23 — Basis Images
- 24 — Fourier Transformation
- 25 — Properties of FT
- 26 — FT Result Display – II
- 27 — Rotation Invariance Property
- 28 — DCT and Walsh Transform
- 29 — Hadamard Transformation
- 30 — Histogram Equalization and Specifications – I
- 31 — KL Transform – II
- 32 — Image Enhancement: Point Processing Techniques
- 33 — Contrast Stretching Operation
- 34 — Histogram Equalization and Specification – I
- 35 — Histogram Equalization and Specification – II
- 36 — Histogram Implementation – I
- 37 — Histogram Implementation – II

This sequence is confirmed by the current NPTEL course page and course mirrors. citeturn1search0turn1search3

---

# Part I — Interpolation and Resampling
## Lectures 16–19

The previous block established that an image is a sampled representation of a continuous
image. These lectures now ask:

> **What happens when we need image samples at locations where we did not originally sample?**

This is interpolation/resampling.

---

# Lecture 16 — Interpolation and Resampling

## 1. Why interpolation is needed

A digital image is defined only at discrete pixel locations:

$$
f[m,n].
$$

But many operations require values at **non-integer coordinates**.

Examples:

- zooming,
- shrinking,
- rotation,
- geometric warping,
- camera transformations,
- image registration.

Suppose a transformation says that an output pixel corresponds to:

$$
(x',y')=(12.4,\,31.7).
$$

There is no pixel stored exactly at that location.

We therefore need an estimate of the image intensity there.

That estimate is obtained through **interpolation**.

---

## 2. Resampling

Resampling means generating a new discrete set of samples from an existing sampled image.

Conceptually:

$$
\text{old sampling grid}
\rightarrow
\text{continuous/interpolated representation}
\rightarrow
\text{new sampling grid}.
$$

Interpolation supplies the missing values.

---

## 3. Enlargement and reduction

### Enlargement

When an image is enlarged, the new grid contains more pixel locations than the original.

Therefore many output locations do not correspond directly to old pixels.

Interpolation is required.

### Reduction

When an image is reduced, multiple original samples may contribute to a smaller number of
output samples.

This is more subtle because simply discarding pixels can cause aliasing.

Therefore resampling should ideally include appropriate low-pass filtering before decimation.

---

## 4. Forward vs inverse mapping

Suppose an image transformation is:

$$
\mathbf{x}'=T(\mathbf{x}).
$$

There are two ways to construct the output.

### Forward mapping

For every input pixel:

$$
\mathbf{x}\rightarrow\mathbf{x}'.
$$

Then place its value at the corresponding output location.

The problem is that output locations can be left empty, and several input pixels can map to the
same output location.

### Inverse mapping

For every output location:

$$
\mathbf{x}'\rightarrow\mathbf{x}=T^{-1}(\mathbf{x}').
$$

Then interpolate the input image at $\mathbf{x}$.

This is usually preferable because every output pixel gets a value.

---

## 5. Continuous interpretation

It is useful to think of the discrete image as samples of an underlying continuous function:

$$
f(x,y).
$$

Interpolation constructs an approximation:

$$
\hat f(x,y)
$$

from the known samples.

Then the new sample is:

$$
g[m,n]=\hat f(x_m,y_n).
$$

The quality of the result depends on how well the interpolation model approximates the
underlying image.

---

# Lecture 17 — Interpolation Techniques

The lecturer introduces practical interpolation methods.

---

## 1. Nearest-neighbor interpolation

The simplest method is to assign the value of the closest known pixel.

For an arbitrary location $(x,y)$:

$$
\hat f(x,y)=f[\operatorname{round}(x),\operatorname{round}(y)].
$$

### Advantages

- extremely simple,
- fast,
- no arithmetic beyond choosing a neighbor.

### Disadvantages

- blocky appearance when enlarging,
- discontinuities,
- poor approximation to smooth intensity variation.

---

## 2. Linear interpolation

For 1-D interpolation between two samples:

$$
f(x_1),\qquad f(x_2),
$$

a point between them is estimated using a weighted average:

$$
f(x)\approx
(1-\alpha)f(x_1)+\alpha f(x_2),
$$

where

$$
\alpha=\frac{x-x_1}{x_2-x_1}.
$$

The closer $x$ is to $x_1$, the larger the contribution from $f(x_1)$.

---

## 3. Bilinear interpolation

For an image, linear interpolation is applied in two dimensions.

Suppose the point lies inside a pixel rectangle with four neighboring values:

$$
f_{00},\quad f_{10},\quad f_{01},\quad f_{11}.
$$

First interpolate in one direction:

$$
f(x,y_0)
=
(1-\alpha)f_{00}+\alpha f_{10},
$$

$$
f(x,y_1)
=
(1-\alpha)f_{01}+\alpha f_{11}.
$$

Then interpolate between those two results:

$$
\hat f(x,y)
=
(1-\beta)f(x,y_0)
+
\beta f(x,y_1).
$$

Equivalently:

$$
\hat f(x,y)=
(1-\alpha)(1-\beta)f_{00}
+\alpha(1-\beta)f_{10}
+(1-\alpha)\beta f_{01}
+\alpha\beta f_{11}.
$$

The four neighboring pixels therefore contribute according to their spatial proximity.

---

## 4. Higher-order interpolation

The course also motivates more sophisticated interpolation schemes.

Instead of assuming intensity varies linearly between samples, a higher-order polynomial or
other interpolation kernel can be used.

The general tradeoff is:

```text
simple interpolation
    ↓
fast but less accurate

higher-order interpolation
    ↓
better approximation but more computation
```

---

# Lecture 18 — Interpolation with Examples – I

This lecture works through numerical/geometric examples of interpolation.

## 1. Coordinate mapping

A typical problem is:

1. specify an output pixel,
2. map it back to the corresponding input coordinate,
3. identify the neighboring input pixels,
4. calculate the interpolation weights,
5. calculate the output intensity.

The important skill is therefore not memorizing a formula alone.

You should be able to execute:

$$
\text{output coordinate}
\rightarrow
\text{input coordinate}
\rightarrow
\text{neighbors}
\rightarrow
\text{weights}
\rightarrow
\text{intensity}.
$$

---

## 2. Nearest-neighbor example logic

If an inverse-mapped coordinate is:

$$
(x,y)=(5.2,7.8),
$$

nearest-neighbor interpolation chooses the closest pixel location.

The fractional coordinates are simply discarded/rounded according to the selected convention.

---

## 3. Bilinear example logic

For:

$$
(x,y)=(5.2,7.8),
$$

the four surrounding pixels are at:

$$
(5,7),\;(6,7),\;(5,8),\;(6,8).
$$

The fractional coordinates determine the weights.

For:

$$
\alpha=0.2,\qquad\beta=0.8,
$$

the weights are:

$$
(1-\alpha)(1-\beta),
\quad
\alpha(1-\beta),
\quad
(1-\alpha)\beta,
\quad
\alpha\beta.
$$

They sum to one.

This is an important sanity check:

$$
\sum w_i=1.
$$

---

# Lecture 19 — Interpolation with Examples – II

The second example-oriented lecture continues interpolation/resampling and connects it to
geometric transformations.

## 1. Rotation + interpolation

A rotation usually maps an output pixel to a non-integer input coordinate.

Therefore rotation is naturally implemented as:

$$
\text{inverse rotation}
+
\text{interpolation}.
$$

For each output location:

$$
\begin{bmatrix}
x\\y
\end{bmatrix}
=
R^{-1}
\begin{bmatrix}
x'\\y'
\end{bmatrix}.
$$

The input value at $(x,y)$ is then interpolated.

---

## 2. Scaling + interpolation

Similarly, scaling by factors $s_x,s_y$ gives:

$$
x=\frac{x'}{s_x},
\qquad
y=\frac{y'}{s_y}.
$$

Again, the resulting coordinates are generally fractional.

---

## 3. Shrinking and aliasing

When the output sampling rate is lower than the input sampling rate, high-frequency image
content can alias.

Therefore reduction should conceptually be:

$$
\text{low-pass filtering}
\rightarrow
\text{decimation}.
$$

This is the image equivalent of the sampling-theorem discussion from Lectures 3–5.

---

## 4. Speedrun takeaway for Lectures 16–19

Know:

- why interpolation is required,
- forward vs inverse mapping,
- nearest-neighbor interpolation,
- linear interpolation,
- bilinear interpolation,
- coordinate mapping,
- why geometric transformations need interpolation,
- why downsampling needs anti-aliasing.

---

# Part II — Image Transformations
## Lectures 20–21

---

# Lecture 20 — Image Transformation – I

The course now moves from coordinate transformations to **image transforms**.

A transform represents the image in another mathematical coordinate system.

Instead of working directly with pixels, we can represent an image using transform coefficients.

---

## 1. General transform viewpoint

Let an image be represented as a vector:

$$
\mathbf f.
$$

A transform maps it to:

$$
\mathbf F=T\mathbf f.
$$

The inverse transform is:

$$
\mathbf f=T^{-1}\mathbf F.
$$

The transformed coefficients can provide a different representation of the same image.

---

## 2. Why transform images?

Different representations make different properties easier to see or manipulate.

For example:

- spatial representation → local pixel values,
- frequency representation → smooth vs rapidly varying content,
- transform coefficients → compact or structured representation.

Transforms are therefore useful for:

- filtering,
- compression,
- feature extraction,
- analysis.

---

## 3. Basis-vector viewpoint

If the transform is linear, the image can be represented as a weighted combination of basis
functions.

Conceptually:

$$
f(x,y)=
\sum_k c_k\phi_k(x,y).
$$

The coefficients $c_k$ tell us how much of each basis image is present.

This idea becomes explicit in Lecture 23.

---

# Lecture 21 — Image Transformation – II

The lecture continues the mathematical formulation of image transforms.

## 1. Orthogonal transforms

An important class is the orthogonal transform.

If the transformation matrix $T$ satisfies:

$$
T^TT=I,
$$

then:

$$
T^{-1}=T^T.
$$

This makes the inverse transform especially convenient.

---

## 2. Energy preservation

For an orthonormal transform, the total signal energy is preserved.

If:

$$
\mathbf F=T\mathbf f,
$$

then:

$$
\|\mathbf F\|^2=\|\mathbf f\|^2.
$$

Therefore:

$$
\sum_i |F_i|^2
=
\sum_i |f_i|^2.
$$

This is an important property for transforms used in image processing.

---

## 3. Transform-domain processing

Once an image is transformed:

$$
f
\rightarrow
F,
$$

we can modify $F$ and then transform back:

$$
F
\rightarrow
\hat F
\rightarrow
\hat f.
$$

This is the general pattern behind frequency-domain processing.

---

# Part III — Separable Transforms and Basis Images
## Lectures 22–23

---

# Lecture 22 — Separable Transformation

A 2-D transform can be computationally expensive if treated as one large operation.

A **separable transform** allows the 2-D transformation to be performed as two successive
1-D transformations.

---

## 1. Separable transform equation

For a separable transform:

$$
F(u,v)
=
\sum_x\sum_y
f(x,y)T_u(x)T_v(y).
$$

This can be evaluated as:

1. transform each row,
2. transform each column.

---

## 2. Matrix formulation

For an $N\times N$ image:

$$
\boxed{
F=T f T^T
}
$$

for the common orthogonal-transform convention.

The computation can be broken into:

$$
G=Tf
$$

followed by:

$$
F=GT^T.
$$

This reduces the conceptual problem from one 2-D operation to two sets of 1-D operations.

---

## 3. Why separability matters

The main benefit is computational efficiency.

A transform that would otherwise require a large number of 2-D operations can be implemented
using repeated 1-D operations.

This idea is used heavily for the DFT and DCT.

---

# Lecture 23 — Basis Images

The lecturer now gives a geometric interpretation of transform coefficients.

---

## 1. Basis image

A **basis image** is an image corresponding to one basis function of the transform.

An arbitrary image can be reconstructed as a weighted sum of these basis images:

$$
f(x,y)
=
\sum_u\sum_v
F(u,v)\phi_{u,v}(x,y).
$$

The transform coefficient:

$$
F(u,v)
$$

is the weight assigned to basis image $\phi_{u,v}$.

---

## 2. Low-frequency vs high-frequency basis images

For transforms such as the Fourier transform:

### Low-frequency basis functions

Change slowly across the image.

They represent:

- smooth intensity variation,
- large-scale structures.

### High-frequency basis functions

Change rapidly.

They represent:

- edges,
- fine texture,
- rapid intensity variation.

This interpretation is crucial for understanding frequency-domain image processing.

---

## 3. Transform coefficients as image information

The transform does not destroy information by itself.

It reorganizes the information.

Instead of:

```text
pixel values
```

we obtain:

```text
basis-image weights
```

This makes certain tasks easier.

---

# Part IV — Fourier Transform
## Lectures 24–27

---

# Lecture 24 — Fourier Transformation

The Fourier transform is introduced as the principal frequency-domain representation.

---

## 1. 1-D Fourier transform

For a continuous signal:

$$
F(u)=
\int_{-\infty}^{\infty}
f(x)e^{-j2\pi ux}\,dx.
$$

The inverse is:

$$
f(x)=
\int_{-\infty}^{\infty}
F(u)e^{j2\pi ux}\,du.
$$

For images, the variables become two-dimensional.

---

## 2. 2-D Fourier transform

The continuous 2-D transform is:

$$
F(u,v)
=
\int\int
f(x,y)
e^{-j2\pi(ux+vy)}
\,dx\,dy.
$$

The inverse is:

$$
f(x,y)
=
\int\int
F(u,v)
e^{j2\pi(ux+vy)}
\,du\,dv.
$$

For a digital image, the corresponding DFT is used.

---

## 3. 2-D DFT

For an $M\times N$ image:

$$
F(u,v)
=
\sum_{x=0}^{M-1}
\sum_{y=0}^{N-1}
f(x,y)
e^{-j2\pi
\left(
\frac{ux}{M}+
\frac{vy}{N}
\right)}.
$$

The inverse is:

$$
f(x,y)
=
\frac1{MN}
\sum_{u=0}^{M-1}
\sum_{v=0}^{N-1}
F(u,v)
e^{j2\pi
\left(
\frac{ux}{M}+
\frac{vy}{N}
\right)}.
$$

---

## 4. Spatial frequency

The Fourier transform tells us how strongly different spatial frequencies occur.

A slowly varying image produces strong low-frequency components.

Sharp transitions and fine texture produce stronger high-frequency components.

---

# Lecture 25 — Properties of the Fourier Transform

The lecturer develops properties that make Fourier-domain processing useful.

---

## 1. Linearity

If:

$$
g(x,y)=af(x,y)+bh(x,y),
$$

then:

$$
G(u,v)=aF(u,v)+bH(u,v).
$$

---

## 2. Translation property

A spatial shift produces a phase change in the Fourier domain.

If:

$$
g(x,y)=f(x-x_0,y-y_0),
$$

then:

$$
G(u,v)
=
F(u,v)
e^{-j2\pi(ux_0+vy_0)}.
$$

The magnitude is unchanged:

$$
|G(u,v)|=|F(u,v)|.
$$

This becomes important for rotation/translation invariance.

---

## 3. Convolution property

Spatial convolution corresponds to multiplication in the frequency domain:

$$
g=f*h
$$

implies:

$$
G=FH.
$$

This is one of the central reasons frequency-domain filtering is useful.

---

## 4. Multiplication property

Spatial multiplication corresponds to convolution in the frequency domain.

This gives the duality:

$$
\boxed{
\text{convolution in space}
\leftrightarrow
\text{multiplication in frequency}
}
$$

and:

$$
\boxed{
\text{multiplication in space}
\leftrightarrow
\text{convolution in frequency}.
}
$$

---

## 5. Separability

The 2-D Fourier transform is separable.

Therefore:

1. transform every row,
2. transform every column.

This greatly reduces implementation complexity.

---

# Lecture 26 — FT Result Display – II

The Fourier transform of an image is complex:

$$
F(u,v)=R(u,v)+jI(u,v).
$$

Therefore the result has:

### Magnitude

$$
|F(u,v)|
=
\sqrt{R^2(u,v)+I^2(u,v)}.
$$

### Phase

$$
\phi(u,v)
=
\tan^{-1}
\left(
\frac{I(u,v)}{R(u,v)}
\right).
$$

Both contain information about the image.

---

## 1. Why the spectrum is difficult to display

The dynamic range of the magnitude can be very large.

A few coefficients may have extremely large values while many others are small.

Direct display can therefore hide useful information.

---

## 2. Logarithmic display

A common display transformation is:

$$
D(u,v)=
c\log(1+|F(u,v)|).
$$

This compresses the dynamic range and makes weak spectral components visible.

---

## 3. Spectrum centering

The zero-frequency component is normally located at the origin of the DFT coordinate system.

For visualization, the spectrum is commonly shifted so that the DC component is at the center.

This produces the familiar centered Fourier spectrum.

---

## 4. Interpreting the displayed spectrum

Central region:

- low frequencies.

Farther from center:

- higher frequencies.

Thus:

```text
center → slowly varying image information
outer region → rapid spatial variation
```

---

# Lecture 27 — Rotation Invariance Property

The Fourier transform has a particularly important geometric property:

> **Rotation in the spatial domain produces the same rotation in the frequency domain.**

If:

$$
g(x,y)
$$

is a rotated version of:

$$
f(x,y),
$$

then its Fourier spectrum is rotated by the same angle.

---

## 1. Magnitude invariance to translation

Translation changes the phase but not the magnitude:

$$
|G(u,v)|=|F(u,v)|.
$$

Therefore the Fourier magnitude is **translation invariant**.

---

## 2. Rotation relationship

If the image is rotated by:

$$
\theta,
$$

the Fourier magnitude is also rotated by:

$$
\theta.
$$

Therefore rotation can be detected or normalized in the frequency domain.

---

## 3. Why this matters

This property is useful in:

- pattern recognition,
- image registration,
- object matching,
- invariant feature construction.

A transformed representation can therefore make geometric relationships easier to analyze.

---

# Part V — DCT, Walsh and Hadamard
## Lectures 28–29

---

# Lecture 28 — DCT and Walsh Transform

The Fourier transform uses complex exponentials.

Other transforms can represent an image using real-valued basis functions.

---

# 1. Discrete Cosine Transform

The DCT represents the image using cosine basis functions.

A common 2-D DCT form is:

$$
C(u,v)=
\alpha(u)\alpha(v)
\sum_x\sum_y
f(x,y)
\cos
\left[
\frac{(2x+1)u\pi}{2N}
\right]
\cos
\left[
\frac{(2y+1)v\pi}{2N}
\right].
$$

The normalization factor is:

$$
\alpha(0)=\frac1{\sqrt N},
\qquad
\alpha(k)=\sqrt{\frac2N}
\quad(k>0).
$$

---

## 2. DCT intuition

The DCT separates image information into different spatial frequencies.

Low-frequency coefficients usually contain a large portion of the image's energy.

High-frequency coefficients often contain finer detail.

This energy concentration is one reason DCT is useful for compression.

---

## 3. DCT vs DFT

DCT:

- real-valued basis,
- cosine functions,
- often excellent energy compaction.

DFT:

- complex-valued,
- sine/cosine through complex exponentials,
- natural for frequency analysis and filtering.

---

# 4. Walsh transform

The Walsh transform uses basis functions taking values such as:

$$
+1,\quad -1.
$$

The basis functions are square-wave-like rather than sinusoidal.

The transform therefore does not organize basis functions primarily by conventional sinusoidal
frequency.

Instead, they are often ordered by **sequency** — the number/rate of sign changes.

---

# Lecture 29 — Hadamard Transformation

The Hadamard transform is closely related to the Walsh transform.

---

## 1. Hadamard matrix

A Hadamard matrix has entries:

$$
+1,\quad -1
$$

and satisfies an orthogonality condition.

The basic recursive construction is:

$$
H_1=[1]
$$

and:

$$
H_{2N}
=
\begin{bmatrix}
H_N&H_N\\
H_N&-H_N
\end{bmatrix}.
$$

For example:

$$
H_2=
\begin{bmatrix}
1&1\\
1&-1
\end{bmatrix}.
$$

---

## 2. Orthogonality

The Hadamard matrix satisfies:

$$
H^TH=NI
$$

under the unnormalized convention.

A normalized version can be constructed by scaling.

---

## 3. Image transform

For a 2-D image:

$$
F=HfH^T.
$$

Because the transform uses only additions and subtractions, it can be computationally attractive.

---

## 4. Walsh vs Hadamard

The two are closely related.

The important distinction is generally the ordering of the same/similar binary basis functions.

For speedrunning, remember:

```text
Fourier → sinusoidal complex basis
DCT → cosine basis
Walsh → ±1 square-wave basis, sequency ordering
Hadamard → orthogonal ±1 matrix transform
```

---

# Part VI — Histogram and Statistical Image Representation
## Lectures 30–31

---

# Lecture 30 — Histogram Equalization and Specifications – I

The course now shifts from transform-domain representation to **image enhancement**.

The histogram is a basic statistical description of an image.

---

# 1. Image histogram

For a discrete image with gray levels:

$$
r_k,\qquad k=0,1,\ldots,L-1,
$$

the histogram is:

$$
h(r_k)=n_k,
$$

where $n_k$ is the number of pixels having gray level $r_k$.

---

## 2. Normalized histogram

If the image contains $MN$ pixels:

$$
p(r_k)=
\frac{n_k}{MN}.
$$

This is an empirical probability distribution of gray levels.

Therefore:

$$
\sum_{k=0}^{L-1}p(r_k)=1.
$$

---

# 3. What does the histogram tell us?

A histogram describes how frequently each intensity occurs.

It does **not** tell us where those pixels occur.

Two completely different images can have the same histogram.

Therefore:

> histogram is a statistical intensity description, not a spatial description.

---

# 4. Histogram-based enhancement

Suppose an image uses only a narrow portion of the available gray-level range.

The image may appear:

- dark,
- washed out,
- low contrast.

A transformation can redistribute the gray levels.

This motivates histogram equalization and histogram specification.

---

# 5. Histogram equalization

The basic objective is to transform the input intensity:

$$
r
\rightarrow
s
$$

so that the output intensities are distributed more uniformly.

For a continuous random variable, the transformation is:

$$
s=T(r)=
\int_0^r p_r(w)\,dw.
$$

Since this is the cumulative distribution function:

$$
F_r(r)=
\int_0^r p_r(w)\,dw,
$$

we have:

$$
s=F_r(r).
$$

If $r$ is continuous, $s$ is approximately uniformly distributed on $[0,1]$.

---

# Lecture 31 — KL Transform – II

The K-L transform (Karhunen–Loève transform), also called the **principal component transform**
in its sample/statistical form, is introduced as a data-dependent transform.

The key idea is:

> choose basis directions according to the covariance/statistics of the image data.

---

## 1. Data vectors

Treat image data as vectors:

$$
\mathbf x.
$$

The mean is:

$$
\boldsymbol\mu=E[\mathbf x].
$$

The covariance matrix is:

$$
C=
E[
(\mathbf x-\boldsymbol\mu)
(\mathbf x-\boldsymbol\mu)^T
].
$$

---

## 2. Eigenvectors

Find eigenvectors of:

$$
C.
$$

Let:

$$
C\mathbf e_i=\lambda_i\mathbf e_i.
$$

The eigenvectors form the transform basis.

---

## 3. Transform

After centering the data:

$$
\mathbf y=
E^T(\mathbf x-\boldsymbol\mu),
$$

where the columns of $E$ are the eigenvectors.

The inverse is:

$$
\mathbf x=
E\mathbf y+\boldsymbol\mu.
$$

---

## 4. Why K-L transform is useful

The eigenvectors are ordered according to eigenvalues.

A large eigenvalue means that direction contains a large amount of variance.

Therefore the first few transform components can often retain most of the signal information.

This gives **energy/information compaction**.

---

## 5. Relation to PCA

The K-L transform is closely related to what is commonly called:

$$
\boxed{\text{PCA}}
$$

in modern machine learning/statistics.

The important distinction from fixed transforms such as Fourier or DCT is:

```text
Fourier/DCT
→ fixed basis

K-L/PCA
→ basis learned from the data covariance.
```

---

# Part VII — Point Processing and Contrast
## Lectures 32–33

---

# Lecture 32 — Image Enhancement: Point Processing Techniques

Image enhancement aims to produce an image that is more suitable for a particular purpose.

The first class considered is **point processing**.

---

# 1. Point processing

The output pixel depends only on the corresponding input pixel:

$$
s=T(r).
$$

For an image:

$$
g(x,y)=T(f(x,y)).
$$

There is no dependence on neighboring pixels.

This makes point processing fundamentally different from mask/spatial filtering.

---

# 2. Image negative

A basic transformation is:

$$
s=L-1-r.
$$

This reverses the gray-level scale.

It is useful for:

- photographic negatives,
- highlighting bright structures in dark regions,
- certain medical images.

---

# 3. Log transformation

A logarithmic transformation has the form:

$$
s=c\log(1+r).
$$

It expands low-intensity values and compresses high-intensity values.

This is useful when the image contains a large dynamic range.

---

# 4. Power-law / gamma transformation

The general form is:

$$
s=cr^\gamma.
$$

The value of $\gamma$ controls the mapping.

### If $\gamma<1$

Dark intensities are expanded.

### If $\gamma>1$

Dark intensities are compressed and higher intensities are emphasized.

Gamma transformations are important in display and imaging systems.

---

# 5. Piecewise-linear transformations

A general piecewise-linear transformation uses selected control points:

$$
(r_1,s_1),\quad(r_2,s_2),\ldots
$$

and performs linear interpolation between them.

This lets us selectively enhance particular intensity ranges.

Applications include:

- contrast stretching,
- intensity-level slicing,
- thresholding.

---

# 6. Intensity-level slicing

The goal is to emphasize a particular range of gray levels.

For example:

$$
s=
\begin{cases}
L-1,&a\le r\le b\\
0,&\text{otherwise}
\end{cases}
$$

produces a binary-like highlighting of a selected range.

Another version preserves the background rather than suppressing it.

---

# 7. Bit-plane slicing

An $n$-bit image can be decomposed into binary images corresponding to each bit.

For pixel value:

$$
r=\sum_{k=0}^{n-1}b_k2^k,
$$

where:

$$
b_k\in\{0,1\}.
$$

The bit planes can be examined individually.

Higher-order bits generally carry more visually significant information than lower-order
bits, although lower-order planes can contain important fine detail/noise.

---

# Lecture 33 — Contrast Stretching Operation

Contrast stretching is a piecewise-linear point operation.

---

# 1. Low-contrast image

An image may occupy only a small intensity interval:

$$
r_{\min}\le r\le r_{\max}.
$$

The unused gray-level range is wasted.

Contrast stretching maps this narrow interval into a larger output range.

---

# 2. Basic linear contrast stretch

A simple mapping from:

$$
[r_{\min},r_{\max}]
$$

to:

$$
[s_{\min},s_{\max}]
$$

is:

$$
s=
s_{\min}
+
\frac{r-r_{\min}}
{r_{\max}-r_{\min}}
(s_{\max}-s_{\min}).
$$

This expands the dynamic range.

---

# 3. S-shaped / piecewise mappings

The lecturer considers more general piecewise-linear mappings.

The slope determines local contrast:

$$
\text{slope}>1
\Rightarrow
\text{contrast expansion}
$$

and:

$$
\text{slope}<1
\Rightarrow
\text{contrast compression}.
$$

Therefore the transformation can selectively emphasize desired intensity regions.

---

# 4. Thresholding as a limiting case

A very steep transition can approximate a threshold operation:

$$
s=
\begin{cases}
0,&r<T\\
L-1,&r\ge T.
\end{cases}
$$

Thus thresholding can be understood as another point transformation.

---

# Part VIII — Histogram Equalization and Specification
## Lectures 34–37

---

# Lecture 34 — Histogram Equalization and Specification – I

The course now develops histogram equalization in discrete form.

---

# 1. Continuous equalization idea

Start with:

$$
s=T(r)
=
\int_0^r p_r(w)\,dw.
$$

This is the cumulative distribution function.

Its derivative is:

$$
\frac{ds}{dr}=p_r(r).
$$

If $s=T(r)$ is monotonic, the transformed variable has approximately uniform density.

---

# 2. Discrete histogram equalization

For a digital image with $L$ levels:

$$
s_k=
(L-1)
\sum_{j=0}^{k}p(r_j).
$$

Since:

$$
p(r_j)=\frac{n_j}{MN},
$$

we get:

$$
\boxed{
s_k=
(L-1)
\sum_{j=0}^{k}
\frac{n_j}{MN}
}
$$

followed by quantization/rounding to the available gray levels.

---

# 3. Why the result is not perfectly uniform

In the continuous case, the CDF transform can produce an exactly uniform distribution under
the assumptions.

For a discrete image:

- the gray levels are finite,
- probabilities are discrete,
- output levels must be quantized.

Therefore the resulting histogram is generally only approximately uniform.

---

# 4. Example procedure

Given a histogram:

1. count $n_k$,
2. divide by total number of pixels,
3. compute cumulative probabilities,
4. multiply by $L-1$,
5. round to a valid output level,
6. remap every input gray level using the resulting lookup table.

The transformation can therefore be implemented efficiently using a lookup table.

---

# Lecture 35 — Histogram Equalization and Specification – II

This lecture extends histogram equalization to **histogram specification/matching**.

---

# 1. Goal of histogram specification

Equalization asks for:

> approximately uniform output histogram.

Specification asks for:

> a desired histogram.

Suppose the desired output random variable is $z$ with density:

$$
p_z(z).
$$

We want the transformation:

$$
r\rightarrow z
$$

such that the output has the desired distribution.

---

# 2. Two-stage transformation

First equalize the input:

$$
s=T(r)
=
\int_0^r p_r(w)\,dw.
$$

Then define a transformation:

$$
v=G(z)
=
\int_0^z p_z(w)\,dw.
$$

If we can obtain:

$$
z=G^{-1}(s),
$$

then:

$$
\boxed{
z=G^{-1}(T(r))
}
$$

produces the desired distribution in the continuous ideal case.

---

# 3. Discrete implementation

In a digital image, the inverse transformation may not map neatly to unique gray levels.

Therefore the practical process is:

1. compute input CDF,
2. equalize input,
3. compute desired CDF,
4. match equalized values to the closest desired CDF values,
5. construct a mapping table,
6. transform the image.

---

# 4. Why histogram matching is useful

Histogram specification can be used when we want images to have similar intensity statistics.

Applications include:

- standardizing images,
- matching image appearance,
- preprocessing,
- controlled enhancement.

---

# Lecture 36 — Histogram Implementation – I

The lecturer moves from the mathematics to implementation.

---

# 1. Histogram computation

For an image with gray levels:

$$
0,\ldots,L-1,
$$

initialize:

$$
h[k]=0.
$$

For every pixel value $r$:

$$
h[r]\leftarrow h[r]+1.
$$

After scanning the image:

$$
\sum_{k=0}^{L-1}h[k]=MN.
$$

This is the most basic histogram algorithm.

---

# 2. Normalization

The normalized histogram is:

$$
p[k]=\frac{h[k]}{MN}.
$$

It can therefore be interpreted as an empirical probability distribution.

---

# 3. Cumulative histogram

For equalization, calculate:

$$
c[k]=\sum_{j=0}^{k}p[j].
$$

Then:

$$
s[k]=\operatorname{round}
\left[
(L-1)c[k]
\right].
$$

This creates a lookup table:

$$
k\rightarrow s[k].
$$

---

# 4. Lookup-table implementation

Instead of calculating the transformation separately for every pixel, calculate it once for
each possible input intensity.

Then process each pixel using:

$$
g(x,y)=s[f(x,y)].
$$

This is much more efficient.

For an 8-bit image, only 256 mapping values need to be computed.

---

# 5. Histogram-based image operations

The lecturer uses implementation examples to emphasize that image-processing algorithms can
often be broken into:

```text
statistics
   ↓
mapping table
   ↓
pixel-wise application
```

This is particularly convenient for point-processing operations.

---

# Lecture 37 — Histogram Implementation – II

The implementation discussion continues with histogram-based enhancement and practical issues.

---

# 1. Histogram equalization algorithm

A complete implementation can be summarized as:

### Step 1

Read the image.

### Step 2

Compute:

$$
h[k].
$$

### Step 3

Normalize:

$$
p[k]=\frac{h[k]}{MN}.
$$

### Step 4

Compute cumulative distribution:

$$
c[k]=\sum_{j=0}^{k}p[j].
$$

### Step 5

Generate mapping:

$$
s[k]=(L-1)c[k].
$$

### Step 6

Quantize/round $s[k]$.

### Step 7

Replace every pixel value $k$ by $s[k]$.

---

# 2. Complexity

Histogram computation requires one pass through the image:

$$
O(MN).
$$

The lookup table has:

$$
O(L)
$$

entries.

The transformation itself is another:

$$
O(MN)
$$

pass.

Thus overall complexity is essentially:

$$
O(MN+L).
$$

For ordinary 8-bit images, $L=256$, so the $MN$ term dominates.

---

# 3. CDF implementation viewpoint

The histogram can be converted into a cumulative histogram.

The CDF is monotonic:

$$
c[k+1]\ge c[k].
$$

Therefore the equalization mapping is also monotonic.

This is important because gray-level ordering is preserved:

$$
r_1<r_2
\Rightarrow
T(r_1)\le T(r_2).
$$

---

# 4. Histogram specification implementation

Histogram specification can similarly be implemented using lookup tables.

The general structure is:

```text
input histogram
      ↓
input CDF
      ↓
equalized level
      ↓
match to desired CDF
      ↓
output mapping
      ↓
output image
```

The expensive part is not the final pixel mapping; once the table is constructed, each pixel
is handled by a simple lookup.

---

# Part IX — What Lectures 16–37 Build Together

The sequence is easier to remember as one continuous progression.

---

## Block 1 — Interpolation

### Lectures 16–19

You start with a sampled image and ask:

> How do I obtain values at new coordinates?

This gives:

$$
\text{resampling}
\rightarrow
\text{interpolation}
\rightarrow
\text{geometric image operations}.
$$

Know:

- nearest neighbor,
- linear interpolation,
- bilinear interpolation,
- inverse mapping,
- interpolation during rotation/scaling,
- anti-aliasing during reduction.

---

## Block 2 — General image transforms

### Lectures 20–23

The image is represented using a transform basis:

$$
\mathbf F=T\mathbf f.
$$

Then:

- orthogonal transforms,
- separability,
- basis images

prepare the mathematical foundation for Fourier/DCT/Walsh/Hadamard transforms.

---

## Block 3 — Fourier analysis

### Lectures 24–27

The image is interpreted as a sum of spatial frequencies.

Key ideas:

$$
f(x,y)
\leftrightarrow
F(u,v).
$$

Then:

- Fourier transform,
- convolution theorem,
- phase/magnitude,
- spectrum display,
- translation,
- rotation

are developed.

---

## Block 4 — Alternative transforms

### Lectures 28–29

The course compares other bases:

```text
Fourier → sinusoidal complex basis
DCT → cosine basis
Walsh → binary/sign-changing basis
Hadamard → orthogonal ±1 matrix basis
```

These are important for compression and representation.

---

## Block 5 — Statistical transforms

### Lectures 30–31

The representation shifts from fixed mathematical bases to image statistics.

Histogram:

$$
h(r_k)=n_k.
$$

K-L/PCA:

$$
C
\rightarrow
\text{eigenvectors}
\rightarrow
\text{data-adapted basis}.
$$

---

## Block 6 — Point enhancement

### Lectures 32–33

The image is enhanced by transforming each pixel independently:

$$
g(x,y)=T(f(x,y)).
$$

Important transformations:

- negative,
- log,
- gamma/power law,
- piecewise-linear,
- contrast stretching,
- intensity slicing,
- bit-plane slicing.

---

## Block 7 — Histogram-based enhancement

### Lectures 34–37

The intensity distribution itself is manipulated.

Histogram:

$$
p(r_k)=\frac{n_k}{MN}.
$$

Equalization:

$$
s_k=(L-1)\sum_{j=0}^{k}p(r_j).
$$

Specification:

$$
z=G^{-1}(T(r)).
$$

Then the mathematical operations are turned into efficient lookup-table implementations.

---

# Master Checklist — Lectures 16–37

## Interpolation and resampling

- [ ] Explain why interpolation is needed.
- [ ] Distinguish interpolation from resampling.
- [ ] Understand forward mapping.
- [ ] Understand inverse mapping.
- [ ] Know nearest-neighbor interpolation.
- [ ] Know linear interpolation.
- [ ] Know bilinear interpolation.
- [ ] Calculate interpolation weights.
- [ ] Understand interpolation during rotation.
- [ ] Understand interpolation during scaling.
- [ ] Explain why downsampling can cause aliasing.
- [ ] Explain the role of low-pass filtering before decimation.

## Transform fundamentals

- [ ] Write:
  $$
\mathbf F=T\mathbf f.
$$
- [ ] Explain inverse transform.
- [ ] Understand orthogonal transforms.
- [ ] Know:
  $$
T^TT=I.
$$
- [ ] Understand energy preservation.
- [ ] Explain separability.
- [ ] Know:
  $$
F=T f T^T.
$$
- [ ] Understand basis images.
- [ ] Interpret transform coefficients.

## Fourier transform

- [ ] 2-D Fourier transform.
- [ ] 2-D DFT.
- [ ] Magnitude spectrum.
- [ ] Phase spectrum.
- [ ] Translation property.
- [ ] Convolution theorem.
- [ ] Multiplication/convolution duality.
- [ ] Separability.
- [ ] Log spectrum display.
- [ ] Spectrum centering.
- [ ] Rotation property.
- [ ] Translation invariance of magnitude.

## DCT / Walsh / Hadamard

- [ ] DCT basis.
- [ ] DCT energy compaction.
- [ ] Difference between DCT and DFT.
- [ ] Walsh basis.
- [ ] Sequency.
- [ ] Hadamard matrix.
- [ ] Hadamard recursion.
- [ ] Hadamard orthogonality.
- [ ] Relation between Walsh and Hadamard transforms.

## Histogram / K-L

- [ ] Histogram definition.
- [ ] Normalized histogram.
- [ ] Understand that histogram loses spatial information.
- [ ] Histogram equalization.
- [ ] CDF interpretation.
- [ ] K-L transform.
- [ ] Covariance matrix.
- [ ] Eigenvectors/eigenvalues.
- [ ] Relation to PCA.
- [ ] Fixed basis vs data-adaptive basis.

## Point processing

- [ ] General point transformation:
  $$
s=T(r).
$$
- [ ] Negative transformation.
- [ ] Log transformation.
- [ ] Gamma transformation.
- [ ] Piecewise-linear transformation.
- [ ] Contrast stretching.
- [ ] Intensity-level slicing.
- [ ] Bit-plane slicing.

## Histogram enhancement

- [ ] Discrete histogram equalization formula.
- [ ] Why equalization is only approximately uniform in the discrete case.
- [ ] Histogram specification.
- [ ] Desired CDF.
- [ ] Inverse-CDF mapping.
- [ ] Lookup-table implementation.
- [ ] Computational complexity.

---

# Essential Equations — Lectures 16–37

## Bilinear interpolation

$$
\hat f(x,y)=
(1-\alpha)(1-\beta)f_{00}
+\alpha(1-\beta)f_{10}
+(1-\alpha)\beta f_{01}
+\alpha\beta f_{11}.
$$

## Orthogonal transform

$$
T^TT=I.
$$

## Transform

$$
\mathbf F=T\mathbf f.
$$

## Separable 2-D transform

$$
F=T f T^T.
$$

## 2-D Fourier transform

$$
F(u,v)
=
\int\int
f(x,y)e^{-j2\pi(ux+vy)}dx\,dy.
$$

## 2-D DFT

$$
F(u,v)
=
\sum_x\sum_y
f(x,y)
e^{-j2\pi
\left(
\frac{ux}{M}+\frac{vy}{N}
\right)}.
$$

## Convolution theorem

$$
f*h
\leftrightarrow
FH.
$$

## Fourier magnitude

$$
|F|=\sqrt{R^2+I^2}.
$$

## Fourier phase

$$
\phi=\tan^{-1}\left(\frac{I}{R}\right).
$$

## Log spectrum

$$
D=c\log(1+|F|).
$$

## DCT

$$
C(u,v)=
\alpha(u)\alpha(v)
\sum_x\sum_y
f(x,y)
\cos
\left[
\frac{(2x+1)u\pi}{2N}
\right]
\cos
\left[
\frac{(2y+1)v\pi}{2N}
\right].
$$

## Hadamard recursion

$$
H_{2N}
=
\begin{bmatrix}
H_N&H_N\\
H_N&-H_N
\end{bmatrix}.
$$

## Histogram

$$
h(r_k)=n_k.
$$

## Normalized histogram

$$
p(r_k)=\frac{n_k}{MN}.
$$

## Histogram equalization

$$
s_k=
(L-1)
\sum_{j=0}^{k}p(r_j).
$$

## Continuous equalization

$$
s=
\int_0^r p_r(w)\,dw.
$$

## Histogram specification

$$
z=G^{-1}(T(r)).
$$

## Point processing

$$
g(x,y)=T(f(x,y)).
$$

## Negative

$$
s=L-1-r.
$$

## Log

$$
s=c\log(1+r).
$$

## Gamma

$$
s=cr^\gamma.
$$

## Linear contrast stretch

$$
s=
s_{\min}
+
\frac{r-r_{\min}}
{r_{\max}-r_{\min}}
(s_{\max}-s_{\min}).
$$

## K-L / PCA covariance

$$
C=
E[
(\mathbf x-\boldsymbol\mu)
(\mathbf x-\boldsymbol\mu)^T
].
$$

## K-L transform

$$
\mathbf y=
E^T(\mathbf x-\boldsymbol\mu).
$$

---

# What Not to Confuse

### Interpolation vs resampling

**Interpolation:** estimating values between known samples.

**Resampling:** producing a new sampled image, usually using interpolation.

---

### Forward vs inverse mapping

**Forward:**

$$
\text{input}\rightarrow\text{output}.
$$

**Inverse:**

$$
\text{output}\rightarrow\text{input}.
$$

Inverse mapping is generally preferred for image warping because it avoids holes in the output.

---

### Spatial domain vs transform domain

Spatial:

$$
f(x,y)
$$

Transform:

$$
F(u,v).
$$

The transform is another representation of the same image information.

---

### Fourier magnitude vs phase

Magnitude describes the strength of frequency components.

Phase carries spatial alignment/structural information.

Do not assume magnitude alone contains all the information.

---

### Histogram vs image

A histogram records:

> how many pixels have each intensity.

It does **not** record:

> where those pixels occur.

---

### Histogram equalization vs specification

Equalization:

> transform toward a uniform intensity distribution.

Specification:

> transform toward a chosen target distribution.

---

### Point processing vs mask processing

Point processing:

$$
g(x,y)=T(f(x,y)).
$$

Only the current pixel matters.

Mask processing:

$$
g(x,y)=T(\text{neighborhood around }(x,y)).
$$

Neighbors matter.

---

### Fixed transform vs K-L transform

Fourier/DCT/Hadamard:

> basis is specified in advance.

K-L/PCA:

> basis is determined from the data covariance.

---

# The Main Story

The course has now moved from:

$$
\boxed{
\text{digital image representation}
}
$$

to:

$$
\boxed{
\text{how to change its sampling grid}
}
$$

then:

$$
\boxed{
\text{how to represent it in useful transform domains}
}
$$

and finally:

$$
\boxed{
\text{how to enhance its intensity distribution}.
}
$$

The progression is:

```text
Sampling
   ↓
Interpolation / Resampling
   ↓
Image transformations
   ↓
Separable transforms
   ↓
Basis images
   ↓
Fourier representation
   ↓
Alternative transforms
   ↓
Histogram / statistical representation
   ↓
Point processing
   ↓
Contrast enhancement
   ↓
Histogram equalization / specification
   ↓
Efficient implementation
```

The next major course block after Lecture 37 moves from point operations to **mask/spatial
processing**, followed by frequency-domain processing and restoration.
