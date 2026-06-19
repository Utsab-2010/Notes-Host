---
title: "Inorder Traversal of a BT"
lastmod: 2026-06-16
---

Left - > Parent -> RIght
###  Recursive Approach
```python 
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        
        if root:
            stack.extend(self.inorderTraversal(root.left))
            stack.append(root.val)
            stack.extend(self.inorderTraversal(root.right))
        return stack
```

### Iterative Approach

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        inorder = []
        curr = root
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            inorder.append(curr.val)
            curr = curr.right
        
        return inorder
            

```


Tree:   4 
       / \
      2   6
     / \ / \
    1  3 5  7
      / \
     3a  3b
 The inorder is still strictly **Left → Node → Right** applied recursively at every level:

**1 → 2 → 3a → 3 → 3b → 4 → 5 → 6 → 7**
### Logic
For the iterative approach think about it this way. You need to go from left to center to right recursively.

You first go down the left as far as you can go. Then if you find null. you take the right child. Now in the right child becomes a new root and you can recursively see that this will continue. 
Now if you don't find a right child. You go back to the parent. having visited the last node(current parent). you now move up to the parent of this node(P2) and then visit the right child of P2. This P2 is again a root that needs to be explored by the same format.

we maintain this with a stack.