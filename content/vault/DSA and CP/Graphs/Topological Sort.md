---
title: "Topological Sort"
lastmod: 2026-07-05
---

## What it is
A **topological sort** (topo sort) of a **Directed Acyclic Graph (DAG)** is a linear ordering of vertices such that for every directed edge `u -> v`, `u` comes before `v` in the ordering.

- Only defined for **DAGs**. If the graph has a cycle, no valid topological order exists.
- Not unique — a graph can have multiple valid topological orderings.
- Classic use cases: task scheduling with dependencies, build systems (compiling files in the right order), course prerequisite ordering, resolving package dependencies.
## Two main approaches

### 1. Kahn's Algorithm (BFS-based, uses in-degree)

**Idea:** Repeatedly remove nodes with in-degree 0 (no remaining dependencies), and decrease the in-degree of their neighbors.

**Steps:**
1. Compute in-degree of every vertex.
2. Push all vertices with in-degree 0 into a queue.
3. Pop a vertex, add it to the result, and decrement in-degree of its neighbors.
4. If a neighbor's in-degree becomes 0, push it into the queue.
5. Repeat until the queue is empty.
6. If the result contains fewer vertices than the graph has, there's a **cycle** → no valid topo order.

**Complexity:** `O(V + E)` time, `O(V)` extra space.

### 2. DFS-based Algorithm

**Idea:** Run DFS. When a vertex finishes exploring all its descendants (post-order), push it onto a stack. Reverse the stack at the end (or just pop it in order) to get the topo order.

**Steps:**

1. Mark all vertices unvisited.
2. For each unvisited vertex, run DFS.
3. In DFS, after visiting all neighbors of `v`, push `v` onto a stack. (This is equivalent to updating the postvisit number of that node.)
4. After all DFS calls finish, pop the stack — that's the topological order. (equivalent to ordering the vertices based on the postvisit number)
5. Cycle detection: track nodes in the current recursion path (a "visiting" state); if you hit a node that's currently being visited, there's a cycle.

**Complexity:** `O(V + E)` time, `O(V)` extra space (recursion stack + result stack).

---
## Kahn's vs DFS — when to prefer which

|                                        | Kahn's (BFS)                                  | DFS-based                                        |
|:--------------------------------------:| --------------------------------------------- | ------------------------------------------------ |
|            Cycle detection             | Natural (leftover nodes)                      | Needs explicit "in-progress" marking             |
| Gives lexicographically smallest order | Yes, if you use a min-heap instead of a queue | No, harder to control                            |
|          Iterative by default          | Yes                                           | Recursive (can hit stack limits on large graphs) |
|               Intuition                | "Process what's ready"                        | "Finish dependents first"                        |

---

## Python Implementation

```python
from collections import deque, defaultdict

# ---------- Kahn's Algorithm (BFS) ----------
def topo_sort_kahn(num_vertices, edges):
    """
    edges: list of (u, v) meaning u -> v (u is a prerequisite of v)
    Returns topological order, or [] if a cycle exists.
    """
    adj = defaultdict(list)
    in_degree = [0] * num_vertices

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([v for v in range(num_vertices) if in_degree[v] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != num_vertices:
        return []  # cycle detected, no valid topo order

    return order


# ---------- DFS-based Algorithm ----------
def topo_sort_dfs(num_vertices, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    UNVISITED, VISITING, DONE = 0, 1, 2
    state = [UNVISITED] * num_vertices
    stack = []
    has_cycle = [False]

    def dfs(node):
        state[node] = VISITING
        for neighbor in adj[node]:
            if state[neighbor] == UNVISITED:
                dfs(neighbor)
            elif state[neighbor] == VISITING:
                has_cycle[0] = True  # back edge -> cycle
        state[node] = DONE
        stack.append(node)

    for v in range(num_vertices):
        if state[v] == UNVISITED:
            dfs(v)

    if has_cycle[0]:
        return []

    return stack[::-1]


if __name__ == "__main__":
    # Example: 6 vertices, edges represent dependencies
    n = 6
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]

    print("Kahn's:", topo_sort_kahn(n, edges))
    print("DFS:   ", topo_sort_dfs(n, edges))
```

---

## C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

// ---------- Kahn's Algorithm (BFS) ----------
vector<int> topoSortKahn(int n, vector<pair<int,int>>& edges) {
    vector<vector<int>> adj(n);
    vector<int> inDegree(n, 0);

    for (auto& [u, v] : edges) {
        adj[u].push_back(v);
        inDegree[v]++;
    }

    queue<int> q;
    for (int i = 0; i < n; i++)
        if (inDegree[i] == 0) q.push(i);

    vector<int> order;
    while (!q.empty()) {
        int node = q.front(); q.pop();
        order.push_back(node);
        for (int neighbor : adj[node]) {
            if (--inDegree[neighbor] == 0)
                q.push(neighbor);
        }
    }

    if ((int)order.size() != n) return {};  // cycle detected
    return order;
}

// ---------- DFS-based Algorithm ----------
void dfsUtil(int node, vector<vector<int>>& adj, vector<int>& state,
             stack<int>& st, bool& hasCycle) {
    state[node] = 1; // visiting
    for (int neighbor : adj[node]) {
        if (state[neighbor] == 0) {
            dfsUtil(neighbor, adj, state, st, hasCycle);
        } else if (state[neighbor] == 1) {
            hasCycle = true; // back edge -> cycle
        }
    }
    state[node] = 2; // done
    st.push(node);
}

vector<int> topoSortDFS(int n, vector<pair<int,int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& [u, v] : edges) adj[u].push_back(v);

    vector<int> state(n, 0); // 0 = unvisited, 1 = visiting, 2 = done
    stack<int> st;
    bool hasCycle = false;

    for (int i = 0; i < n; i++)
        if (state[i] == 0)
            dfsUtil(i, adj, state, st, hasCycle);

    if (hasCycle) return {};

    vector<int> order;
    while (!st.empty()) {
        order.push_back(st.top());
        st.pop();
    }
    return order;
}

int main() {
    int n = 6;
    vector<pair<int,int>> edges = {{5,2}, {5,0}, {4,0}, {4,1}, {2,3}, {3,1}};

    auto kahnOrder = topoSortKahn(n, edges);
    auto dfsOrder  = topoSortDFS(n, edges);

    cout << "Kahn's: ";
    for (int v : kahnOrder) cout << v << " ";
    cout << "\n";

    cout << "DFS:    ";
    for (int v : dfsOrder) cout << v << " ";
    cout << "\n";

    return 0;
}
```

---

## Notes / gotchas

- **Cycle detection is built-in** to both methods — always check for it before trusting the output, especially in scheduling problems (e.g., LeetCode "Course Schedule II").
- If the problem needs the **lexicographically smallest** valid ordering, swap the `queue` in Kahn's for a `priority_queue` (min-heap).
- The DFS version's recursion can overflow the call stack on very large/deep graphs (say, >10^5 nodes) — convert to an iterative DFS with an explicit stack if needed.
- Multiple valid outputs are normal; don't assume there's a unique "correct" answer unless the graph enforces one (e.g., it's already a simple path).
- Time complexity for both: **O(V + E)**. Space: **O(V + E)** for the adjacency list plus **O(V)** for auxiliary structures.