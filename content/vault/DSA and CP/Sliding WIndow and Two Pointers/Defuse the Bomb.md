---
title: "Defuse the Bomb"
lastmod: 2026-06-07
---

#cp_easy 

You have a bomb to defuse, and your time is running out! Your informer will provide you with a **circular** array `code` of length of `n` and a key `k`.

To decrypt the code, you must replace every number. All the numbers are replaced **simultaneously**.

- If `k > 0`, replace the `ith` number with the sum of the **next** `k` numbers.
- If `k < 0`, replace the `ith` number with the sum of the **previous** -`k` numbers.
- If `k == 0`, replace the `ith` number with `0`.

As `code` is circular, the next element of `code[n-1]` is `code[0]`, and the previous element of `code[0]` is `code[n-1]`.

Given the **circular** array `code` and an integer key `k`, return _the decrypted code to defuse the bomb_!

**Example 1:**

**Input:** code = [5,7,1,4], k = 3
**Output:** [12,10,16,13]
**Explanation:** Each number is replaced by the sum of the next 3 numbers. The decrypted code is [7+1+4, 1+4+5, 4+5+7, 5+7+1]. Notice that the numbers wrap around.

**Example 2:**

**Input:** code = [1,2,3,4], k = 0
**Output:** [0,0,0,0]
**Explanation:** When k is zero, the numbers are replaced by 0. 

**Example 3:**

**Input:** code = [2,4,9,3], k = -2
**Output:** [12,5,6,13]
**Explanation:** The decrypted code is [3+9, 2+3, 4+2, 9+4]. Notice that the numbers wrap around again. If k is negative, the sum is of the **previous** numbers.


```python
class Solution:
    def decrypt(self, code: list[int], k: int) -> list[int]:
        N = len(code)
        result = [0] * N
        
        if k == 0:
            return result
        
        # Define initial window boundaries based on k
        if k > 0:
            left = 1
            right = k
        else:
            left = N + k  # If k is negative, N + k steps backward from the end
            right = N - 1
            
        # Calculate the sum for the initial window (i = 0)
        current_window_sum = 0
        for i in range(left, right + 1):
            current_window_sum += code[i % N]
            
        result[0] = current_window_sum
        
        # Slide the window across the rest of the array
        for i in range(1, N):
            # Remove the element leaving the window
            current_window_sum -= code[left % N]
            # Advance boundaries circularly
            left += 1
            right += 1
            # Add the element entering the window
            current_window_sum += code[right % N]
            
            result[i] = current_window_sum
            
        return result
```