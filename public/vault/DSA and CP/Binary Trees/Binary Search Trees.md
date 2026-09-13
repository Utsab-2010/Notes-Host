---
title: "Binary Search Trees"
lastmod: 2026-06-18
---

#dsa 
## Core invariant

Every node satisfies: **left subtree values < node < right subtree values**, recursively at every level. This single rule makes search, insert, and delete all reduce to a root-to-leaf path — no backtracking, no scanning.

---

## Structure

```
        40
       /  \
      20   60
     / \  / \
   10  30 50  70
```

- Left child is always strictly less than the parent
- Right child is always strictly greater
- *Inorder traversal always yields a **sorted sequence** (a direct consequence of the invariant, not a coincidence)*
- Duplicates are usually disallowed

---

## Traversals

All traversals apply the same rule **recursively at every node**.

|Traversal|Order|Output on tree above|
|---|---|---|
|**Inorder**|Left → Node → Right|10, 20, 30, 40, 50, 60, 70|
|**Preorder**|Node → Left → Right|40, 20, 10, 30, 60, 50, 70|
|**Postorder**|Left → Right → Node|10, 30, 20, 50, 70, 60, 40|
|**Level-order (BFS)**|Level by level|40, 20, 60, 10, 30, 50, 70|

> **Inorder subtlety:** It doesn't mean "visit left child at _some_ point before the node." It means the _entire_ left subtree is exhausted before the node, and the _entire_ right subtree after. There is no room to interleave nodes from elsewhere.

---

## Operations

### Search — O(h)

At each node, compare target with node value and go left or right. Never need to scan both sides.

```python
def search(node, target):
    if node is None or node.val == target:
        return node
    if target < node.val:
        return search(node.left, target)   # go left
    return search(node.right, target)      # go right
```

### Insert — O(h)

Walk down exactly as in search, attach a new leaf at the first `None` slot.

```python
def insert(node, val):
    if node is None:
        return TreeNode(val)           # found the slot
    if val < node.val:
        node.left = insert(node.left, val)
    elif val > node.val:
        node.right = insert(node.right, val)
    return node
```

### Delete — O(h)

Three cases, in increasing complexity:

|Case|Condition|Action|
|---|---|---|
|1|Node is a leaf|Just remove it|
|2|Node has one child|Splice it out — link parent directly to the child|
|3|Node has two children|Replace node's value with its **inorder successor** (leftmost node in right subtree), then delete the successor|

```python
def inorder_successor(node):
    # leftmost node in right subtree
    cur = node.right
    while cur.left is not None:
        cur = cur.left
    return cur
```

---

## Complexity

|Operation|Average|Worst case|
|---|---|---|
|Search|O(log n)|O(n)|
|Insert|O(log n)|O(n)|
|Delete|O(log n)|O(n)|
|Space|O(n)|O(n)|

Height `h` determines everything. Balanced tree → `h = O(log n)`. Inserting already-sorted elements gives a degenerate tree (a linked list) with `h = O(n)`. This is why **AVL trees** and **Red-Black trees** exist — they enforce balance after every operation to keep `h = O(log n)` in the worst case.

---

## Inorder traversal (code)

```python
def inorder(node, result=[]):
    if node:
        inorder(node.left, result)
        result.append(node.val)        # visit
        inorder(node.right, result)
    return result
```

---

## Open questions

1. Why does inorder traversal of a BST _always_ give a sorted list? Prove it by induction on tree height.
2. If you insert `n` elements in sorted order, what does the tree look like? What is the worst-case search time?
3. Can you reconstruct a unique BST from only its inorder traversal? What if you also have the preorder?
4. When deleting a two-child node, can you use the inorder _predecessor_ instead of the successor? Does it matter?