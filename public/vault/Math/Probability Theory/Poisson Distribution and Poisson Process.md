---
title: "Poisson Distribution and Poisson Process"
lastmod: 2026-07-27
---


# Definition

It is a discrete value distribution given by 
$$\large P(X = k) = \frac{e^{-\lambda}\lambda^k}{k!}$$
where k is the number of events. It is used to describe **the number of events that happen (independently and one at a time) in a fixed time interval when the average event rate per interval is given by $\lambda$.**

# Derivation and Intuition
**Start With Binomial**
Binomial$(n, p)$ counts successes out of $n$ independent trials, each with success probability $p$, mean $np$.

Now ask a different kind of question: instead of "how many successes out of $n$ trials," ask "how many events happen in a fixed time window?" — how many customers walk into a shop in an hour, how many typos are on a page, how many radioactive decays happen in a second.

To connect the two, chop the hour into a huge number of tiny slices — say $n = 3600$ one-second slices. In each tiny slice, either a customer arrives or doesn't (roughly a coin flip with small probability $p$). So "arrivals in an hour" looks like Binomial$(n, p)$ with $n$ huge and $p$ tiny, but $np = \lambda$ (the average rate) staying fixed.

![771|681x410](/vault/attachments/pasted-image-20260727192158.png)
**Poisson is what Binomial becomes when $n \to \infty$, $p \to 0$, with $np \to \lambda$ held fixed.** Taking that limit of the binomial PMF collapses it into:

$$P(X = k) = \frac{e^{-\lambda}\lambda^k}{k!}$$

## The Intuition, Stated Plainly
Poisson answers: **"if events happen at some average rate $\lambda$ over an interval, independently and one at a time, how many will actually occur?"**

$\lambda$ does double duty — it's both the mean and the variance: $$E[X] = \text{Var}(X) = \lambda$$

This is a distinctive fingerprint: if a count-based dataset has variance roughly equal to its mean, that's a strong hint it might be Poisson.

**Why mean = variance?** Chase it back to the Binomial limit. Binomial has mean $np$ and variance $np(1-p)$. As $p \to 0$, $(1-p) \to 1$, so variance $\to np$ = mean. The shrinking variance gap is a direct trace of where Poisson came from.

## Why the Formula Looks the Way It Does

Don't just memorize $e^{-\lambda}\lambda^k/k!$ — it falls straight out of a Taylor series you already know:

$$e^\lambda = \sum_{k=0}^\infty \frac{\lambda^k}{k!}$$

Poisson probabilities are literally these terms, normalized by dividing by $e^\lambda$ so they sum to 1:

$$P(X=k) = \frac{\lambda^k/k!}{e^\lambda} = \frac{\lambda^k e^{-\lambda}}{k!}$$

The whole PMF is just "take the terms of $e^\lambda$'s expansion and turn them into probabilities."

---

# The Poisson Process

The Poisson **distribution** gives the count in one fixed window. The Poisson **process** describes the entire timeline of random events — Poisson-distributed counts fall out of it as a consequence.

A Poisson process with rate $\lambda$ (events per unit time) is defined by three properties:

1. **Independent increments** — what happens in one time window tells you nothing about a disjoint window. Arrivals from 2–3pm are independent of arrivals from 3–4pm.
2. **Stationary increments** — the _distribution_ of counts depends only on window length, not on where it starts. Any 1-hour window looks statistically the same (assuming a _homogeneous_ rate — see extensions below).
3. **No simultaneous events / rare events in small windows** — in a tiny interval $dt$: $P(\text{exactly one event}) \approx \lambda, dt$, $P(\text{2+ events})$ is negligible (order $dt^2$), $P(\text{0 events}) \approx 1 - \lambda, dt$.

Property 3 is the real engine — it's the binomial-limit story again, now over continuous time: chop $[0, t]$ into $n$ tiny slices of length $dt = t/n$, treat each as an independent coin flip with success probability $\lambda, dt$, sum them, and as $n \to \infty$ the count over $[0,t]$ converges to Poisson$(\lambda t)$.

## The Two Faces of the Same Object

A Poisson process can be described by either of two equivalent random quantities — switching between them is the main technical skill.

**Face 1 — Counts.** Number of events in $[0, t]$ is $$N(t) \sim \text{Poisson}(\lambda t)$$

**Face 2 — Waiting times.** The gap between consecutive events (interarrival time) is $$T \sim \text{Exponential}(\lambda)$$ and these gaps are **independent** of each other.

**Why exponential specifically?** It comes from the memorylessness baked into property 3: $P(\text{no event in } dt) \approx e^{-\lambda, dt}$. Chain this over $[0, t]$: probability of zero events in $[0,t]$ is $e^{-\lambda t}$ — which is exactly $P(\text{first arrival time} > t)$ for an Exponential$(\lambda)$ variable. So "count is Poisson" and "gaps are Exponential" are the same fact seen from two angles: one discrete and additive (counting), one continuous and multiplicative (waiting).

This is also why Exponential is **memoryless**: if you've waited 10 minutes for a bus with no arrival, the distribution of _additional_ waiting time is identical to having just started waiting. The process has no memory of elapsed time — a direct consequence of independent increments.

## Why "Rare Events" Keep Showing Up as Poisson

Poisson is often called "the distribution of rare events" — radioactive decay, typos per page, server crashes, mutations per genome, calls to a call center. This isn't mystical: it's the **law of rare events**, which is really the Binomial-limit derivation restated. Whenever there's a _huge_ number of "opportunities" for something to happen, each with a _tiny_ individual probability, and these opportunities are roughly independent, the total count is well-approximated by Poisson — regardless of the messy micro-level details of what's actually happening. This is a genuine universality result, similar in flavor to why Gaussians show up everywhere via CLT, except Poisson is the limiting law for rare discrete counts rather than averaged continuous quantities.

## Useful Extensions

- **Inhomogeneous Poisson process** — rate $\lambda(t)$ varies over time (e.g. website traffic higher at noon than 3am). Stationary increments is lost, independent increments is kept; counts over $[0,t]$ become Poisson with mean $\int_0^t \lambda(s), ds$ instead of $\lambda t$.
- **Superposition** — merge two independent Poisson processes with rates $\lambda_1, \lambda_2$ and the result is a Poisson process with rate $\lambda_1 + \lambda_2$. Rates just add.
- **Thinning** — randomly keep each event independently with probability $p$ (e.g. random subsampling of arrivals); what's left is still a Poisson process, now with rate $\lambda p$.

## Scenarios to Anchor Intuition

|Scenario|What plays the role of $\lambda$|Poisson answers|
|---|---|---|
|Customers arriving at a shop|Average arrivals per hour|P(exactly $k$ customers in an hour)|
|Typos on a page|Average typos per page|P(exactly $k$ typos on a given page)|
|Radioactive decay|Average decays per second|P(exactly $k$ decays in a second)|
|Server crashes|Average crashes per month|P(exactly $k$ crashes in a month)|
|Mutations along a genome|Average mutations per unit length|P(exactly $k$ mutations in a segment)|
|Calls to a call center|Average calls per minute|P(exactly $k$ calls in a minute), and gaps between calls are Exponential|

In every row: a large number of "chances" for the event, each individually unlikely, roughly independent of each other — that's the signature that says "try Poisson first."

## Connecting Back

- modes of convergence note → the Binomial-to-Poisson limit here is a concrete instance of convergence in distribution, same flavor of statement as CLT, just landing on Poisson instead of Gaussian as the limiting law
- KS test note → Poisson process counts are a natural place to sanity-check "is my event data actually Poisson" — e.g. checking if interarrival times look Exponential via a KS test against the Exponential CDF
- scaling laws / data work → if modeling rare failure events (bad training runs, corrupted samples, outlier gradients) as roughly independent rare occurrences, Poisson/Exponential machinery is the natural first model before reaching for anything fancier