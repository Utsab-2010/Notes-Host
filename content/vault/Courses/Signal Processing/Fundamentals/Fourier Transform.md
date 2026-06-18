---
title: "Fourier Transform"
---

# Fourier Transform — simple explanation **with equations** 🎧📐

This note keeps the math **clean and minimal**, and every equation is paired with intuition.

---

## 1. Big picture (again, but mathematically)
The **Fourier Transform (FT)** converts a signal from:

- **Time domain** → `x(t)`
- **Frequency domain** → `X(f)` or `X(ω)`

It answers:
> “How much of each frequency is present in the signal?”

---

## 2. Fourier Series (where everything starts)
For a **periodic signal** with period `T`, we write it as a sum of sinusoids:

$$
x(t) = \sum_{k=-\infty}^{\infty} c_k e^{j 2\pi k f_0 t}
$$

where  
$$f_0 = \frac{1}{T}$$

and the coefficients are:

$$
c_k = \frac{1}{T} \int_{T} x(t)\, e^{-j 2\pi k f_0 t}\, dt

$$


🔹 **Meaning**:  
Each `c_k` tells **how much of frequency `k f₀`** is present.

---

## 3. From Fourier Series → Fourier Transform
What if the signal is **not periodic**?

Idea:
- Let the period `T → ∞`
- Frequency spacing `f₀ → 0`
- Discrete frequencies become **continuous**

That converts the sum into an integral.

---

## 4. Fourier Transform (continuous-time)

### Forward Fourier Transform
$$X(f) = \int_{-\infty}^{\infty} x(t)\, e^{-j 2\pi f t}\, dt$$ 
or using angular frequency `ω = 2πf`:

$$
X(\omega) = \int_{-\infty}^{\infty} x(t)\, e^{-j \omega t}\, dt
$$

🔹 **Interpretation**:
- Multiply the signal by a complex sinusoid
- Integrate → measure similarity
- Result = strength of frequency `f`

---

### Inverse Fourier Transform
\[
x(t) = \int_{-\infty}^{\infty} X(f)\, e^{j 2\pi f t}\, df
\]

(or)

\[
x(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} X(\omega)\, e^{j \omega t}\, d\omega
\]

🔹 **Meaning**:  
Add back **all frequencies** to reconstruct the signal.

---

## 5. What is `X(f)` exactly?
`X(f)` is **complex**:

$$
X(f) = |X(f)| e^{j \angle X(f)}
$$

- `|X(f)|` → **Magnitude spectrum** (strength)
- `∠X(f)` → **Phase spectrum** (timing info)

Most plots show only `|X(f)|`.

---

## 6. Discrete Fourier Transform (DFT)
Computers work with **samples**, not continuous signals.

Given `N` samples `x[n]`, the DFT is:

$$
X[k] = \sum_{n=0}^{N-1} x[n]\, e^{-j \frac{2\pi}{N} k n}
$$

where:
- `n` → time index
- `k` → frequency bin
- Total bins = `N`

---

### Inverse DFT
\[
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k]\, e^{j \frac{2\pi}{N} k n}
\]

---

## 7. FFT (important clarification ⚡)
- **FFT** is **NOT a new formula**
- It is a **fast algorithm** to compute the DFT

Mathematically:
\[
\text{FFT} \equiv \text{DFT}
\]

Difference is only **speed**, not result.

---

## 8. Frequency resolution (very important)
For DFT:

\[
\Delta f = \frac{f_s}{N}
\]

where:
- `f_s` = sampling frequency
- `N` = number of samples

🔹 More samples ⇒ better frequency resolution  
🔹 Zero-padding improves **visual smoothness**, not true resolution

---

## 9. One-line intuition for the equations 🧠
\[
X(f) = \int x(t)\, e^{-j 2\pi f t}\, dt
\]

=  
**“Slide a sine wave of frequency `f` over the signal and measure how well it matches.”**

---

## 10. Ultra-short summary
- Fourier Series → periodic signals
- Fourier Transform → non-periodic signals
- DFT → sampled signals
- FFT → fast way to compute DFT

---

If you want next:
- 🔁 **Derivation: Fourier Series → FT step-by-step**
- 🔍 **Physical meaning of phase**
- 🧮 **DFT bins, leakage, windowing**
- 🧠 **FFT as filtering operation**

Just say th
