---
title: "CPP Strings CheatSheet"
---

## Basics

```cpp
// Declare
string s = "hello";
string s(5, 'a');       // "aaaaa"
string s(arr);          // from char array

// Length
s.size()                // returns size_t (unsigned — cast to int for subtraction)
s.length()              // same as size()

// Access
s[i]                    // no bounds check
s.at(i)                 // throws if out of range
s.front()               // s[0]
s.back()                // s[s.size()-1]

// Append
s += "world";
s.push_back('!');
s.append("xyz");

// Substring
s.substr(pos, len)      // from index pos, length len
s.substr(2, 3)          // if len omitted → goes to end

// Empty / clear
s.empty()               // true if ""
s.clear();              // wipes string
```

---

## Search / Find

```cpp
// find — returns index, or string::npos if not found
s.find("lo")            // search for substring
s.find('l')             // works for char too
s.find("lo", 3)         // start search at index 3

// Always check like this:
if (s.find("lo") != string::npos) {
    // found it
}
// npos = SIZE_MAX — never compare to -1

// rfind — last occurrence
s.rfind("l")

// find_first_of / find_last_of — find any char in a set
s.find_first_of("aeiou")        // first vowel
s.find_last_of("aeiou")
s.find_first_not_of("abc")      // first char NOT in set

// C++20+
s.starts_with("he")
s.ends_with("lo")

// C++23+
s.contains("lo")                // true/false (older: use find != npos)
```

---

## Modify

```cpp
// Erase
s.erase(pos, len)       // remove len chars starting at pos
s.erase(2, 3)
s.pop_back()            // remove last char

// Insert
s.insert(pos, "xyz")    // insert string at pos

// Replace
s.replace(pos, len, "new")      // replaces len chars at pos with "new"

// Reverse
#include <algorithm>
reverse(s.begin(), s.end());

// Sort characters in-place
sort(s.begin(), s.end());

// To lower / upper
#include <cctype>
for (char& c : s) c = tolower(c);
for (char& c : s) c = toupper(c);
```

---

## Convert

```cpp
// string → number
stoi("42")              // → int
stol("42")              // → long
stoll("42")             // → long long
stof("3.14")            // → float
stod("3.14")            // → double

// number → string
to_string(42)           // → "42"
to_string(3.14)         // → "3.140000"

// string ↔ char array
s.c_str()               // → const char*
string s(arr);          // char* → string

// char ↔ int (essential for freq arrays / hashing)
'a' - 'a'               // → 0
'z' - 'a'               // → 25
(int)'A'                // → 65 (ASCII)
(char)65                // → 'A'

// char checks
#include <cctype>
isalpha(c)              // a-z or A-Z?
isdigit(c)              // 0-9?
isalnum(c)              // alpha or digit?
isspace(c)              // space/tab/newline?
islower(c)
isupper(c)

// stringstream — useful for tokenizing / parsing
#include <sstream>
stringstream ss("3 14 15");
int x; ss >> x;         // reads 3
```

---

## Compare / Sort

```cpp
// Comparison — just works on std::string
s1 == s2                // equality
s1 < s2                 // lexicographic
s1.compare(s2)          // 0 if equal, <0 or >0 otherwise

// Sort vector of strings
sort(v.begin(), v.end());                       // lexicographic (default)
sort(v.begin(), v.end(), [](auto& a, auto& b){
    return a.size() < b.size();                 // sort by length
});

// Frequency count — lowercase a-z
int freq[26] = {};
for (char c : s)
    freq[c - 'a']++;

// Iterate
for (char c : s) { ... }                        // range-based
for (int i = 0; i < (int)s.size(); i++) { ... } // index-based

// Split by delimiter
#include <sstream>
stringstream ss(s);
string token;
vector<string> tokens;
while (getline(ss, token, ','))
    tokens.push_back(token);

// Count occurrences of a char
#include <algorithm>
count(s.begin(), s.end(), 'a');
```

---

## Gotchas

- `s.size()` is **unsigned** — `s.size() - 1` on an empty string wraps to a huge number. Cast: `(int)s.size()`.
- Always check `find` result with `!= string::npos`, never `== -1`.
- `s[i]` does no bounds checking — use `s.at(i)` when debugging.
- `char - 'a'` is used everywhere for mapping characters to array indices.