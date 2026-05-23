## Assign Cookies — Algorithm & Intuition

**Problem:** Given children with greed factors and cookies with sizes, assign at most one cookie per child. A child is satisfied if `cookie_size >= greed_factor`. Maximize the number of satisfied children.

---

### Intuition

**The Dream:** Satisfy as many children as possible.

**Key Insight:** Give the **smallest sufficient cookie** to the **least greedy child** first. Don't waste a big cookie on a child who'd be happy with a small one.

```
greed = [1, 2]     → sorted: [1, 2]   (least greedy first)
size  = [1, 2, 3]  → sorted: [1, 2, 3] (smallest cookie first)
```

---

### Two-Pointer Greedy

```
greed: [1, 2]        ← r pointer (child)
size:  [1, 2, 3]     ← l pointer (cookie)

Step 1: greed[r=0]=1 <= size[l=0]=1 → SATISFIED! r++, l++
Step 2: greed[r=1]=2 <= size[l=1]=2 → SATISFIED! r++, l++
Step 3: l=2 < m=3, but r=2 == n=2 → STOP

Answer = r = 2 ✅
```

---

### Algorithm

```
1. Sort greed[] ascending  → tackle easiest children first
2. Sort size[]  ascending  → try smallest cookies first

3. l = cookie pointer, r = child pointer

4. While cookies remain AND children remain:
     If current cookie satisfies current child:
         child is happy → r++ (move to next child)
     
     Either way → l++ (cookie is used or too small, move on)

5. Return r (number of satisfied children)
```

---

### Why `l` always increments but `r` doesn't

```
greed = [2]
size  = [1, 3]

Cookie 1 (size=1) < greed[0]=2 → can't satisfy, DISCARD cookie (l++)
Cookie 2 (size=3) >= greed[0]=2 → satisfied! (r++, l++)
```

A cookie too small for child `r` is **too small for every remaining child** (they're sorted by increasing greed). So it's safe to discard it permanently.

---

### Complexity

| | |
|---|---|
| Time | O(N log N + M log M) — sorting dominates |
| Space | O(1) — two pointers, no extra structure |

---

### Variable Naming Note

In your code, `l` iterates over **cookies** (`size`) and `r` iterates over **children** (`greed`) — which is a bit counterintuitive naming-wise, but the logic is correct. A cleaner mental mapping:

```python
cookie = 0   # index into size[]
child  = 0   # index into greed[]

while cookie < m and child < n:
    if greed[child] <= size[cookie]:
        child += 1      # child satisfied!
    cookie += 1         # cookie consumed or wasted
return child
```