def fractional_knapsack(capacity: float, items: list[tuple]) -> float:
    """
    items: list of (value, weight)
    Returns: maximum value achievable
    """

    # Step 1: Sort by value per kg, descending
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0.0
    remaining = capacity

    for value, weight in items:
        if remaining <= 0:
            break

        if weight <= remaining:
            # Take the whole item
            total_value += value
            remaining -= weight
        else:
            # Take the fraction that fits
            fraction = remaining / weight
            total_value += value * fraction
            remaining = 0   # bag is full

    return total_value


# --- Tests ---
cases = [
    (50,  [(60,10),(100,20),(120,30)],  240.0),   # classic example
    (10,  [(500,30)],                   166.67),  # only a fraction of one item
    (50,  [(60,10),(100,20),(120,30),(200,40)],  255.0),
    (0,   [(60,10),(100,20)],           0.0),     # no capacity
    (100, [(60,10),(100,20),(120,30)],  280.0),   # fits everything
]

for capacity, items, expected in cases:
    result = fractional_knapsack(capacity, items)
    status = "✓" if abs(result - expected) < 0.01 else "✗"
    print(f"{status}  capacity={capacity}, result={result:.2f}, expected={expected:.2f}")