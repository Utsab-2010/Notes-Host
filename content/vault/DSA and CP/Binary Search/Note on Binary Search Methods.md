---
title: "Note on Binary Search Methods"
lastmod: 2026-06-22
---

# L<=R vs L < R - When to use which one?
Yeah that's a common trap — `L <= R` is the more "natural" feeling loop because it feels exhaustive, but it's actually the harder variant to get right for this class of problems.

Quick mental model for when to use which:

**`L <= R`** — you're searching for an **exact target**. Loop ends when the space is empty, you return inside the loop when you find it. Classic binary search on a sorted array.

**`L < R`** — you're searching for a **position/condition**. Loop ends when `L == R`, which is your answer. No need to return inside — the convergence _is_ the answer.

This problem is the second type — you're not looking for a specific value, you're converging on a position that satisfies a property. So `L < R` fits naturally and the boundary math just works out clean.

Rule of thumb: if you're writing `return mid` inside the loop, `L <= R` is fine. If you find yourself wanting to `return L` after the loop, switch to `L < R`.