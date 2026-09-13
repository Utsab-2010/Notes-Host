---
title: "Kolmogorov-Smirnov Test"
lastmod: 2026-07-23
---

# What Problem It's Solving

You have a sample of data and you want to answer: "does this data come from some specific distribution?" or "do these two samples come from the _same_ distribution?" The KS test answers exactly this, and the reason it's nice is that it's **nonparametric** — it doesn't assume your data is Gaussian or anything else. It works directly off the empirical CDF, so it makes almost no assumptions about the underlying distribution shape.

Two flavors:

- **One-sample KS test**: compare your sample's distribution against a known reference distribution (e.g. "is this data Normal(0,1)?")
- **Two-sample KS test**: compare two samples against each other (e.g. "did these two experiments produce data from the same distribution?") — this is the one that shows up constantly in practice.

## The Core Idea

Build the **empirical CDF (ECDF)** of your sample(s) — literally just, for each point $x$, what fraction of your data is $\leq x$. It's a step function that climbs from 0 to 1.

The KS statistic is just the **maximum vertical distance** between two ECDFs (or between your ECDF and the reference CDF):

$$D = \sup_x |F_1(x) - F_2(x)|$$

That's the whole test. No means, no variances, no binning — just literally the biggest gap between the two cumulative curves, measured anywhere along the x-axis.

Intuition: if two samples come from the same distribution, their ECDFs should track each other closely everywhere, so $D$ should be small. If they come from different distributions — different mean, different spread, different shape, different skew, anything — the ECDFs will diverge somewhere, and $D$ picks that up regardless of _what kind_ of difference it is. This is the whole appeal over something like a t-test: a t-test only catches a difference in means; KS catches differences in shape, spread, skew, tails, anything, because it's comparing the entire distribution curve, not a single summary statistic.

## Why the Max, Specifically

This is the part that's easy to skim past but is actually the clever bit. Why not compare the average gap between the CDFs, or the area between them (which would be more like a Wasserstein-style distance)?

Using the max makes the null distribution of $D$ **distribution-free** — meaning if the null hypothesis is true (samples really are from the same distribution), the distribution of $D$ doesn't depend on what that underlying distribution actually is. This falls out of a classical result (Kolmogorov's theorem / the Donsker invariance principle, if you want the heavier version): properly rescaled, $\sqrt{n} D$ converges to the same universal distribution (the Kolmogorov distribution) no matter what continuous distribution the data actually comes from. That's what lets you get a clean, universal p-value/critical-value table instead of needing a different table for every possible reference distribution. That's the real reason KS is popular — you get an assumption-light test with a plug-and-play significance threshold.

## The Test Statistic and Decision Rule

$$D_{n,m} = \sup_x |F_n(x) - F_m(x)|$$

for sample sizes $n$ and $m$. Reject the null (samples are from the same distribution) if $D$ exceeds a critical value that depends on $n$, $m$, and your significance level $\alpha$ — roughly:

$$D_{\text{crit}} \approx c(\alpha)\sqrt{\dfrac{n+m}{nm}}$$

where $c(\alpha)$ comes from the Kolmogorov distribution (e.g. $c(0.05) \approx 1.36$). Bigger $D$ than this threshold → statistically significant evidence the distributions differ.

# What It's Good At vs Bad At

**Good at:**

- Detecting _any_ kind of distributional difference (location, scale, shape) without having to specify in advance which one you're looking for
- Works with continuous data without needing to bin it (unlike a chi-squared goodness-of-fit test)
- No distributional assumptions on the data itself

**Bad at / gotchas:**

- **Less sensitive in the tails.** The ECDF has less data density out in the tails, so KS is comparatively weaker at catching differences that live specifically in the tails (which, annoyingly, is often exactly where you care most — e.g. detecting rare/extreme-event differences). This is a well-known blind spot.
- **Not great with discrete data** — the theory assumes continuous distributions; with ties/discreteness the null distribution of $D$ isn't exactly right anymore (there are corrected variants, but vanilla KS gets shaky).
- **Doesn't tell you _how_ the distributions differ**, just _that_ they differ. A big $D$ could be driven by a mean shift, a variance change, a skew difference, or a weird bump in the middle — you'd need to actually look at the ECDFs (or follow up with other tests) to diagnose which.
- Sensitive to sample size in a way people misuse: with huge $n$, even a trivial, practically-meaningless distributional difference will become "statistically significant." Worth remembering the p-value here answers "is there _any_ detectable difference," not "is the difference large or important."

## Where I've Actually Seen It Used in ML Contexts

- **Dataset drift / distribution shift detection.** Comparing feature distributions between training data and production/serving data over time — if KS statistic between train-time and current feature distribution crosses a threshold, that's a common trigger for "retrain the model" alerts in MLOps pipelines.
- **Comparing pruned vs full dataset distributions** — directly relevant to what I've been doing with data pruning: could sanity check whether a pruned subset (e.g. after EL2N pruning) preserves the same per-feature or per-class distribution as the full dataset, or whether pruning is systematically distorting the input distribution. This seems like a genuinely useful quick diagnostic to bolt onto the Zipf-slope analysis — cheap to compute, orthogonal signal to the log-log Zipf plots.
- **GAN evaluation** — comparing the distribution of generated samples against real samples along some scalar projection (e.g. a learned feature, or a pixel intensity histogram) as a quick, non-fancy alternative/complement to FID.
- **A/B testing** — checking whether two experiment arms actually produced comparably-distributed outcome data, not just comparable means.

## Connecting Back

- FID note → FID is basically doing a related job (comparing real vs generated distributions) but assumes Gaussian structure in feature space and uses Fréchet distance instead of the KS sup-difference; KS is the assumption-free, cruder cousin
- data pruning / Zipf slope work → worth actually trying KS between full-data and pruned-data feature distributions as a cheap side-check next time I'm benchmarking EL2N vs random pruning
- scaling laws note → distribution shift context is relevant if pruning methods are implicitly changing the input distribution rather than purely selecting "hard/easy" examples — KS gives a way to quantify that directly instead of just eyeballing histograms