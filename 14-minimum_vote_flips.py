def weighted_vote_flipping(n: int, k: int, votes: list[int], weights: list[int]) -> int:
    """
    votes[i]   -> 0 or 1
    weights[i] -> weight of voter i

    Returns:
        Minimum flips needed for candidate 1 to win
        OR -1 if impossible within k flips
    """

    # Current total weights
    s1 = sum(weights[i] for i in range(n) if votes[i] == 1)
    s0 = sum(weights[i] for i in range(n) if votes[i] == 0)

    # Already winning
    if s1 > s0:
        return 0

    # Collect weights of all 0-voters
    zero_weights = sorted([weights[i] for i in range(n) if votes[i] == 0], reverse=True)

    flips = 0

    # Greedily flip highest-weight 0-voters
    for weight in zero_weights:

        # Cannot exceed k flips
        if flips >= k:
            break

        # Flip this vote: 0 -> 1
        s1 += weight
        s0 -= weight

        flips += 1

        # Candidate 1 wins
        if s1 > s0:
            return flips

    return -1


# --- Tests ---
cases = [
    (3, 1, [1, 0, 1], [10, 5, 10], 0),
    (4, 2, [0, 0, 1, 1], [10, 20, 5, 5], 1),
    (3, 1, [0, 0, 0], [100, 100, 100], -1),
    (5, 2, [0, 1, 0, 1, 0], [5, 10, 20, 15, 25], 1),
    (5, 3, [0, 0, 0, 1, 1], [1, 2, 3, 4, 5], 1),
]


for n, k, votes, weights, expected in cases:

    result = weighted_vote_flipping(n, k, votes, weights)

    status = "✓" if result == expected else "✗"

    print(f"{status}  n={n}, k={k}, result={result}, expected={expected}")
