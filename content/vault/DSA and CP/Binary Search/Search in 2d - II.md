---
title: "Search in 2d - II"
lastmod: 2026-07-03
---

#cp-medium 





## My Solution

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        
        m = len(matrix)
        n = len(matrix[0])
        i = m // 2
        j = n // 2
        
        if matrix[i][j] == target:
            return True
        elif matrix[i][j] < target:
            # search bottom-left, top-right, bottom-right
            block1 = self.searchMatrix([row[j+1:] for row in matrix[:i]], target) if i > 0 and j+1 < n else False
            block2 = self.searchMatrix([row[:j] for row in matrix[i+1:]], target) if i+1 < m and j > 0 else False
            block3 = self.searchMatrix([row[j+1:] for row in matrix[i+1:]], target) if i+1 < m and j+1 < n else False
            return block1 or block2 or block3
        else:
            # search top-left, top-right, bottom-left
            block1 = self.searchMatrix([row[:j] for row in matrix[:i]], target) if i > 0 and j > 0 else False
            block2 = self.searchMatrix([row[j+1:] for row in matrix[:i]], target) if i > 0 and j+1 < n else False
            block3 = self.searchMatrix([row[:j] for row in matrix[i+1:]], target) if i+1 < m and j > 0 else False
            return block1 or block2 or block3
```

## Approach
The key insight is the **corner choice**.

---

**Why top-right corner?**

Look at what's true at `matrix[row][col]` when you start at the top-right:
- Everything **below** it (same column, larger row) is **strictly greater**
- Everything **to the left** (same row, smaller col) is **strictly smaller**

*At each step, we ensure that we are at the top right of the modified/pruned matrix*
So at every step you have **unambiguous elimination**:
- `matrix[row][col] == target` → found it
- `matrix[row][col] < target` → target can't be anywhere in this row to the left (all smaller *since you start from the top right*), so **eliminate the entire row** → `row++`
- `matrix[row][col] > target` → target can't be anywhere in this column below (all greater ), so **eliminate the entire column** → `col--`

Each step eliminates a full row or column, so worst case is `m + n` steps.

---

**Why not top-left or bottom-right?**
Top-left `matrix[0][0]` — everything right is larger AND everything down is larger. So if target is greater than current, *you don't know* whether to go right or down. **No unambiguous elimination.**

Same problem at bottom-right — if target is smaller, you can't decide between up or left.
Top-right and bottom-left are the only two corners where one direction is strictly larger and the other strictly smaller, giving you a deterministic decision at every step.

---

**Analogy**

Think of it like a sorted decision tree. At each cell you're asking — is the target in the "greater" half or "smaller" half? The corner is the only place where those two halves map cleanly to two directions (row vs column) without overlap.


## Optimal Solution
```python
class Solution:
    def searchMatrix(self, matrix, target):
        row = 0
        col = len(matrix[0]) - 1  # start top-right

        while row < len(matrix) and col >= 0:
            if matrix[row][col] == target:
                return True
            elif matrix[row][col] < target:
                row += 1      # eliminate this row
            else:
                col -= 1      # eliminate this column
        return False
```