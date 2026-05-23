## Jump Game I — Algorithm & Intuition

**Problem:** Given an array where each element = max jump length from that index, can you reach the last index starting from index 0?

---

### Intuition

**The Dream:** From index 0, keep extending how far you can reach. If your reach ever covers the last index, you're done.

**Key Insight:** At every position, ask — *"is this index even reachable?"* If `i > max_idx`, you're standing on an island no jump ever reached. Game over.

```
arr = [2, 3, 1, 1, 4]

From index 0, jump up to 2 steps → can reach index 0,1,2
From index 1, jump up to 3 steps → can reach index 4 ✅
```

---

### `max_idx` — The Reach Tracker

```
max_idx = farthest index reachable so far

At index i:
  Can I even be here?  →  i <= max_idx
  How far can I jump?  →  i + arr[i]
  Update reach         →  max_idx = max(max_idx, i + arr[i])
```

---

### Dry Run — `[2, 1, 1, 0, 4]` → False

```
i  | arr[i] | i > max_idx? | max_idx = max(max_idx, i+arr[i])
---|--------|--------------|-------------------------------
0  |   2    |  0 > 0? No   |  max(0, 0+2) = 2
1  |   1    |  1 > 2? No   |  max(2, 1+1) = 2
2  |   1    |  2 > 2? No   |  max(2, 2+1) = 3
3  |   0    |  3 > 3? No   |  max(3, 3+0) = 3
4  |   4    |  4 > 3? YES  |  return False ❌
```

```
Timeline:
Index:    0    1    2    3    4
Array:   [2,   1,   1,   0,   4]
Reach:    2    2    3    3    ✗
                              ↑
                         can't get here, max_idx stuck at 3
```

---

### Dry Run — `[2, 3, 1, 1, 4]` → True

```
i  | arr[i] | i > max_idx? | max_idx = max(max_idx, i+arr[i])
---|--------|--------------|-------------------------------
0  |   2    |  0 > 0? No   |  max(0, 0+2) = 2
1  |   3    |  1 > 2? No   |  max(2, 1+3) = 4
2  |   1    |  2 > 4? No   |  max(4, 2+1) = 4
3  |   1    |  3 > 4? No   |  max(4, 3+1) = 4
4  |   4    |  4 > 4? No   |  max(4, 4+4) = 8
Loop ends → return True ✅
```

---

### Algorithm

```
1. max_idx = 0   ← farthest index reachable, start at 0

2. For each index i:

     If i > max_idx:
         this index is unreachable → return False

     max_idx = max(max_idx, i + arr[i])
               ↑ can we extend our reach from here?

3. Loop finished without getting stuck → return True
```

---

### The Trap Case — Zero in the Middle

```
arr = [2, 1, 1, 0, 4]
                ↑
            arr[3] = 0, jump nowhere from here
            AND max_idx = 3, can't skip over it
            → stuck, index 4 unreachable
```

> A zero doesn't always kill you — only if it's the **farthest you can reach**.

```
arr = [3, 0, 0, 1, 4]
       ↑
    jump 3 from index 0 → reach index 3 directly, skip the zeros ✅
```

---

### Complexity

| | |
|---|---|
| Time | O(N) — single pass |
| Space | O(1) — one variable |

The greedy choice: always extend `max_idx` as far as possible at each step — there's no reason to hold back, more reach never hurts.