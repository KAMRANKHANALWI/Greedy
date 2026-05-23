## Fractional Knapsack — Algorithm & Intuition

**Problem:** Given a knapsack of fixed `capacity` and a list of items with `(value, weight)`, maximise the total value. Unlike 0/1 Knapsack, you can take **fractions** of items.

```
capacity = 50
items = [(value=60, weight=10), (value=100, weight=20), (value=120, weight=30)]
→ max value = 240.0
```

---

### Intuition

**The Dream:** Pack the bag with the most valuable stuff per unit of weight.

**Key Insight:** Sort items by **value per kg** (value/weight ratio) descending. Always fill the bag with the best deal first. If an item doesn't fully fit, take just the fraction that does.

```
items sorted by value/weight:
  (60, 10)  → 60/10 = 6.0 $/kg   ← best deal
  (100, 20) → 100/20 = 5.0 $/kg
  (120, 30) → 120/30 = 4.0 $/kg  ← worst deal

capacity = 50:
  Take all of item 1 (weight=10): value += 60,  remaining = 40
  Take all of item 2 (weight=20): value += 100, remaining = 20
  Take all of item 3 (weight=30): can't fit fully.
    Fraction = 20/30 = 2/3
    value += 120 × (2/3) = 80,  remaining = 0

Total = 60 + 100 + 80 = 240.0 ✅
```

---

### Why Value/Weight Ratio?

```
Imagine you have 10 kg of capacity left. Which gives more value?

Item A: value=100, weight=20 → ratio=5  → 10kg gives 50 value
Item B: value=60,  weight=10 → ratio=6  → 10kg gives 60 value

Take item B first → more value per precious kg of capacity.

Ratio is the "exchange rate" of weight for value.
Always spend your capacity at the best exchange rate first.
```

---

### Dry Run — Classic Example

```
capacity=50
items after sorting by ratio:
  (60, 10)  ratio=6.0
  (100, 20) ratio=5.0
  (120, 30) ratio=4.0

remaining=50, total_value=0.0

Item      | weight | remaining | fits? | action            | total_value | remaining
----------|--------|-----------|-------|--------------------|-------------|----------
(60,  10) |   10   |    50     | Yes   | take all           |    60.0     |    40
(100, 20) |   20   |    40     | Yes   | take all           |   160.0     |    20
(120, 30) |   30   |    20     | No    | take 20/30 = 0.667 |   160+80=240|     0

Total = 240.0 ✅
```

---

### Dry Run — Only Fraction Fits

```
capacity=10, items=[(500,30)]
ratio = 500/30 = 16.67

remaining=10, total_value=0.0

Item      | weight | fits? | fraction       | total_value
----------|--------|-------|----------------|------------
(500, 30) |   30   | No    | 10/30 = 0.333  | 500×0.333 = 166.67

Total = 166.67 ✅
```

---

### Whole Item vs Fraction — The Decision

```
For each item (value, weight):

  If weight <= remaining:
      Take the WHOLE item
      total_value += value
      remaining   -= weight

  Else:
      Take a FRACTION
      fraction     = remaining / weight
      total_value += value × fraction
      remaining    = 0        ← bag is full, stop
```

```
The fraction formula explained:
  You have 'remaining' kg of space.
  The item weighs 'weight' kg.
  You can take (remaining/weight) of the item.
  Value gained = full_value × (remaining/weight)
```

---

### Algorithm

```
1. Sort items by (value/weight) descending  ← best ratio first

2. remaining = capacity
   total_value = 0.0

3. For each (value, weight) in sorted items:
       If remaining <= 0: break

       If weight <= remaining:
           total_value += value
           remaining   -= weight
       Else:
           total_value += value × (remaining / weight)
           remaining    = 0

4. Return total_value
```

---

### Fractional vs 0/1 Knapsack

```
Fractional Knapsack:
  Can split items → greedy by ratio works perfectly.
  Greedy optimal proof: if you pick a lower-ratio item before a higher-ratio one,
  you can swap and gain more value — contradiction.

0/1 Knapsack:
  Can't split items → greedy by ratio fails.
  Example: capacity=10, items=[(6,4),(5,3),(5,3)]
  Ratio order: 6/4=1.5, 5/3=1.67 → greedy picks (5,3) first
  → (5,3)+(5,3)=10 value, uses all capacity ✅
  But (6,4) alone = 6 with room wasted — greedy is suboptimal here!

  0/1 Knapsack needs DP.
  Fractional Knapsack needs Greedy.
```

---

### Edge Cases

```
Capacity = 0:
  remaining=0 → loop breaks immediately → total=0.0 ✅

All items fit:
  capacity=100, items=[(60,10),(100,20),(120,30)]
  Take all three → 280.0

Single item, partial:
  capacity=10, items=[(500,30)]
  → take 1/3 of item → 166.67

Item with weight=0:
  Infinite ratio → should be handled separately (edge case in real problems)
```

---

### Complexity

| | |
|---|---|
| Time | O(N log N) — sorting dominates |
| Space | O(N) — for sorted items copy |