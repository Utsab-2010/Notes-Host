---
title: "Search in a 2d array"
lastmod: 2026-06-23
---

You are given an m x n integer matrix matrix with the following two properties:

    Each row is sorted in non-decreasing order.
    The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

 

Example 1:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true

Example 2:

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false

 

Constraints:

    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 100
    -104 <= matrix[i][j], target <= 104

 


### Optimal Approach
```python
class Solution:
    # Function to search target in 2D matrix using binary search
    def searchMatrix(self, matrix, target):
        # Get number of rows and columns
        n = len(matrix)
        m = len(matrix[0])

        # Set initial binary search range
        low = 0
        high = n * m - 1

        # Perform binary search
        while low <= high:
            # Calculate middle index
            mid = (low + high) // 2

            # Convert 1D index to 2D indices
            row = mid // m
            col = mid % m

            # Check if target is found
            if matrix[row][col] == target:
                return True
            # Discard left half
            elif matrix[row][col] < target:
                low = mid + 1
            # Discard right half
            else:
                high = mid - 1

        # Target not found
        return False

# Driver code
if __name__ == "__main__":
    # Define 2D matrix
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]

    # Create object of Solution
    obj = Solution()

    # Call the method and print result
    print("true" if obj.searchMatrix(matrix, 8) else "false")
```