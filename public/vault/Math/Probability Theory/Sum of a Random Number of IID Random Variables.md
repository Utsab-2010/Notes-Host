---
title: "Sum of a Random Number of IID Random Variables"
lastmod: 2026-07-27
---

## The Setup
Normally when you sum random variables, $Y = X_1 + \cdots + X_n$, the number of terms $n$ is fixed and known in advance. This note is about the twist where the number of terms is _itself random_:

$$Y = X_1 + X_2 + \cdots + X_N$$

where $N$ is a random variable taking nonnegative integer values, and $X_1, X_2, \dots$ are i.i.d. Crucially, $N$ is assumed **independent** of the $X_i$'s — how many terms you sum doesn't depend on what those terms turn out to be.

This shows up constantly once you look for it: total claims paid out by an insurer (random number of claims, each a random size), total time spent searching across a random number of stores, total load on a server from a random number of incoming jobs each with random size.

#### Main Properties:
$$\large \boxed{E[Y] = \mu E[N]}$$
$$\large \boxed{\text{Var}(Y) = E[N]\sigma^2 + \mu^2\text{Var}(N)}$$
$$\boxed{M_Y(s) = M_N(s)\Big|_{e^s ,\to, M_X(s)}}$$

---
# Why You Can't Just Plug In $E[N]$

The tempting shortcut is: "just replace $N$ by its average and sum that many terms." This is wrong, and worth seeing _why_ it's wrong rather than just being told so.

Take $X_i \sim \text{Uniform}(0,1)$, and let $N$ be either $1$ or $3$, each with probability $1/2$. Then $E[N] = 2$.

- The **actual** random sum $Y = X_1 + \cdots + X_N$ takes values anywhere in $[0,3]$ (since sometimes you're summing 3 terms), and its distribution is literally a 50/50 mixture: half the time it's just $X_1$ (uniform on $[0,1]$), half the time it's $X_1+X_2+X_3$ (a triangular-ish distribution on $[0,3]$).
- If you'd instead just plugged in $E[N]=2$ and computed $X_1+X_2$, you'd get a completely different, single triangular distribution confined to $[0,2]$.

These aren't close. The lesson: **the randomness of $N$ doesn't just add noise around the "plug in the mean" answer — it can change the entire shape and support of the distribution.** So random-$N$ sums genuinely need their own machinery; you can't fake it by conditioning on the mean.


---
# Strategy: Condition on $N$, Then Un-Condition

The whole derivation follows one clean pattern that's worth internalizing because it recurs everywhere in probability: **fix $N=n$ (a known, ordinary sum), work out what you want in that easy case, then average over $N$ using the law of iterated expectations / law of total variance.**

This works because once you condition on ${N=n}$, and using the assumed independence of $N$ from the $X_i$'s, the quantity $X_1+\cdots+X_n$ behaves exactly like an ordinary fixed-length sum — independent of the conditioning event itself. That's the technical justification for why conditioning cleanly separates the two sources of randomness (how many terms, and what the terms are).

## Mean of $Y$

Condition on $N=n$: given that, $Y$ is just the fixed sum $X_1+\cdots+X_n$, so $$E[Y \mid N=n] = n\mu$$ where $\mu = E[X_i]$ is the common mean. Since this holds for every value of $n$, we can write it as a statement about random variables: $$E[Y\mid N] = N\mu$$ Now apply the law of iterated expectations ($E[Y] = E[E[Y|N]]$): $$\large \boxed{E[Y] = \mu E[N]}$$

Reassuringly simple — the mean _does_ behave like "plug in $E[N]$," even though (as the counterexample above shows) the full distribution absolutely does not.

## Variance of $Y$

Same conditioning move, now for variance. Given $N=n$, since the $X_i$ are independent of each other: $$\text{Var}(Y\mid N=n) = n\sigma^2$$ so as a random variable, $\text{Var}(Y\mid N) = N\sigma^2$.

To combine this into an unconditional variance you need the **law of total variance**: $$\text{Var}(Y) = E[\text{Var}(Y\mid N)] + \text{Var}(E[Y\mid N])$$

Plug in both pieces — $E[\text{Var}(Y|N)] = E[N]\sigma^2$, and $\text{Var}(E[Y|N]) = \text{Var}(N\mu) = \mu^2\text{Var}(N)$:

$$\large \boxed{\text{Var}(Y) = E[N]\sigma^2 + \mu^2\text{Var}(N)}$$

Notice the two terms have a clean interpretation:

- $E[N]\sigma^2$ — the variance you'd expect from summing a fixed (average) number of random terms
- $\mu^2\text{Var}(N)$ — **extra** variance purely because the number of terms itself is uncertain

This second term is exactly the piece that "plug in $E[N]$" reasoning silently throws away — and it's why the random-$N$ sum always has _at least_ as much variance as the naive fixed-$n$ version, often a lot more.

## Transform (MGF) of $Y$

This is the cleanest and most useful result of the three, and the reason it's worth carrying the transform machinery around at all: it turns a messy convolution problem into simple substitution.

Condition on $N=n$: $Y$ is a fixed sum of $n$ i.i.d. terms, so its transform is just the $n$-th power of the single-term transform: $$E[e^{sY}\mid N=n] = \big(M_X(s)\big)^n$$

Un-condition using the law of iterated expectations: $$M_Y(s) = E[e^{sY}] = E\big[(M_X(s))^N\big] = \sum_{n=0}^\infty (M_X(s))^n, p_N(n)$$

Look closely at what this actually says: this is exactly the formula for $M_N(s) = E[e^{sN}]$, **except every $e^s$ has been replaced by $M_X(s)$**. That's the whole recipe in one sentence:

$$\boxed{M_Y(s) = M_N(s)\Big|_{e^s ,\to, M_X(s)}}$$

Once you have $M_N$ and $M_X$ in closed form, you get $M_Y$ almost by inspection — no need to redo the conditioning argument each time.

---
# Worked Examples

**Gas stations (a finite, concrete case).** Three gas stations, each open independently with probability $1/2$; amount of gas at an open station is Uniform$(0, 1000)$. Number of open stations $N \sim \text{Binomial}(3, 1/2)$, so $M_N(s) = \frac{1}{8}(1+e^s)^3$. Substituting $M_X(s)$ (the Uniform MGF) for every $e^s$ gives the transform of the total gas available directly — no need to separately work out the mixture-of-sums distribution by hand.

**Geometric number of exponential waiting times (the elegant case).** Jane visits bookstores looking for a book. Each store carries it independently with probability $p$; time spent per store is $\text{Exponential}(\lambda)$; she stops as soon as she finds it. Number of stores visited $N \sim \text{Geometric}(p)$.

- $E[Y] = E[N]E[X] = \frac{1}{p}\cdot\frac{1}{\lambda}$
- $\text{Var}(Y) = E[N]\text{Var}(X) + (E[X])^2\text{Var}(N) = \frac{1}{p\lambda^2} + \frac{1}{\lambda^2}\cdot\frac{1-p}{p^2} = \frac{1}{\lambda^2 p^2}$
- Substituting $M_X(s) = \frac{\lambda}{\lambda-s}$ into $M_N(s) = \frac{pe^s}{1-(1-p)e^s}$ and simplifying collapses down to $$M_Y(s) = \frac{p\lambda}{p\lambda - s}$$ which is recognizably the MGF of an **Exponential$(p\lambda)$** random variable.

This is a genuinely surprising and pretty result: **a Geometric-many sum of Exponentials is itself exactly Exponential** (just with a rescaled rate $p\lambda$), even though summing a _fixed_ number $n\ge 2$ of Exponentials is emphatically not exponential anymore (it becomes an Erlang/Gamma distribution instead). The randomness in $N$ is doing something special here — it's not adding "extra shape," it's collapsing the sum back down to the same family it started in. This only works because Geometric is the discrete analogue of Exponential's memorylessness; the two memoryless distributions pairing up is what makes the closure happen.

**Geometric number of Geometric random variables (discrete mirror image).** Same setup, discrete version: $N\sim\text{Geometric}(p)$, each $X_i\sim\text{Geometric}(q)$, all independent. Same substitution trick on the transforms gives $$M_Y(s) = \frac{(pq) e^s}{1-(1-pq)e^s}$$ which is exactly the MGF of a **Geometric$(pq)$** random variable. Same phenomenon as above, same reason — memorylessness of Geometric composing with memorylessness of Geometric to stay inside the same family, just with the parameters multiplying together.

