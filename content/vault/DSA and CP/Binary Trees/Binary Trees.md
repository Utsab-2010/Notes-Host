---
title: "Binary Trees"
---

## 1. What is a Binary Tree?

A **binary tree** is a hierarchical data structure where each node has **at most two children**, referred to as the **left child** and the **right child**.

```
        1          ← Root
       / \
      2   3        ← Internal nodes
     / \    \
    4   5    6     ← Leaf nodes (no children)
```

Every node contains:

- A **value/data**
- A pointer/reference to the **left child** (or `None`)
- A pointer/reference to the **right child** (or `None`)

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

---

## 2. Terminology

|Term|Meaning|
|---|---|
|**Root**|The topmost node (no parent)|
|**Leaf**|A node with no children|
|**Internal node**|Any node with at least one child|
|**Parent / Child**|Direct ancestor / descendant|
|**Siblings**|Nodes sharing the same parent|
|**Depth of a node**|Number of edges from the root to that node (root has depth 0)|
|**Height of a node**|Number of edges on the longest path from that node to a leaf|
|**Height of tree**|Height of the root node|
|**Level**|All nodes at the same depth (root is level 0 or 1 depending on convention)|
|**Subtree**|A node and all its descendants|
|**Ancestor / Descendant**|Any node on the path to the root / any node reachable going downward|

> **Depth vs Height:** Depth is measured top-down (from root). Height is measured bottom-up (from leaves). A leaf node has height 0.

---

## 3. Types of Binary Trees

### 3.1 Full Binary Tree

Every node has either **0 or 2 children** — never just one.

```
      1
     / \
    2   3
   / \
  4   5
```

**Property:** If there are `n` internal nodes, there are `n+1` leaf nodes.

---

### 3.2 Complete Binary Tree

All levels are **fully filled except possibly the last**, and the last level is filled **from left to right**.

```
      1
     / \
    2   3
   / \ /
  4  5 6
```

Used in: **Heaps** (array representation works because no gaps exist).

---

### 3.3 Perfect Binary Tree

**All internal nodes have exactly 2 children** and **all leaves are at the same level**.

```
        1
       / \
      2   3
     / \ / \
    4  5 6  7
```

**Properties:**

- Height `h` → exactly `2^(h+1) - 1` total nodes
- Exactly `2^h` leaf nodes
- A perfect binary tree is both full and complete

---

### 3.4 Balanced Binary Tree

The height difference between left and right subtrees of **every node** is at most 1.

Height of a balanced tree with `n` nodes: **O(log n)**

Examples: AVL tree, Red-Black tree.

> An unbalanced tree (e.g. a skewed tree) degrades to O(n) for search/insert — the BST worst case.

---

### 3.5 Degenerate / Skewed Tree

Every internal node has only **one child**. Essentially a linked list.

```
1
 \
  2
   \
    3
     \
      4
```

Height = n-1 → all operations O(n). The worst case for BSTs when inserting sorted data.

---

### 3.6 Binary Search Tree (BST)

A binary tree with the ordering property:

- **Left subtree** contains only nodes with values **less than** the parent.
- **Right subtree** contains only nodes with values **greater than** the parent.
- This holds **recursively** for every node.

```
      5
     / \
    3   7
   / \ / \
  2  4 6  8
```

Operations: Search, Insert, Delete — all O(log n) average, O(n) worst case.

---

## 4. Key Properties

### Node Count

|Tree Type|Max Nodes at Level `l`|Total Nodes (height h)|
|---|---|---|
|Any binary tree|`2^l`|`2^(h+1) - 1` (if perfect)|
|Perfect BT|`2^l`|`2^(h+1) - 1`|

- **Minimum nodes** for height `h`: `h + 1` (skewed tree)
- **Maximum nodes** for height `h`: `2^(h+1) - 1` (perfect tree)

### Height

- **Minimum height** for `n` nodes: `⌊log₂(n)⌋`
- **Maximum height** for `n` nodes: `n - 1` (skewed)

### Leaf Nodes in a Full Binary Tree

If a full binary tree has `L` leaves, it has exactly `L - 1` internal nodes, and `2L - 1` total nodes.

---

## 5. Tree Traversals

Traversal = visiting every node exactly once in a specific order.

### 5.1 Inorder (Left → Root → Right)

```python
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)
```

**Key use:** Inorder traversal of a BST gives elements in **sorted ascending order**.

---

### 5.2 Preorder (Root → Left → Right)

```python
def preorder(root):
    if root:
        print(root.val)
        preorder(root.left)
        preorder(root.right)
```

**Key use:** Used to **serialize/copy** a tree. The root always appears first.

---

### 5.3 Postorder (Left → Right → Root)

```python
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val)
```

**Key use:** Used to **delete** a tree (process children before parent) or evaluate expression trees.

---

### 5.4 Level Order (BFS)

Visit nodes level by level, left to right. Uses a **queue**.

```python
from collections import deque

def level_order(root):
    if not root:
        return
    q = deque([root])
    while q:
        node = q.popleft()
        print(node.val)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
```

**Key use:** Finding shortest path, checking if tree is complete, printing level-wise.

---

### Traversal Summary

|Traversal|Order|Common Use|
|---|---|---|
|Inorder|L → Root → R|Sorted output from BST|
|Preorder|Root → L → R|Tree serialization, copy|
|Postorder|L → R → Root|Deletion, expression eval|
|Level Order|Level by level|BFS problems, shortest path|

---

## 6. Important Recursive Patterns

Most binary tree problems reduce to a few recurring recursive patterns.

### Height of a tree

```python
def height(root):
    if not root:
        return -1  # or 0 depending on convention
    return 1 + max(height(root.left), height(root.right))
```

### Count nodes

```python
def count(root):
    if not root:
        return 0
    return 1 + count(root.left) + count(root.right)
```

### Check if two trees are identical

```python
def is_same(p, q):
    if not p and not q: return True
    if not p or not q:  return False
    return p.val == q.val and is_same(p.left, q.left) and is_same(p.right, q.right)
```

### Diameter of a tree

The diameter is the longest path between any two nodes (may or may not pass through root).

```python
def diameter(root):
    res = [0]
    def height(node):
        if not node: return 0
        l, r = height(node.left), height(node.right)
        res[0] = max(res[0], l + r)
        return 1 + max(l, r)
    height(root)
    return res[0]
```

---

## 7. Tree Reconstruction

### From Inorder + Preorder

- First element of preorder = root.
- Find root in inorder → elements to its left form the left subtree, right form the right subtree.
- Recurse.

### From Inorder + Postorder

- Last element of postorder = root.
- Same split logic using inorder.

> **You cannot uniquely reconstruct a binary tree from just one traversal.** You always need inorder + one of (preorder or postorder). Exception: if the tree is a BST, inorder alone suffices since it gives sorted values.

---

## 8. Extra Pointers Worth Knowing

### Null/None paths

When recursing, `if not root: return base_case` is the standard base case. Be careful about what you return — `0`, `-1`, `True`, `False`, or `None` all mean different things depending on the problem.

### Stack-based iterative traversals

Recursive traversals use the call stack implicitly. For very deep trees (risk of stack overflow), iterative versions using an explicit stack are safer.

```python
# Iterative inorder
def inorder_iter(root):
    stack, result = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

### Morris Traversal

Inorder traversal in **O(1) space** (no stack, no recursion) using temporary thread links. Rarely asked but impressive to know.

### LCA (Lowest Common Ancestor)

The LCA of two nodes `p` and `q` is the deepest node that is an ancestor of both.

```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left  = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root   # p and q are on opposite sides
    return left or right
```

### Common Interview Problem Categories

- **Path problems:** max path sum, root-to-leaf paths, path sum equals target
- **View problems:** left view, right view, top view, bottom view (level order + tracking)
- **Symmetry / Mirror:** check if tree is symmetric, invert a binary tree
- **Serialization:** encode a tree to string and decode it back
- **BST-specific:** validate BST, kth smallest, range sum
- **Construction:** build from traversals, construct BST from preorder

### Array representation (for complete binary trees)

Same index formula as heaps:

- Left child of `i` → `2*i + 1`
- Right child of `i` → `2*i + 2`
- Parent of `i` → `(i-1) // 2`