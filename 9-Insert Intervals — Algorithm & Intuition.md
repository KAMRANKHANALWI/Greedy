## Insert Intervals — Algorithm & Intuition

**Problem:** Given a list of **non-overlapping, sorted** intervals, insert a new interval and merge any overlaps. Return the resulting list of intervals.

```
intervals   = [[1,3],[6,9],[11,14],[16,18]]
newInterval = [5,13]
result      = [[1,3],[5,14],[16,18]]
```

---

### Intuition

**The Dream:** Slide the new interval into the sorted list, expanding it wherever it collides, then stitch everything back together.

**Key Insight:** Every existing interval falls into exactly one of three buckets relative to the new interval:

```
BEFORE:    ends before new interval starts  → safe, add as-is
OVERLAP:   overlaps with new interval       → merge into it
AFTER:     starts after new interval ends   → safe, add as-is
```

Handle these three buckets in order, one pass, three phases.

---

### The Three Cases — Visually

```
newInterval = [ns, ne]

Case 1 — BEFORE (no overlap, interval ends first):
  |--existing--|
                    |--new--|
  existing[1] < ns   →  add existing, move on

Case 2 — OVERLAP (merge):
  |--existing--|            existing starts before new ends
       |--new--|            existing[0] <= ne
  → expand: ns = min(ns, existing[0])
             ne = max(ne, existing[1])

Case 3 — AFTER (no overlap, interval starts after):
                    |--new--|
                              |--existing--|
  → new interval already inserted, add remaining as-is
```

---

### Dry Run — `[[1,3],[6,9],[11,14],[16,18]]`, newInterval `[5,13]`

```
ns=5, ne=13, i=0, result=[]

--- Phase 1: intervals ending before ns=5 ---
  [1,3]: end=3 < ns=5 ✅ → add to result, i=1
  [6,9]: end=9 < ns=5 ❌ → stop Phase 1
  result = [[1,3]]

--- Phase 2: overlapping intervals (start <= ne=13) ---
  [6,9]:  start=6  <= ne=13 ✅ → ns=min(5,6)=5,  ne=max(13,9)=13,  i=2
  [11,14]: start=11 <= ne=13 ✅ → ns=min(5,11)=5, ne=max(13,14)=14, i=3
  [16,18]: start=16 <= ne=14 ❌ → stop Phase 2

  Insert merged [ns=5, ne=14] into result
  result = [[1,3],[5,14]]

--- Phase 3: remaining intervals ---
  [16,18] → add as-is, i=4
  result = [[1,3],[5,14],[16,18]]

Final: [[1,3],[5,14],[16,18]] ✅
```

---

### Dry Run — `[[1,2],[3,5],[6,7],[8,10],[12,16]]`, newInterval `[4,8]`

```
ns=4, ne=8

Phase 1 (end < 4):
  [1,2]: end=2 < 4 ✅ → add
  [3,5]: end=5 < 4 ❌ → stop
  result = [[1,2]]

Phase 2 (start <= 8):
  [3,5]:  start=3 <= 8 ✅ → ns=min(4,3)=3, ne=max(8,5)=8
  [6,7]:  start=6 <= 8 ✅ → ns=min(3,6)=3, ne=max(8,7)=8
  [8,10]: start=8 <= 8 ✅ → ns=min(3,8)=3, ne=max(8,10)=10
  [12,16]:start=12 <= 10 ❌ → stop

  Insert [3,10]
  result = [[1,2],[3,10]]

Phase 3:
  [12,16] → add
  result = [[1,2],[3,10],[12,16]] ✅
```

---

### Algorithm

```
1. ns, ne = newInterval   ← start and end of new interval

2. Phase 1 — add all intervals that end BEFORE new interval starts:
     While intervals[i][1] < ns:
         result.append(intervals[i])
         i++

3. Phase 2 — merge all overlapping intervals into new interval:
     While intervals[i][0] <= ne:
         ns = min(ns, intervals[i][0])
         ne = max(ne, intervals[i][1])
         i++
     result.append([ns, ne])   ← insert the (expanded) new interval

4. Phase 3 — add all remaining intervals:
     While i < n:
         result.append(intervals[i])
         i++

5. Return result
```

---

### The Two Boundary Conditions Explained

```
Phase 1 stop condition:  intervals[i][1] < ns
  → "Does this interval END before the new one STARTS?"
  → If yes, no overlap → add it.
  → Stops the moment an interval could possibly overlap.

Phase 2 stop condition:  intervals[i][0] <= ne
  → "Does this interval START before or at the new one's END?"
  → If yes, it overlaps → merge.
  → Stops the moment we're past all overlaps.
```

```
The ne in Phase 2 grows as we merge:
  ne = max(ne, intervals[i][1])

So an interval that wouldn't have overlapped originally
might get pulled in because ne expanded.
This is the "chain reaction" merge.
```

---

### Edge Cases

```
New interval before all:
  intervals = [[3,5],[6,9]], new = [1,2]
  Phase 1: nothing (3 > 2)
  Phase 2: nothing (3 > 2)
  Insert [1,2], then add [3,5],[6,9]
  → [[1,2],[3,5],[6,9]] ✅

New interval after all:
  intervals = [[1,5]], new = [6,8]
  Phase 1: [1,5] added (end=5 < 6)
  Phase 2: nothing (no more)
  Insert [6,8]
  → [[1,5],[6,8]] ✅

Empty intervals list:
  Phase 1,2,3 all skip
  result = [[ns, ne]] ✅

New interval engulfs all:
  intervals = [[2,3],[4,5]], new = [1,10]
  Phase 1: nothing (2 > 1)
  Phase 2: both merged into [1,10]
  → [[1,10]] ✅
```

---

### Complexity

| | |
|---|---|
| Time | O(N) — single linear pass, each interval touched once |
| Space | O(N) — result list |