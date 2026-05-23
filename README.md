# Greedy Algorithms

A curated collection of greedy algorithm problems — each with a clean Python solution and a hand-written Algorithm & Intuition breakdown covering the key insight, dry runs, and complexity.

---

## Problems

| # | Problem | Key Idea |
|---|---------|----------|
| 1 | Assign Cookies | Smallest sufficient cookie to least greedy child |
| 2 | Lemonade Change | Guard $5 bills — they're the most versatile |
| 3 | Shortest Job First | Shortest burst → minimum average waiting time |
| 4 | Jump Game I | Track farthest reachable index |
| 5 | Jump Game II | BFS window expansion — min jumps to reach end |
| 6 | Job Sequencing | Highest profit first, fill latest available slot |
| 7 | N Meetings in One Room | Earliest ending meeting leaves most room |
| 8 | Non-overlapping Intervals | Min removals = total − max non-overlapping kept |
| 9 | Insert Intervals | Three-phase: before, merge, after |
| 10 | Min Platforms at Railway Station | Two-pointer sweep on sorted arrivals/departures |
| 11 | Valid Parenthesis String | Track `[lo, hi]` range of possible open brackets |
| 12 | Candy | Two-pass: fix left constraint then right |
| 13 | Fractional Knapsack | Sort by value/weight ratio, take greedily |
| 14 | Minimum Vote Flips | Flip heaviest 0-voter first — double swing effect |
| 15 | Max Array Sum After K Negations | Unified penalty pool: neg runs + pos gaps |

---

## Structure

Each problem has two files:

```
N-problem_name.py          # solution
N-Problem_Name — Algorithm & Intuition.md   # breakdown
```

The `.md` files cover intuition, dry runs, edge cases, and complexity — written to reinforce understanding, not just memorization.

---

## Topics Covered

`activity selection` · `interval scheduling` · `two pointers` · `sweep line` · `range tracking` · `knapsack` · `scheduling` · `greedy proof by exchange`