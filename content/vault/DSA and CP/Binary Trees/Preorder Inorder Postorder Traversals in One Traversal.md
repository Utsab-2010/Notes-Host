---
title: "Preorder Inorder Postorder Traversals in One Traversal"
---

This approach traverses the binary tree in a single pass while computing the preorder, inorder and postorder traversals at the same time. A stack is used for state management. The stack keeps track of the traversal state for each node. It stores nodes and their state information allowing the algorithm to resume traversal from intermediate points. For each node, it identifies its state i.e. if it's in the preorder state, it records the node's value and pushes the left child onto the stack. Moving to the inorder state, it records the node's value and pushes the right child onto the stack. Finally, in the post-order state, it stores the node's value and pops the node. As the algorithm executes over each node, it pushes each value in separate arrays for preorder, inorder and postorder traversals depending upon the current order and sequence. Hence, we are able to traverse the tree just once and get all three traversals from it.

- Start at the root of the binary tree.Initialise a stack that holds a tree node and an integer value representing its state corresponding to pre order, inorder and postorder. Initialise empty arrays to store the three traversals as well.Check if the tree is empty. If so, return empty traversals.

![](https://static.takeuforward.org/content/-GvXoCuOz)

- Push the root node onto the stack along with its state ‘1’ (preorder) to start the traversal.
- While the stack isn’t empty, pop the top node of the stack and for each node:
    - If the state is ‘1’ ie. preorder: store the node’s data in the preorder array and move its state to 2 (inorder) for this node. Push this updated state back onto the stack and push its left child as well.
    - If the state is ‘2’ ie. inorder: store the node’s data is the inorder array and update its state to 3 (postorder) for this node. Push the updated state back onto the stack and push the right child onto the stack as well.
    - If the state is ‘3’ ie. postorder: store the node’s data in the postorder array and pop it.
- Return the preorder, inorder and postorder array.
![](/vault/attachments/pasted-image-20260613230436.png)



```python
# Node structure for the binary tree
class Node:
    # Constructor to initialize the node with a value
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None

# Solution class containing the traversal function
class Solution:
    # Function to get the Preorder,
    # Inorder and Postorder traversal
    # Of Binary Tree in One traversal
    def preInPostTraversal(self, root):
        # Lists to store traversals
        pre, ino, post = [], [], []

        # If the tree is empty, return empty traversals
        if root is None:
            return []

        # Stack to maintain nodes and their traversal state
        st = [(root, 1)]

        while st:
            node, state = st.pop()

            # this is part of pre
            if state == 1:
                # Store the node's data in the preorder traversal
                pre.append(node.data)
                # Move to state 2 (inorder) for this node
                st.append((node, 2))

                # Push left child onto the stack for processing
                if node.left:
                    st.append((node.left, 1))

            # this is a part of in
            elif state == 2:
                # Store the node's data in the inorder traversal
                ino.append(node.data)
                # Move to state 3 (postorder) for this node
                st.append((node, 3))

                # Push right child onto the stack for processing
                if node.right:
                    st.append((node.right, 1))

            # this is part of post
            else:
                # Store the node's data in the postorder traversal
                post.append(node.data)

        # Returning the traversals
        return [pre, ino, post]

# Main function
if __name__ == "__main__":
    # Creating a sample binary tree
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    # Create object of Solution class
    sol = Solution()

    # Getting the traversals
    traversals = sol.preInPostTraversal(root)

    # Extracting and printing the traversals
    pre = traversals[0]
    ino = traversals[1]
    post = traversals[2]

    print("Preorder traversal:", *pre)
    print("Inorder traversal:", *ino)
    print("Postorder traversal:", *post)

```