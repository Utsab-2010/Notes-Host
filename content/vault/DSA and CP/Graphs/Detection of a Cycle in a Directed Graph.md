---
title: "Detection of a Cycle in a Directed Graph"
lastmod: 2026-07-05
---

#cp-theory

## Kahn's Algo
A Topological Sort is a linear ordering of vertices such that for every directed edge from u to v, u comes before v in the ordering. Importantly, a valid topological order exists only if the graph is a Directed Acyclic Graph (DAG). This gives us a powerful idea that if we try to generate a topological sort but cannot include all vertices (some nodes remain stuck due to dependencies), then the graph must contain a cycle.  
  
[Kahn’s Algorithm (Topological Sorting Using BFS)](https://takeuforward.org/data-structure/kahns-algorithm-topological-sort-algorithm-bfs-g-22/) makes this detection very straightforward. It repeatedly removes nodes with zero in-degree and if at the end, the number of removed nodes is less than the total nodes, that means some nodes were locked in cycles, and hence a cycle exists.
- Compute the in-degree of all nodes in the graph.
- Add all nodes with in-degree equal to zero into a queue.
- Process nodes from the queue one by one, increasing the count of processed nodes.
- For each processed node, reduce the in-degree of its neighbors by one.
- If any neighbor’s in-degree becomes zero, push it into the queue.
- After processing, compare the count of processed nodes with the total number of nodes to decide if a cycle exists.

```python
from collections import deque

class Solution:
    # Function to detect cycle in a directed graph using Kahn's Algorithm
    def hasCycle(self, V, adj):
        # Store in-degrees of all nodes
        indegree = [0] * V
        for u in range(V):
            for v in adj[u]:
                indegree[v] += 1

        # Queue for nodes with 0 in-degree
        q = deque()
        for i in range(V):
            if indegree[i] == 0:
                q.append(i)

        # Count visited nodes
        count = 0
        while q:
            node = q.popleft()
            count += 1

            # Reduce in-degree of neighbors
            for neighbor in adj[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    q.append(neighbor)

        # If count != V, cycle exists
        return count != V


if __name__ == "__main__":
    V = 4
    adj = [[1], [2], [3], [1]]

    obj = Solution()
    if obj.hasCycle(V, adj):
        print("Cycle detected")
    else:
        print("No cycle")

```


# DFS Method
## Why three states instead of one boolean
So each node gets one of three states:
- **`WHITE` (0) — unvisited**: haven't touched it yet.
- **`GRAY` (1) — visiting**: currently in the middle of exploring it (it's an ancestor of the node we're at right now, i.e., on the current DFS call stack).
- **`BLACK` (2) — done**: fully explored, along with everything reachable from it.

Main Point : **The only real cycle signal:** while exploring node `u`'s neighbors, if you hit a neighbor that is `GRAY`, that means you've looped back to one of your own ancestors — a genuine **back edge**, i.e., a cycle.

If you hit a neighbor that's `BLACK`, that's totally fine — it just means that neighbor was already fully verified as cycle-free via some other path (this is the "diamond shape" case from before, e.g. two courses both leading into a later course).

## Walkthrough of the logic
1. Build adjacency list: `course -> [courses that depend on it]` (or prerequisite direction — just be consistent).
2. For each node, if it's `WHITE`, start a DFS from it.
3. On entering a node, mark it `GRAY`.
4. For each neighbor:
    - If `GRAY` → cycle found, return `False` immediately.
    - If `WHITE` → recurse into it; if that recursive call finds a cycle, propagate `False` up.
    - If `BLACK` → skip, already safe.
5. After all neighbors are processed, mark the node `BLACK` (we're done with it, it's safe).
6. If no DFS call ever finds a cycle, return `True`. <---IMPORTANT for the below example

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        WHITE, GRAY, BLACK = 0, 1, 2

        adj = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            # b is a prerequisite of a, so edge b -> a
            adj[b].append(a)
		# this is just forming the dag part. Not important!
		
		
        state = [WHITE] * numCourses

        def dfs(node):
            state[node] = GRAY  # currently on the recursion stack

            for neighbor in adj[node]:
                if state[neighbor] == GRAY:
                    return False          # back edge -> cycle
                if state[neighbor] == WHITE:
                    if not dfs(neighbor):
                        return False       # cycle found deeper in recursion

            state[node] = BLACK  # fully explored, safe
            return True

        for course in range(numCourses):
            if state[course] == WHITE:
                if not dfs(course):
                    return False

        return True
```

## Trace on your earlier counterexample

`prerequisites = [[1,0],[2,0],[4,1],[3,2],[4,3]]` → edges `0->1, 0->2, 1->4, 2->3, 3->4`
- `dfs(0)`: mark `0` GRAY → visit `1`
    - `dfs(1)`: mark `1` GRAY → visit `4`
        - `dfs(4)`: mark `4` GRAY → no neighbors → mark `4` BLACK, return `True`
    - back in `dfs(1)`: mark `1` BLACK, return `True`
- back in `dfs(0)`: visit `2`
    - `dfs(2)`: mark `2` GRAY → visit `3`
        - `dfs(3)`: mark `3` GRAY → visit `4`, which is **BLACK** → fine, skip → mark `3` BLACK, return `True`
    - back in `dfs(2)`: mark `2` BLACK, return `True`
- mark `0` BLACK, return `True` ✅ — correctly identifies no cycle, unlike your BFS version.

## Complexity
- **Time:** `O(V + E)` — each node and edge visited once.
- **Space:** `O(V)` for the state array, plus `O(V)` worst-case recursion depth (a long chain of prerequisites). For very large `numCourses` this could hit Python's recursion limit — Kahn's algorithm avoids that entirely since it's iterative by nature.
