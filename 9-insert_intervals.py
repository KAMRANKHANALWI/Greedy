def insert(intervals, newInterval):
    result = []
    i = 0
    n = len(intervals)
    ns, ne = newInterval

    # Case 1: Current interval ends BEFORE new interval starts → no overlap, add it
    while i < n and intervals[i][1] < ns:
        result.append(intervals[i])
        i += 1

    # Case 2: Overlapping intervals → keep merging into newInterval
    while i < n and intervals[i][0] <= ne:
        ns = min(ns, intervals[i][0])
        ne = max(ne, intervals[i][1])
        i += 1

    # Insert the (possibly expanded) new interval
    result.append([ns, ne])

    # Case 3: Remaining intervals start AFTER new interval ends → add as-is
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


# Test cases
test_cases = [
    {
        "intervals":    [[1,3],[6,9],[11,14],[16,18]],
        "newInterval":  [5, 13],
        "description":  "New interval overlaps multiple"
    },
    {
        "intervals":    [[1,2],[3,5],[6,7],[8,10],[12,16]],
        "newInterval":  [4, 8],
        "description":  "LeetCode example 2"
    },
    {
        "intervals":    [[1,5]],
        "newInterval":  [6, 8],
        "description":  "New interval after all"
    },
    {
        "intervals":    [[3,5],[6,9]],
        "newInterval":  [1, 2],
        "description":  "New interval before all"
    },
    {
        "intervals":    [[1,3],[6,9]],
        "newInterval":  [2, 5],
        "description":  "Partial overlap with first"
    },
    {
        "intervals":    [],
        "newInterval":  [4, 7],
        "description":  "Empty intervals list"
    },
]

for tc in test_cases:
    result = insert(tc["intervals"], tc["newInterval"])
    print(f"Test : {tc['description']}")
    print(f"  intervals   : {tc['intervals']}")
    print(f"  newInterval : {tc['newInterval']}")
    print(f"  result      : {result}")
    print()