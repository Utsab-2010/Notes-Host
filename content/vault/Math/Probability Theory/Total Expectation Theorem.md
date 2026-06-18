---
title: "Total Expectation Theorem"
---

## Law of Total Expectation (Partition of Events)

$$  
\text{Let } {A_1, A_2, \dots, A_n} \text{ be a partition of } \Omega  
\text{ with } P(A_i) > 0.  
$$

$$\large  
\mathbb{E}[X]  
= \sum_{i=1}^{n} \mathbb{E}[X \mid A_i] . P(A_i)  
$$

---

### Law of Total Expectation (Conditioning on a Discrete Random Variable)

$$\large
\mathbb{E}[X]  
= \sum_{y} \mathbb{E}[X \mid Y = y]. P(Y = y)  
$$

---

## Law of Iterated Expectation (General / Tower Property)

$$  \large
\mathbb{E}[X]  
= \mathbb{E}\left[\mathbb{E}[X \mid Y] \right]  
$$

---

## Law of Total Expectation (Continuous Case)

$$ \large  
\mathbb{E}[X]  
= \int_{-\infty}^{\infty} \mathbb{E}[X \mid Y = y] , f_Y(y), dy  
$$

---

## Conditional Law of Total Expectation

$$  \large
\mathbb{E}[X \mid Z]  
= \mathbb{E}\left[ \mathbb{E}[X \mid Y, Z] \mid Z \right]  
$$

---
## Conditional Event-Based Version

Let (A) be an event with $\mathbb{P}(A) > 0$ and let ${E_1, E_2, \dots, E_n}$ be a **partition of (A)**.

$$  
\mathbb{E}[X \mid A]
=
\sum_{i=1}^{n}  
\mathbb{P}(E_i \mid A).  
\mathbb{E}[X \mid A \cap E_i]  
$$

---
