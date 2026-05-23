def candy(ratings: list[int]) -> int:
    n = len(ratings)
    candies = [1] * n   # everyone starts with 1

    # Pass 1: left → right, fix left-neighbor constraint
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Pass 2: right → left, fix right-neighbor constraint
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)


# --- Tests ---
cases = [
    ([1, 0, 2],       5),
    ([1, 2, 2],       4),
    ([1, 3, 2, 2, 1], 7),
    ([1],             1),
    ([1, 2, 3],       6),   # strict increase → [1,2,3]
    ([3, 2, 1],       6),   # strict decrease → [3,2,1]
    ([1, 3, 2, 1, 4, 5, 2], 13),
]

for ratings, expected in cases:
    result = candy(ratings)
    status = "✓" if result == expected else "✗"
    print(f"{status}  {ratings} → {result}")