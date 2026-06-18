---
title: "Single Element in a Sorted array of pairs"
---

You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once.

Return _the single element that appears only once_.

Your solution must run in `O(log n)` time and `O(1)` space.

**Example 1:**

**Input:** nums = [1,1,2,3,3,4,4,8,8]
**Output:** 2

## Approach
The array is sorted, and all elements except one appear exactly twice. If we observe carefully, every pair starts at even index and ends at odd index when the array is still balanced (i.e., before the unique element is encountered).
But once the unique element is inserted, this pairing pattern breaks and the shift happens after that unique element. So we can use this pattern to cut the search space in half using binary search:
- If the pairing is proper (i.e., `arr[mid] == arr[mid ^ 1]`), then the unique (non-duplicate) element lies in the right half.
- If the pairing breaks (i.e., `arr[mid] != arr[mid ^ 1]`), then the unique element lies in the left half.

This leads us to an O(log n) solution by binary eliminating half of the array every step.

### My Solution
```cpp
class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int L =0,R=nums.size()-1;
        while(L<=R){
            int mid = L + (R-L)/2;
            if (R==0) return nums[0];
            
            if (mid%2==0){
                if(nums[mid]==nums[mid+1]) L = mid+2;
                else if (nums[mid]==nums[mid-1]) R = mid-2;
                else if (nums[mid]!=nums[mid-1]) return nums[mid];
            }
            else{
                if(nums[mid]==nums[mid-1]) L = mid+1;
                else if (nums[mid]==nums[mid+1]) R = mid-1;
                else if (nums[mid]!=nums[mid+1]) return nums[mid];

            }

        }
        return 0;
    }
};

```


### Better Solution
```cpp
class Solution {
public:
    int singleNonDuplicate(vector<int>& nums) {
        int L = 0, R = nums.size() - 1;

        while (L < R) {
            int mid = L + (R - L) / 2;
            // force mid to be even so comparison is always (mid, mid+1)
            if (mid % 2 == 1) mid--;

            if (nums[mid] == nums[mid + 1])
                L = mid + 2;  // pair is intact, single is to the right
            else
                R = mid;      // pair is broken, single is here or left
        }

        return nums[L];
    }
};
```

## Notes
1. *Force the mid to be even:*  I liked this approach, cleaned it up quite a bit
2. 