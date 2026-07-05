---
title: "Split Array Largest Sum"
lastmod: 2026-07-04
---

#cp-hard

Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty subarrays such that the largest sum of any subarray is **minimized**.

Return _the minimized largest sum of the split_.

A **subarray** is a contiguous part of the array.

**Example 1:**

**Input:** nums = [7,2,5,10,8], k = 2
**Output:** 18
**Explanation:** There are four ways to split nums into two subarrays.
The best way is to split it into [7,2,5] and [10,8], where the largest sum among the two subarrays is only 18.

**Example 2:**

**Input:** nums = [1,2,3,4,5], k = 2
**Output:** 9
**Explanation:** There are four ways to split nums into two subarrays.
The best way is to split it into [1,2,3] and [4,5], where the largest sum among the two subarrays is only 9.

**Constraints:**

- `1 <= nums.length <= 1000`
- `0 <= nums[i] <= 106`
- `1 <= k <= min(50, nums.length)`
## Approach
To split an array into k subarrays such that the largest sum of any subarray is minimized, we use binary search. The key insight is that if a sum S is feasible (i.e., the array can be split into k subarrays with sums ≤ S), then any larger sum is also feasible. This monotonic property allows efficient narrowing down of the minimum feasible S using binary search.(*Focus on the explaination given in green below. I copied this part from leetcode, doesn't make sense to me rn*)
Approach
1. Binary Search Setup:

    Low: Maximum element in the array (smallest possible sum for any subarray).
    High: Total sum of the array (largest possible sum if the array is not split).

2. Feasibility Check:

    For a candidate sum mid, count how many subarrays are needed such that each subarray's sum ≤ mid. If this count ≤ k, mid is feasible. *Basically if count =k then there is a chance that mid might be the lowest max one so we do R = mid. but if count  < k , then the max value has to be lesser such that count can go to k, i.e R <mid. Hence we search again from R = mid.*
3. Adjust Search Range:
    If feasible, try smaller sums. R = mid
    If not feasible, try larger sums. L = mid +1

This is a minimization problem with a monotonic condition, similar to allocating resources (e.g., minimizing the maximum weight a ship carries).
**Complexity**
    Time complexity: O(nlogm)     where n is the array length and m is the range of sums.
    Space complexity: O(1)     uses constant extra space.



## My Solution
```python
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        L = max(nums)
        R = sum(nums)

        while(L<R):
            numst=nums.copy()
            sum_s = L + (R-L)//2
            kt = 0
            maxt = 0
            sumt = 0
            # i = range(len(nums)):
            while numst:
                num = numst.pop()
                sumt+= num

                if sumt > sum_s:
                    kt+=1
                    sumt-=num
                    print(sumt)

                    maxt = sumt if sumt>maxt else maxt
                    numst.append(num)
                    sumt = 0
                elif len(numst) == 0:
                    kt+=1
                    # print(sumt)
                    maxt = sumt if sumt>maxt else maxt

            print(sum_s, kt, maxt,L,R)

            if kt>k:
                L = sum_s + 1
            elif kt<=k:
                R = sum_s 

                
                
        return L



```