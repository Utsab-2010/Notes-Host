---
title: "Koko eating Banana"
lastmod: 2026-07-03
---

#cp-medium 
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

 

Example 1:

Input: piles = [3,6,7,11], h = 8
Output: 4

Example 2:

Input: piles = [30,11,23,4,20], h = 5
Output: 30

Example 3:

Input: piles = [30,11,23,4,20], h = 6
Output: 23

 

Constraints:

    1 <= piles.length <= 104
    piles.length <= h <= 109
    1 <= piles[i] <= 109


## my solution
```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        L = 1
        R = max(piles)
        while(L<R):
            k = L + (R-L)//2

            hk = 0
            for num in piles:
                hk += num//k if not num%k else num//k + 1

            if hk > h:
                L = k + 1
            else:
                R = k
        return L
```

## Approach
Since this was a *check condition type of binary search I used the $L<R$ approach*.
Basically, the the atmax value of k you need to eat an element of the list is just the max value available in the list.

So we do a binary search between 1 to that max value of K. 
For each k we calc the $h_k$ value.
- Now if $h_k > h$ : Then k needs to be strictly bigger than what it is till now , hence L = mid + 1
- Other wise ( $h_k \leq h$ ): means k can be lesser, so R = mid. We include R coz mid is still a valid option for the final k value, since we don't know the list of numbers.
Loop ends when L=R=$k_{opt}$  and we return it.