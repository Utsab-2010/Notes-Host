---
title: "Well Known Distributions"
---


### 1. Bernoulli Distribution

**Use case:** Single experiment with success/failure

**PMF**  
$$
P(X = 1) = p, \quad P(X = 0) = 1 - p  
$$

**Mean**   $\mathbb{E}[X] = p$
**Variance**  $\mathrm{Var}(X) = p(1 - p)$
**Special Properties**
- Indicator random variable
- Building block of Binomial distribution

---

### 2. Binomial Distribution

**Use case:** Number of successes in (n) independent Bernoulli trials

**PMF**  
$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}  
$$
**Mean**  $np$
**Variance**  $np(1-p)$

**Special Properties**

- Sum of Bernoulli random variables
-  Approximated by Poisson (small (p)) and Normal (large (n))
---

### 3. Geometric Distribution

**Use case:** Number of trials until first success

**PMF**  
$$  
P(X = k) = (1-p)^{k-1}p, \quad k \ge 1  
$$

**Mean**  $\frac{1}{p}$
**Variance**  $\frac{1-p}{p^2}$

**Special Properties**
- Memoryless:  $$ 
    P(X > s+t \mid X > s) = P(X > t)  
    $$

---

### 4. Poisson Distribution

**Use case:** Number of events in fixed time or space interval

**PMF**  
$$
P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}  $$

**Mean**   $\lambda$
**Variance**  $\lambda$

**Special Properties**
- Independent increments
- limit of Binomial distribution

---

### 5. Discrete Uniform Distribution

**Use case:** All outcomes equally likely

**PMF**  
[  
P(X = k) = \frac{1}{n}, \quad k = 1,2,\dots,n  
]

**Mean**  
[  
\frac{n+1}{2}  
]

**Variance**  
[  
\frac{n^2 - 1}{12}  
]

---

## 🔹 Continuous Distributions

---

### 6. Continuous Uniform Distribution

**Use case:** Random variable over an interval

**PDF**  
[  
f(x) = \frac{1}{b-a}, \quad a \le x \le b  
]

**CDF**  
[  
F(x) = \frac{x-a}{b-a}  
]

**Mean**  
[  
\frac{a+b}{2}  
]

**Variance**  
[  
\frac{(b-a)^2}{12}  
]

---

### 7. Exponential Distribution

**Use case:** Waiting time until next event

**PDF**  $$
f(x) = \lambda e^{-\lambda x}, \quad x \ge 0  
$$

**CDF**  $$
F(x) = 1 - e^{-\lambda x}  
$$

**Mean**  $\frac{1}{\lambda}$

**Variance**  $\frac{1}{\lambda^2}$

**Special Properties**
- Memoryless (continuous analogue of Geometric)

---

### 8. Normal (Gaussian) Distribution

**Use case:** Noise, natural variation, measurement errors

**PDF**  $$

f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}  
$$

**Mean**  $\mu$
**Variance**  \sigma^2$

**Special Properties**
- Central Limit Theorem
- Fully determined by mean and variance
- Symmetric bell-shaped curve

---

### 9. Gamma Distribution

**Use case:** Waiting time until (k) events

**PDF**  
[  
f(x) = \frac{\lambda^k x^{k-1} e^{-\lambda x}}{\Gamma(k)}  
]

**Mean**  
[  
\frac{k}{\lambda}  
]

**Variance**  
[  
\frac{k}{\lambda^2}  
]

**Special Properties**

- Generalizes Exponential distribution
    

---

### 10. Chi-Square Distribution

**Use case:** Sum of squared standard normals

**Definition**  
[  
X = \sum_{i=1}^k Z_i^2, \quad Z_i \sim \mathcal{N}(0,1)  
]

**Mean**  
[  
k  
]

**Variance**  
[  
2k  
]

**Special Properties**

- Used in hypothesis testing
    
- Special case of Gamma distribution
    

---

### 11. Student’s t Distribution

**Use case:** Mean estimation with small samples

**Mean**  
[  
0 \quad (k > 1)  
]

**Variance**  
[  
\frac{k}{k-2} \quad (k > 2)  
]

**Special Properties**

- Heavier tails than Normal
    
- Converges to Normal as (k \to \infty)
    

---

### 12. Beta Distribution

**Use case:** Random variables on ([0,1]), Bayesian priors

**PDF**  
[  
f(x) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}  
]

**Mean**  
[  
\frac{\alpha}{\alpha + \beta}  
]

**Variance**  
[  
\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}  
]
