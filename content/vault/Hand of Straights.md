---
title: "Hand of Straights"
lastmod: 2026-06-10
---

#cp_medium 

Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size `groupSize`, and consists of `groupSize` consecutive cards.

Given an integer array `hand` where `hand[i]` is the value written on the `ith` card and an integer `groupSize`, return `true` if she can rearrange the cards, or `false` otherwise.

**Example 1:**

**Input:** hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
**Output:** true
**Explanation:** Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]

**Example 2:**

**Input:** hand = [1,2,3,4,5], groupSize = 4
**Output:** false
**Explanation:** Alice's hand can not be rearranged into groups of 4.

**Constraints:**

- `1 <= hand.length <= 104`
- `0 <= hand[i] <= 109`
- `1 <= groupSize <= hand.length`


### My Approach
I sorted the array, then started checking on a per group basis. For each group iteration, I popped the first one and maintained what the expected next one will be . Next I check the expected next one and inc both value for the next expected one in the group if it satisfied. If a num from the list could not be added to the group, it was added in a temp list which was later added back to the remaining list and list was reordered.
```python
# import heapq as hq
class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        
        hand.sort()
        
        while hand:
            # print(hand)
            size = groupSize -1
            first = hand.pop(0) 
            exp_num = first + 1
            temp = []
            while size >0 and hand:
                num = hand.pop(0)
                if num == exp_num:
                    exp_num +=1
                    size -=1
                else:
                    temp.append(num)
                    # return False
            # print("temp",temp)
            if size !=0:
                return False
            #pushing back the remaining
            hand.extend(temp)
            hand.sort()
            
            
            
        return True
```


### Better and Faster Approach
basically instead of resorting it every time, it just checks for the successor in the remaining list and keeps eliminating the ones added to the group by labelling with -1.

```python
class Solution(object):
    def find_successors(self, hand, groupSize, i, n):
        next_val = hand[i] + 1
        hand[i] = -1  # Mark as used
        count = 1
        i += 1
        while i < n and count < groupSize:
            if hand[i] == next_val:
                next_val = hand[i] + 1
                hand[i] = -1
                count += 1
            i += 1
        return count == groupSize

    def isNStraightHand(self, hand, groupSize):
        n = len(hand)
        if n % groupSize != 0:
            return False
        hand.sort()
        for i in range(n):
            if hand[i] >= 0:
                if not self.find_successors(hand, groupSize, i, n):
                    return False
        return True
        
```