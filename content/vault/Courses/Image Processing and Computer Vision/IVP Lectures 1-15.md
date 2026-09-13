---
title: "IVP Lectures 1-15"
lastmod: 2026-09-07
---

# Digital Image Processing — Detailed Speedrun Notes
## Prof. P. K. Biswas, IIT Kharagpur
### Lectures 1–15

---
## How to use this document

These are **detailed speedrun notes**, not a replacement for the lectures.

The goal is:

> **Watch the lectures quickly later, while using these notes as a coverage checklist.**

The notes follow the actual sequence of the supplied NPTEL playlist and deliberately preserve
the way the lecturer develops the subject. Closely related lectures are grouped conceptually,
but every lecture is separately accounted for.

The official NPTEL course listing gives the first 15 lectures as:

1. Introduction to Digital Image Processing
2. Application of Digital Image Processing
3. Image Digitalisation, Sampling, Quantization and Display
4. Signal Reconstruction from Samples: Convolution Concept
5. Signal Reconstruction from Image
6. Quantizer Design
7. Relationship between Pixels
8. Relationship of Adjacency and Connected Components Labeling
9. Application of Distance Measures
10. Basic Transform
11. Image Formation – I
12. Image Formation – II
13. Image Geometry – I
14. Image Geometry – II
15. Stereo Imaging Model – II

The course then moves to interpolation/resampling, so **Lecture 15 is the end of the
first camera/stereo block**.

---

# Part I — Why Digital Image Processing?
## Lectures 1–2

---

# Lecture 1 — Introduction to Digital Image Processing

## 1. What does "Digital Image Processing" mean?

The lecturer starts by unpacking the phrase itself.

A **digital image** is an image represented in digital/numerical form, and **digital image
processing** means processing such images using a digital computer.

The important distinction is that the course is not merely about manipulating photographs.
An image is treated as a signal carrying information, and the computer is used to transform,
analyze, or extract information from that signal.

A useful abstraction is:

$$
\text{physical scene}
\rightarrow
\text{image acquisition}
\rightarrow
\text{digital image}
\rightarrow
\text{processing}
\rightarrow
\text{information / improved image}.
$$

---

## 2. Why do we need image processing?

The lecturer identifies three broad motivations.
### 2.1 Improvement of pictorial information for human perception

The first major application is to make an image **look better or become easier to interpret**.

Examples of operations that fit here:
- removing noise,
- improving contrast,
- sharpening,
- removing blur,
- enhancing details.

The computer is therefore being used as a tool to improve the visual representation.

### 2.2 Autonomous machine applications

The second major motivation is that the image is not necessarily meant to be viewed by a
human at all.

Instead, the image can be processed so that a machine can:
- detect an object,
- measure an object,
- recognize an object,
- inspect a manufactured product,
- track something,
- make a decision.

This is the connection between image processing and **machine vision / computer vision**.

### 2.3 Efficient storage and transmission

The third motivation is reducing the amount of data required to:

- store an image,
- transmit an image,
- transmit video.

This introduces the idea that an image contains **redundancy** and that image-processing
techniques can exploit that redundancy.

This motivation eventually leads toward image compression.

---

## 3. Image-processing applications introduced

The lecture uses examples to show the breadth of the field.

Important application areas include:

### Medical imaging

Examples include:

- X-ray imaging,
- CT,
- mammography,
- medical diagnosis.

The objective can be enhancement for a doctor as well as extraction of useful information.

### Remote sensing

Images acquired from:

- aircraft,
- satellites,

can be processed for:

- weather analysis,
- crop assessment,
- geographical analysis,
- atmospheric studies.

### Astronomy

Image processing is useful when the objects being observed are faint, noisy, or extremely
far away.

Examples include:

- stars,
- galaxies,
- star formation.

### Machine vision

This is particularly important for industrial automation.

An imaging system can inspect objects on a production line and determine whether they satisfy
specified requirements.

---

## 4. Image-processing system as a pipeline

The lecture introduces the broad stages of a digital image-processing system.

The important conceptual pipeline is:

```text
Image acquisition
       ↓
Preprocessing
       ↓
Segmentation
       ↓
Representation / description
       ↓
Recognition / interpretation
       ↓
Image understanding
```

A **knowledge base** can interact with the different stages.

### Image acquisition

Obtaining the image from a sensor.

### Preprocessing

Initial operations such as:

- noise removal,
- contrast improvement,
- correction of undesirable effects.

The purpose is to make the subsequent processing easier.

### Segmentation

Partitioning the image into meaningful constituent parts.

For example:

```text
whole image
     ↓
background + object(s)
```

Segmentation is therefore a major transition from a raw image to meaningful regions.

### Representation and description

Once objects/regions have been isolated, they have to be represented in a form suitable
for computer processing.

Examples include descriptions based on:

- boundaries,
- shapes,
- regions,
- features.

### Recognition

The system uses the extracted description to determine what an object is.

### Knowledge base

The knowledge base can contain prior information and help coordinate the different processing
stages.

---

## 5. What Lecture 1 is trying to establish

The lecturer is essentially defining the **scope of the entire subject**.

Do not reduce DIP to:

> "filters applied to pictures."

The course covers a pipeline from acquiring a signal all the way to extracting semantic information
from it.

---

# Lecture 2 — Applications of Digital Image Processing

Lecture 2 continues the motivation and goes deeper into actual applications.

---

## 1. Human-oriented vs machine-oriented processing

A key distinction is:
### Human perception
The output is primarily intended to be viewed.

Examples:
- contrast enhancement,
- noise removal,
- deblurring,
- visual enhancement.

### Machine interpretation
The image is processed to extract a description that a computer can use.
Examples:
- industrial inspection,
- automated target detection,
- tracking,
- fingerprint recognition,
- analysis of aerial/satellite imagery.

The same image-processing operation can therefore have very different objectives depending
on the final consumer of the information.

---

## 2. Industrial machine vision

The lecturer discusses automation of industrial processes. A typical example is a bottling/assembly line.

The general idea is:
```text
manufacturing process
        ↓
camera acquires image
        ↓
extract relevant object information
        ↓
inspect / classify
        ↓
accept, reject, or control process
```

This illustrates why machine vision is different from simply making an image visually pleasing.

The computer has to extract **features/descriptions** useful for a decision.

---

## 3. Other application examples

The lecture discusses applications such as:

- automated target detection and tracking,
- fingerprint recognition,
- aerial image processing,
- satellite image processing,
- weather-related analysis,
- crop assessment.

The important commonality is that the image becomes an **information source**.

---

## 4. The complete digital image-processing system

The lecture ends by tying the application discussion back to the processing pipeline.

The stages are:

### 1. Image acquisition
Capture the image.

### 2. Preprocessing
Correct obvious undesirable effects.

### 3. Segmentation
Separate the image into meaningful regions/objects.

### 4. Representation and description
Represent each relevant object in a compact/useful form and extract features.

### 5. Recognition and interpretation
Determine what the objects/features represent.

### 6. Knowledge base
Prior information can assist the processing stages and facilitate communication between modules.

### Why this matters later
The rest of the course develops mathematical tools corresponding to different pieces of this
pipeline.

---

# Part II — Turning an Image into Numbers
## Lectures 3–6

This block is foundational.

The lecturer now asks:

> **How can a continuous physical image be represented by a finite collection of numbers?**

The answer has two principal stages:

$$
\boxed{\text{sampling}+\text{quantization}}
$$

Sampling discretizes **space**.

Quantization discretizes **intensity**.

---

# Lecture 3 — Image Digitalisation, Sampling, Quantization and Display

## 1. Why is digitization necessary?

A physical image is fundamentally continuous.

The image can be represented as:

$$
f(x,y)
$$

where:

- $x,y$ are spatial coordinates,
- $f(x,y)$ is the intensity at that location.

For a real image, the intensity can vary continuously across space.

A computer, however, cannot store infinitely many spatial positions and arbitrary real-valued
intensities.

Therefore we need digitization.

---

# 2. Image digitization has two stages

The lecturer emphasizes two separate operations:

$$
\boxed{\text{Sampling}}
\quad+\quad
\boxed{\text{Quantization}}
$$

### Sampling
Select discrete spatial positions.

### Quantization
Convert the intensity measured at each selected position into one of a finite number of
allowed values.
This distinction should become automatic.

---

# 3. Image sampling

Suppose the continuous image is

$$
f(x,y).
$$

Sampling chooses points on a spatial grid:

$$
x=m\Delta_x,\qquad y=n\Delta_y.
$$

The resulting samples are:

$$
f[m,n]=f(m\Delta_x,n\Delta_y).
$$

Thus the image is converted from a continuous surface to a discrete set of spatial samples.

---

## 4. Intensity profile

The lecturer motivates the continuous nature of the image by considering a line through an
image.

If we select a horizontal line, the image becomes a 1-D intensity profile:

$$
g(x)=f(x,y_0).
$$

The intensity can take values between a minimum and maximum along that line.

The same idea applies to vertical lines or arbitrary directions.

This lets the lecturer reduce the initial image problem to the familiar problem of sampling a
1-D signal.

---

# 5. Signal bandwidth

To understand how densely a signal must be sampled, we need its **frequency content**.

For a periodic 1-D signal, Fourier series can be used.

For an aperiodic signal, the Fourier transform is used.

The frequency spectrum tells us the range of frequencies present in the signal.

If the highest frequency present is $B$, the sampling theorem gives the familiar condition:

$$
\boxed{f_s\geq 2B}
$$

where $f_s$ is the sampling frequency.

The minimum value $2B$ is the **Nyquist rate**.

---

# 6. Aliasing

If:

$$
f_s < 2B,
$$

the signal is undersampled.

The spectral replicas generated by sampling overlap.

The resulting distortion is called **aliasing**.

The key conceptual picture is:

```text
adequate sampling
spectral replicas separated
        ↓
reconstruction possible

insufficient sampling
spectral replicas overlap
        ↓
aliasing
```

Once aliasing has occurred, the original signal cannot in general be uniquely recovered from
the samples.

---

# 7. Sampling a 2-D image

An image is a 2-D signal, so frequency is also 2-D.

Instead of a single frequency variable, we have spatial frequency components in two directions.

Conceptually:

$$
(\omega_x,\omega_y).
$$

The sampling operation therefore creates a 2-D grid of samples.

The same basic idea applies:

> the spatial sampling density must be sufficiently high relative to the highest spatial
> frequencies in the image.

---

# 8. Quantization

After sampling, the spatial coordinates are discrete, but the measured sample value can still
be continuous.

Suppose a sampled value is $x$.

A quantizer maps it to one of $L$ allowed reconstruction levels:

$$
x\rightarrow Q(x).
$$

Therefore:

```text
continuous image
      ↓
spatial sampling
      ↓
discrete locations + continuous intensities
      ↓
quantization
      ↓
digital image
```

---

# 9. Number of bits

If there are $L$ intensity levels, the number of bits required per sample is:

$$
b=\log_2 L.
$$

For example, 256 gray levels require:

$$
b=\log_2(256)=8
$$

bits per pixel.

For a typical RGB color image, there are three color planes:

- red,
- green,
- blue.

If each plane uses 8 bits, then:

$$
8+8+8=24
$$

bits per pixel.

---

# 10. Display

The final digital values need to be displayed in a way that humans can perceive.

The important conceptual point is that the digital representation is an intermediate numerical
representation:

```text
physical image
      ↓
digitization
      ↓
numbers / pixel matrix
      ↓
processing
      ↓
display
```

---

# Lecture 4 — Signal Reconstruction from Samples: Convolution Concept

Lecture 4 temporarily steps back from images and develops the 1-D signal reconstruction machinery.

The purpose is to understand **how a continuous signal can be reconstructed from its samples**.

---

# 1. Representing sampling mathematically

Let the original continuous signal be:

$$
x(t).
$$

Sampling can be represented by multiplying $x(t)$ by a periodic impulse train, often written
as a comb function.

Conceptually:

$$
x_s(t)=x(t)\operatorname{comb}(t,\Delta t).
$$

The impulse train selects the values of $x(t)$ at regular intervals.

---

# 2. Why Fourier analysis is useful

Sampling in the time/spatial domain has a very simple interpretation in the frequency domain.

Multiplication in one domain corresponds to convolution in the other.

Thus the spectral effect of sampling can be understood through the Fourier transform.

The sampled spectrum consists of repeated copies of the original spectrum.

This is the frequency-domain explanation of the Nyquist condition and aliasing.

---

# 3. Convolution

The lecturer introduces convolution as an operation between two signals.

For continuous signals:

$$
y(t)=x(t)*h(t)
$$

with

$$
y(t)=
\int_{-\infty}^{\infty}
x(\tau)h(t-\tau)\,d\tau.
$$

Equivalently, one signal can be thought of as being:

1. reversed,
2. shifted,
3. multiplied,
4. integrated.

The important signal-processing property is:

$$
\boxed{
x(t)*h(t)
\quad\longleftrightarrow\quad
X(\omega)H(\omega)
}
$$

under the Fourier transform.

So convolution in the signal domain corresponds to multiplication in the frequency domain.

---

# 4. Reconstruction idea

After sampling, we have impulses whose amplitudes are the sample values.

To reconstruct the original continuous signal, we pass the sampled signal through a suitable
reconstruction/interpolation operation.

The ideal reconstruction filter has a frequency response that:

- retains the original spectral copy,
- rejects the unwanted replicated spectra.

For a band-limited signal satisfying the sampling theorem, the original signal can theoretically
be reconstructed.

---

# 5. Why this lecture matters

The key chain is:

$$
\text{sampling}
\rightarrow
\text{spectral replicas}
\rightarrow
\text{reconstruction filter}
\rightarrow
\text{original signal}.
$$

This is the mathematical foundation for the image-reconstruction discussion in the next lecture.

---

# Lecture 5 — Signal Reconstruction from Image

Lecture 5 transfers the reconstruction idea from 1-D signals to images.

---

# 1. Image as a 2-D signal

The continuous image is:

$$
f(x,y).
$$

Sampling creates:

$$
f[m,n].
$$

The inverse problem is:

> Given the discrete samples $f[m,n]$, how can we reconstruct a continuous image?

---

# 2. Two-dimensional sampling

Instead of a 1-D impulse train, a 2-D sampling grid is used.

The sample locations form a lattice:

```text
•   •   •   •

•   •   •   •

•   •   •   •
```

Each dot is a sampled image location.

---

# 3. 2-D frequency domain

An image has spatial frequencies in both directions.

We can think of the spectrum as:

$$
F(\omega_x,\omega_y).
$$

Sampling produces repeated copies of the 2-D spectrum.

The separation between copies depends on the sampling frequencies in the two directions.

Therefore the sampling requirements are fundamentally 2-D versions of the 1-D sampling theorem.

---

# 4. Reconstruction

The reconstruction process attempts to isolate the original spectral region from the periodic
spectral replicas.

Conceptually:

$$
\text{sampled image}
\rightarrow
\text{2-D reconstruction filter}
\rightarrow
\text{continuous image}.
$$

The important idea is that interpolation/reconstruction is not an arbitrary visual trick.
It has a signal-processing interpretation.

---

# 5. Quantization revisited

The lecturer connects the two stages of digitization:

### Sampling

$$
f(x,y)\rightarrow f[m,n]
$$

### Quantization

$$
f[m,n]\rightarrow Q(f[m,n]).
$$

Only after both operations do we have a true digital image.

---

# 6. Key takeaway from Lectures 3–5

Keep the following distinction absolutely clear:

```text
Sampling
→ discretizes spatial coordinates.

Quantization
→ discretizes intensity values.

Reconstruction
→ attempts to recover a continuous signal/image from samples.

Aliasing
→ information loss caused by insufficient sampling.
```

---

# Lecture 6 — Quantizer Design

Now the lecturer focuses on the second half of digitization:

> **Given a finite number of intensity levels, where should the quantization levels be placed?**

This is more subtle than simply dividing the intensity range uniformly.

---

# 1. Quantization model

Let:

- $u$ = input value,
- $u'$ = quantized/reconstructed value.

The quantization error is:

$$
e=u-u'.
$$

A good quantizer should make this error small.

---

# 2. Decision levels and reconstruction levels

A scalar quantizer divides the input range into intervals.

Each interval is represented by a reconstruction value.

Schematically:

```text
input axis

---|---------|---------|---------|---
  t1        t2        t3        t4
    r1        r2        r3
```

Here:

- $t_k$ are **transition/decision levels**,
- $r_k$ are **reconstruction levels**.

An input falling inside a particular interval is mapped to the corresponding $r_k$.

---

# 3. Mean-square quantization error

A natural objective is:

$$
D=E[(u-u')^2].
$$

For a continuous random variable with probability density $p_u(u)$, the distortion is
computed by integrating the squared error weighted by the input probability density.

The design problem is therefore:

> choose the decision levels and reconstruction levels that minimize mean-square error.

---

# 4. Lloyd–Max quantizer

The lecturer introduces the **Lloyd–Max optimum mean-square-error quantizer**.

The goal is to minimize:

$$
E[(u-u')^2]
$$

for a specified number of quantization levels and a specified input probability density.

The optimum conditions produce two important relationships.

---

## 4.1 Optimum reconstruction level

For a given quantization interval $[t_k,t_{k+1}]$, the optimum reconstruction value is
the conditional mean:

$$
\boxed{
r_k=
\frac{
\int_{t_k}^{t_{k+1}}u\,p_u(u)\,du
}{
\int_{t_k}^{t_{k+1}}p_u(u)\,du
}
}
$$

Interpretation:

> The reconstruction level should be the probability-weighted center of the input values
> that get mapped to that level.

---

## 4.2 Optimum decision level

For two neighboring reconstruction values $r_k$ and $r_{k+1}$, the optimum transition
level lies midway between them:

$$
\boxed{
t_{k+1}=\frac{r_k+r_{k+1}}{2}
}
$$

for the standard squared-error criterion.

So the Lloyd–Max design alternates between:

```text
decision levels → determine reconstruction levels
        ↓
reconstruction levels → determine decision levels
        ↓
iterate
```

---

# 5. Why the equations are nonlinear

The optimum conditions depend on one another.

The transition levels determine the integration intervals, while the reconstruction levels depend
on those intervals.

Thus the equations have to be solved simultaneously.

The lecturer notes that numerical methods such as **Newton iteration** can be used.

---

# 6. Large number of quantization levels

When the number of levels is large, the probability density can sometimes be approximated
locally as piecewise constant.

This leads to simpler approximations.

The general principle remains:

> allocate quantization resolution according to the statistics of the input.

---

# 7. Uniform input distribution

If the input is uniformly distributed over a range, the optimum quantizer becomes a
**uniform quantizer**.

For a uniform density, the transition levels and reconstruction levels are equally spaced.

Let the quantization step be:

$$
q.
$$

Then:

$$
q=\frac{t_{L+1}-t_1}{L}
$$

for $L$ equal intervals.

The reconstruction level is centered within its interval:

$$
r_k=t_k+\frac q2.
$$

---

# 8. Quantization error for a uniform quantizer

For a uniform quantizer, the error is uniformly distributed over:

$$
-\frac q2\leq e\leq\frac q2.
$$

The mean-square error is:

$$
E[e^2]=\frac{q^2}{12}.
$$

This is an important result.

---

# 9. Relationship with number of bits

If the full input range has width $A$ and the quantizer uses $B$ bits, there are:

$$
L=2^B
$$

levels.

Therefore:

$$
q=\frac{A}{2^B}.
$$

As $B$ increases, the quantization step decreases exponentially.

Since:

$$
D=\frac{q^2}{12},
$$

the quantization error decreases rapidly with the number of bits.

---

# 10. Non-uniform input distributions

The lecturer also discusses the case where the input probability density is not uniform,
including distributions such as Gaussian/Laplacian-type densities.

The important lesson is:

> **The optimum quantizer depends on the probability distribution of the input.**

If values are concentrated heavily in one region, it can be wasteful to assign the same
resolution everywhere.

---

# 11. Practical issue

In many practical situations, the exact probability density of the input is not known in
advance.

A uniform quantizer is therefore attractive because it is simple and does not require detailed
prior statistical knowledge.

---

# Part III — Relationships Between Pixels
## Lectures 7–9

Once the image is a matrix of numbers, we need a language for describing the spatial relationship
between its elements.

This block develops:

- neighborhoods,
- adjacency,
- connectivity,
- connected components,
- distance,
- image operations.

---

# Lecture 7 — Relationship Between Pixels

## 1. Digital image as a matrix

A digital image can be represented as:

$$
f(x,y)
$$

where $x,y$ are now discrete coordinates.

Each matrix element is a **pixel**.

The lecturer asks:

> How are these pixels related to one another?

---

# 2. Neighborhood

For a pixel:

$$
p=(x,y),
$$

its immediate spatial neighbors can be defined in different ways.

---

## 2.1 4-neighborhood

The four horizontally/vertically adjacent pixels are:

$$
N_4(p)=
\{(x-1,y),(x+1,y),(x,y-1),(x,y+1)\}.
$$

These correspond to:

- left,
- right,
- up,
- down.

---

## 2.2 Diagonal neighborhood

The four diagonal pixels are:

$$
N_D(p)=
\{(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)\}.
$$

---

## 2.3 8-neighborhood

The full surrounding neighborhood is:

$$
N_8(p)=N_4(p)\cup N_D(p).
$$

It contains up to eight surrounding pixels.

---

# 3. Adjacency

Neighborhood tells us which pixels are spatially close.

**Adjacency** additionally depends on the set of pixels under consideration.

For example, in a binary image we may care only about pixels whose value is 1.

Two pixels can be called adjacent if:

1. they satisfy the selected neighborhood relationship, and
2. their values belong to the relevant set.

---

# 4. 4-, 8-, and m-adjacency

### 4-adjacency

Two pixels are adjacent if one lies in the other's 4-neighborhood.

### 8-adjacency

Two pixels are adjacent if one lies in the other's 8-neighborhood.

### m-adjacency

Mixed adjacency is introduced to avoid certain ambiguities produced by 8-connectivity.

The diagonal connection is accepted under a condition involving the common 4-neighbors.

The purpose is to avoid treating diagonal connections as connected in situations where they
produce ambiguous connectivity.

---

# 5. Paths

A path is a sequence of pixels in which consecutive pixels satisfy the chosen adjacency rule.

Conceptually:

$$
p_0\rightarrow p_1\rightarrow p_2\rightarrow\cdots\rightarrow p_n.
$$

If every consecutive pair is adjacent according to the chosen definition, the sequence forms
a valid path.

---

# 6. Connectivity

Two pixels are connected if there exists an allowed path between them.

This gives us a way to define image regions.

A **connected component** is a maximal set of mutually connected pixels.

---

# Lecture 8 — Adjacency and Connected Components Labeling

Lecture 8 develops connectivity into an actual algorithm.

---

# 1. Why connected components matter

Suppose a binary image contains multiple objects.

We can interpret:

- one intensity value as background,
- another intensity value as object.

Then we want to determine which object pixels belong together.

Connected-component labeling solves this problem.

It is therefore a bridge from:

$$
\text{raw binary image}
\rightarrow
\text{separate objects / regions}.
$$

---

# 2. Connected-component labeling

The lecturer discusses the standard labeling idea using a **two-pass approach**.

### First pass

Scan the image systematically.

When an object pixel is encountered:

- inspect already-processed neighbors,
- assign a new label if no labeled neighbor exists,
- otherwise copy an existing label,
- if multiple different labels are found to represent the same connected region,
  record their equivalence.

This can produce temporary labels such as:

```text
1 1 0 2
1 3 3 2
0 3 4 0
```

where labels 3 and 4 may later be found to belong to the same connected component.

---

# 3. Equivalence classes

If the scan discovers that two labels actually correspond to the same connected region,
the labels are placed into an equivalence class.

For example:

$$
3\sim4.
$$

Then the algorithm can later replace both with a single canonical label.

This is why the first pass may contain more labels than the final number of components.

---

# 4. Second pass

The image is scanned again.

Every temporary label is replaced by its final representative.

For example, if:

$$
3\sim4,
$$

then all pixels carrying 4 may be reassigned to 3.

At the end:

> every pixel belonging to one connected component has the same final label.

---

# 5. Why this is important for image understanding

Connected-component labeling provides a simple route from pixels to objects.

Once components are labeled, we can calculate properties such as:

- area,
- bounding box,
- centroid,
- shape descriptors,
- size.

This makes it an early example of the transition from **low-level image representation to
higher-level image understanding**.

---

# Lecture 9 — Application of Distance Measures

The lecture continues the pixel-relationship discussion.

The main topics are:

1. distance measures,
2. distance transformations,
3. skeletonization,
4. arithmetic/logical image operations,
5. neighborhood operations.

---

# 1. Euclidean distance

For two points:

$$
p=(x_1,y_1),\qquad q=(x_2,y_2),
$$

the Euclidean distance is:

$$
\boxed{
D_E(p,q)=
\sqrt{(x_1-x_2)^2+(y_1-y_2)^2}
}
$$

This corresponds to ordinary straight-line geometric distance.

---

# 2. City-block distance

The city-block distance is:

$$
\boxed{
D_4(p,q)=
|x_1-x_2|+|y_1-y_2|
}
$$

It corresponds to movement restricted to horizontal and vertical steps.

This is analogous to navigating city streets.

---

# 3. Chessboard distance

The chessboard distance is:

$$
\boxed{
D_8(p,q)=
\max(
|x_1-x_2|,
|y_1-y_2|
)
}
$$

It corresponds to movement where diagonal motion is allowed at the same unit cost.

---

# 4. Why different distance measures?

They correspond to different notions of neighborhood.

```text
4-neighborhood
    ↓
city-block style movement

8-neighborhood
    ↓
chessboard style movement

continuous plane
    ↓
Euclidean movement
```

The choice of distance should therefore match the geometry of the application.

---

# 5. Distance transformation

The lecturer discusses applying distance concepts to a binary image.

A distance transform assigns to pixels a value representing their distance from another
specified set of pixels, commonly the background.

For example:

```text
object boundary → small distance
object interior → larger distance
```

The resulting image is a **distance map**.

---

# 6. Skeleton of a binary object

The distance transform can be used to obtain a compact representation of the shape.

The **skeleton** captures the central structural information of a region.

Intuitively:

```text
thick object
    ↓
distance transform
    ↓
central/maximal structure
    ↓
skeleton
```

The skeleton is useful because it can represent a complex shape with fewer structural
elements.

The lecturer describes it as a compact description of shape.

---

# 7. Arithmetic operations on images

Images can be treated as numerical arrays, so pixel-wise arithmetic operations are possible.

For two images $f$ and $g$:

### Addition

$$
h(x,y)=f(x,y)+g(x,y).
$$

### Subtraction

$$
h(x,y)=f(x,y)-g(x,y).
$$

### Multiplication

$$
h(x,y)=f(x,y)g(x,y).
$$

### Division

$$
h(x,y)=\frac{f(x,y)}{g(x,y)}
$$

where defined.

These operations can be useful for:

- combining information,
- background subtraction,
- masking,
- normalization,
- enhancement.

---

# 8. Logical operations

For binary images, logical operations such as:

- AND,
- OR,
- NOT,

can be performed pixel-by-pixel.

These are useful for manipulating binary masks and regions.

---

# 9. Pixel-by-pixel operations vs neighborhood operations

This is an important distinction.

### Pixel-by-pixel operation

The output at $(x,y)$ depends only on the input value at $(x,y)$:

$$
g(x,y)=T(f(x,y)).
$$

### Neighborhood operation

The output at $(x,y)$ depends on a collection of neighboring pixels.

Conceptually:

$$
g(x,y)=
T\left(
\{f(x+i,y+j)\}
\right).
$$

This distinction becomes fundamental later when the course discusses spatial filtering.

---

# Part IV — Geometric Transformations
## Lecture 10

Lecture 10 begins the transition from discrete image geometry to **camera/image formation**.

The lecturer introduces basic mathematical transformations in both 2-D and 3-D.

The main transformations are:

- translation,
- rotation,
- scaling.

He also introduces:

- inverse transformations,
- homogeneous coordinates,
- perspective transformation.

---

# Lecture 10 — Basic Transform

# 1. Translation

For a 2-D point:

$$
P=
\begin{bmatrix}
x\\y
\end{bmatrix},
$$

translation by:

$$
(t_x,t_y)
$$

gives:

$$
x'=x+t_x,
\qquad
y'=y+t_y.
$$

In matrix form using homogeneous coordinates:

$$
\begin{bmatrix}
x'\\y'\\1
\end{bmatrix}
=
\begin{bmatrix}
1&0&t_x\\
0&1&t_y\\
0&0&1
\end{bmatrix}
\begin{bmatrix}
x\\y\\1
\end{bmatrix}.
$$

---

# 2. Scaling

Scaling is:

$$
x'=s_xx,
\qquad
y'=s_yy.
$$

Homogeneous form:

$$
\begin{bmatrix}
x'\\y'\\1
\end{bmatrix}
=
\begin{bmatrix}
s_x&0&0\\
0&s_y&0\\
0&0&1
\end{bmatrix}
\begin{bmatrix}
x\\y\\1
\end{bmatrix}.
$$

If:

$$
s_x=s_y,
$$

the object is scaled equally in both directions.

---

# 3. Rotation

Rotation by angle $\theta$ about the origin is:

$$
\begin{bmatrix}
x'\\y'
\end{bmatrix}
=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}
\begin{bmatrix}
x\\y
\end{bmatrix}.
$$

The rotation matrix is:

$$
R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
$$

---

# 4. Inverse transformations

Every transformation is also considered from the inverse perspective.

For example, inverse translation is:

$$
x=x'-t_x,
\qquad
y=y'-t_y.
$$

Inverse scaling uses:

$$
\frac1{s_x},\qquad\frac1{s_y}
$$

provided the scale factors are nonzero.

Inverse rotation is:

$$
R^{-1}(\theta)=R(-\theta).
$$

This inverse viewpoint becomes important when mapping image coordinates back into the scene.

---

# 5. 3-D transformations

The same ideas are extended to 3-D coordinates:

$$
(X,Y,Z).
$$

Scaling becomes:

$$
X'=s_xX,\qquad
Y'=s_yY,\qquad
Z'=s_zZ.
$$

Translation becomes:

$$
X'=X+t_x,
\qquad
Y'=Y+t_y,
\qquad
Z'=Z+t_z.
$$

Rotations can be defined about the $X$, $Y$, and $Z$ axes.

---

# 6. Why homogeneous coordinates?

Ordinary Cartesian coordinates make translation different from matrix multiplication.

Homogeneous coordinates solve this by adding an additional coordinate.

A 2-D point:

$$
(x,y)
$$

becomes:

$$
(x,y,1).
$$

A 3-D point:

$$
(X,Y,Z)
$$

becomes:

$$
(X,Y,Z,1).
$$

This lets translation, rotation, scaling, and perspective transformations be represented
using matrix multiplication.

This is particularly convenient when transformations are composed.

---

# 7. Perspective transformation

The lecturer then connects transformations to camera imaging.

A 3-D point:

$$
(X,Y,Z)
$$

is mapped to an image point:

$$
(x,y).
$$

For the standard pinhole/perspective model:

$$
x=\lambda\frac{X}{Z},
\qquad
y=\lambda\frac{Y}{Z},
$$

where $\lambda$ represents the focal-length parameter under the lecture's convention.

The crucial feature is:

$$
\boxed{\text{image coordinate}\propto \frac{\text{world coordinate}}{Z}}
$$

so depth directly affects image position.

---

# 8. Example

The lecturer gives numerical exercises such as:

- given a camera focal length,
- given a 3-D point,
- find the corresponding image coordinate.

For example, with focal length $f=5$ and:

$$
(X,Y,Z)=(50,70,100),
$$

the ideal aligned-coordinate pinhole projection gives:

$$
x=5\frac{50}{100}=2.5,
$$

$$
y=5\frac{70}{100}=3.5.
$$

The exact sign convention depends on the chosen image-plane convention, but the important
relationship is the $1/Z$ dependence.

---

# 9. Composition matters

Transformations are generally **not commutative**.

For example:

$$
T\,S\neq S\,T
$$

in general.

So:

> translating and then scaling does not necessarily produce the same result as scaling
> and then translating.

This is why the lecturer uses questions involving the order of translation and scaling.

---

# Part V — Image Formation
## Lectures 11–12

The next conceptual step is:

> **Given a 3-D world and a camera, how exactly does a 3-D point become an image point?**

---

# Lecture 11 — Image Formation I

## 1. Camera as a mapping

The camera performs a mapping:

$$
(X,Y,Z)
\rightarrow
(x,y).
$$

The lecturer uses an idealized camera model to make this relationship mathematically tractable.

The central model is perspective projection.

---

# 2. Pinhole camera geometry

Imagine a tiny aperture through which rays from the scene pass.

A 3-D point and its image point lie on the same line passing through the camera center.

Thus the geometry is based on similar triangles.

---

# 3. Perspective projection equation

For a camera coordinate system aligned with the world coordinate system:

$$
x=f\frac{X}{Z},
\qquad
y=f\frac{Y}{Z}.
$$

This is the fundamental equation.

---

# 4. Depth dependence

Consider two points with identical $X,Y$ but different $Z$.

The farther point has a smaller projected coordinate magnitude.

Therefore:

$$
Z\uparrow
\Rightarrow
\text{projected size}\downarrow.
$$

This explains perspective:

> distant objects appear smaller.

---

# 5. Homogeneous representation

Perspective projection contains division by $Z$, so homogeneous coordinates are especially
useful.

A projective mapping can be written as a matrix transformation followed by normalization.

Conceptually:

$$
\begin{bmatrix}
x\\y\\1
\end{bmatrix}
\sim
P
\begin{bmatrix}
X\\Y\\Z\\1
\end{bmatrix},
$$

where $P$ represents the camera projection mapping.

The symbol $\sim$ means equality up to a nonzero scale factor.

---

# 6. Inverse perspective problem

A single image point does **not** determine a unique 3-D point.

If the image point is fixed, all 3-D points along the corresponding viewing ray can project
to it.

So the inverse mapping is not:

$$
(x,y)\rightarrow(X,Y,Z)
$$

as a unique point.

Instead:

$$
(x,y)\rightarrow\text{a ray in 3-D}.
$$

This is a very important computer-vision concept.

---

# Lecture 12 — Image Formation II

Lecture 12 generalizes the imaging geometry.

---

# 1. Why the simple model is insufficient

The simplest derivation assumes:

- world coordinate system and camera coordinate system are aligned,
- camera is conveniently positioned,
- camera axes correspond directly to world axes.

A real camera can be translated and rotated arbitrarily.

Therefore we need a **generalized imaging model**.

---

# 2. World coordinates vs camera coordinates

Let a point in the world coordinate system be:

$$
P_w=
\begin{bmatrix}
X_w\\Y_w\\Z_w
\end{bmatrix}.
$$

The same point in the camera coordinate system is:

$$
P_c=
\begin{bmatrix}
X_c\\Y_c\\Z_c
\end{bmatrix}.
$$

The two coordinate systems are related by:

$$
P_c=RP_w+t
$$

under the standard rigid transformation convention.

Here:

- $R$ is a rotation matrix,
- $t$ is a translation vector.

---

# 3. Generalized camera mapping

The complete conceptual chain becomes:

$$
\boxed{
\text{world coordinates}
\rightarrow
\text{camera coordinates}
\rightarrow
\text{perspective projection}
\rightarrow
\text{image coordinates}
}
$$

This separation is extremely important.

The first stage tells us how the camera is positioned relative to the world.

The second stage tells us how the camera projects its own coordinate system onto the image.

---

# 4. Inverse perspective transformation

Given an image point, the inverse perspective operation produces the line/ray in 3-D
that could have generated that point.

This is useful in:

- ray tracing,
- camera geometry,
- 3-D reconstruction,
- stereo.

---

# 5. Important conceptual distinction

Do not confuse:

### Camera pose

Where the camera is and how it is oriented.

with:

### Perspective projection

How a camera-coordinate 3-D point maps onto the 2-D image plane.

The generalized imaging model combines both.

---

# Part VI — Image Geometry
## Lectures 13–14

The camera is now treated as a geometrical object whose position and orientation can be
arbitrary.

---

# Lecture 13 — Image Geometry I

## 1. Coordinate systems

The lecturer distinguishes:

### World coordinate system

Describes where objects exist in the physical scene.

$$
(X,Y,Z)
$$

### Camera coordinate system

Describes points relative to the camera.

$$
(X_c,Y_c,Z_c)
$$

### Image coordinate system

Describes the projected location on the image plane.

$$
(x,y)
$$

### Pixel coordinate system

The final coordinates used to address the digital image array.

The complete chain is:

```text
World coordinates
       ↓
Camera coordinates
       ↓
Image-plane coordinates
       ↓
Pixel coordinates
```

---

# 2. Camera orientation

The camera may be rotated relative to the world.

The lecturer discusses camera orientation using rotational parameters, including concepts
such as:

- pan,
- tilt,

and the corresponding transformations.

The exact parameterization is less important than understanding:

> camera orientation changes the coordinate system in which the 3-D point is expressed
> before projection.

---

# 3. Translation of camera center

The camera center need not coincide with the world origin.

If the camera center is displaced, a translation is required before applying the camera rotation.

Thus the world-to-camera mapping includes both:

$$
R
$$

and:

$$
t.
$$

---

# 4. General camera mapping

The basic structure is:

$$
P_c=R(P_w-C)
$$

if $C$ denotes the camera center in world coordinates.

Equivalent formulations may absorb the translation differently.

The key is that the camera coordinate system is obtained by:

1. shifting the origin,
2. rotating the axes,
3. projecting.

---

# 5. Worked geometry problems

The lecturer uses numerical examples involving:

- a displaced camera center,
- pan angle,
- tilt angle,
- a specified 3-D world point,

and asks for the resulting image coordinates.

These exercises are important because they force the transformation chain to be applied in
the correct order.

---

# Lecture 14 — Image Geometry II

Lecture 14 continues the generalized imaging model and works through the geometry in more detail.

---

# 1. Camera pose as a transformation

The complete camera pose is encoded through rotation and translation.

A homogeneous rigid transformation can be written:

$$
\begin{bmatrix}
X_c\\Y_c\\Z_c\\1
\end{bmatrix}
=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
\begin{bmatrix}
X_w\\Y_w\\Z_w\\1
\end{bmatrix}.
$$

This form is useful because the entire pose becomes a single matrix multiplication.

---

# 2. Projection after pose transformation

After converting the world point to camera coordinates:

$$
(X_c,Y_c,Z_c),
$$

perspective projection is applied:

$$
x=f\frac{X_c}{Z_c},
\qquad
y=f\frac{Y_c}{Z_c}.
$$

Therefore:

$$
\boxed{
P_w
\rightarrow
P_c
\rightarrow
(x,y)
}
$$

is the complete geometric process.

---

# 3. Inverse problem

If an image point is known, we can recover the corresponding viewing ray in camera coordinates.

But without depth, we cannot determine the unique 3-D point.

This is the fundamental ambiguity of monocular vision.

---

# 4. Why stereo becomes necessary

If we observe the same physical point from a second camera position, the second image provides
another viewing ray.

Their intersection gives the 3-D point.

This leads directly into stereo imaging.

---

# 5. Example structure

The lecturer uses a camera whose center is displaced relative to a world coordinate system,
with specified orientation parameters.

A typical problem is:

```text
given:
camera displacement
camera pan
camera tilt
world point

find:
camera-coordinate point
then image coordinate
```

The important part is the sequence, not memorizing one numerical example.

---

# Part VII — Stereo Imaging
## Lecture 15

Lecture 15 completes the first camera-geometry block by introducing stereo.

The central question is:

> **How can two 2-D images provide enough information to recover a 3-D point?**

---

# 1. Basic stereo setup

Use two cameras observing the same scene:

```text
Camera 1                         Camera 2
    \                               /
     \                             /
      \                           /
       \                         /
        \                       /
             3-D point
```

A physical point projects to:

$$
(x_L,y_L)
$$

in the left image and:

$$
(x_R,y_R)
$$

in the right image.

These are called **corresponding points**.

---

# 2. Why corresponding points differ

The cameras observe the point from different locations.

Therefore the viewing rays are different.

Consequently, the same 3-D point appears at different image positions.

The difference between those positions is the **disparity**.

---

# 3. Simplified rectified stereo geometry

Consider two cameras with baseline:

$$
B.
$$

Assume:

- cameras have parallel optical axes,
- image planes are aligned,
- corresponding points lie on the same horizontal scanline.

Then disparity can be defined as:

$$
d=x_L-x_R
$$

under one common sign convention.

---

# 4. Depth from disparity

For the standard pinhole stereo setup:

$$
\boxed{
Z=\frac{fB}{d}
}
$$

where:

- $Z$ = depth,
- $f$ = focal length,
- $B$ = baseline,
- $d$ = disparity.

This is one of the most important equations in the first 15 lectures.

---

# 5. Intuition

The equation says:

$$
Z\propto\frac1d.
$$

Therefore:

### Nearby point

Large disparity:

$$
d\text{ large}
$$

so:

$$
Z\text{ small}.
$$

### Distant point

Small disparity:

$$
d\text{ small}
$$

so:

$$
Z\text{ large}.
$$

Thus:

```text
large disparity → close
small disparity → far
```

---

# 6. Derivation intuition

For a point at depth $Z$, the left and right image coordinates depend on the camera centers.

Using similar triangles:

$$
x_L=f\frac{X+B/2}{Z},
$$

$$
x_R=f\frac{X-B/2}{Z}
$$

for a symmetric camera arrangement.

Subtracting:

$$
d=x_L-x_R
$$

gives:

$$
d=f\frac{B}{Z}.
$$

Therefore:

$$
\boxed{
Z=\frac{fB}{d}.
}
$$

The exact coordinate origin can differ, but the depth-disparity relationship is unchanged.

---

# 7. Stereo reconstruction

The stereo problem can therefore be viewed as:

```text
Left image       Right image
     ↓                ↓
find corresponding points
          ↓
       disparity
          ↓
      depth estimate
          ↓
       3-D point
```

This is a major conceptual transition:

**single-view image formation gives a ray; stereo gives enough constraints to estimate depth.**

---

# 8. The correspondence problem

The depth equation is easy once the correspondence is known.

The difficult practical problem is:

> Given a pixel in the left image, which pixel in the right image represents the same
> physical point?

This is the **stereo correspondence problem**.

Later computer-vision algorithms solve this using image appearance, local matching,
constraints, and optimization.

The present lecture is primarily establishing the geometric model.

---

# 9. Relation to camera calibration

Stereo depth requires knowledge of camera parameters such as:

- focal length,
- relative camera geometry,
- baseline.

Therefore camera calibration is essential.

The broader pipeline is:

```text
calibrate camera
       ↓
acquire stereo pair
       ↓
find correspondences
       ↓
compute disparity
       ↓
triangulate / recover depth
```

---

# Part VIII — The Complete Conceptual Chain of Lectures 1–15

At this point, the first 15 lectures form one coherent story.

---

## Stage 1 — Why images are processed

### Lectures 1–2

You begin with the motivation:

```text
image
 ↓
improve it / analyze it / extract information / compress it
```

The lecturer introduces the full image-processing pipeline.

---

## Stage 2 — How an image becomes digital

### Lectures 3–6

The physical image:

$$
f(x,y)
$$

is converted to a finite numerical representation.

### Sampling

$$
f(x,y)
\rightarrow
f[m,n]
$$

discretizes space.

### Quantization

$$
f[m,n]
\rightarrow
Q(f[m,n])
$$

discretizes intensity.

### Sampling theory

Ensures that the original signal can be reconstructed when sampled sufficiently densely.

### Quantizer design

Determines how the finite intensity levels should be placed.

---

## Stage 3 — How pixels form meaningful regions

### Lectures 7–9

Now the image is a matrix.

The course defines:

```text
pixels
 ↓
neighborhood
 ↓
adjacency
 ↓
connectivity
 ↓
connected components
```

and then:

```text
pixels
 ↓
distance
 ↓
distance transform
 ↓
shape/skeleton information
```

It also introduces pixel-wise and neighborhood operations.

---

## Stage 4 — How coordinates are transformed

### Lecture 10

The lecturer introduces:

- translation,
- scaling,
- rotation,
- inverse transformations,
- homogeneous coordinates,
- perspective transformation.

These become the mathematical language of camera geometry.

---

## Stage 5 — How cameras form images

### Lectures 11–14

The course asks:

$$
(X,Y,Z)\rightarrow(x,y).
$$

It develops:

- pinhole camera geometry,
- perspective projection,
- world coordinates,
- camera coordinates,
- camera translation,
- camera rotation,
- homogeneous transformations,
- inverse perspective mapping.

---

## Stage 6 — How depth can be recovered

### Lecture 15

A single camera gives a viewing ray.

Two cameras give two rays.

Their relative displacement creates disparity.

Then:

$$
\boxed{
Z=\frac{fB}{d}
}
$$

gives depth under the standard stereo assumptions.

---

# Master Checklist — If You Want to Speedrun Lectures 1–15

## A. Digital image fundamentals

- [ ] Define digital image processing.
- [ ] Explain the three broad motivations for DIP.
- [ ] Explain the complete image-processing pipeline.
- [ ] Distinguish enhancement for humans from machine vision.

## B. Digitization

- [ ] Define $f(x,y)$.
- [ ] Explain sampling.
- [ ] Explain quantization.
- [ ] Explain why both are necessary.
- [ ] Define spatial resolution.
- [ ] Define intensity/gray-level resolution.
- [ ] Explain bandwidth.
- [ ] Explain Fourier spectrum conceptually.
- [ ] State the Nyquist condition.
- [ ] Explain aliasing.
- [ ] Explain spectral replicas caused by sampling.
- [ ] Explain 2-D spatial frequency.

## C. Reconstruction

- [ ] Understand the sampling comb.
- [ ] Understand convolution.
- [ ] Understand multiplication/convolution duality.
- [ ] Understand spectral replication.
- [ ] Understand reconstruction filtering.
- [ ] Extend the idea from 1-D signals to 2-D images.

## D. Quantization

- [ ] Define quantization error.
- [ ] Define transition/decision levels.
- [ ] Define reconstruction levels.
- [ ] Write mean-square error.
- [ ] Understand Lloyd–Max quantization.
- [ ] Know the centroid/conditional-mean reconstruction condition.
- [ ] Know the midpoint decision-level condition.
- [ ] Understand iterative optimization.
- [ ] Understand the uniform-input special case.
- [ ] Know:
  $$
D=\frac{q^2}{12}.
$$
- [ ] Know:
  $$
q=\frac{A}{2^B}.
$$

## E. Pixel relationships

- [ ] 4-neighborhood.
- [ ] Diagonal neighborhood.
- [ ] 8-neighborhood.
- [ ] 4-adjacency.
- [ ] 8-adjacency.
- [ ] m-adjacency.
- [ ] Path.
- [ ] Connectivity.
- [ ] Connected component.
- [ ] Connected-component labeling.
- [ ] Two-pass labeling.
- [ ] Equivalence classes.

## F. Distance and image operations

- [ ] Euclidean distance.
- [ ] City-block distance.
- [ ] Chessboard distance.
- [ ] Distance transform.
- [ ] Skeleton.
- [ ] Pixel-wise arithmetic operations.
- [ ] Pixel-wise logical operations.
- [ ] Neighborhood operations.

## G. Transformations

- [ ] Translation.
- [ ] Scaling.
- [ ] Rotation.
- [ ] Inverse transformations.
- [ ] 2-D transformations.
- [ ] 3-D transformations.
- [ ] Homogeneous coordinates.
- [ ] Transformation composition.
- [ ] Non-commutativity of transformations.
- [ ] Perspective transformation.

## H. Camera geometry

- [ ] World coordinate system.
- [ ] Camera coordinate system.
- [ ] Image coordinate system.
- [ ] Pixel coordinate system.
- [ ] Pinhole camera model.
- [ ] Perspective projection:
  $$
x=fX/Z,\quad y=fY/Z.
$$
- [ ] Camera translation.
- [ ] Camera rotation.
- [ ] Rigid world-to-camera transformation.
- [ ] Inverse perspective transformation.
- [ ] Viewing ray interpretation.

## I. Stereo

- [ ] Stereo camera setup.
- [ ] Corresponding points.
- [ ] Disparity.
- [ ] Baseline.
- [ ] Triangulation intuition.
- [ ] Depth-disparity relationship:
  $$
Z=\frac{fB}{d}.
$$
- [ ] Why large disparity means small depth.
- [ ] Why correspondence is the hard practical problem.

---

# Essential Equations — Lectures 1–15

## Sampling

$$
f[m,n]=f(m\Delta_x,n\Delta_y)
$$

## Nyquist rate

$$
f_s\geq2B
$$

## Quantization error

$$
e=u-u'
$$

## Mean-square quantization error

$$
D=E[(u-u')^2]
$$

## Lloyd–Max reconstruction condition

$$
r_k=
\frac{
\int_{t_k}^{t_{k+1}}u\,p_u(u)\,du
}{
\int_{t_k}^{t_{k+1}}p_u(u)\,du
}
$$

## Lloyd–Max decision condition

$$
t_{k+1}
=
\frac{r_k+r_{k+1}}{2}
$$

## Uniform quantization step

$$
q=\frac{A}{2^B}
$$

## Uniform quantization MSE

$$
D=\frac{q^2}{12}
$$

## Euclidean distance

$$
D_E(p,q)=
\sqrt{(x_1-x_2)^2+(y_1-y_2)^2}
$$

## City-block distance

$$
D_4(p,q)=
|x_1-x_2|+|y_1-y_2|
$$

## Chessboard distance

$$
D_8(p,q)=
\max(|x_1-x_2|,|y_1-y_2|)
$$

## 2-D translation

$$
x'=x+t_x,\qquad y'=y+t_y
$$

## 2-D scaling

$$
x'=s_xx,\qquad y'=s_yy
$$

## 2-D rotation

$$
\begin{bmatrix}
x'\\y'
\end{bmatrix}
=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}
\begin{bmatrix}
x\\y
\end{bmatrix}
$$

## World-to-camera transformation

$$
P_c=RP_w+t
$$

or, depending on the definition of camera center,

$$
P_c=R(P_w-C).
$$

## Perspective projection

$$
x=f\frac{X_c}{Z_c},
\qquad
y=f\frac{Y_c}{Z_c}
$$

## Stereo depth

$$
Z=\frac{fB}{d}.
$$

---

# What Not to Confuse

### Sampling vs quantization

Sampling:

> "Where do I measure?"

Quantization:

> "What numerical value am I allowed to store?"

---

### Neighborhood vs adjacency

Neighborhood:

> spatially nearby locations.

Adjacency:

> a relationship between pixels based on a chosen neighborhood and the relevant pixel set.

---

### Connectivity vs distance

Connectivity asks:

> "Can I get from here to there through valid neighboring pixels?"

Distance asks:

> "How far apart are these two locations according to a chosen metric?"

---

### Perspective projection vs camera pose

Camera pose:

> Where is the camera and how is it oriented?

Perspective projection:

> Given a point in camera coordinates, where does it appear in the image?

---

### Single-view reconstruction vs stereo

Single camera:

$$
\text{pixel}\rightarrow\text{3-D ray}.
$$

Stereo:

$$
\text{two pixels}\rightarrow\text{two rays}\rightarrow\text{3-D point/depth}.
$$

---

# The Main Story to Remember

If you remember only one conceptual chain from the first 15 lectures, remember this:

$$
\boxed{
\text{Physical scene}
\rightarrow
\text{continuous image}
\rightarrow
\text{sampling}
\rightarrow
\text{quantization}
\rightarrow
\text{digital image}
}
$$

Then:

$$
\boxed{
\text{digital pixels}
\rightarrow
\text{neighborhood}
\rightarrow
\text{connectivity}
\rightarrow
\text{regions / objects}
}
$$

Then:

$$
\boxed{
\text{coordinates}
\rightarrow
\text{transformations}
\rightarrow
\text{camera}
\rightarrow
\text{projection}
}
$$

And finally:

$$
\boxed{
\text{two projections}
\rightarrow
\text{disparity}
\rightarrow
\text{depth}
\rightarrow
\text{3-D reconstruction}.
}
$$

That is the conceptual progression that the lecturer is building across Lectures 1–15.

---

# Source / Verification Notes

The lecture sequence and titles were cross-checked against the official NPTEL course listing
for **Digital Image Processing, IIT Kharagpur, Prof. Prabir Kumar Biswas**, as well as NPTEL
course mirrors and indexed lecture transcripts.

In particular, the official NPTEL listing confirms the sequence through Lecture 15:
Introduction → Applications → Digitization → Reconstruction → Quantizer Design → Pixel
Relationships → Connected Components → Distance Measures → Basic Transform → Image Formation
→ Image Geometry → Stereo Imaging.

Indexed transcript material was also used to preserve the lecturer's actual progression, including
the sampling/aliasing discussion, Lloyd–Max quantizer conditions, connected-component labeling,
distance transforms/skeletonization, homogeneous transformations, generalized camera geometry,
and stereo imaging.

**Important:** these notes are a detailed paraphrased study document. They are not a verbatim
transcript of the lectures.
