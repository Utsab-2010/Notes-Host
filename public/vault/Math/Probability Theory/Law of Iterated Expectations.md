---
title: "Law of Iterated Expectations"
lastmod: 2026-05-30
---

## Mathematical Definition

For any two random variables $X$ and $Y$, the law states:

$$E[X] = E[E[X|Y]]$$

### Breaking down the notation:

- **$E[X|Y]$ (The "Inner" Expectation):** This is the average of $X$ given that you already know the value of $Y$. It is a function of $Y$, meaning it varies depending on what $Y$ is.
- **$E[\dots]$ (The "Outer" Expectation):** This takes the average of all those conditional results, weighted by the probability of each $Y$ occurring.
- **The Result:** The conditioning on $Y$ is "averaged out," leaving you with the true total mean of $X$.

## Application to Cumulative Distribution Functions (CDFs)

As seen in the derivation from your handwritten note, this law is often applied to probabilities (since a probability is just the expectation of an indicator function).

**The Equation:**

$$F_Z(z) = P(Z \le z) = E_C[P(Z \le z | C)]$$

### Why this matters:

- **Simplification:** Often, it is mathematically "messy" to find the distribution of $Z$ directly. However, if you assume some context $C$ is known, the distribution might become a simple Normal or Bernoulli distribution.
- **Eliminating Latent Variables:** Once you've solved the conditional probability, the outer expectation $E_C$ allows you to mathematically remove the "helper" variable $C$, leaving you with the final marginal distribution.
- **Independence:** This is why the note concludes that the result **"will not depend on C"**—the variable $C$ has been integrated/averaged out of the final equation.