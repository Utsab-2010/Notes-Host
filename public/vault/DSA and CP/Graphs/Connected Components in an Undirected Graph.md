---
title: "Connected Components in an Undirected Graph"
lastmod: 2026-07-28
---

## What is a Connected Component?

A **connected component** is a group of nodes in an undirected graph where every node can reach every other node in the same group — and there's no path to nodes outside it.

Think of it like islands. Each island is a connected component. You can walk anywhere on an island, but you can't cross to another island.

```
1 - 2    4 - 5    7
    |        |
    3        6
```

The graph above has **3 connected components**: `{1,2,3}`, `{4,5,6}`, `{7}`.

---
## The Core Idea
The algorithm is simple:
1. Keep a `visited` set/array.
2. Loop over every node.
3. If a node hasn't been visited, it's the start of a new component — do a DFS/BFS from it to mark the whole component.
4. Each time you kick off a new DFS/BFS, increment a counter.

That's it. The counter at the end = number of connected components.

---

## Python Implementation
### DFS (Recursive)
```python
def count_components_dfs(n, edges):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n

    def dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    count = 0
    for node in range(n):
        if not visited[node]:
            dfs(node)
            count += 1  # new component found

    return count
```

### BFS (Iterative — safer for large graphs, no recursion limit)

```python
from collections import deque

def count_components_bfs(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n
    count = 0

    for start in range(n):
        if not visited[start]:
            count += 1
            queue = deque([start])
            visited[start] = True
            while queue:
                node = queue.popleft()
                for neighbor in adj[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

    return count
```

### Union-Find (DSU)

Elegant alternative — union nodes connected by an edge, count distinct roots at the end.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        # union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

def count_components_dsu(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    # count distinct roots
    return len({dsu.find(i) for i in range(n)})
```

---

## C++ Implementation

### DFS (Recursive)

```cpp
#include <vector>
using namespace std;

void dfs(int node, vector<vector<int>>& adj, vector<bool>& visited) {
    visited[node] = true;
    for (int neighbor : adj[node]) {
        if (!visited[neighbor])
            dfs(neighbor, adj, visited);
    }
}

int countComponents(int n, vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }

    vector<bool> visited(n, false);
    int count = 0;

    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i, adj, visited);
            count++;
        }
    }
    return count;
}
```

### BFS (Iterative)

```cpp
#include <vector>
#include <queue>
using namespace std;

int countComponentsBFS(int n, vector<vector<int>>& edges) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }

    vector<bool> visited(n, false);
    int count = 0;

    for (int start = 0; start < n; start++) {
        if (visited[start]) continue;
        count++;
        queue<int> q;
        q.push(start);
        visited[start] = true;
        while (!q.empty()) {
            int node = q.front(); q.pop();
            for (int neighbor : adj[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
    }
    return count;
}
```

### Union-Find (DSU)

```cpp
#include <vector>
#include <unordered_set>
using namespace std;

class DSU {
public:
    vector<int> parent, rank_;

    DSU(int n) : parent(n), rank_(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);  // path compression
        return parent[x];
    }

    void unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return;
        if (rank_[px] < rank_[py]) swap(px, py);
        parent[py] = px;
        if (rank_[px] == rank_[py]) rank_[px]++;
    }
};

int countComponentsDSU(int n, vector<vector<int>>& edges) {
    DSU dsu(n);
    for (auto& e : edges) dsu.unite(e[0], e[1]);

    unordered_set<int> roots;
    for (int i = 0; i < n; i++) roots.insert(dsu.find(i));
    return roots.size();
}
```

---

## Complexity

|Method|Time|Space|
|---|---|---|
|DFS / BFS|O(V + E)|O(V + E)|
|DSU (with path compression + union by rank)|O(E · α(V)) ≈ O(E)|O(V)|

`α` is the inverse Ackermann function — practically constant. DSU is slightly faster in practice for dense edge lists.

---

## When to Use What

- **DFS** — simplest to write, fine for most cases. Watch out for recursion depth on very large graphs (Python's default limit is 1000).
- **BFS** — iterative, no stack overflow risk, same complexity.
- **DSU** — best when you're processing edges one at a time (streaming), or when you also need to answer "are these two nodes in the same component?" queries cheaply.

---

## Common Variations

- **Directed graphs** — components aren't symmetric; you need **Strongly Connected Components (SCC)** — Kosaraju's or Tarjan's algorithm.
- **Grid graphs** — same idea, but neighbors are up/down/left/right cells. No explicit adjacency list needed.
- **Counting component sizes** — track size inside DFS/BFS or maintain a `size[]` array in DSU.