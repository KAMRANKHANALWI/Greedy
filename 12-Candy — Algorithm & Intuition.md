## Candy — Algorithm & Intuition

**Problem:** `n` children stand in a line, each with a rating. Distribute candies such that:
1. Every child gets at least 1 candy.
2. A child with a **higher rating than a neighbour** gets **more candy** than that neighbour.

Minimise the total number of candies.

```
ratings = [1, 0, 2]  →  candies = [2, 1, 2]  →  total = 5
ratings = [1, 2, 2]  →  candies = [1, 2, 1]  →  total = 4
```

---

### Intuition

**The Dream:** Give every child the minimum candies possible while satisfying both left and right neighbour constraints.

**Key Insight:** Satisfying both constraints simultaneously in one pass is hard. But satisfying one side at a time and combining is easy.

```
Pass 1 (→): Ensure every child with higher rating than LEFT neighbour gets more.
Pass 2 (←): Ensure every child with higher rating than RIGHT neighbour gets more.
Final:      Take max of both passes at each position — satisfies both.
```

---

### Why Two Passes?

```
ratings = [1, 3, 2, 2, 1]

One-pass left-to-right only:
  candies = [1, 2, 1, 1, 1]   ← right constraint ignored

One-pass right-to-left only:
  candies = [1, 1, 2, 2, 1]   ← left constraint ignored

Two-pass:
  After left pass:  [1, 2, 1, 1, 1]   ← left constraint fixed
  After right pass: [1, 2, 2, 2, 1]   ← right constraint fixed
  max of both:      [1, 2, 2, 2, 1]   ← both satisfied, total=7 ✅
```

---

### Pass 1 — Left to Right

```
Rule: If ratings[i] > ratings[i-1], then candies[i] = candies[i-1] + 1

ratings = [1, 3, 2, 2, 1]
Start:     [1, 1, 1, 1, 1]   ← everyone starts with 1

i=1: ratings[1]=3 > ratings[0]=1 → candies[1] = 1+1 = 2
i=2: ratings[2]=2 > ratings[1]=3? No → stay 1
i=3: ratings[3]=2 > ratings[2]=2? No → stay 1
i=4: ratings[4]=1 > ratings[3]=2? No → stay 1

After Pass 1: [1, 2, 1, 1, 1]
```

---

### Pass 2 — Right to Left

```
Rule: If ratings[i] > ratings[i+1], then candies[i] = max(candies[i], candies[i+1] + 1)

Note the max() — preserve the gain from Pass 1.

After Pass 1: [1, 2, 1, 1, 1]

i=3: ratings[3]=2 > ratings[4]=1 → candies[3] = max(1, 1+1) = 2
i=2: ratings[2]=2 > ratings[3]=2? No → stay 1
i=1: ratings[1]=3 > ratings[2]=2 → candies[1] = max(2, 1+1) = 2
i=0: ratings[0]=1 > ratings[1]=3? No → stay 1

After Pass 2: [1, 2, 1, 2, 1]  →  total = 7 ✅
```

---

### Dry Run — `[1, 3, 2, 2, 1]`

```
ratings:      [1,  3,  2,  2,  1]
Start:        [1,  1,  1,  1,  1]

Left pass (→):
  i=1: 3>1 → 1+1=2     [1, 2, 1, 1, 1]
  i=2: 2>3? No          [1, 2, 1, 1, 1]
  i=3: 2>2? No          [1, 2, 1, 1, 1]
  i=4: 1>2? No          [1, 2, 1, 1, 1]

Right pass (←):
  i=3: 2>1 → max(1,2)=2 [1, 2, 1, 2, 1]
  i=2: 2>2? No          [1, 2, 1, 2, 1]
  i=1: 3>2 → max(2,2)=2 [1, 2, 1, 2, 1]
  i=0: 1>3? No          [1, 2, 1, 2, 1]

Total = 1+2+1+2+1 = 7 ✅
```

---

### Dry Run — `[1, 2, 3]` (Strictly Increasing)

```
ratings:     [1, 2, 3]
Start:       [1, 1, 1]

Left pass:   [1, 2, 3]   ← each step gets +1

Right pass:
  i=1: 2>3? No
  i=0: 1>2? No
  No changes: [1, 2, 3]

Total = 6 ✅
```

---

### Dry Run — `[3, 2, 1]` (Strictly Decreasing)

```
ratings:     [3, 2, 1]
Start:       [1, 1, 1]

Left pass:
  i=1: 2>3? No
  i=2: 1>2? No
  No changes: [1, 1, 1]

Right pass:
  i=1: 2>1 → max(1, 1+1) = 2   [1, 2, 1]
  i=0: 3>2 → max(1, 2+1) = 3   [3, 2, 1]

Total = 6 ✅
```

---

### Why `max()` in Pass 2?

```
candies[i] = max(candies[i], candies[i+1] + 1)
              ↑                    ↑
    value earned in Pass 1    value needed for right constraint

We might need a high value from Pass 1 (left constraint)
AND a high value from Pass 2 (right constraint).
Taking max keeps both satisfied.

Example: peak of a mountain
ratings = [1, 5, 1]

Left pass:  [1, 2, 1]   ← child 1 needs 2 for left constraint
Right pass:
  i=1: 5>1 → max(2, 1+1) = max(2, 2) = 2  ✅  (left constraint preserved)

Without max:
  candies[1] = 1+1 = 2   ← same here, but imagine:
  
ratings = [1, 2, 3, 1]
Left pass: [1, 2, 3, 1]
Right pass:
  i=2: 3>1 → max(3, 1+1) = 3  ← max protects the 3 from Left pass
  Without max: candies[2] = 2 → LEFT constraint broken (2 should > 1 from i=1, but 2=2, not >)
```

---

### Algorithm

```
1. candies = [1] * n   ← start everyone with 1

2. Left pass (i = 1 to n-1):
     If ratings[i] > ratings[i-1]:
         candies[i] = candies[i-1] + 1

3. Right pass (i = n-2 down to 0):
     If ratings[i] > ratings[i+1]:
         candies[i] = max(candies[i], candies[i+1] + 1)

4. Return sum(candies)
```

---

### Complexity

| | |
|---|---|
| Time | O(N) — two linear passes |
| Space | O(N) — the candies array |