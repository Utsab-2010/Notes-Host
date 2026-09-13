---
title: "Course Schedule"
lastmod: 2026-07-05
---

#cp-medium 

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.

- For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.

Return `true` if you can finish all courses. Otherwise, return `false`.

**Example 1:**

**Input:** numCourses = 2, prerequisites = [[1,0]]
**Output:** true
**Explanation:** There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.

**Example 2:**

**Input:** numCourses = 2, prerequisites = `[[1,0],[0,1]]`
**Output:** false
**Explanation:** There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

---
## Solution (BFS)

Just check for cyclicity in the dg and return false is cyclic else true.
















# Special Note
## Wrong Solution
I used CC detection for Undir Graphs which breaks for DGs.
### Why the "parent" check is wrong
In an undirected graph, the standard BFS/DFS cycle check is: _"if I see a visited neighbor that isn't my immediate parent, it's a cycle."_ That works there because every edge is traversed from both directions, so any revisit that isn't the edge you just came from must be a genuine back edge.

In a **directed graph**, this breaks down completely. A node can be reached from multiple different parents perfectly legitimately (a "diamond" shape or a "cross edge") — that's not a cycle, it's just a DAG with converging paths. Your check flags this as a cycle anyway.
```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        
        cc = 0
        visited = [0]*numCourses
        adj = [[] for _ in range(numCourses)]
        # print(adj)
        for course in prerequisites:
            # print(course)
            # a,b then b->a
            adj[course[1]].append(course[0])
        print(adj)
        
        for start in range(numCourses):
            if not visited[start]:
                # cc+=1
                q = []
                q.append([start,-1])
                # visited = [0]*numCourses 
                while (q):
                    node,parent = q.pop(0)
                    visited[node] = 1
                    for course in adj[node]:
                        if not visited[course]:
                            q.append([course,node])
                        elif parent != course:
                            return False
        
        # if cc>1:
        #     return False
        # else:
        return True

            
```