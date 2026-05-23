## Valid Parenthesis String — Algorithm & Intuition

**Problem:** Given a string with `(`, `)`, and `*` (where `*` can be `(`, `)`, or empty string), determine if it's **valid** — every `(` can be matched with a `)`.

```
"()"   → True
"(*)"  → True   (* used as empty)
"(*))" → True   (* used as '(')
"(*("  → False  (two unmatched '(')
```

---

### Intuition

**The Dream:** Check if there's at least one valid assignment of `*` characters that makes the string balanced.

**Key Insight:** Instead of trying all `3^k` combinations of `*` replacements, track a **range** `[lo, hi]` — the minimum and maximum number of unmatched `(` brackets that could exist at each point.

```
lo = minimum possible unmatched '('   (treat * as ')' or empty)
hi = maximum possible unmatched '('   (treat * as '(' always)

If 0 is inside this range at the end → valid.
```

---

### How Each Character Updates the Range

```
Character '(':
  Every scenario gains one unmatched '('
  lo += 1,  hi += 1

Character ')':
  Every scenario loses one unmatched '('
  lo -= 1,  hi -= 1

Character '*':
  Best case:  treat as ')' → lose one open  → lo -= 1
  Worst case: treat as '(' → gain one open  → hi += 1
  (Treating as empty would be: lo stays, hi stays — but
   this is already captured by the lo/hi range spread)
```

---

### The Two Guards

```
Guard 1: if hi < 0 → return False
  Even in the best case (every * treated as '('),
  there are too many ')' to ever close → impossible.

Guard 2: lo = max(lo, 0)
  lo can't go negative — negative unmatched '(' makes no sense.
  If lo would go to -1, it means * CAN be used as ')' to over-close,
  but we can also use * as empty — so the minimum valid count is 0.
```

---

### Dry Run — `"(*)"`

```
lo=0, hi=0

Char | lo change | hi change | Guard 1 | Guard 2 | lo | hi
-----|-----------|-----------|---------|---------|----|----|
 '(' |   lo+1    |   hi+1    |  1>=0   |  max(1,0)| 1  |  1
 '*' |   lo-1=0  |   hi+1=2  |  2>=0   |  max(0,0)| 0  |  2
 ')' |   lo-1=-1 |   hi-1=1  |  1>=0   |  max(-1,0)→0| 0 | 1

End: lo=0 → True ✅
```

```
lo=0 means "it's possible to have 0 unmatched '('" → valid!
hi=1 means "worst case, 1 unmatched '(' remains" → not all paths valid.
But lo=0 is all we need.
```

---

### Dry Run — `"(*("` → False

```
lo=0, hi=0

Char | lo     | hi     | hi<0? | lo=max(lo,0)
-----|--------|--------|-------|-------------
 '(' | 0+1=1  | 0+1=1  |  No   |      1
 '*' | 1-1=0  | 1+1=2  |  No   |      0
 '(' | 0+1=1  | 2+1=3  |  No   |      1

End: lo=1 ≠ 0 → False ❌
```

```
Even treating * as ')' (best case), we still have 1 unmatched '('.
```

---

### Dry Run — `")*((" ` → False

```
lo=0, hi=0

Char | lo     | hi     | hi<0?     | lo=max(lo,0)
-----|--------|--------|-----------|-------------
 ')' | 0-1=-1 | 0-1=-1 | hi=-1 ❌  | → return False immediately

String starts with ')' and no '(' before it → impossible.
```

---

### Why This Works — The Range Intuition

```
Think of [lo, hi] as: "all possible counts of unmatched '(' right now."

If 0 ∈ [lo, hi] at the end:
  → There EXISTS an assignment of * that results in 0 unmatched '('
  → String is valid

We don't enumerate every assignment.
We just track whether 0 is achievable.
```

```
"(*)" step-by-step range:

Start:    [0, 0]   ← no chars processed
After '(': [1, 1]  ← must have 1 unmatched
After '*': [0, 2]  ← could be 0 (if * = ')') or 2 (if * = '(')
After ')': [0, 1]  ← best case closes to 0, worst case closes to 1
End: 0 ∈ [0, 1] → Valid ✅
```

---

### Algorithm

```
1. lo = 0, hi = 0   ← range of possible unmatched '('

2. For each character ch in s:

     If ch == '(':  lo += 1,  hi += 1
     If ch == ')':  lo -= 1,  hi -= 1
     If ch == '*':  lo -= 1,  hi += 1

     If hi < 0:   return False   ← too many ')' even in best case
     lo = max(lo, 0)             ← can't have negative unmatched '('

3. Return lo == 0   ← 0 unmatched '(' is achievable
```

---

### lo vs hi — What Each Represents

```
lo = minimum unmatched '(' = pessimistic count
     (treat every * as ')' or empty — closes as many opens as possible)

hi = maximum unmatched '(' = optimistic count
     (treat every * as '(' — opens as many as possible)

Valid string: lo reaches 0 → it's POSSIBLE to balance everything.
```

---

### Complexity

| | |
|---|---|
| Time | O(N) — single pass through string |
| Space | O(1) — just two counters |