def assign(greed: list, size: list):
    n = len(greed)
    m = len(size)
    greed.sort()
    size.sort()
    l, r = 0, 0
    
    while l < m and r < n:
        if greed[r] <= size[l]:
            r += 1
        l += 1
    return r

g = [1,2]
s = [1,2,3]
print(assign(g, s))