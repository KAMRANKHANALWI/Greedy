# ============================================================
# PROBLEM: Maximum Array Sum with K Subarray Negations
# ============================================================
#
# Given an array a[1..N] and integer K, you may negate at most
# K contiguous subarrays (overlapping flips stack).
# Find the maximum possible array sum after operations.
#
# Example:
#   a = [-10, 20, -30, 40, -50], k = 2
#
#   Flip a[2]=-30 → 30  (op 1)
#   Flip a[4]=-50 → 50  (op 2)
#   Result = [-10, 20, 30, 40, 50] → sum = 130  ✅
#
# Constraints:
#   1 <= n <= 10^5
#   1 <= k <= 10^5
#   -10^9 <= a[i] <= 10^9
#
# ============================================================
# APPROACH: Greedy
# ============================================================
#
# DREAM SCENARIO: every element is positive
#   → sum = sum of |a[i]|  (this is the max we can ever get)
#
# KEY OBSERVATION: a contiguous block of negatives costs just 1 flip!
#   [-10, 20, -30, 40, -50]
#     N1  P1   N2  P2   N3   ← 3 negative runs, 2 positive gaps
#   So with k=2, we can fully fix only 2 out of 3 runs.
#
# WHEN BUDGET IS SHORT (neg_runs > k), two options per deficit:
#
#   Option A — SKIP a run (leave it negative):
#     Penalty = 2 × that run's absolute sum
#     (contributes -X instead of +X → lose 2X from dream)
#
#   Option B — MERGE two runs by flipping across the gap:
#     Penalty = 2 × the positive gap sum between them
#     (those positives flip negative → lose 2×gap from dream)
#
#   BOTH options have the same penalty math!
#   So treat neg_run sums and pos_gap sums as ONE candidate pool.
#   Greedy: sort candidates, pick cheapest `deficit` many → minimize loss.
#
# ALGORITHM:
#   1. abs_sum = sum of |a[i]|
#   2. Find negative runs → their absolute sums
#      Find positive gaps between runs → their sums
#   3. If neg_runs <= k: return abs_sum (fix everything!)
#   4. deficit = len(neg_runs) - k
#      candidates = neg_runs + pos_gaps → sort
#   5. answer = abs_sum - 2 * sum(candidates[:deficit])
#
# TIME COMPLEXITY : O(N log N) — sorting candidates
# SPACE COMPLEXITY: O(N)       — storing runs and gaps
#
# ============================================================

import sys
input = sys.stdin.readline

def solve(n, k, a):

    # STEP 1: best possible sum if all elements were positive
    abs_sum = sum(abs(x) for x in a)

    neg_runs = []   # absolute sum of each consecutive negative block
    pos_gaps = []   # sum of each positive block sitting between two negative runs

    i = 0
    seen_neg = False   # tracks if we've encountered at least one negative run
    cur_pos = 0        # accumulates current positive gap

    # STEP 2: scan array, extract runs and gaps
    while i < n:

        if a[i] < 0:

            # consume the entire negative run
            s = 0
            while i < n and a[i] < 0:
                s += -a[i]   # store as positive (absolute value)
                i += 1

            # positive gap before this run is only valid
            # if there was a previous negative run to bridge between
            if seen_neg:
                pos_gaps.append(cur_pos)

            neg_runs.append(s)
            seen_neg = True
            cur_pos = 0       # reset gap accumulator

        else:

            # consume the entire positive block
            while i < n and a[i] >= 0:
                cur_pos += a[i]
                i += 1

    # STEP 3: if we have enough flips to fix all negative runs → dream achieved
    m = len(neg_runs)
    if m <= k:
        return abs_sum

    # STEP 4: we're short on flips
    # deficit = how many times we must "sacrifice" something
    deficit = m - k

    # merge neg_run sums and pos_gap sums into one pool
    # both represent equal-penalty choices (skip a run OR merge via gap)
    candidates = sorted(neg_runs + pos_gaps)

    # STEP 5: greedily pick cheapest deficit candidates to minimize total loss
    return abs_sum - 2 * sum(candidates[:deficit])


if __name__ == "__main__":
    try:
        n = int(input())
        k = int(input())
        a = [int(input()) for _ in range(n)]
        print(solve(n, k, a))
    except (EOFError, ValueError):
        pass