---
title: "Nearest 0 from cell in a matrix"
lastmod: 2026-07-03
---

#cp-medium 
Given an `m x n` binary matrix `mat`, return _the distance of the nearest_ `0` _for each cell_.
The distance between two cells sharing a common edge is `1`.
**Example 1:**
![](https://assets.leetcode.com/uploads/2021/04/24/01-1-grid.jpg)
**Inpu
t:** mat = \[[0,0,0],[0,1,0],[0,0,0]]
**Output:**\[[0,0,0],[0,1,0],[0,0,0]]

**Example 2:**
![](https://assets.leetcode.com/uploads/2021/04/24/01-2-grid.jpg)
**Input:** mat =\ [0,0,0],[0,1,0],[1,1,1]]
**Output:** \[[0,0,0],[0,1,0],[1,2,1]]

**Constraints:**
- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 104`
- `1 <= m * n <= 104`
- `mat[i][j]` is either `0` or `1`.
- There is at least one `0` in `mat`.


### Naive Solution
I did BFS from each cell and calculated the nearest cell with 0. Complexity -> (MN * (M+N))
```python
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        
        m = len(mat)
        n = len(mat[0])

        zeros = [[-1 for _ in range(n)] for _ in range(m)]

        for a in range(m):
            for b in range(n):
                
                visited = [[0 for _ in range(n)] for _ in range(m)]

                que= []
                que.append((a,b,0))

                while que:
                    i,j,pos = que.pop(0)
                    
                    if mat[i][j] == 0:
                        zeros[a][b] = pos
                        break

                    print(i,j)
                    visited[i][j] = 1
                    # print(visited)
                    dirs = [(i+1,j),(i,j+1),(i,j-1),(i-1,j)]

                    pos+=1
                    for adj in dirs:
                        p,q = adj
                        if p>=0 and p<m and q>=0 and q<n and not visited[p][q]:
                            que.append((p,q,pos))
                            # print(adj)
                
        return zeros                            
                    
```


### Optimal Solution
Notice that we can think of this in the reverse way - a flood fill starting from the nodes with 0. all non-zero nodes next to 0 will have 1 as the distance. In the next phase, the nodes next to those with distance 1, will get distance 2 and so on till all nodes have been visited.

We can also think of this like a graph where at the 0th layer we have all the 0 nodes, and then the adjacent nodes are the 1st layer and so on layer wise. And we basically need to find the layer of each corresponding node.


