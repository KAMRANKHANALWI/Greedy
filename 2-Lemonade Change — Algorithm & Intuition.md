## Lemonade Change — Algorithm & Intuition

**Problem:** You sell lemonade for $5. Customers pay with $5, $10, or $20 bills (one at a time). Give correct change to every customer. Return `True` if you can serve all customers, `False` otherwise.

```
bills = [5, 5, 5, 10, 20]
→ True ✅

bills = [5, 5, 10, 10, 20]
→ False ❌
```

---

### Intuition

**The Dream:** Always have the right change ready when a customer needs it.

**Key Insight:** You only have two types of change to track — **$5 bills** and **$10 bills**. $20 bills are useless for giving change (no denomination needs $20 back), so just pocket them.

```
Customer pays $5  → no change needed, keep the $5
Customer pays $10 → give back $5
Customer pays $20 → give back $15 = ($10 + $5)  ← preferred
                              OR = ($5  + $5 + $5)  ← fallback
```

---

### Why Prefer $10 + $5 over $5 + $5 + $5 for $20?

```
$5 bills are the ONLY bill that satisfies both:
  - $10 customers (need one $5 back)
  - $20 customers (need change as part of $15)

$10 bills can ONLY help $20 customers.

So $5 bills are more "versatile" → spend them last.
When giving $15 change for $20, always prefer using a $10
to preserve $5 bills for future $10-paying customers.
```

> Greedily guard your $5s — they're the most in-demand resource.

---

### Three Cases

```
Bill = $5:
  No change needed.
  five += 1   ← bank it

Bill = $10:
  Must give $5 change.
  If five > 0:  five -= 1, ten += 1  ✅
  Else:         return False          ❌

Bill = $20:
  Must give $15 change.
  Option A (preferred): ten >= 1 and five >= 1
      → ten -= 1, five -= 1   ✅  (saves $5s)
  Option B (fallback):  five >= 3
      → five -= 3              ✅
  Else: return False            ❌
```

---

### Dry Run — `[5, 5, 5, 10, 20]` → True

```
five=0, ten=0

Bill  | Action                        | five | ten
------|-------------------------------|------|----
  $5  | bank it                       |  1   |  0
  $5  | bank it                       |  2   |  0
  $5  | bank it                       |  3   |  0
 $10  | give $5 change                |  2   |  1
 $20  | give $10+$5 change            |  1   |  0
------|-------------------------------|------|----

All customers served → True ✅
```

---

### Dry Run — `[5, 5, 10, 10, 20]` → False

```
five=0, ten=0

Bill  | Action                        | five | ten
------|-------------------------------|------|----
  $5  | bank it                       |  1   |  0
  $5  | bank it                       |  2   |  0
 $10  | give $5 change                |  1   |  1
 $10  | give $5 change                |  0   |  2
 $20  | need $10+$5 → ten=2 but five=0 ❌
      | need $5×3   → five=0          ❌
      | return False
------|-------------------------------|------|----

Can't make change → False ❌
```

```
The problem: two $10 bills drained all $5s.
When $20 arrived, we had tens but no fives → stuck.
```

---

### Algorithm

```
1. five = 0, ten = 0   ← track only useful change denominations

2. For each bill in bills:

     If bill == 5:
         five += 1                     ← free money, bank it

     If bill == 10:
         If five > 0: five -= 1, ten += 1
         Else: return False            ← can't make $5 change

     If bill == 20:
         If ten > 0 and five > 0:      ← preferred: use $10 first
             ten -= 1, five -= 1
         Elif five >= 3:               ← fallback: three $5s
             five -= 3
         Else: return False            ← can't make $15 change

3. return True                         ← all customers served
```

---

### The Greediness — Where Is It?

```
Only one greedy decision exists in this problem:

When giving $15 change for a $20 bill,
ALWAYS prefer ($10 + $5) over ($5 + $5 + $5).

Why? Because $5 bills are needed by both $10 and $20 customers,
but $10 bills are only useful for $20 customers.

Using a $10 bill "spends" the less flexible resource first
→ preserves the more flexible $5 for future use.
```

This is the classic greedy pattern: **use the least versatile resource first**.

---

### Edge Cases

```
First customer pays $10 or $20:
  → five=0, can't make change → immediately return False

All $5 bills:
  → just accumulate, always True

$20 when ten=0 but five >= 3:
  → fallback kicks in, still works

$20 when ten > 0 but five = 0:
  → Option A fails (no five), Option B fails (five < 3) → False
  → This is the trap: having $10s but no $5s is useless for $20 change
```

---

### Complexity

| | |
|---|---|
| Time | O(N) — single pass through bills |
| Space | O(1) — just two counters |