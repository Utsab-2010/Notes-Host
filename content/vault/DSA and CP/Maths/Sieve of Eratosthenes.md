---
title: "Sieve of Eratosthenes"
---

A classic algorithm to find **all prime numbers up to a limit N** efficiently.

---
## Core Idea

Start by assuming every number ≥ 2 is prime. Then, for each prime you find, **mark all its multiples as not prime**. What's left unmarked at the end is your list of primes.

---

## Algorithm

1. Create a boolean array `is_prime[0..N]`, initialized to `True`.
2. Set `is_prime[0] = is_prime[1] = False`.
3. For each `i` from `2` to `√N`:
   - If `is_prime[i]` is still `True`, mark all multiples of `i` starting from `i*i` as `False`.
4. All indices still marked `True` are prime.

> **Why start marking from `i*i`?**
> Any smaller multiple of `i` (like `2*i`, `3*i`, ...) would have already been marked by a smaller prime earlier. So `i*i` is the first unmarked multiple that needs attention.

---

## Implementation

```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(n+1) if is_prime[i]]

print(sieve(30))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

---

## Complexity

| | Value |
|---|---|
| Time | O(N log log N) |
| Space | O(N) |

The time complexity comes from the harmonic series of primes: `N/2 + N/3 + N/5 + ...` which converges to `O(N log log N)` — essentially linear in practice.

---

## Useful Variants

### Smallest Prime Factor (SPF) Sieve
Instead of just marking composites, store the **smallest prime factor** of every number. Enables O(log n) factorization of any number up to N.

```python
def spf_sieve(n):
    spf = list(range(n + 1))  # spf[i] = i initially
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i*i, n+1, i):
                if spf[j] == j:  # not yet assigned
                    spf[j] = i
    return spf

# Factorize any number in O(log n):
def factorize(x, spf):
    factors = []
    while x > 1:
        factors.append(spf[x])
        x //= spf[x]
    return factors
```

### Segmented Sieve
When N is huge (up to ~10¹²), you can't store an array of size N. Instead, sieve in **blocks/segments** using only primes up to √N. Keeps space to O(√N).

---

## Common Interview Patterns

- **Count primes up to N** → direct sieve output
- **Prime factorization of many numbers** → SPF sieve
- **Check if a number is prime repeatedly** → precompute sieve once, then O(1) lookups
- **Sum/count of primes in a range [L, R]** → prefix sum over sieve array

---

## Extra Pointers

- For N up to **10⁶**, a plain sieve is fast and fits easily in memory.
- For N up to **10⁷**, still fine in Python with a `bytearray` instead of a list (much more memory-efficient).
- Using a `bytearray` instead of `[True/False]` list can give a **2–3x speedup** in Python due to lower memory overhead.

```python
def sieve_fast(n):
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))
    return [i for i in range(n+1) if is_prime[i]]
```