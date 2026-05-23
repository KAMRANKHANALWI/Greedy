## Non-overlapping Intervals — Algorithm & Intuition

**Problem:** Given a list of intervals, find the **minimum number of intervals to remove** so that no two intervals overlap.

```
intervals = [[1,3],[2,5],[3,6],[4,7],[5,8],[6,9],[8,10]]
→ remove 4 intervals
```

---

### Intuition

**The Dream:** Keep as many intervals as possible without any overlap. The answer is then `total - kept`.

**Key Insight:** This is the **exact same problem as N Meetings in One Room** — just asked from the other direction. Instead of maximising what you keep, you minimise what you remove.

```
Minimum removals = Total intervals − Maximum non-overlapping intervals kept
```

So the strategy is identical: **sort by end time, greedily keep every interval that doesn't overlap with the last kept one**.

---

### Why Sort by End Time?

```
Prefer intervals that end early → they leave the most room for future intervals.

intervals = [[1,10],[2,3],[4,5]]

Sort by end: [2,3], [4,5], [1,10]
  Keep [2,3]  → last_end = 3
  Keep [4,5]  → starts at 4 >= 3 ✅, last_end = 5
  Skip [1,10] → starts at 1 < 5 ❌ (overlaps)
  kept=2, removed=1

Sort by start: [1,10],[2,3],[4,5]
  Keep [1,10] → last_end = 10
  Skip [2,3]  → starts at 2 < 10 ❌
  Skip [4,5]  → starts at 4 < 10 ❌
  kept=1, removed=2  ← WRONG, not greedy optimal
```

---

### Dry Run — `[[1,3],[2,5],[3,6],[4,7],[5,8],[6,9],[8,10]]`

```
Sort by end: (already mostly sorted in this case)
  [1,3],[2,5],[3,6],[4,7],[5,8],[6,9],[8,10]

kept=1, last_end = 3   ← first interval always kept

Interval | start | end | start >= last_end? | Action        | last_end | kept
---------|-------|-----|--------------------|---------------|----------|-----
 [2,5]   |   2   |  5  |  2 >= 3?  ❌       | REMOVE        |    3     |  1
 [3,6]   |   3   |  6  |  3 >= 3?  ✅       | KEEP          |    6     |  2
 [4,7]   |   4   |  7  |  4 >= 6?  ❌       | REMOVE        |    6     |  2
 [5,8]   |   5   |  8  |  5 >= 6?  ❌       | REMOVE        |    6     |  2
 [6,9]   |   6   |  9  |  6 >= 6?  ✅       | KEEP          |    9     |  3
 [8,10]  |   8   | 10  |  8 >= 9?  ❌       | REMOVE        |    9     |  3

kept = 3
removed = 7 - 3 = 4 ✅
```

```
Timeline:
  [1,3]          → kept ✅
  [2,5]          → overlaps [1,3] → removed ❌
  [3,6]          → starts at 3 = end of [1,3] → kept ✅
  [4,7],[5,8]    → overlap [3,6] → removed ❌
  [6,9]          → starts at 6 = end of [3,6] → kept ✅
  [8,10]         → overlaps [6,9] → removed ❌
```

---

### The Touching-Endpoint Rule

```
Condition: start >= last_end   (note: >=, not >)

Why >= here but > in N Meetings?
  In N Meetings: meetings sharing an endpoint are considered overlapping.
  In this problem: [1,3] and [3,6] are NON-overlapping (standard interval convention).

Always check the problem's definition of overlap — it changes the condition.
```

---

### Bug in the Code — Worth Noting

```python
# BUG: uses unsorted intervals[0][1] instead of sorted_intervals[0][1]
sorted_intervals = sorted(intervals, key=lambda x: x[1])
kept = 1
last_end = intervals[0][1]   ← ❌ should be sorted_intervals[0][1]

for start, end in intervals[1:]:   ← ❌ should iterate over sorted_intervals[1:]
```

The code sorts into `sorted_intervals` but then iterates `intervals` — the unsorted list. For the given test case it may still pass, but it's incorrect in general.

Correct version:
```python
sorted_intervals = sorted(intervals, key=lambda x: x[1])
kept = 1
last_end = sorted_intervals[0][1]   ← ✅

for start, end in sorted_intervals[1:]:   ← ✅
```

---

### Algorithm

```
1. Sort intervals by end time ascending

2. kept = 1
   last_end = sorted_intervals[0][1]   ← first interval always kept

3. For each [start, end] in sorted_intervals[1:]:
       If start >= last_end:            ← no overlap
           kept += 1
           last_end = end

4. Return len(intervals) - kept         ← minimum removals
```

---

### Relationship to N Meetings in One Room

```
N Meetings:              find maximum meetings you CAN schedule
Non-overlapping:         find minimum intervals you must REMOVE

Both sort by end time.
Both greedily keep non-overlapping intervals.

Non-overlapping answer = total - (N Meetings answer)
```

---

### Complexity

| | |
|---|---|
| Time | O(N log N) — sorting dominates |
| Space | O(N) — for the sorted copy |