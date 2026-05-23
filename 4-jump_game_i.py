def jump_game_i(arr):
    max_idx = 0
    for i in range(len(arr)):
        if i > max_idx:
            return False
        max_idx = max(max_idx, i + arr[i])
    return True


# arr = [2, 3, 1, 0, 4]
arr = [2, 1, 1, 0, 4]
print(jump_game_i(arr))