---
title: "Coin Change"
lastmod: 2026-07-05
---

#cp-medium 
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return _the fewest number of coins that you need to make up that amount_. If that amount of money cannot be made up by any combination of the coins, return `-1`.

You may assume that you have an infinite number of each kind of coin.

**Example 1:**

**Input:** coins = [1,2,5], amount = 11
**Output:** 3
**Explanation:** 11 = 5 + 5 + 1

**Example 2:**

**Input:** coins = [2], amount = 3
**Output:** -1

**Example 3:**

**Input:** coins = [1], amount = 0
**Output:** 0

**Constraints:**

- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 231 - 1`
- `0 <= amount <= 104`
---
## Approach
Frame the solution like a recursive dp. Your current state is given by the current amount that needs to be filled. So from the current state you branch off to all feasible amounts i.e. for each coin value less than the current amount, you branch off to compute f(amount-coin). You do this recursively, while keeping a memo of size (amount+1). 

Now if there is NO possible way to get the change you must return -1.

So I am using 3 possible values in my memo\[amount]:
- -2 for still unfilled/yet to process
- -1 as invalid for that amount
- 0+ for any valid solution to the amount

Base Case:
- if f(amount) already computed use it directly. ( check if amount =-2)
- if amount = 0 means that 0 coins are needed to reach it. return 0

Invalid Case:
- First of all we start from current 'amount' state.
- We then branch off to all 'amount -coin' states and compute it. (If coin<=amount)
	- They return either -1 or some non-negative value. We collect them in a list
	- If we have non-negative values in this collection. we get the min_val. and fill memo\[amount] = min_val + 1
	- If only -1 in the collection or no coin <=amount(len(vals) =0):
		- Then we put memo\[amount] = -1 and return it.
		- This -1 will backpropagate to the top if there are no valid paths down the tree with non-negative answers.


NOTE: Probably -2 as the placeholder is over-complicating things. the recursive equation is pretty straight forward and easy and the following tabulation method is an easier approach. keeping the table initialised with infinity. so while taking minimum we don't need to check if its -1.

---
## Solution (memo method)

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        n = len(coins)
        memo = [-2 for _ in range(amount+1)]


        return self.helper(coins,amount,memo)
         

    def helper(self,coins,amount,memo):

        if memo[amount] != -2:
            return memo[amount]
        
        if amount == 0:
            memo[amount] = 0
            return memo[amount]

        vals = []
        for coin in coins:
            
            if coin <= amount:
               vals.append(self.helper(coins,amount-coin,memo)) 
        
        if len(vals):
            min_val = 2**32-1
            flag = 0
            for val in vals:
                if val<min_val and val!=-1:
                    min_val = val
                    flag=1

            
            memo[amount] = min_val + 1 if flag else -1
            return memo[amount]
        else:
            memo[amount] = -1
            return memo[amount]
```

## Tabulation Method
To prevent the extra space used in recursive stack, we can convert the memoization solution into a tabulation solution.

- Start by making a 2D table where rows represent different choices and columns represent target values.
- Initialize the first row based on whether each target can be formed using only the first option repeatedly.
- If a target is divisible by the first option, store how many times it is used, otherwise, mark it as not possible.
- Go row by row, and for each target value, compute the result by checking two cases, excluding or including the current option.
- To include the current option, reduce the target and use the value already computed in the same row.
- Store the minimum result between including and excluding, and finally return the value in the last row and last column.

```python
# Solution class to implement tabulation approach
class Solution:
    # Function to find minimum coins
    def coinChange(self, coins, amount):
        # Creating dp array of size amount+1
        dp = [float('inf')] * (amount + 1)

        # Base case: dp[0] = 0
        dp[0] = 0

        # Loop through all amounts from 1 to amount
        for i in range(1, amount + 1):
            # Try each coin
            for coin in coins:
                # If coin can be used
                if i - coin >= 0 and dp[i - coin] != float('inf'):
                    # Update dp[i] with minimum coins
                    dp[i] = min(dp[i], 1 + dp[i - coin])

        # If dp[amount] is still infinity, return -1
        return -1 if dp[amount] == float('inf') else dp[amount]


# Driver function
if __name__ == "__main__":
    coins = [1, 2, 5]
    amount = 11

    obj = Solution()
    print(obj.coinChange(coins, amount))

```