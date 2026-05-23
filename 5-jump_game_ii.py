def jump_game_ii(nums):
    jumps = 0
    l = 0
    r = 0
    n = len(nums)

    while r < n - 1:
        farthest = 0

        for i in range(l, r + 1):
            farthest = max(farthest, i + nums[i])

        l = r + 1
        r = farthest
        jumps += 1

    return jumps

nums = [2,3,1,1,4]
print(jump_game_ii(nums))