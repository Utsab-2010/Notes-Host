---
title: "Find Peak Element"
lastmod: 2026-07-03
---

#cp-medium 
A peak element is an element that is strictly greater than its neighbors.

Given a **0-indexed** integer array `nums`, find a peak element, and return its index. If the array contains multiple peaks, return the index to **any of the peaks**.

You may imagine that `nums[-1] = nums[n] = -∞`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.

You must write an algorithm that runs in `O(log n)` time.

**Example 1:**

**Input:** nums = [1,2,3,1]
**Output:** 2
**Explanation:** 3 is a peak element and your function should return the index number 2.

**Example 2:**

**Input:** nums = [1,2,1,3,5,6,4]
**Output:** 5
**Explanation:** Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.

**Constraints:**

- `1 <= nums.length <= 1000`
- `-231 <= nums[i] <= 231 - 1`
- `nums[i] != nums[i + 1]` for all valid `i`.


## My Solution
```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        L = 0
        R = len(nums) -1

        while (L<=R):
            mid = L + (R-L)//2
            print(mid,L,R)
            if len(nums)==1:
                return 0
            
            
            if mid>=1 and mid <= len(nums)-2:
                if nums[mid]>nums[mid-1] and nums[mid]>nums[mid+1]:
                    return mid
            elif mid == 0 and  nums[mid]>nums[mid+1]:
                return mid
            elif mid == len(nums)-1 and nums[mid]>nums[mid-1]:
                return mid

            if (mid!=0 and nums[mid-1]>nums[mid]) or mid==len(nums)-1:
                R = mid -1
            elif (mid!=(len(nums)-1) and nums[mid+1]>nums[mid]) or mid==0:
                L = mid + 1
        return -1
        wayyy too mach conditions
```


## Best Solution
```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[mid + 1]:
                right = mid
            else:
                left = mid + 1

        return left
```


# How to Improve my Solution?
The issue isn't that you missed edge cases — it's that you picked an approach that **forces** you to handle edge cases manually.
### Why your solution explodes with conditions
You're asking: _"is `mid` a peak?"_ at every step. To answer that, you need to check both neighbors, which means you need to guard against `mid=0` and `mid=n-1` separately. That's where all the noise comes from.
### Why the clean solution has zero edge cases
It never asks _"is this a peak?"_. It only asks one thing:
> **Which side is going uphill?**
```python
if nums[mid] > nums[mid + 1]:
    right = mid   # peak is on the left side (could be mid itself)
else:
    left = mid + 1  # nums[mid+1] > nums[mid], so peak is strictly to the right
```
`mid + 1` is always safe because the loop condition is `left < right`, which guarantees `mid < right <= n-1`, so `mid+1` always exists. No boundary checks needed at all.

The insight that makes it work: **a peak must exist on the uphill side**. If `nums[mid+1] > nums[mid]`, the right side is climbing — a peak _must_ exist there (even if the array just keeps climbing, the last element is a peak since `nums[n] = -∞`).