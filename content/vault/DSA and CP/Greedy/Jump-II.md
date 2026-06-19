---
title: "Jump-II"
lastmod: 2026-06-14
---

#cp_medium 
You are given a 0-indexed array of integers nums of length n. You are initially positioned at index 0.

Each element nums[i] represents the maximum length of a forward jump from index i. In other words, if you are at index i, you can jump to any index (i + j) where:

    0 <= j <= nums[i] and
    i + j < n

Return the minimum number of jumps to reach index n - 1. The test cases are generated such that you can reach index n - 1.

 

Example 1:

Input: nums = [2,3,1,1,4]
Output: 2
Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:

Input: nums = [2,3,0,1,4]
Output: 2

 

Constraints:

    1 <= nums.length <= 104
    0 <= nums[i] <= 1000
    It's guaranteed that you can reach nums[n - 1].


### My Approach
I was basically doing it from the last step. I kept finding the max jump I can take from last step to some intermediate step. Then I set that intermediate step as the anchor(j) and repeated the above thing till I reached idx = 0. "i" is the search pointer. This approach depends on the  fact that its given that there *exists* are path till the last index. 

To understand the validity of this logic, you can think of say greedy approach having 3 jumps and optimal having 2 jumps. But you realise that based on the jump structures , if you actually start following the greedy strat, the information of the existence of the optimal solution implies that after the first step you can directly reach the 0th position following greedy. Hence greedy steps = optimal steps!
```python
class Solution:
    def jump(self, nums: List[int]) -> int:
        count = 0
        n = len(nums)
        j = n-1
        count = 0
        
        while j>0:
            i = j-1
            max_idx = j-1
            while i>=0:
                gap = j-i
                if gap<=nums[i]:
                    max_idx = i
                i-=1
            j=max_idx
            count+=1
        return count
```

### Optimal Approach
Similar to the Jump-I problem. You traverse the array one cell at a time and keep updating the val of the max_idx you could have reached from that sub-range that you have traversed. 
Now when you start you assign the , the max_reach from the start to another variable and when you reach that position, you update the variable with the curr_max_reach and so on.

```python
class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 1:
            return 0

        jumps = 0
        curr_end = 0   # end of current jump range
        max_reach = 0  # farthest index we can reach while scanning this range

        # We only need to process until n-2, because once we can reach last index,
        # we stop. No need to jump from the last index itself.
        for i in range(n - 1):
            max_reach = max(max_reach, i + nums[i])

            # Time to take one jump: we finished scanning current range.
            if i == curr_end:
                jumps += 1
                curr_end = max_reach

                # Optimization: if this jump can reach/past last index, done.
                if curr_end >= n - 1:
                    break

        return jumps
```