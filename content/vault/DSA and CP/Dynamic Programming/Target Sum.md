---
title: "Target Sum"
lastmod: 2026-07-06
---

#cp-medium 

You are given an integer array `nums` and an integer `target`.

You want to build an **expression** out of nums by adding one of the symbols `'+'` and `'-'` before each integer in nums and then concatenate all the integers.
- For example, if `nums = [2, 1]`, you can add a `'+'` before `2` and a `'-'` before `1` and concatenate them to build the expression `"+2-1"`.
Return the number of different **expressions** that you can build, which evaluates to `target`.

**Example 1:**
**Input:** nums = [1,1,1,1,1], target = 3
**Output:** 5
**Explanation:** There are 5 ways to assign symbols to make the sum of nums be target 3.
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3

**Example 2:**
**Input:** nums = [1], target = 1
**Output:** 1

**Constraints:**
- `1 <= nums.length <= 20`
- `0 <= nums[i] <= 1000`
- `0 <= sum(nums[i]) <= 1000`
- `-1000 <= target <= 1000`

### Approach
We consider subsequences considering indices 0 to i. then we do the typical take/notake logic.
We consider that number of possibilities branch into two - either i'th element is + or i'th element is -1 and remember that whatever combination it might be the i'th element is always involved. Based on this we can write for function as 
- F(arr\[0,i],target) = F(arr\[0,i-1],target-arr\[i]) +F(arr\[0,i-1],target+ arr\[i])  
- We make a 2D array to store it

Base Case:
- -1 is placeholder for not processed
- when we at the last element 0 , we either return 1  if target is equal to either + or - the num0 value or we return 2 if element 0 is 0 . so -+ both work.


```python
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total = 0
        for num in nums:
            total+= abs(num)
        

        memo = [[-1 for _ in range(2*total+1)] for _ in range(len(nums))]
        # print(len(memo),len(memo[0]))

        if abs(target) >total: # if problem is invalid from the start return 0
            return 0 
            
        return self.helper(nums,target,len(nums)-1,memo)
    
    def helper(self,nums,target,i,memo):
        # print(i/,target)
        if memo[i][target] != -1:
            return memo[i][target]
        
        if i==0:   # only if num[0]is 0 the value of memo below goes to 2 otherwise stays at 1
            memo[i][target] = 0
            memo[i][target] += target == nums[i] 
            memo[i][target] += target == -nums[i]
            return memo[i][target]
        
        memo[i][target] = self.helper(nums,target+nums[i],i-1,memo) + self.helper(nums,target-nums[i],i-1,memo)
        
        return memo[i][target]
```