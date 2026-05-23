def min_platforms(arrivals, departures):
    """
    arrivals  : list of arrival times
    departures: list of departure times
    Returns   : minimum platforms needed
    """

    arrivals.sort()
    departures.sort()

    n = len(arrivals)
    i = 0        # pointer for arrivals
    j = 0        # pointer for departures
    platforms = 0
    max_platforms = 0

    # Process events in chronological order using two pointers
    while i < n:
        if arrivals[i] <= departures[j]:
            # A train arrives before the next departure → need one more platform
            platforms += 1
            max_platforms = max(max_platforms, platforms)
            i += 1
        else:
            # A train departs before the next arrival → free up a platform
            platforms -= 1
            j += 1

    return max_platforms


# --- Example ---
arrivals   = [1, 2, 3, 5, 7, 8]
departures = [4, 6, 5, 8, 9, 10]

print(f"Minimum platforms needed: {min_platforms(arrivals, departures)}")