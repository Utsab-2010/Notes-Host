---
title: "Max Consecutive One III"
---

#cp_medium

Given a binary array `nums` and an integer `k`, return _the maximum number of consecutive_ `1`_'s in the array if you can flip at most_ `k` `0`'s.

**Example 1:**

**Input:** nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
**Output:** 6
**Explanation:** [1,1,1,0,0,**1**,1,1,1,1,**1**]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

**Example 2:**

**Input:** nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
**Output:** 10
**Explanation:** [0,0,1,1,**1**,**1**,1,1,1,**1**,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

**Constraints:**

- `1 <= nums.length <= 105`
- `nums[i]` is either `0` or `1`.
- `0 <= k <= nums.length`


```python

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        l = -1
        r = 0
        max_len = 0
        zero_cnt = 0
        zeros = []
        while(r<len(nums)):
            if nums[r] == 0:
                zero_cnt = zero_cnt + 1
                zeros.append(r)
                if zero_cnt > k:
                    l = zeros.pop(0)
                    zero_cnt = zero_cnt - 1
            max_len = r-l if r-l>max_len else max_len
            r = r + 1
        return max_len

```

### Approach:
Basically  we have two pointers to keep a dynamic window. We expand the window to the right as much as we can till a max threshold of 0s inside, then we update the left pointer so that the first zero in the window is removed.

*Note:* In the above case, my window is from [L+1,R] where they are the pointer indices.

1. Start with two pointers Left and right . -1 and 0
2. starting with right pointer, iteratively keep moving it left.
3. while doing so,
	1. If the position is zero:
		1. increase the count of zeros in the window.
		2. add the zero idx to queue.
		3. if zeros is more than threshold, then we update  the left pntr to the first value of the queue(basically the idx of the zero that we wanna remove from our sub-window)
	2. Then update the max_len if r-l is bigger
	3. Then inc r and continue