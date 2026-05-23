## N Meetings in One Room — Algorithm & Intuition

**Problem:** Given `n` meetings, each with a start and end time, find the **maximum number of meetings** that can be held in a single room (no two meetings can overlap).

```
meetings = [
    (M1, start=1, end=3),
    (M2, start=2, end=6),
    (M3, start=5, end=7),
    (M4, start=3, end=8),
    (M5, start=6, end=9),
    (M6, start=8, end=10),
]
```

---

### Intuition

**The Dream:** Fit as many meetings as possible into the room.

**Key Insight:** Always pick the meeting that **ends the earliest**. The sooner a meeting ends, the more room is left for future meetings. A meeting that finishes late "blocks" the room for longer — even if it started at the same time.

```
Two candidates starting at time 2:
  M2 ends at 6  → blocks room until 6
  M3 ends at 7  → blocks room until 7

Pick M2 (ends sooner) → room free at 6, more meetings can follow.
```

---

### Why "Earliest End" and Not "Earliest Start"?

```
meetings = [(A, 1, 10), (B, 2, 3), (C, 4, 5)]

Sort by start:  A(1,10), B(2,3), C(4,5)
  Pick A → room blocked until 10 → only 1 meeting fits ❌

Sort by end:    B(2,3), C(4,5), A(1,10)
  Pick B → room free at 3
  Pick C → starts at 4 > 3 → fits! Room free at 5
  Skip A → starts at 1 ≤ 5 → overlaps ❌
  Total = 2 meetings ✅
```

Earliest start is wrong — a meeting can start early but hog the room forever.

---

### Dry Run — The Example

```
Sort by end time:
  M1 (1,3), M3 (5,7), M2 (2,6), M5 (6,9), M4 (3,8), M6 (8,10)
  ↓
  M1(end=3), M2(end=6), M3(end=7), M4(end=8), M5(end=9), M6(end=10)

last_end = -1

Meeting | start | end | start > last_end? | Action       | last_end
--------|-------|-----|-------------------|--------------|--------
  M1    |   1   |  3  |  1 > -1 ✅        | SELECT M1    |   3
  M2    |   2   |  6  |  2 > 3  ❌        | SKIP         |   3
  M3    |   5   |  7  |  5 > 3  ✅        | SELECT M3    |   7
  M4    |   3   |  8  |  3 > 7  ❌        | SKIP         |   7
  M5    |   6   |  9  |  6 > 7  ❌        | SKIP         |   7
  M6    |   8   | 10  |  8 > 7  ✅        | SELECT M6    |  10

Selected: [M1, M3, M6]  → 3 meetings ✅
```

```
Timeline:
Time: 1   2   3   4   5   6   7   8   9   10
      |--M1--|               |--M3--|
                              (M2 skipped: overlaps M1)
                                         |---M6---|
                              (M4,M5 skipped: overlap M3)
```

---

### Algorithm

```
1. Sort meetings by end time ascending  → earliest-finishing first

2. last_end = -1      ← room is free from the start
   selected = []

3. For each (id, start, end) in sorted meetings:
       If start > last_end:          ← no overlap with previous meeting
           SELECT this meeting
           last_end = end            ← room now occupied until 'end'

4. Return selected meetings
```

---

### The Overlap Check: `start > last_end`

```
Non-overlap:  ---|M_prev|---[gap]---|M_curr|---
                            ↑
                       start > last_end ✅

Touching:     ---|M_prev|---|M_curr|---
                            ↑
                       start == last_end ❌ (still overlapping)

Overlap:      ---|M_prev|---
                   |---M_curr|---
                       start < last_end ❌
```

> The condition is `start > last_end`, not `>=`. Meetings sharing an endpoint are considered overlapping.

---

### This is the Classic Activity Selection Problem

This problem is the textbook greedy algorithm called **Activity Selection**. It's provably optimal: sorting by end time and greedily picking is guaranteed to give the maximum number of non-overlapping activities.

Exchange argument: if any other selection has more meetings than the greedy one, you can swap meetings one by one and always get at least as many — contradiction.

---

### Complexity

|       |                                   |
| ----- | --------------------------------- |
| Time  | O(N log N) — sorting dominates    |
| Space | O(N) — to store selected meetings |
