def shortest_job_first(arr: list):
    if not arr:
        return 0
    
    arr.sort()
    t, wt = 0, 0
    
    for job in arr:
        wt += t
        t += job
    return wt // len(arr)

# jobs = [3, 1, 4, 2, 5]
jobs = [1,2,3]
print(shortest_job_first(jobs))
        