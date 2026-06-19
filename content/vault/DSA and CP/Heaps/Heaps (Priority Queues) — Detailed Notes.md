---
title: "Heaps (Priority Queues) — Detailed Notes"
lastmod: 2026-06-16
---



> Based on: _Heaps Visually Explained (Priority Queues)_ Topic: Max Heap — structure, insertion, deletion, and building from an array

---

## 1. What is a Heap?

A **heap** is a special **complete binary tree** that satisfies the **heap property**:

- **Max Heap**: Every parent node is **greater than or equal to** its children. The maximum element is always at the root.
- **Min Heap**: Every parent node is **less than or equal to** its children. The minimum element is always at the root.

> Think of a heap as a "partially sorted" tree — it doesn't guarantee full ordering like a BST, but it guarantees the root is always the extreme (max or min) value.

### Complete Binary Tree — Quick Recap

A binary tree is **complete** if:

- All levels are fully filled **except possibly the last level**.
- The last level is filled **from left to right** with no gaps.

This property is what makes heaps efficiently representable as arrays.

---

## 2. Array Representation of a Heap

Heaps are almost always stored as **arrays**, not as pointer-based trees. The mapping is:

For a node at index `i` (1-indexed):

|Relation|Formula|
|---|---|
|Left child|`2*i`|
|Right child|`2*i + 1`|
|Parent|`i // 2`|

For **0-indexed** arrays:

|Relation|Formula|
|---|---|
|Left child|`2*i + 1`|
|Right child|`2*i + 2`|
|Parent|`(i - 1) // 2`|

> **Why arrays?** Because a complete binary tree has no "gaps" in level-order traversal, the array mapping is lossless and contiguous — no pointers needed, cache-friendly.

---

## 3. Insertion into a Max Heap

**Goal:** Add a new element while maintaining the heap property.

**Steps:**

1. Insert the new element at the **end of the array** (next available position in the last level, left to right).
2. **Sift up** (also called "bubble up" or "heapify up"): Compare the new element with its **parent**.
    - If the new element is **greater than its parent**, swap them.
    - Repeat until the element is in the correct position (either it's ≤ its parent, or it's become the root).

**Example:**

```
Insert 85 into: [90, 75, 80, 55, 60, 65, 70]

Step 1 — Place at end:
[90, 75, 80, 55, 60, 65, 70, 85]
                                ^

Step 2 — 85 > parent(55)? Yes → swap
[90, 75, 80, 85, 60, 65, 70, 55]

Step 3 — 85 > parent(75)? Yes → swap
[90, 85, 80, 75, 60, 65, 70, 55]

Step 4 — 85 > parent(90)? No → stop
Final: [90, 85, 80, 75, 60, 65, 70, 55]
```

**Time Complexity:** O(log n) — at most, the element travels from the leaf to the root, which is the height of the tree.

---

## 4. Deletion from a Max Heap

In a heap, you can only efficiently delete the **root** (i.e., the maximum in a max heap). This is the "extract max" operation.

**Steps:**

1. **Save** the root value (this is what you're returning).
2. **Replace** the root with the **last element** in the array.
3. **Remove** the last element (shrink array by 1).
4. **Sift down** (also called "heapify down"): Compare the new root with its children.
    - Swap it with the **larger child** (in max heap) if that child is greater than the current node.
    - Repeat until the element is in the correct position (both children are smaller, or it's a leaf).

**Example:**

```
Delete root from: [90, 85, 80, 75, 60, 65, 70, 55]

Step 1 — Save 90 (return this)
Step 2 — Replace root with last element (55):
[55, 85, 80, 75, 60, 65, 70]

Step 3 — Sift down:
55 vs children {85, 80} → larger is 85 → swap
[85, 55, 80, 75, 60, 65, 70]

55 vs children {75, 60} → larger is 75 → swap
[85, 75, 80, 55, 60, 65, 70]

55 has no children larger → stop
Final: [85, 75, 80, 55, 60, 65, 70]
```

**Time Complexity:** O(log n)

> **Important:** The "replace root with last element" trick is the key insight — it maintains the complete binary tree structure while giving us a starting point to restore the heap property.

---

## 5. Building a Heap from an Array (Heapify)

Given an **arbitrary array**, how do we turn it into a valid max heap?

### Naive approach:

Insert each element one by one → O(n log n)

### Efficient approach — Bottom-Up Heapify (Floyd's Algorithm):

**O(n)** — this is surprising and important!

**Key insight:** Leaf nodes (bottom half of the array) already satisfy the heap property trivially. So we only need to sift-down the **non-leaf nodes**.

**Steps:**

1. Start from the **last non-leaf node** (index `n//2` in 1-indexed, or `n//2 - 1` in 0-indexed).
2. Call `sift_down` on that node.
3. Move left (decrement index) and repeat for all nodes up to the root.

**Example:**

```
Input array: [10, 20, 15, 30, 40]

Visualized as tree:
        10
       /  \
      20   15
     / \
    30  40

Last non-leaf = index 2 (value 20)

Step 1 — Heapify at index 2 (value 20):
20 vs {30, 40} → larger is 40 → swap
        10
       /  \
      40   15
     / \
    30  20

Step 2 — Heapify at index 1 (value 10):
10 vs {40, 15} → larger is 40 → swap
        40
       /  \
      10   15
     / \
    30  20

10 vs {30, 20} → larger is 30 → swap
        40
       /  \
      30   15
     / \
    10  20

Done. Max heap: [40, 30, 15, 10, 20]
```

**Why O(n)?** Most nodes are near the bottom and have very little work to do. The math works out to O(n) even though there are O(n) nodes and each sift-down is O(log n) in the worst case — because the nodes near the leaves sift down barely at all.

---

## 6. Heap Sort

Heaps enable an elegant in-place O(n log n) sorting algorithm:

1. **Build** a max heap from the array → O(n)
2. **Repeatedly extract the max:**
    - Swap the root (max) with the last element.
    - Reduce heap size by 1.
    - Sift down the new root.
3. After n-1 extractions, the array is sorted in ascending order.

**Time:** O(n log n) | **Space:** O(1) in-place

---

## 7. Priority Queue — The Abstraction

A **Priority Queue** is an abstract data type (ADT) where:

- Each element has a **priority**.
- The element with the **highest priority** is always served (dequeued) first.

A heap is the most common and efficient underlying data structure to implement a priority queue.

|Operation|Time Complexity|
|---|---|
|Insert|O(log n)|
|Extract Max/Min|O(log n)|
|Peek Max/Min|O(1)|
|Build from array|O(n)|

---

## 8. Key Properties Summary

|Property|Value|
|---|---|
|Structure|Complete Binary Tree|
|Storage|Array (index-based)|
|Max element access|O(1) — always at root|
|Insert|O(log n)|
|Delete (root)|O(log n)|
|Build heap|O(n)|
|Heap Sort|O(n log n), O(1) space|

---

## 9. Extra Pointers Worth Knowing

### Heap vs BST

- A **BST** maintains full ordering (left < root < right at every node) — supports search in O(log n).
- A **heap** only guarantees the root is the max/min — does **not** support efficient arbitrary search.
- Use a heap when you only care about repeatedly extracting the max or min.

### Python's `heapq`

Python's standard library `heapq` is a **min-heap** by default. To simulate a max-heap, negate the values before inserting: `heapq.heappush(h, -val)`.

```python
import heapq

# Min heap
h = []
heapq.heappush(h, 10)
heapq.heappush(h, 5)
heapq.heappush(h, 20)
print(heapq.heappop(h))  # → 5

# Max heap trick
h = []
heapq.heappush(h, -10)
heapq.heappush(h, -5)
heapq.heappush(h, -20)
print(-heapq.heappop(h))  # → 20
```

### `heapq.heapify` is O(n)

```python
arr = [10, 20, 15, 30, 40]
heapq.heapify(arr)  # In-place, O(n) — not O(n log n)
```

### Common CP/Interview Patterns

- **Kth largest/smallest element** → maintain a heap of size K
- **Merge K sorted lists** → use a min-heap of size K
- **Top K frequent elements** → count frequencies, then use heap
- **Sliding window maximum** → use a max-heap or deque
- **Dijkstra's shortest path** → uses a min-heap for greedy extraction

### Deletion of Arbitrary Elements

Standard heaps don't support O(log n) deletion of arbitrary elements. Workaround: mark elements as "deleted" lazily and skip them on extraction (common in Dijkstra's with duplicate entries). True arbitrary deletion requires a more advanced structure like an indexed priority queue.

### Two-Heap Trick

A classic technique: maintain a **max-heap** for the lower half and a **min-heap** for the upper half of a stream. Enables O(log n) median finding — useful in problems like "Find Median from Data Stream" (LeetCode 295).

---

## 10. Sift Up vs Sift Down — When to Use Which

|Operation|Direction|Used In|
|---|---|---|
|Insertion|Sift **up** (leaf → root)|Adding new element|
|Deletion|Sift **down** (root → leaf)|Extracting max/min|
|Build heap|Sift **down** only|Floyd's bottom-up heapify|

> An important subtle point: building a heap with repeated `sift_up` calls (inserting one by one) is O(n log n). Building with `sift_down` from the bottom up is O(n). The asymmetry exists because there are many more nodes near the bottom of the tree, and sift-down on those nodes is cheap.