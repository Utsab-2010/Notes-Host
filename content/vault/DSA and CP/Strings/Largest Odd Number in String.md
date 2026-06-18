---
title: "Largest Odd Number in String"
---

problem: Find the largest odd number inside of a string
#cp_easy 

```cpp
#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    // Returns the largest odd number substring from the given string
    string largeOddNum(string& s) {
        int ind = -1;

        // Find the last odd digit in the string
        int i;
        for (i = s.length() - 1; i >= 0; i--) {
            if ((s[i] - '0') % 2 == 1) {
                ind = i;
                break;
            }
        }

        // Skip leading zeroes up to the odd digit
        i = 0;
        while (i <= ind && s[i] == '0') i++;

        // Return substring from first non-zero to odd digit
        return s.substr(i, ind - i + 1);
    }
};

int main() {
    Solution solution;
    string num = "504";
    string result = solution.largeOddNum(num);
    cout << "Largest odd number: " << result << endl;
    return 0;
}

```