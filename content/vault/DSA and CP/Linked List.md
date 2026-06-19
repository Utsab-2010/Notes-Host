---
title: "Linked List"
lastmod: 2026-06-03
---

## 1. What is a Linked List?

A **linked list** is a data structure made up of a chain of **nodes**, where each node holds:
- Some **data**
- A **pointer** to the next node

Unlike arrays, linked list elements are **not stored in contiguous memory**. Each node can be anywhere in memory — they're connected only through pointers.
```
[data | next] --> [data | next] --> [data | next] --> NULL
   Node 1             Node 2             Node 3
```
---

## 2. Why Use a Linked List?

|Feature|Array|Linked List|
|---|---|---|
|Size|Fixed at compile time|Grows/shrinks at runtime|
|Insert at beginning|O(n) — shift elements|O(1) — just rewire pointers|
|Random access (arr[i])|O(1)|O(n) — must walk the list|
|Memory|Contiguous block|Scattered, each node on heap|

**Use a linked list when** you need frequent insertions/deletions, especially at the front, and don't need random access.

---

## 3. Types of Linked Lists

|Type|Description|
|---|---|
|**Singly Linked**|Each node points only to the **next** node|
|**Doubly Linked**|Each node points to both **next** and **previous** nodes|
|**Circular Linked**|Last node points back to the **first** node|

This note focuses on **Singly Linked Lists** — the most common and foundational type.

---

## 4. The Node — Building Block

Every linked list is made of nodes. In C++, a node is defined as a `struct` or `class`.

```cpp
struct Node {
    int data;       // the value stored
    Node* next;     // pointer to the next node
};
```

### Breaking down the syntax:

```cpp
struct Node {
```

`struct` defines a custom data type called `Node`.

```cpp
    int data;
```

This stores the actual value (can be any type: `int`, `string`, `float`, etc.)

```cpp
    Node* next;
```

This is a **pointer** to another `Node`. The `*` means "pointer to". It holds the **memory address** of the next node.

---

## 5. Creating Nodes (Allocating Memory)

```cpp
Node* newNode = new Node();
newNode->data = 10;
newNode->next = NULL;
```

### What's happening here?

```cpp
Node* newNode
```

Declares a pointer named `newNode` that can point to a `Node`.

```cpp
= new Node();
```

`new` allocates memory on the **heap** (not the stack) and returns a pointer to it.

```cpp
newNode->data = 10;
```

The `->` operator accesses a member of the struct **through a pointer**. Think of it as: "go to what `newNode` points to, then access `data`."

> **Tip:** `newNode->data` is the same as `(*newNode).data`. The arrow `->` is just cleaner shorthand.

```cpp
newNode->next = NULL;
```

Sets the next pointer to `NULL` (nothing), meaning this is the last node.

---

## 6. The Head Pointer

The **head** is just a pointer that always points to the **first node** in the list.

```cpp
Node* head = NULL;  // empty list
```

If `head == NULL`, the list is empty. The entire list is accessible by starting from `head` and following `next` pointers.

---

## 7. A Complete Linked List Class

```cpp
#include <iostream>
using namespace std;

// Step 1: Define the Node
struct Node {
    int data;
    Node* next;
};

// Step 2: Define the LinkedList
class LinkedList {
public:
    Node* head;  // points to the first node

    // Constructor — start with empty list
    LinkedList() {
        head = NULL;
    }

    // Insert at the beginning
    void insertFront(int value) {
        Node* newNode = new Node();  // create new node
        newNode->data = value;       // set its data
        newNode->next = head;        // point it to current head
        head = newNode;              // update head to new node
    }

    // Insert at the end
    void insertEnd(int value) {
        Node* newNode = new Node();
        newNode->data = value;
        newNode->next = NULL;

        if (head == NULL) {          // if list is empty
            head = newNode;
            return;
        }

        Node* temp = head;           // start from head
        while (temp->next != NULL) { // walk until last node
            temp = temp->next;
        }
        temp->next = newNode;        // attach new node at end
    }

    // Delete a node by value
    void deleteNode(int value) {
        if (head == NULL) return;    // empty list, nothing to do

        // Special case: delete the head node
        if (head->data == value) {
            Node* toDelete = head;
            head = head->next;       // move head forward
            delete toDelete;         // free memory
            return;
        }

        // Find the node just before the target
        Node* temp = head;
        while (temp->next != NULL && temp->next->data != value) {
            temp = temp->next;
        }

        if (temp->next == NULL) return; // value not found

        Node* toDelete = temp->next;
        temp->next = temp->next->next;  // skip over the node
        delete toDelete;                // free memory
    }

    // Print the entire list
    void display() {
        Node* temp = head;
        while (temp != NULL) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
};

int main() {
    LinkedList list;

    list.insertEnd(10);
    list.insertEnd(20);
    list.insertEnd(30);
    list.insertFront(5);

    list.display();          // Output: 5 -> 10 -> 20 -> 30 -> NULL

    list.deleteNode(20);
    list.display();          // Output: 5 -> 10 -> 30 -> NULL

    return 0;
}
```

---

## 8. Traversal — Walking the List

Traversal means visiting every node one by one.

```cpp
Node* temp = head;          // start at head

while (temp != NULL) {      // keep going until the end
    cout << temp->data;     // do something with this node
    temp = temp->next;      // move to the next node
}
```

Think of `temp` as a "cursor" — you never move the actual `head`, just a temporary copy of the pointer.

---

## 9. Key Operations Summary

### Insert at Front — O(1)

```cpp
newNode->next = head;   // new node points to old head
head = newNode;         // head now points to new node
```

### Insert at End — O(n)

```cpp
// Walk to last node, then:
lastNode->next = newNode;
```

### Delete a Node — O(n)

```cpp
// Find node before target, then:
prevNode->next = prevNode->next->next;
delete targetNode;
```

### Search — O(n)

```cpp
Node* temp = head;
while (temp != NULL) {
    if (temp->data == target) return true;
    temp = temp->next;
}
return false;
```

---

## 10. Memory Management

Since nodes are created with `new`, they live on the **heap**. You must manually free them with `delete` to avoid **memory leaks**.

```cpp
// Bad — memory leak!
Node* n = new Node();
// never deleted, memory is lost

// Good
Node* n = new Node();
delete n;  // memory freed
```

When deleting a node from the list, always save the pointer first, **then** delete:

```cpp
Node* toDelete = temp->next;       // save the pointer
temp->next = temp->next->next;     // unlink it
delete toDelete;                   // THEN delete
```

---

## 11. Common Pitfalls

|Mistake|What goes wrong|
|---|---|
|Forgetting `delete`|Memory leak — heap fills up over time|
|Deleting then accessing|Dangling pointer — undefined behaviour|
|Not updating `head` on front insert|List looks empty or broken|
|Moving `head` during traversal|Lose track of the list start|
|Not checking for `NULL` before `->next`|Segmentation fault (crash)|

---

## 12. Quick Syntax Cheat Sheet

```cpp
// Declare a pointer
Node* ptr;

// Create a node on the heap
Node* ptr = new Node();

// Access member via pointer (arrow operator)
ptr->data = 42;
ptr->next = NULL;

// Access member via dereferenced pointer (equivalent)
(*ptr).data = 42;

// Check for empty list / end of list
if (head == NULL) { ... }
if (temp->next == NULL) { ... }

// Move to next node
temp = temp->next;

// Free a node from heap
delete ptr;
```

---

## 13. Doubly Linked List (Brief)

In a doubly linked list, each node has **two pointers** — `next` and `prev`.

```cpp
struct Node {
    int data;
    Node* next;
    Node* prev;  // extra pointer going backwards
};
```

This allows you to traverse in **both directions**, but uses slightly more memory per node.

---

## 14. When to Use What

|Situation|Best Choice|
|---|---|
|Frequent insert/delete at front|Linked List|
|Need random access (index lookup)|Array / Vector|
|Unknown or changing size|Linked List|
|Cache-friendly performance matters|Array / Vector|
|Need both front and back operations|Doubly Linked List or `std::deque`|

---

_Happy coding! The key to linked lists is getting comfortable with pointer manipulation — once pointers click, the rest follows naturally._