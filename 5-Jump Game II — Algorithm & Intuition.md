## Jump Game II — Algorithm & Intuition

**Problem:** You are guaranteed to reach the last index. Find the **minimum number of jumps** to get there.

---

### Intuition

**The Dream:** Cover the array in as few jumps as possible, like a BFS — explore all positions reachable in jump 1, then from those explore all reachable in jump 2, and so on.

**Key Insight:** Think in **layers/levels** like BFS on a tree. Each jump is one level. From the current window `[l, r]`, find the farthest you can reach — that becomes your next window.

```
nums = [2, 3, 1, 1, 4]

Level 0 (start):  [0]          → can reach up to index 2
Level 1 (jump 1): [1, 2]       → can reach up to index 4
Level 2 (jump 2): [3, 4]       → r >= n-1, STOP
```

---

### The BFS Window Mental Model

```
nums:  [2,  3,  1,  1,  4]
idx:    0   1   2   3   4

Jump 1 window: l=0, r=0
  From 0: can reach 0+2=2
  farthest = 2
  → new window [1, 2], jumps=1

Jump 2 window: l=1, r=2
  From 1: can reach 1+3=4
  From 2: can reach 2+1=3
  farthest = 4
  → new window [3, 4], jumps=2

r=4 >= n-1=4 → STOP, return 2 ✅
```

---

### Dry Run — `[2, 3, 1, 1, 4]`

```
jumps=0, l=0, r=0, n=5

--- While r=0 < 4 ---
  i=0: farthest = max(0, 0+2) = 2
  l=1, r=2, jumps=1

--- While r=2 < 4 ---
  i=1: farthest = max(0, 1+3) = 4
  i=2: farthest = max(4, 2+1) = 4
  l=3, r=4, jumps=2

--- While r=4 < 4? NO → exit ---

return 2 ✅
```

```
Visualization:

Index:  0    1    2    3    4
nums:  [2,   3,   1,   1,   4]
        |___|         |
       jump 1       jump 2
       window       window
       [0,0]→[1,2]  [1,2]→[3,4]
```

---

### Algorithm

```
1. jumps=0, l=0, r=0   ← window [l,r] = current jump level

2. While r < n-1:       ← haven't reached end yet

     farthest = 0

     For i in [l, r]:   ← scan every index in current window
         farthest = max(farthest, i + nums[i])
                    ↑ best reach from this level

     l = r + 1          ← next window starts after current
     r = farthest        ← next window ends at farthest reach
     jumps += 1          ← took one jump to get here

3. return jumps
```

---

### Jump Game I vs II — The Key Difference

```
Jump I  → tracks ONE variable (max_idx)
           "Can I reach the end at all?"

Jump II → tracks a WINDOW [l, r] (two variables)
           "What's the minimum jumps to reach the end?"
           Each window = one jump level
```

---

### Why This is Greedy BFS

```
Jump I  is like DFS  → just checking reachability
Jump II is like BFS  → exploring level by level, 
                        first time you reach end = min jumps
```

Each iteration of the while loop = **one BFS level = one jump**. You never revisit a window, and you always expand to the farthest possible — no reason to stop short.

---

### Complexity

| | |
|---|---|
| Time | O(N) — each index visited exactly once across all windows |
| Space | O(1) — just four variables |