---
title: "Binary Search — `<=` vs `<` Boundary Conditions"
---

Binary Search — `<=` vs `<` Boundary Conditions

> **The golden rule:** Ask — _"Has this index been fully eliminated as a candidate?"_
> 
> - **Yes** → skip it: use `mid + 1` / `mid - 1`
> - **No** → keep it: use `mid`

---

## 1. The Two Styles of Binary Search

Every binary search loop falls into one of two mental models. The choice of `<=` vs `<` follows directly from which model you pick.

### Style A — Explicit check, shrink past mid

```cpp
while (L <= R) {                // L and R are both live candidates
    int mid = L + (R - L) / 2;
    if (arr[mid] == target) return mid;   // checked explicitly
    if (arr[mid] < target)  L = mid + 1; // mid ruled out → skip it
    else                    R = mid - 1; // mid ruled out → skip it
}
// loop ends when search space is empty (L > R)
```

Because `mid` is tested in the `if`, it is definitively ruled out. So `mid ± 1` is safe — you won't skip the answer.

### Style B — Answer lives at boundary, keep mid

```cpp
while (L + 1 < R) {              // answer is always inside [L, R]
    int mid = L + (R - L) / 2;
    if (arr[mid] <= target) L = mid; // mid not ruled out → keep it
    else                    R = mid; // mid not ruled out → keep it
}
// loop ends at L + 1 == R → check both
if (arr[L] == target) return L;
if (arr[R] == target) return R;
```

`mid` is never checked directly inside the loop, so you cannot skip it. The loop guarantees that exactly two candidates remain at termination.

---

## 2. What Each Pointer Means (The Invariant)

Understanding the _invariant_ of each pointer is more reliable than thinking about edge cases one by one.

|Pointer|Invariant in Style B|
|---|---|
|`L`|Last index that is **definitely ≤ target** — still a candidate because we haven't verified it equals the target|
|`R`|First index that is **definitely > target** — still a candidate, it could be the answer|

Once you know what each pointer guarantees, the boundary checks write themselves.

---

## 3. Condition Boundaries — `<=` vs `<` Inside the Loop

The same rule applies when choosing whether to include endpoints in range checks.

|Situation|Operator|Reason|
|---|---|---|
|`target` could equal `nums[L]`|`>=` (include)|`nums[L]` is still a candidate — not yet ruled out|
|`target` vs `nums[mid]` (already checked above)|`<` (exclude)|`nums[mid]` was tested on the line above — definitively ruled out|
|`target` could equal `nums[R]`|`<=` (include)|`nums[R]` is still a candidate|

### Example — Rotated Sorted Array

```cpp
if (nums[L] <= nums[mid]) {
    // left half is sorted
    if (target >= nums[L] && target < nums[mid])
    //          ^^                    ^
    //  nums[L] is live          nums[mid] already checked
    //  → include with >=        → exclude with <
        R = mid - 1;
    else
        L = mid + 1;
}
```

---

## 4. Common Mistakes Decoded

|Mistake|Why it breaks|
|---|---|
|`while (L < R)` with `R = mid - 1`|Skips `mid` before checking it — can miss the answer when `L == R` is the target|
|`while (L <= R)` with `R = mid`|If `arr[mid]` keeps being chosen as `R`, `L` never catches up — infinite loop|
|Range check uses `<` on both boundaries|Misses the case where `target` equals the left boundary exactly|
|Range check uses `<=` on `mid`|Re-examines a `mid` that was already tested — can push into the wrong half|

---

## 5. Quick Decision Checklist

Before writing any boundary operator, ask these questions in order:

1. **Has this index already been explicitly checked?**
    
    - Yes (e.g. `nums[mid] == target` was already tested) → use `<` / `mid ± 1`
    - No → use `<=` / `mid`
2. **Can the target equal this boundary value?**
    
    - Yes → use `>=` or `<=` to include it
    - No → use `>` or `<` to exclude it
3. **Which loop style am I using?**
    
    - Style A (`while L <= R`) → always use `mid ± 1`
    - Style B (`while L + 1 < R`) → always use plain `mid`

---


> **One-line test:** "Has this index already been definitively eliminated?" → Yes: `<` or `mid ± 1`. No: `<=` or `mid`.
