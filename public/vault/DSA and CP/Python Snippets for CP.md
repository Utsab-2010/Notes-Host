---
title: "Python Snippets for CP"
lastmod: 2026-07-28
---


## Fast I/O

```python
import sys
input = sys.stdin.readline
data = sys.stdin.read().split()  # read everything at once, fastest for many tokens

# single line ints
n, m = map(int, input().split())
# array of ints
arr = list(map(int, input().split()))
# read whole input, use an index pointer instead of repeated input()
it = iter(sys.stdin.read().split())
n = int(next(it)); arr = [int(next(it)) for _ in range(n)]

print(*arr)                      # space-separated print
sys.stdout.write("\n".join(map(str, arr)) + "\n")  # bulk print, faster than loop
```

## Sorting

```python
arr.sort()                       # in-place
arr.sort(reverse=True)
arr.sort(key=lambda x: x[1])                 # by second element
arr.sort(key=lambda x: (x[0], -x[1]))        # multi-key, mixed direction
sorted_idx = sorted(range(len(arr)), key=lambda i: arr[i])  # argsort
arr.sort(key=len)                # by length (strings/lists)
```

## String <-> other conversions

```python
s = "abc"
list(s)                          # ['a','b','c']
"".join(chars)                   # list -> string
s.split()                        # whitespace split
s.split(",")                     # delimiter split
",".join(map(str, arr))          # list of ints -> csv string

ord('a'); chr(97)                # char <-> int
int("101", 2)                    # binary string -> int
bin(5)                           # -> '0b101'
bin(5)[2:]                       # strip prefix
format(5, 'b')                   # '101', no prefix
format(5, '08b')                 # zero-padded to 8 bits

int("ff", 16); hex(255)          # hex conversions
str(123)                         # int -> string
int("123")                       # string -> int, raises on bad input

s[::-1]                          # reverse string
"".join(sorted(s))                # sorted string
s.isdigit(); s.isalpha()
s.lower(); s.upper()
s.replace("a", "b")
s.strip()                        # trim whitespace
```

## Bit manipulation

```python
n & 1                            # check odd/even
n >> 1; n << 1                   # divide/multiply by 2
n & (n-1)                        # drop lowest set bit
n & (-n)                         # isolate lowest set bit
bin(n).count('1')                # popcount
n.bit_count()                    # popcount, Python 3.10+
n.bit_length()                   # number of bits

1 << k                           # 2^k
n | (1 << k)                     # set bit k
n & ~(1 << k)                    # clear bit k
n ^ (1 << k)                     # toggle bit k
(n >> k) & 1                     # check bit k
```

## Collections module

```python
from collections import Counter, defaultdict, deque, OrderedDict

c = Counter(arr)                 # frequency map
c.most_common(3)                 # top-3 (elem, count)
c.most_common()[-1]              # least common
c1 + c2; c1 - c2                 # counter arithmetic (union/diff of multisets)

d = defaultdict(int)             # auto 0
d = defaultdict(list)            # auto []
d = defaultdict(set)

dq = deque(arr)
dq.appendleft(x); dq.popleft()   # O(1) both ends
dq.rotate(1)                     # rotate right by 1
```

## heapq (min-heap only; negate for max-heap)

```python
import heapq
h = []
heapq.heapify(arr)               # in-place, O(n)
heapq.heappush(h, x)
heapq.heappop(h)
heapq.heappushpop(h, x)          # push then pop, more efficient combo
heapq.nlargest(3, arr)
heapq.nsmallest(3, arr)

heapq.heappush(h, (-x, x))       # simulate max-heap with tuples
```

## bisect (sorted array ops)

```python
import bisect
bisect.bisect_left(arr, x)       # first index where x can be inserted (leftmost)
bisect.bisect_right(arr, x)      # rightmost
bisect.insort(arr, x)            # insert keeping sorted, O(n)
```

## itertools

```python
from itertools import permutations, combinations, product, accumulate, groupby, pairwise

list(permutations(arr, 2))
list(combinations(arr, 2))
list(product([0,1], repeat=3))   # all binary strings length 3
list(accumulate(arr))            # prefix sums
list(accumulate(arr, max))       # prefix max
list(pairwise(arr))              # (a0,a1),(a1,a2)... Python 3.10+

for key, group in groupby(arr):  # group consecutive equal elements
    print(key, list(group))
```

## math

```python
import math
math.gcd(a, b); math.lcm(a, b)
math.isqrt(n)                    # integer sqrt, no float error
math.ceil(a/b); math.floor(a/b)
-(-a // b)                       # ceil div without float
math.comb(n, r); math.factorial(n)
math.inf; -math.inf              # sentinel values
math.log2(n)
```

## 2D arrays / matrix

```python
grid = [[0]*m for _ in range(n)]        # correct — independent rows
# grid = [[0]*m]*n   -> WRONG, shared references

grid = [list(map(int, input().split())) for _ in range(n)]
transposed = list(zip(*grid))            # transpose
flat = [x for row in grid for x in row]  # flatten
```

## Misc handy tricks

```python
a, b = b, a                      # swap
x = arr[i] if i < len(arr) else default

from functools import lru_cache
@lru_cache(maxsize=None)         # memoize a recursive function
def f(n): ...

sys.setrecursionlimit(10**6)     # avoid recursion depth errors

set(arr) & set(arr2)             # intersection
set(arr) | set(arr2)             # union
set(arr) - set(arr2)             # difference

all(cond for x in arr); any(cond for x in arr)

from copy import deepcopy
grid2 = deepcopy(grid)           # nested structures need this, not grid[:]
```