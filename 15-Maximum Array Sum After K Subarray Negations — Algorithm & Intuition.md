## Maximum Array Sum After K Subarray Negations — Algorithm & Intuition

**Problem:** Given array `a[1..N]` and integer `K`, you may negate at most `K` **contiguous subarrays** (flip all signs in a chosen range). Find the **maximum possible sum** after all operations.

```
a = [-10, 20, -30, 40, -50],  k = 2

Flip a[2]=-30 → 30   (op 1)
Flip a[4]=-50 → 50   (op 2)
Result = [-10, 20, 30, 40, 50] → sum = 130  ✅
```

> **Note:** This is NOT the simple "flip any k individual elements" problem. Here you flip contiguous subarrays — a single flip can fix an entire run of negatives at once.

---

### Intuition

**The Dream:** Every element is positive — sum = `sum of |a[i]|`. This is the theoretical maximum you can ever achieve.

**Key Insight:** A contiguous block of negative numbers costs only **1 flip** to fix entirely — no matter how long it is.

```
a = [-10, -20, -30, 40, -50]
         └─── 1 flip ───┘

One flip turns the entire [-10,-20,-30] block positive.
```

So instead of thinking "flip individual elements", think in terms of **negative runs** (consecutive negative blocks) and the **positive gaps** between them.

---

### Structure of the Array

```
a = [-10, 20, -30, 40, -50]
     └N1┘ └G1┘ └N2┘ └G2┘ └N3┘

N = negative run,  G = positive gap

neg_runs = [10, 30, 50]   (absolute sums of each run)
pos_gaps = [20, 40]        (sums of each gap between runs)
```

With `k` flips and `m` negative runs:

```
If k >= m:  flip every run → dream achieved → return abs_sum
If k < m:   we're short — deficit = m - k runs can't all be fixed
```

---

### When Budget is Short — Two Options Per Deficit

With `deficit = m - k` unsolvable units, at each step you have exactly two choices:

**Option A — Skip a negative run (leave it unfixed):**
```
A run with absolute sum X contributes +X in the dream.
Left unfixed, it contributes -X.
Penalty = dream − actual = 2X
```

**Option B — Merge two adjacent runs by flipping across the gap:**
```
a = [... N1 ... G ... N2 ...]

Flip the subarray spanning [end of N1 → start of N2]:
  N1 → positive (fixed) ✅
  G  → flips to negative ❌  (gap becomes a new negative block)
  N2 → positive (fixed) ✅

Net effect: N1 and N2 are fixed, but G (sum = P) is now negative.
Penalty = 2P  (gap flipped from +P to -P)

This used 1 flip but fixed 2 runs → deficit decreases by 1.
```

```
The elegant symmetry:
  Skip run (abs sum X)  → penalty 2X
  Merge via gap (sum P) → penalty 2P

BOTH have the same penalty formula: 2 × (size of sacrificed chunk).
So neg_run sums and pos_gap sums are interchangeable in cost!
```

---

### The Unified Candidate Pool

```
neg_runs = [10, 30, 50]
pos_gaps = [20, 40]

candidates = sorted([10, 30, 50, 20, 40]) = [10, 20, 30, 40, 50]

deficit = 3 - 2 = 1

Pick cheapest 1 candidate: 10
Penalty = 2 × 10 = 20

answer = abs_sum − penalty = 150 − 20 = 130  ✅
```

> Picking the cheapest candidates from the merged pool greedily minimizes total loss — this is the core greedy choice.

---

### Dry Run — `[-10, 20, -30, 40, -50]`, k=2

```
abs_sum = 10+20+30+40+50 = 150

Scanning for runs and gaps:

  i=0: a[0]=-10 < 0 → consume negative run
       s = 10, i=1
       seen_neg=False → don't record gap
       neg_runs = [10], seen_neg=True, cur_pos=0

  i=1: a[1]=20 >= 0 → consume positive block
       cur_pos = 20, i=2

  i=2: a[2]=-30 < 0 → consume negative run
       s = 30, i=3
       seen_neg=True → record pos_gaps.append(20)
       neg_runs = [10,30], cur_pos=0

  i=3: a[3]=40 >= 0 → consume positive block
       cur_pos = 40, i=4

  i=4: a[4]=-50 < 0 → consume negative run
       s = 50, i=5
       seen_neg=True → record pos_gaps.append(40)
       neg_runs = [10,30,50], cur_pos=0

neg_runs = [10, 30, 50]  (3 runs)
pos_gaps = [20, 40]      (2 gaps)

m=3, k=2 → m > k → deficit=1

candidates = sorted([10,30,50,20,40]) = [10,20,30,40,50]
pick cheapest 1: [10]

answer = 150 - 2×10 = 130  ✅
```

---

### Dry Run — `[-5, 10, -3, 8, -7]`, k=1

```
abs_sum = 5+10+3+8+7 = 33

neg_runs = [5, 3, 7]
pos_gaps = [10, 8]

m=3, k=1, deficit=2

candidates = sorted([5,3,7,10,8]) = [3,5,7,8,10]
pick cheapest 2: [3, 5]

answer = 33 - 2×(3+5) = 33 - 16 = 17
```

```
Interpretation: sacrifice the smallest run (abs=3) and the next smallest run (abs=5).
  - Skip [-3] → stays negative, penalty=6
  - Skip [-5] → stays negative, penalty=10
  - Use 1 flip to fix [-7] → +7

Result: -5 + 10 - 3 + 8 - 7
  → can we do better with merging?

Alternative: use 1 flip to flip [-5, 10, -3] → [5, -10, 3]
  Then [-5] and [-3] become positive, but [10] becomes -10.
  Sum = 5 - 10 + 3 + 8 - 7 = -1  ← worse!

The greedy correctly identified [3,5] as cheapest pair → 17 ✅
```

---

### Why `pos_gaps` Only Counts Gaps Between Two Negative Runs

```
a = [10, -3, 8, -7]
     └P0┘ └N1┘ └G1┘ └N2┘

P0 = leading positive block (before any negative run)
G1 = gap between N1 and N2

P0 is NOT a valid gap candidate — there's no N0 to its left,
so you can't "merge" across P0. It's never at risk of being flipped.

Only gaps BETWEEN two negative runs can become the "bridge" in Option B.

Code tracks this with `seen_neg`:
  if seen_neg:
      pos_gaps.append(cur_pos)   ← only after we've seen a neg run
```

---

### If k >= Number of Negative Runs

```
a = [-10, 20, -30, 40], k=5

neg_runs = [10, 30]  →  m=2
k=5 >= m=2  →  fix both runs, no deficit

abs_sum = 10+20+30+40 = 100
return 100  ✅

Remaining k=3 flips are wasted (or cancel out — flip anything twice = no change).
```

---

### Algorithm

```
1. abs_sum = sum(|a[i]|)   ← dream scenario

2. Scan array, extract:
     neg_runs → absolute sums of consecutive negative blocks
     pos_gaps → sums of positive blocks that sit between two neg runs

3. m = len(neg_runs)
   If m <= k: return abs_sum   ← enough flips to fix all runs

4. deficit = m - k
   candidates = sorted(neg_runs + pos_gaps)

5. return abs_sum - 2 × sum(candidates[:deficit])
```

---

### Why This is Greedy

```
Greedy choice: pick the cheapest deficit candidates from the pool.

Proof sketch: if we pick any non-minimal candidate over a cheaper one,
we can swap them and reduce total penalty → contradiction.
Greedy gives the minimum penalty, hence maximum sum.
```

---

### Reading Input — The `sys.stdin` Pattern

```python
input = sys.stdin.readline
n = int(input())
k = int(input())
a = [int(input()) for _ in range(n)]
```

The input format expects n, k, and each array element on separate lines. This is common in competitive programming judges. The `try/except (EOFError, ValueError)` handles empty stdin gracefully when testing locally.

---

### Complexity

| | |
|---|---|
| Time | O(N log N) — sorting the candidates list |
| Space | O(N) — storing runs and gaps |