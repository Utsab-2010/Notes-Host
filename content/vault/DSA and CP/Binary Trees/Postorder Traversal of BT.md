---
title: "Postorder Traversal of BT"
---


Left -> RIGght -> Root traversal

### Iterative Approach
- Create two stacks: one for holding nodes and another for storing the final postorder traversal sequence. Initialize an array `postorder` to store the traversal sequence.
- Push the root node to the first stack.
- Process the nodes until the first stack is empty:
    - Pop a node from the top of the first stack.
    - Push this node onto the second stack.
    - Push its left child (if it exists) onto the first stack.
    - Push its right child (if it exists) onto the first stack.
- Once the first stack is empty, retrieve the nodes in the postorder sequence by popping nodes from the second stack one by one and store them in the postorder array.
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack1 = []
        stack2 = [] # Stores the final post-order(technically stores it reversed initially. flipped later on)
        if not root:
            return stack2
        stack1.append(root)
        while stack1:
            curr = stack1.pop()
            stack2.append(curr.val)
            if curr.left:
                stack1.append(curr.left)
            if curr.right:
                stack1.append(curr.right)
            
        stack2.reverse()
        return stack2
```


### Detailed Logic behind the Iterative Approach
The intuition relies on a **reversal trick** that turns a structurally difficult problem into a straightforward one.

### 1. The Bottleneck of Postorder

Iterative postorder traversal ($Left \to Right \to Root$) is notoriously tricky with a single stack. Because the parent node must be visited *last*, you have to traverse down to the leaves, process them, and somehow backtrack to the parent without prematurely removing it from the stack. Tracking whether you are returning from a left child or a right child requires tedious bookkeeping.

### 2. The Reversal Insight

To bypass this complexity, look at the target sequence in reverse:


$$\text{Reverse of } (Left \to Right \to Root) = (Root \to Right \to Left)$$

Generating a $Root \to Right \to Left$ sequence iteratively is incredibly simple because it is just a modified Preorder DFS.

### 3. The Dual Stack Execution

* **`stack1` (The Driver):** Runs the modified DFS. Because a stack is Last-In, First-Out (LIFO), pushing the `left` child before the `right` child ensures the `right` child is popped and processed first. This effortlessly builds the $Root \to Right \to Left$ order.
* **`stack2` (The Inverter):** Instead of printing the nodes, you push them straight into `stack2`. The first node processed ($Root$) sinks to the bottom, while the last nodes processed ($Left$ leaves) stay at the top.

Reversing `stack2` flips the sequence perfectly back into $Left \to Right \to Root$.