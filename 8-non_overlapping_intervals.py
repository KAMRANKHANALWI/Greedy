def erase_overlap_intervals(intervals):
    """
    intervals: list of [start, end]
    Returns: minimum number of intervals to remove
    """
    if not intervals:
        return 0
    
    # Sort by end time
    sorted_intervals = sorted(intervals, key= lambda x : x[1])
    
    kept = 1
    last_end = intervals[0][1]
    
    # Greedily keep non-overlapping intervals
    for start, end in intervals[1:]:
        if start >= last_end:
            kept += 1
            last_end = end
            
    return len(intervals) - kept
    

intervals = [[1,3],[2,5],[3,6],[4,7],[5,8],[6,9],[8,10]]
print(erase_overlap_intervals(intervals))