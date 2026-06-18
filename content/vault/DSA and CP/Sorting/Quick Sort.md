---
title: "Quick Sort"
---

Quick Sort is a **Divide and Conquer** algorithm. It picks an element as a pivot and partitions the given array around the picked pivot.

### Step-by-Step Breakdown

Let's trace the algorithm using an example array: `[10, 80, 30, 90, 40, 50, 70]`

#### 1. Choose a Pivot

There are many different versions of quickSort that pick pivot in different ways:

* Always pick the first element as a pivot.
* Always pick the last element as a pivot (we will use this common approach below).
* Pick a random element as a pivot.
* Pick median as a pivot.

For our array, let's pick the last element, **70**, as the pivot.

#### 2. Partitioning (The Core Element)

The goal of partitioning is to find the correct sorted position for our pivot. We rearrange the array so that:

* All elements **smaller** than the pivot are moved to its **left**.
* All elements **greater** than the pivot are moved to its **right**.

We use a pointer `i` to track the boundary of elements smaller than the pivot. We iterate through the array using index `j`. [Quick Sort Partition](/vault/dsa-and-cp/sorting/quick-sort-partition/)

* **Initial state:** Array = `[10, 80, 30, 90, 40, 50, 70]`, Pivot = `70`, `i = -1`
* **j = 0:** Element `10` < `70`. Increment `i` to `0`. Swap `arr[0]` with `arr[0]` (no change).
`[10, 80, 30, 90, 40, 50, 70]`
* **j = 1:** Element `80` > `70`. Do nothing.
* **j = 2:** Element `30` < `70`. Increment `i` to `1`. Swap `arr[1]` (`80`) and `arr[2]` (`30`).
`[10, 30, 80, 90, 40, 50, 70]`
* **j = 3:** Element `90` > `70`. Do nothing.
* **j = 4:** Element `40` < `70`. Increment `i` to `2`. Swap `arr[2]` (`80`) and `arr[4]` (`40`).
`[10, 30, 40, 90, 80, 50, 70]`
* **j = 5:** Element `50` < `70`. Increment `i` to `3`. Swap `arr[3]` (`90`) and `arr[5]` (`50`).
`[10, 30, 40, 50, 80, 90, 70]`
* **Loop Ends.** Finally, swap the pivot `arr[6]` (`70`) with `arr[i+1]` (`arr[4]` which is `80`).
`[10, 30, 40, 50, 70, 90, 80]`

The pivot `70` is now in its **correct sorted position** (index 4).

#### 3. Recursion

Now the algorithm independently repeats this process for the two sub-arrays generated:

* Left sub-array: `[10, 30, 40, 50]`
* Right sub-array: `[90, 80]`

This continues until the sub-arrays have a size of 0 or 1, at which point the array is fully sorted.

---

## Code Implementations

### 1. Python Implementation

```python
def partition(arr, low, high):
    # Choose the rightmost element as pivot
    pivot = arr[high]
    
    # Pointer for greater element
    i = low - 1
    
    # Traverse through all elements and compare each element with pivot
    for j in range(low, high):
        if arr[j] <= pivot:
            # If element smaller than pivot is found, swap it with the greater element pointed by i
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    # Swap the pivot element with the greater element specified by i
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Return the position from where partition is done
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        # Find pivot element such that element smaller than pivot are on left
        # and element greater than pivot are on right
        pi = partition(arr, low, high)
        
        # Recursive call on the left of pivot
        quick_sort(arr, low, pi - 1)
        
        # Recursive call on the right of pivot
        quick_sort(arr, pi + 1, high)

# Driver code to test above
data = [10, 80, 30, 90, 40, 50, 70]
print("Unsorted Array:", data)

quick_sort(data, 0, len(data) - 1)
print("Sorted Array:", data)

```

---

### 2. C++ Implementation

```cpp
#include <iostream>
#include <vector>

using namespace std;

// Function to swap two elements
void swap(int& a, int& b) {
    int t = a;
    a = b;
    b = t;
}

// Partition function
int partition(vector<int>& arr, int low, int high) {
    // Choose the rightmost element as pivot
    int pivot = arr[high];
    
    // Pointer for greater element
    int i = (low - 1); 

    for (int j = low; j < high; j++) {
        // If current element is smaller than or equal to pivot
        if (arr[j] <= pivot) {
            i++; // increment index of smaller element
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (i + 1);
}

// Quick Sort function
void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        // pi is partitioning index, arr[p] is now at right place
        int pi = partition(arr, low, high);

        // Separately sort elements before partition and after partition
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// Function to print an array
void printArray(const vector<int>& arr) {
    for (int i : arr)
        cout << i << " ";
    cout << endl;
}

int main() {
    vector<int> data = {10, 80, 30, 90, 40, 50, 70};
    cout << "Unsorted Array: ";
    printArray(data);
    
    quickSort(data, 0, data.size() - 1);
    
    cout << "Sorted Array: ";
    printArray(data);
    return 0;
}

```