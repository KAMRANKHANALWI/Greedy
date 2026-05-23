## Minimum Vote Flips — Algorithm & Intuition

**Problem:** `n` voters each have a vote (`0` or `1`) and a weight. You can flip at most `k` votes from 0 → 1. Find the **minimum flips** needed for candidate 1's total weight to exceed candidate 0's, or return `-1` if it's impossible within `k` flips.

```
n=4, k=2
votes   = [0, 0, 1, 1]
weights = [10, 20, 5, 5]

s1 = 5+5 = 10  (candidate 1's total weight)
s0 = 10+20 = 30  (candidate 0's total weight)

Flip voter 1 (weight=20): s1=30, s0=10 → s1 > s0 → 1 flip needed ✅
```

---

### Intuition

**The Dream:** Make candidate 1 win with as few vote flips as possible.

**Key Insight:** Each flip of a 0-voter with weight `w` does **double damage** to candidate 0's lead:
- candidate 1 gains `w`
- candidate 0 loses `w`
- net swing = `2w`

So flip the **heaviest 0-voter first** to close the gap as fast as possible.

```
s1=10, s0=30 → gap = 20, candidate 1 losing by 20

Flip voter with weight=20:
  s1 = 10+20 = 30
  s0 = 30-20 = 10
  s1 > s0 ✅ → 1 flip

If we had flipped the smaller voter (weight=10) instead:
  s1 = 10+10 = 20
  s0 = 30-10 = 20
  s1 == s0 → not winning yet → need another flip
  → 2 flips (suboptimal)
```

---

### The Double Swing Effect

```
Before flip: s1 advantage = s1 - s0 (negative if losing)

Flipping a voter of weight w:
  s1 += w   →  +w
  s0 -= w   →  +w to the gap

Net change in (s1 - s0) = +2w

So flipping a weight-20 voter closes the gap by 40.
Flipping a weight-10 voter only closes it by 20.

Always flip the heaviest 0-voter → maximum gap closure per flip.
```

---

### Dry Run — `n=4, k=2, votes=[0,0,1,1], weights=[10,20,5,5]`

```
s1 = 5+5 = 10    (voters 2 and 3 already vote 1)
s0 = 10+20 = 30  (voters 0 and 1 vote 0)

s1 > s0? 10 > 30? No → proceed

0-voters' weights sorted descending: [20, 10]

flips=0

--- Flip weight=20 ---
  flips < k=2 ✅
  s1 = 10+20 = 30
  s0 = 30-20 = 10
  flips = 1
  s1=30 > s0=10 ✅ → return 1

Answer: 1 ✅
```

---

### Dry Run — `n=3, k=1, votes=[0,0,0], weights=[100,100,100]`

```
s1 = 0    (no one votes 1)
s0 = 300

0-voters' weights sorted: [100, 100, 100]

flips=0

--- Flip weight=100 ---
  flips=0 < k=1 ✅
  s1 = 0+100 = 100
  s0 = 300-100 = 200
  flips = 1
  s1=100 > s0=200? No ❌

--- Next: flips=1 >= k=1 → STOP ---

Never reached s1 > s0 → return -1 ✅
```

---

### Dry Run — Already Winning

```
n=3, k=1, votes=[1,0,1], weights=[10,5,10]

s1 = 10+10 = 20
s0 = 5

s1 > s0? 20 > 5? Yes → return 0 immediately ✅
```

---

### Algorithm

```
1. s1 = sum of weights where vote == 1
   s0 = sum of weights where vote == 0

2. If s1 > s0: return 0   ← already winning

3. zero_weights = weights of all 0-voters, sorted descending
                  (heaviest flippable voters first)

4. flips = 0

   For each weight in zero_weights:
       If flips >= k: break   ← can't flip more

       s1 += weight           ← flip this voter
       s0 -= weight
       flips += 1

       If s1 > s0: return flips   ← winning now!

5. return -1   ← couldn't win within k flips
```

---

### Why Collect 0-Voters' Weights Separately?

```
You only care about who you CAN flip — voters with vote=0.
Voters with vote=1 are already on your side, irrelevant.

Sorting those weights descending lets you greedily take
the highest-impact flip at each step.
```

---

### The `-1` Cases

```
Case 1: k = 0 and already losing
  → Can't flip anyone → return -1

Case 2: Flipped all k allowed voters but still losing
  → Gap too large to close in k flips → return -1

Case 3: Flipped ALL 0-voters (even < k), but still can't win
  → Impossible regardless of k → return -1
  (e.g., all voters vote 1 except one with tiny weight,
   but candidate 0's weight is somehow still larger —
   wait, that can't happen here since all 0s are flippable)
```

---

### Edge Cases

```
All voters vote 1:
  s0 = 0, s1 > 0 → return 0 immediately

All voters vote 0, k = all:
  Flip everyone → s1 = total, s0 = 0 → wins

Equal weights, s1 = s0 after flip:
  s1 > s0 requires strict inequality
  Equal doesn't win → keep flipping
```

---

### Complexity

| | |
|---|---|
| Time | O(N log N) — sorting the 0-voters' weights |
| Space | O(N) — storing the zero_weights list |