---
title: "Search in Rotated Array"
lastmod: 2026-05-30
---

There is an integer array `nums` sorted in ascending order (with **distinct** values).

Prior to being passed to your function, `nums` is **possibly left rotated** at an unknown index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (**0-indexed**). For example, `[0,1,2,4,5,6,7]` might be left rotated by `3` indices and become `[4,5,6,7,0,1,2]`.

Given the array `nums` **after** the possible rotation and an integer `target`, return _the index of_ `target` _if it is in_ `nums`_, or_ `-1` _if it is not in_ `nums`.

You must write an algorithm with `O(log n)` runtime complexity.

**Example 1:**

**Input:** nums = [4,5,6,7,0,1,2], target = 0
**Output:** 4


## Solution

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int L = 0, R = nums.size() - 1;

        while (L <= R) {
            int mid = L + (R - L) / 2;

            if (nums[mid] == target)
                return mid;

            if (nums[L] <= nums[mid]) {
                if (target<nums[mid] && target>=nums[L])
                    R = mid - 1;
                else
                    L = mid + 1;
            } else if (nums[R] >= nums[mid]) {
                if (target > nums[mid] && target<=nums[R])
                    L = mid + 1;
                else
                    R = mid - 1;
            }
        }
        return -1;
    }
};
```
