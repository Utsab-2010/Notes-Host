---
title: "Subset sum equal to target"
lastmod: 2026-07-04
---

#cp-hard 

**Problem Statement:** We are given an array ‘ARR’ with N positive integers. We need to find if there is a subset in “ARR” with a sum equal to K. If there is, return true else return false.

A subset/subsequence is a contiguous or non-contiguous part of an array, where elements appear in the same order as the original array.  
For example, for the array: [2,3,1] , the subsequences will be {{2},{3},{1},{2,3},{2,1},{3,1},{2,3,1}} but {3,2} is **not** a subsequence because its elements are not in the same order as the original array.

---
**Input : ** N = 4, ARR = [4, 3, 5, 2], K = 6 
**Output :** true
**Explanation :** One possible subset with sum = 6 is [4, 2]. There’s also [3, 3] but that doesn’t exist in the array. As soon as we find one subset whose sum is equal to K, the answer is true.  
**Input :** N = 3, ARR = [1, 2, 5], K = 4 
**Output :** false
**Explanation :** Possible subsets and their sums: [1] → 1, [2] → 2, [5] → 5, [1,2] → 3, [1,5] → 6, [2,5] → 7, [1,2,5] → 8. None of them equal 4, so the answer is false.

---
## Approach
**Express the problem in terms of indexes.**  
We can say that initially, we need to find(n-1, target) which means that we need to find whether there exists a subsequence in the array from index 0 to n-1, whose sum is equal to the target. Similarly, we can generalize it for an index.  
  
**Base Cases:**
- If target == 0, it means that we have already found the subsequence from the previous steps, so we can return true.
- If ind == 0, it means we are at the first element, so we need to return arr\[ind\] == target. If the element is equal to the target we return true else false.
  
**Try out all possible choices at a given index.**  
We need to generate all the subsequences.  **We have two choices:**  
- **Exclude the current element in the subsequence:** We first try to find a subsequence without considering the current index element. Basically considering the situation where i'th element is not part of the required target subsequence. For this, we will make a recursive call to f(ind-1,target).
- **Include the current element in the subsequence:** We will try to find a subsequence by considering the current index as element as part of subsequence. As we have included arr[ind], the updated target which we need to find in the rest if the array will be target - arr[ind]. Therefore, we will call f(ind-1,target-arr[ind]).

**Note:** We will consider the current element in the subsequence only when the current element is less or equal to the target.

**Return (taken || notTaken)**  
As we are looking for only one subset, if any of the one among taken or not taken returns true, we can return true from our function. Therefore, we return ‘or(||)’ of both of them.  

**Steps to memoize a recursive solution:**
If we draw the recursion tree, we will see that there are overlapping subproblems. In order to convert a recursive solution the following steps will be taken:  
1. Create a dp array of size `[n][k+1]`. The size of the input array is ‘n’, so the index will always lie between ‘0’ and ‘n-1’. The target can take any value between ‘0’ and ‘k’. Therefore we take the dp array as `dp[n][k+1]`
2. We initialize the dp array to -1.
3. Whenever we want to find the answer of particular parameters (say f(ind,target)), we first check whether the answer is already calculated using the dp array(i.e `dp[ind][target]!= -1` ). If yes, simply return the value from the dp array.
4. If not, then we are finding the answer for the given value for the first time, we will use the recursive relation as usual but before returning from the function, we will set `dp[ind][target]` to the solution we get.

## Memoization Solution
```python
class Solution:
    # Recursive helper function with memoization
    def subsetSumUtil(self, ind, target, arr, dp):
        # Base case: target achieved
        if target == 0:
            return True

        # Base case: first index check
        if ind == 0:
            return arr[0] == target

        # If already computed
        if dp[ind][target] != -1:
            return dp[ind][target] == 1

        # Choice 1: not take the element
        notTaken = self.subsetSumUtil(ind - 1, target, arr, dp)

        # Choice 2: take the element if possible
        taken = False
        if arr[ind] <= target:
            taken = self.subsetSumUtil(ind - 1, target - arr[ind], arr, dp)

        # Store result
        dp[ind][target] = 1 if (notTaken or taken) else 0
        return notTaken or taken

    # Main function to call the helper
    def subsetSumToK(self, n, k, arr):
        dp = [[-1] * (k + 1) for _ in range(n)]
        return self.subsetSumUtil(n - 1, k, arr, dp)


# Driver code
if __name__ == "__main__":
    arr = [1, 2, 3, 4]
    k = 4
    sol = Solution()

    if sol.subsetSumToK(len(arr), k, arr):
        print("Subset with the given target found")
    else:
        print("Subset with the given target not found")

```



