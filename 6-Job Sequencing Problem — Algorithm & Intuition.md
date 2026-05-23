## Job Sequencing Problem — Algorithm & Intuition

**Problem:** Given a list of jobs, each with a `deadline` and a `profit`, schedule at most one job per time slot to **maximize total profit**. Each job takes exactly 1 unit of time and must finish by its deadline.

```
jobs = [
    (J1, deadline=2, profit=80),
    (J2, deadline=3, profit=50),
    (J3, deadline=2, profit=90),
    (J4, deadline=4, profit=30),
    (J5, deadline=1, profit=60),
]
```

---

### Intuition

**The Dream:** Earn as much profit as possible given limited time slots.

**Key Insight:** Always try to schedule the **most profitable job first**. And when placing it, use the **latest available slot** before its deadline — this preserves earlier slots for other jobs that might need them.

```
Sort by profit descending:
  J3 (profit=90) → try slot 2  → slot 2 free ✅
  J1 (profit=80) → try slot 2  → taken, try slot 1 → free ✅
  J5 (profit=60) → try slot 1  → taken, no slot 0 → SKIP ❌
  J2 (profit=50) → try slot 3  → free ✅
  J4 (profit=30) → try slot 4  → free ✅
```

> Why the **latest** slot? Placing a job at its earliest possible slot blocks future jobs from using it. The latest slot is the most "expendable" — it's less likely to be needed by another job.

---

### The Slot Array — Your Timeline

```
max_deadline = 4  →  slots = [None, None, None, None, None]
                               idx:    0     1     2     3     4
                                     (unused, 1-indexed)
```

Each index represents a 1-unit time slot. `None` = free, otherwise holds the job scheduled there.

---

### Dry Run — Step by Step

```
Jobs sorted by profit (desc):
  J3 (d=2, p=90)
  J1 (d=2, p=80)
  J5 (d=1, p=60)
  J2 (d=3, p=50)
  J4 (d=4, p=30)

slots = [_, _, _, _, _]   ← _ means None (slots 1–4)
         0  1  2  3  4

--- J3 (deadline=2, profit=90) ---
  Try slot 2 → free → place J3
  slots = [_,  _, J3,  _,  _]
  profit so far: 90

--- J1 (deadline=2, profit=80) ---
  Try slot 2 → taken
  Try slot 1 → free → place J1
  slots = [_, J1, J3,  _,  _]
  profit so far: 170

--- J5 (deadline=1, profit=60) ---
  Try slot 1 → taken
  No more slots ≤ deadline → SKIP ❌
  profit so far: 170

--- J2 (deadline=3, profit=50) ---
  Try slot 3 → free → place J2
  slots = [_, J1, J3, J2,  _]
  profit so far: 220

--- J4 (deadline=4, profit=30) ---
  Try slot 4 → free → place J4
  slots = [_, J1, J3, J2, J4]
  profit so far: 250
```

```
Final schedule (by slot):
  Slot 1: J1  (profit: 80)
  Slot 2: J3  (profit: 90)
  Slot 3: J2  (profit: 50)
  Slot 4: J4  (profit: 30)

Total profit: 250 ✅  (J5 was sacrificed — couldn't fit)
```

---

### Timeline Visualization

```
Time →   1     2     3     4
       [ J1 | J3 | J2 | J4 ]
         80   90   50   30
          ↑
     J5 (profit=60) wanted slot 1 but it was taken by J1
```

> J5 vs J1 at slot 1: J1 has higher profit (80 > 60), so it's correct that J1 won the slot.

---

### Why "Latest Slot First" is the Smart Choice

```
Suppose J3 (d=2) placed at slot 1 instead of slot 2:

slots = [_, J3, _, _, _]

Now J1 (d=2) tries slot 2 → free ✅ (still works)
But what if a future job has deadline=1?
  → It ONLY has slot 1. It's now blocked by J3 unnecessarily.

By placing J3 at slot 2 (latest), slot 1 stays free
for any job that *only* fits there.
```

**Rule:** The latest free slot ≤ deadline is always the safest placement.

---

### Algorithm

```
1. Sort jobs by profit descending     → tackle most valuable first

2. max_deadline = max deadline in jobs
   slots = [None] × (max_deadline + 1)  → 1-indexed slot array

3. For each job (job_id, deadline, profit):
       For slot from deadline down to 1:
           If slots[slot] is None:
               slots[slot] = job_id    ← place job here
               total_profit += profit
               break                   ← done with this job

4. Return scheduled jobs and total_profit
```

---

### The Greedy Choice Explained

```
Two greedy decisions working together:

① Process jobs by profit (desc)
  → Never skip a high-profit job to accommodate a low-profit one

② Fill latest available slot ≤ deadline
  → Don't "waste" early slots; preserve them for jobs that need them
```

These two together guarantee maximum profit — a greedy proof by exchange argument: swapping any two decisions in this scheme cannot improve the result.

---

### Edge Cases

```
All jobs same deadline:
  jobs = [(A, 2, 100), (B, 2, 80), (C, 2, 60)]
  Only slots 1 and 2 exist → pick A (slot 2) and B (slot 1)
  C is dropped. Profit = 180.

Job with deadline=1, highest profit:
  It MUST go to slot 1. If slot 1 is already taken by a lower-profit
  job → you'd have made a mistake. Sort by profit first prevents this.

Single job:
  Always scheduled. Profit = its profit.
```

---

### Complexity

| | |
|---|---|
| Time | O(N² ) — for each of N jobs, scan up to N slots in worst case |
| Space | O(D) — slot array of size max_deadline |

> Can be optimized to O(N log N) using a **Disjoint Set (Union-Find)** to find the next free slot in near O(1), but the naive slot-scan is intuitive and sufficient for most interview settings.