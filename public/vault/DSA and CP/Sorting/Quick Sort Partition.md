---
title: "Quick Sort Partition"
lastmod: 2026-06-16
---


The **Partition Algorithm** is the operational core of Quick Sort. Its entire job is to take an array (or a subsection of one), select one element to be the **pivot**, and rearrange the surrounding elements so that everything smaller than the pivot moves to its left, and everything larger moves to its right.

By the end of a single partition step, the pivot element lands in its **exact, final sorted position**.

### The Strategy: Two Pointers (`i` and `j`)

The most common implementation is the **Lomuto Partition Scheme**. It typically chooses the last element as the pivot and uses two pointers that walk through the array from left to right:

- **Pivot:** The target value we are comparing everything against (usually `arr[high]`).
    
- **Pointer `j` (The Explorer):** Scans every element from the start (`low`) up to the element just before the pivot (`high - 1`).
    
- **Pointer `i` (The Boundary Marker):** Tracks the tail end of the "smaller than pivot" zone. It starts just outside the valid boundary (`low - 1`) and only advances when `j` finds a value smaller than the pivot.
    

### Step-by-Step Walkthrough

Let's dissect exactly how the partition algorithm works using the array:

`[10, 80, 30, 90, 40, 50, 70]`

- **Setup:** * `pivot = 70` (the last element)
    
    - `i = -1` (tracks the boundary of smaller elements)
        
    - `j = 0` (starts the loop)
        

#### Loop Steps:

1. **`j = 0` (`arr[0] = 10`):** Is $10 \le 70$? **Yes**.
    
    - Increment `i` to `0`.
        
    - Swap `arr[i]` with `arr[j]` (swapping `10` with `10` changes nothing).
        
    - _Array state:_ `[10, 80, 30, 90, 40, 50, 70]`
        
2. **`j = 1` (`arr[1] = 80`):** Is $80 \le 70$? **No**.
    
    - Do nothing. `i` stays at `0`.
        
    - _Array state:_ `[10, 80, 30, 90, 40, 50, 70]`
        
3. **`j = 2` (`arr[2] = 30`):** Is $30 \le 70$? **Yes**.
    
    - Increment `i` to `1`.
        
    - Swap `arr[i]` (`80`) with `arr[j]` (`30`).
        
    - _Array state:_ `[10, 30, 80, 90, 40, 50, 70]`
        
4. **`j = 3` (`arr[3] = 90`):** Is $90 \le 70$? **No**.
    
    - Do nothing. `i` stays at `1`.
        
    - _Array state:_ `[10, 30, 80, 90, 40, 50, 70]`
        
5. **`j = 4` (`arr[4] = 40`):** Is $40 \le 70$? **Yes**.
    
    - Increment `i` to `2`.
        
    - Swap `arr[i]` (`80`) with `arr[j]` (`40`).
        
    - _Array state:_ `[10, 30, 40, 90, 80, 50, 70]`
        
6. **`j = 5` (`arr[5] = 50`):** Is $50 \le 70$? **Yes**.
    
    - Increment `i` to `3`.
        
    - Swap `arr[i]` (`90`) with `arr[j]` (`50`).
        
    - _Array state:_ `[10, 30, 40, 50, 80, 90, 70]`
        

#### The Final Swap (Placing the Pivot)

The loop terminates because `j` has inspected everything up to `high - 1`.

Right now, `i` is at index `3` (value `50`). This means index `0` through `3` are safely packed with elements smaller than `70`. Therefore, the correct home for our pivot (`70`) is right after `i`, at **`i + 1`** (index `4`).

- Swap `arr[i + 1]` (`80`) with `arr[high]` (`70`).
    
- _Final Array state:_ `[10, 30, 40, 50, 70, 90, 80]`
    

The function returns the index **`4`**. The pivot `70` is perfectly placed, dividing the unsorted subsets.

### Code Implementation

Here is the standalone partition function isolated in Python and C++.

#### Python

Python

```
def partition(arr, low, high):
    pivot = arr[high]  # Selecting the pivot
    i = low - 1        # Index of smaller element

    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1     # Increment index of smaller element
            arr[i], arr[j] = arr[j], arr[i]

    # Place the pivot in its correct sorted position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Return the splitting index
    return i + 1
```

#### C++

C++

```
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high]; // Selecting the pivot
    int i = (low - 1);     // Index of smaller element

    for (int j = low; j < high; j++) {
        // If current element is smaller than or equal to pivot
        if (arr[j] <= pivot) {
            i++;           // Increment index of smaller element
            swap(arr[i], arr[j]);
        }
    }
    // Place the pivot in its correct sorted position
    swap(arr[i + 1], arr[high]);
    
    // Return the splitting index
    return (i + 1);
}
```

### Complexity Analysis

- **Time Complexity:** $O(n)$ where $n$ is the number of elements in the current subarray. The pointer `j` goes from `low` to `high - 1` exactly once, doing constant-time comparison and swap operations at each step.
    
- **Space Complexity:** $O(1)$ auxiliary space. The partitioning happens entirely **in-place** by mutating the original array without creating duplicates or subarrays in memory.