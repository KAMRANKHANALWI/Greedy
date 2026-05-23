## Minimum Platforms at Railway Station — Algorithm & Intuition

**Problem:** Given arrival and departure times of trains at a station, find the **minimum number of platforms** needed so no train has to wait.

```
arrivals   = [1, 2, 3, 5, 7, 8]
departures = [4, 6, 5, 8, 9, 10]
→ 3 platforms needed
```

---

### Intuition

**The Dream:** Use the fewest platforms possible while ensuring every train that arrives before another departs has its own platform.

**Key Insight:** Think of this as a **timeline of events** — arrivals and departures. Each arrival needs a platform; each departure frees one. Sort both lists independently and sweep through time, tracking how many platforms are occupied simultaneously. The peak is your answer.

```
Time →   1   2   3   4   5   6   7   8   9   10
Events: [A] [A] [A]     [D] [A] [D] [A] [A]     [D]
                    [D]         [D]         [D] [D]

Platforms in use:
         1   2   3   2   1   2   1   2   3   2   1
                              ↑ peak = 3
```

---

### Why Sort Arrivals and Departures Separately?

You don't care which train departs — only **when** a platform becomes free. By sorting departures independently, you get a clean timeline of "next earliest platform to be released", which is all you need.

```
Sorted arrivals:    [1, 2, 3, 5, 7, 8]
Sorted departures:  [4, 5, 6, 8, 9, 10]
                     ↑
              earliest train to leave
```

---

### Two-Pointer Sweep — The Core Idea

```
i = arrival pointer    (which train is arriving next?)
j = departure pointer  (which train is departing next?)

At each step, compare arrivals[i] vs departures[j]:

  If arrivals[i] <= departures[j]:
      → A new train arrives before the next departure
      → Need one MORE platform
      → i++

  Else:
      → A departure happens before the next arrival
      → One platform is FREED
      → j++

Track platforms and record the maximum.
```

---

### Dry Run — Full Walkthrough

```
arrivals   = [1, 2, 3, 5, 7, 8]
departures = [4, 5, 6, 8, 9, 10]

i=0, j=0, platforms=0, max_platforms=0

Step | arrivals[i] | departures[j] | arr<=dep? | Action        | platforms | max
-----|-------------|---------------|-----------|---------------|-----------|----
  1  |      1      |      4        |  1<=4 ✅  | arrive, i++   |     1     |  1
  2  |      2      |      4        |  2<=4 ✅  | arrive, i++   |     2     |  2
  3  |      3      |      4        |  3<=4 ✅  | arrive, i++   |     3     |  3
  4  |      5      |      4        |  5<=4 ❌  | depart, j++   |     2     |  3
  5  |      5      |      5        |  5<=5 ✅  | arrive, i++   |     3     |  3
  6  |      7      |      5        |  7<=5 ❌  | depart, j++   |     2     |  3
  7  |      7      |      6        |  7<=6 ❌  | depart, j++   |     1     |  3
  8  |      7      |      8        |  7<=8 ✅  | arrive, i++   |     2     |  3
  9  |      8      |      8        |  8<=8 ✅  | arrive, i++   |     3     |  3
 10  |  i=6=n, STOP

max_platforms = 3 ✅
```

---

### Visual Overlap Map

```
Platform 1: |----T1----|  |----T5---|
Platform 2:   |------T2------|  |----T6----|
Platform 3:     |--T3--|  |----T4----|

Time:         1  2  3  4  5  6  7  8  9  10

At time 3: T1, T2, T3 all present → 3 platforms needed (peak)
```

---

### Algorithm

```
1. Sort arrivals ascending
   Sort departures ascending

2. i=0 (arrival ptr), j=0 (departure ptr)
   platforms=0, max_platforms=0

3. While i < n:           ← process all arrivals

     If arrivals[i] <= departures[j]:
         platforms += 1              ← train arrives, need platform
         max_platforms = max(max_platforms, platforms)
         i++

     Else:
         platforms -= 1              ← train departs, free platform
         j++

4. Return max_platforms
```

---

### The `arrivals[i] <= departures[j]` Condition

```
Why <= and not <?

If a train arrives exactly when another departs (same timestamp),
they overlap — the departing train hasn't cleared the platform yet.
So we need the incoming train to wait → counts as a platform needed.

arrivals[i] <= departures[j] → treat simultaneous arrival+departure
                                as "arrival happens first" → need +1 platform
```

---

### Why j Never Goes Out of Bounds

```
We only ever move j when we know a departure happens before an arrival.
Since every train that arrives must also depart, j can only reach
at most as far as i has advanced → j never overtakes i, never out of bounds.
```

---

### Edge Cases

```
All trains at the same time:
  arrivals = [5,5,5], departures = [6,6,6]
  → 3 platforms needed (all overlap)

No overlap at all:
  arrivals = [1,5,9], departures = [3,7,11]
  → 1 platform (one at a time)

One train:
  → always 1 platform
```

---

### Complexity

| | |
|---|---|
| Time | O(N log N) — sorting dominates |
| Space | O(1) — just pointers and counters |