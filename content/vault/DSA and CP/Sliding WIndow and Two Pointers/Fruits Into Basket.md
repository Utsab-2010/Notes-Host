---
title: "Fruits Into Basket"
---

#cp_medium 

You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented by an integer array `fruits` where `fruits[i]` is the **type** of fruit the `ith` tree produces.

You want to collect as much fruit as possible. However, the owner has some strict rules that you must follow:

- You only have **two** baskets, and each basket can only hold a **single type** of fruit. There is no limit on the amount of fruit each basket can hold.
- Starting from any tree of your choice, you must pick **exactly one fruit** from **every** tree (including the start tree) while moving to the right. The picked fruits must fit in one of your baskets.
- Once you reach a tree with fruit that cannot fit in your baskets, you must stop.

Given the integer array `fruits`, return _the **maximum** number of fruits you can pick_.

**Example 1:**

**Input:** fruits = [1,2,1]
**Output:** 3
**Explanation:** We can pick from all 3 trees.

**Example 2:**

**Input:** fruits = [0,1,2,2]
**Output:** 3
**Explanation:** We can pick from trees [1,2,2].
If we had started at the first tree, we would only pick from trees [0,1].

**Example 3:**

**Input:** fruits = [1,2,3,2,2]
**Output:** 4
**Explanation:** We can pick from trees [2,3,2,2].
If we had started at the first tree, we would only pick from trees [1,2].

**Constraints:**

- `1 <= fruits.length <= 105`
- `0 <= fruits[i] < fruits.length`




```python
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        l = -1
        r = 0
        max_len = 0
        nums = []
        nums_idx = []
        while r < len(fruits):
            if fruits[r] not in nums:
                nums.append(fruits[r])
                nums_idx.append(r)
            else:
                idx = nums.index(fruits[r])
                nums_idx[idx] = r

            if len(nums) > 2:
                idx = 1 if (nums_idx[1] < nums_idx[0]) else 0
                
                l = nums_idx.pop(idx)
                temp = nums.pop(idx)
                

            max_len = max(max_len, r - l)

            r = r + 1

        return max_len


```

### Approach:
This problem is basically finding the length of the largest subsequence having only 2 unique integers inside.

We define two pointers with window in [L+1,R]   and we are essentially checking how big we can make this window such that there are only 2 unique numbers inside. ([ ] means inclusive)

1. We start L = -1 and R = 0 and start moving R to the right.
2. We maintain a hashtable containing the first and second unique number in window along with their last idx of occurence in the window.
3. While R < len:
	1. If number is in the table, number the last idx value to R.
	2. If num at R is not in the hash table => new number, we add their value and the idx .
	3. Next  if the number of elements in the table >2 then we have have to move the L pointer to remove one of the prev 2 unique numbers that we had in the hash table. This is done in such a way such that the new window has the max possible length:
		1. So the logic we use is that , we compare the last_occurence_idx of the two numbers and place L at the earlier idx of those two.
		2. e.g 1 1 2 1 1 3 , when R lands on 3 we move L such that window becomes 1 1 3 i.e we place L at 2. Last idx of 2 was k and that of 1 was k +2 in this k(k is some apt integer.)
	4. We then update 