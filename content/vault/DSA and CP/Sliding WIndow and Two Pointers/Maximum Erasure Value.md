---
title: "Maximum Erasure Value"
lastmod: 2026-06-08
---

#cp_medium 

You are given an array of positive integers `nums` and want to erase a subarray containing **unique elements**. The **score** you get by erasing the subarray is equal to the **sum** of its elements.

Return _the **maximum score** you can get by erasing **exactly one** subarray._

An array `b` is called to be a subarray of `a` if it forms a contiguous subsequence of `a`, that is, if it is equal to `a[l],a[l+1],...,a[r]` for some `(l,r)`.

**Example 1:**

**Input:** nums = [4,2,4,5,6]
**Output:** 17
**Explanation:** The optimal subarray here is [2,4,5,6].

**Example 2:**

**Input:** nums = [5,2,1,2,5,2,1,2,5]
**Output:** 8
**Explanation:** The optimal subarray here is [5,2,1] or [1,2,5].

**Constraints:**

- `1 <= nums.length <= 105`
- `1 <= nums[i] <= 104`


```python
class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        L=0
        r = 0
        max_score = 0
        curr_score = 0
        seen = set()
        N = len(nums)
        while(r<N):
            # seen.add(nums[r])
            while nums[r] in seen: #logN
                seen.remove(nums[L])
                curr_score = curr_score - nums[L]
                L = L+1
            
            seen.add(nums[r])
            curr_score = curr_score + nums[r]
            max_score = max(max_score,curr_score)
            r = r+1

        return max_score

```

### Approach:
Basically we have to find the maximum sum  over all unique subsequences in the main sequence.
Use pointers L and R, have a dynamic sliding window.  L = 0, R = 0. Also we use python sets to record the occurrence of values, since we need to just check for repetition we won't need a dict/hash(atleast in python)

1. Starting with R start expanding the window to the right. 
2. If the element is unique increase window_sum and add it to set.
3. if element is repeated, then L be be moved to the previous occurrence of that element and the window contributions of all elements till that point  in the curr_window needs to be removed.
	1. This is what we do step by step in the above solution, we move L by +1 and keep erasing the values from the curr_sum till L erasures the previous occurrence of the current element in consideration.
4. We then update max_sum , inc R and continue.

*O(n) time and O(1) space*
