---
title: "Unbounded Knapsack"
lastmod: 2026-07-05
---

#cp-medium 

**Problem Statement:** A thief wants to rob a store. He is carrying a bag of capacity W. The store has ‘n’ items of infinite supply. Its weight is given by the ‘wt’ array and its value by the ‘val’ array. He can either include an item in its knapsack or exclude it but can’t partially have it as a fraction. We need to find the maximum value of items that the thief can steal. He can take a single item any number of times he wants and put it in his knapsack .

Input: n = 3, W = 8, wt = [2, 4, 6], val = [5, 11, 13]
Output: 22
Explanation:**We can take item with weight 2 (value 5) four times to fill capacity 8,total value = 5 × 4 = 20.
But a better choice: take item with weight 2 (value 5) twice and item with weight 4 (value 11) once → total weight = 2 + 2 + 4 = 8, total value = 5 + 5 + 11 = 21.
Even better: take two items with weight 4 (value 11 each), total value = 22, which is maximum.  
Input:  n = 2, W = 3, wt = \[2, 1], val = \[4, 2]
Output: 6
Explanation: We can take item with weight 1 (value 2) three times , total value = 6.
Taking weight 2 (value 4) plus weight 1 (value 2) also gives 6. No combination yields more than 6.

## Approach
1. f(i,W) = max(f(i,w-arr(i)),  f(i-1,W))
	1. This is basically the max of two scenarios - taken and nottaken
	2. in the taken scenario since , we have infinite amount of items the sequence does not decay to i-1 and we search again from i only. the scenario where the i'th item is no longer needed and we need to shift to f(i-1,w- arr(i)) is already considered within f(i,w-arr(i)) !
2. **2nd method** : We keep a memo of 0 to W. Now for each f(w) we go over all the available items and branch off to f(w- arr\[i]) if the item weight is not more than w. This reduces the space complexity to O(W).
	


## Solution
```python
class Solution:
    # Function to solve unbounded knapsack using tabulation
    def unboundedKnapsack(self, n, W, val, wt):
        # Create DP table where dp[i][j] is max value with i items and capacity j
        dp = [[0] * (W + 1) for _ in range(n)]

        # Base condition: fill first row using infinite supply of first item
        for i in range(wt[0], W + 1):
            dp[0][i] = (i // wt[0]) * val[0]

        # Loop through items
        for ind in range(1, n):
            # Loop through capacities
            for cap in range(W + 1):
                # Case 1: Not take current item
                notTaken = dp[ind - 1][cap]

                # Case 2: Take current item
                taken = float('-inf')
                if wt[ind] <= cap:
                    taken = val[ind] + dp[ind][cap - wt[ind]]

                # Store best value
                dp[ind][cap] = max(notTaken, taken)

        return dp[n - 1][W]


# Driver code
if __name__ == "__main__":
    wt = [2, 4, 6]
    val = [5, 11, 13]
    W = 10
    n = len(wt)

    obj = Solution()
    print("The Maximum value of items the thief can steal is", obj.unboundedKnapsack(n, W, val, wt))

```

## Solution -2 
```python
class Solution:
    def unboundedKnapsack(self, n, W, val, wt):
        dp = [0] * (W + 1)
        for w in range(1, W + 1):
            for i in range(n):
                if wt[i] <= w:
                    dp[w] = max(dp[w], val[i] + dp[w - wt[i]])
        return dp[W]
```










### Space Complexity
**O(N×W) — the DP table**

```python
dp = [[-1] * (W + 1) for _ in range(n)]
```

This 2D array has `n` rows and `W+1` columns, so it stores `N × (W+1)` values ≈ **O(N×W)** space. This is auxiliary space that persists for the whole computation — it's not freed until the function returns.

**O(N) — the recursion stack**

Look at how the recursive calls chain:

```python
notTaken = self.knapsackUtil(wt, val, ind - 1, W, dp)
```

$$ \text{Total Space} = \underbrace{O(N \times W)}_{\text{DP table}} + \underbrace{O(N)}_{\text{recursion stack}} $$
