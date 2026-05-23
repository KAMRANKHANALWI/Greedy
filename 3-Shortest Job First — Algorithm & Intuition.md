## Shortest Job First — Algorithm & Intuition

**Problem:** Given a list of jobs with burst times, schedule them to minimize the **average waiting time**.

---

### Intuition

**The Dream:** Every job waits as little as possible before it starts.

**Key Insight:** If a short job waits behind a long job, it suffers. But if a long job waits behind a short job, only *one* job suffers. So always **run the shortest job first** to minimize total accumulated waiting.

```
jobs = [3, 1, 4, 2, 5]

Order A (unsorted):  3, 1, 4, 2, 5
Waiting times:       0, 3, 4, 8, 10  → total = 25, avg = 5.0

Order B (SJF):       1, 2, 3, 4, 5
Waiting times:       0, 1, 3, 6, 10  → total = 20, avg = 4.0 ✅
```

---

### Why Sorting Works — The Ripple Effect

Each job's burst time **adds to the waiting time of every job behind it.**

```
jobs = [1, 2, 3, 4, 5]  (sorted)

Job 1 (burst=1): contributes 1 to jobs 2,3,4,5 → adds 1×4 = 4
Job 2 (burst=2): contributes 2 to jobs 3,4,5   → adds 2×3 = 6
Job 3 (burst=3): contributes 3 to jobs 4,5     → adds 3×2 = 6
Job 4 (burst=4): contributes 4 to job 5        → adds 4×1 = 4
Job 5 (burst=5): no one waits after it         → adds 5×0 = 0
```

> A job at position `i` (0-indexed) affects `(n - 1 - i)` jobs behind it.
> Putting the **smallest** burst at position 0 minimizes total ripple.

```
jobs = [1, 2, 3]

Iteration 1 (job=1):
  wt += t  →  wt = 0+0 = 0   ← job1 waited 0, no one before it
  t  += job →  t  = 0+1 = 1   ← clock now at 1

Iteration 2 (job=2):
  wt += t  →  wt = 0+1 = 1   ← job2 waited 1 (job1's burst)
  t  += job →  t  = 1+2 = 3   ← clock now at 3

Iteration 3 (job=3):
  wt += t  →  wt = 1+3 = 4   ← job3 waited 3 (job1+job2 burst)
  t  += job →  t  = 3+3 = 6   ← clock now at 6
```

And visually on a timeline:

```
|--1--|----2----|------3------|
  ↑        ↑            ↑
wait=0   wait=1       wait=3
                    (1+2, sum of all before it)

Total wt = 0+1+3 = 4
Avg    wt = 4//3 = 1
```

The elegance of the two variables is:
- `t` → **running memory** of how much CPU time has elapsed
- `wt` → **accumulator** that keeps adding `t` at each step, because each job's waiting time *is* exactly `t` at that moment

so, `t` is essentially the prefix sum of burst times, and waiting time of each job is just that prefix sum up to (but not including) itself.

---

### Dry Run — `[3, 1, 4, 2, 5]`

```
After sort: [1, 2, 3, 4, 5]

t = current time (when next job starts)
wt = accumulated waiting time

Job  | wt += t  | t += job | t    | wt
-----|----------|----------|------|----
  1  | wt += 0  | t += 1   |  1   |  0
  2  | wt += 1  | t += 2   |  3   |  1
  3  | wt += 3  | t += 3   |  6   |  4
  4  | wt += 6  | t += 4   | 10   | 10
  5  | wt += 10 | t += 5   | 15   | 20
-----|----------|----------|------|----

avg = wt // n = 20 // 5 = 4 ✅
```

---

### Algorithm

```
1. Sort jobs ascending  → shortest burst time first

2. t  = 0   (clock: when does the current job start?)
   wt = 0   (total waiting time across all jobs)

3. For each job in sorted order:
       wt += t        ← this job waited exactly t time units
       t  += job      ← clock advances by this job's burst time

4. Return wt // len(jobs)   ← average waiting time (integer division)
```

---

### Key Variable Meanings

```
t  = time elapsed so far = start time of current job
                         = waiting time of current job

wt = sum of waiting times of all jobs processed so far
```

> A job's **waiting time** = time at which it starts = `t` at that moment,
> because it arrived at time 0 and CPU was busy until `t`.

---

### Complexity

| | |
|---|---|
| Time | O(N log N) — sorting dominates |
| Space | O(1) — just two counters |

The greedy choice is globally optimal here — SJF is provably the schedule that minimizes average waiting time when all jobs are available at time 0.



