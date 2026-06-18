---
title: "Find 1st and last pos of element in sorted array"
---

Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value.

If `target` is not found in the array, return `[-1, -1]`.

You must write an algorithm with `O(log n)` runtime complexity.

**Example 1:**

**Input:** nums = [5,7,7,8,8,10], target = 8
**Output:** [3,4]

**Example 2:**

**Input:** nums = [5,7,7,8,8,10], target = 6
**Output:** [-1,-1]

**Example 3:**

**Input:** nums = [], target = 0
**Output:** [-1,-1]

**Constraints:**

- `0 <= nums.length <= 105`
- `-109 <= nums[i] <= 109`
- `nums` is a non-decreasing array.
- `-109 <= target <= 109`


## My Solution
```cpp
class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        //getting the right limit
        vector<int> idx = {-1,-1};
        int n = (int)nums.size();
        if (n == 0) return idx;
        int L=0,R=n-1;

        while(L<=R){
            int mid=L+(R-L)/2;
            if(nums[mid]<=target) L = mid+1;
            else R = mid-1;
        }
        // right boundary
        if (R >= 0 && R < n && nums[R] == target) idx[1] = R;

        L=0,R=n-1;
        while(L<=R){
            int mid=L+(R-L)/2;
            if(nums[mid]<target) L = mid+1;
            else R = mid-1;
        }
        // left boundary  
        if (L >= 0 && L < n && nums[L] == target) idx[0] = L;        
        return idx;
    }
};
```

### Approach

The idea is to run two separate binary searches on the sorted array: one to find the **right boundary** and one to find the **left boundary** of the target.
## Right Boundary
Use `nums[mid] <= target` to push `L` rightward as far as possible. When the loop exits, `R` sits at the last index where the value is `<= target` — check if it equals target exactly.
```cpp
if (nums[mid] <= target) L = mid + 1;
else R = mid - 1;
// exit: R = rightmost index of target (if it exists)
```

## Left Boundary
Use `nums[mid] < target` (strict) to push `R` leftward. When the loop exits, `L` sits at the first index where the value is `>= target` — check if it equals target exactly.

```cpp
if (nums[mid] < target) L = mid + 1;
else R = mid - 1;
// exit: L = leftmost index of target (if it exists)
```

## Critical Details
**Style A exits with L and R crossed** (`L = R + 1`), so after every search one pointer is guaranteed to be out of bounds. Always guard before accessing:
```cpp
if (R >= 0 && R < n && nums[R] == target) idx[1] = R;
if (L >= 0 && L < n && nums[L] == target) idx[0] = L;
```
