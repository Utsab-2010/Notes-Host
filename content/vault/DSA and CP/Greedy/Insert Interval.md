---
title: "Insert Interval"
---

#cp_medium 




### My Code (badly written)
```python
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        N = len(intervals)
        pre_i,pos_i = 0,N-1

        j = pos_i
        newIntervals= []

        if not (N):
            return [newInterval]
        elif N==1:
            
        else:
            for i in range(len(intervals)-1):
                
                if intervals[i][0] <= newInterval[0]:
                    pre_i = i
                if intervals[j][1] >= newInterval[1]:
                    pos_i = j
                j-=1        
        merged_pre = []
        merged_pos = []
        merged = []
        if newInterval[0]-intervals[pre_i][1] <= 0 :
            merged_pre= [intervals[pre_i][0],newInterval[1]]
            pre_i-=1
        if newInterval[1] - intervals[pos_i][0] >= 0:
            merged_pos = [newInterval[0],intervals[pos_i][1]]
            pos_i+=1
        
        if merged_pre and merged_pos:
            merged = [merged_pre[0],merged_pos[1]]
        elif merged_pre:
            merged = merged_pre
        elif merged_pos:
            merged = merged_pos
        else:
            merged = newInterval
        print(merged)
        print(pre_i,pos_i)
        if pre_i >=0:
            for i in range(pre_i+1):
                newIntervals.append(intervals[i])
        newIntervals.append(merged)
        if pos_i < len(intervals):
            for i in range(pos_i,len(intervals)):
                newIntervals.append(intervals[i])

        return newIntervals
        
        
            
```
*Did not cover the edge cases properly!*

### Better Code
```python
class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        n = len(intervals)
        i = 0
        res = []

        # Case 1: No overlapping before merging intervals
        while i < n and intervals[i][1] < newInterval[0]:
            res.append(intervals[i])
            i += 1

        # Case 2: Overlapping and merging intervals
        while i < n and newInterval[1] >= intervals[i][0]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        res.append(newInterval)

        # Case 3: No overlapping after merging newInterval
        while i < n:
            res.append(intervals[i])
            i += 1

        return res
```