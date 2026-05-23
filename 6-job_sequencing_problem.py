def job_sequencing(jobs):
    """
    jobs: list of tuples → (job_id, deadline, profit)
    Returns: (scheduled_jobs, total_profit)
    """

    # Step 1: Sort by profit descending (greedy choice)
    jobs = sorted(jobs, key=lambda x: x[2], reverse=True)

    # Step 2: Find max deadline — this is our timeline size
    max_deadline = max(job[1] for job in jobs)

    # Step 3: Initialize slots (None = free)
    slots = [None] * (max_deadline + 1)  # index 1..max_deadline

    scheduled = []
    total_profit = 0

    # Step 4: For each job (greediest first), find latest free slot ≤ deadline
    for job_id, deadline, profit in jobs:
        # Try from deadline down to slot 1
        for slot in range(deadline, 0, -1):
            if slots[slot] is None:
                slots[slot] = job_id
                scheduled.append((slot, job_id, profit))
                total_profit += profit
                break  # Job placed, move to next

    # Sort by slot for clean output
    scheduled.sort()
    return scheduled, total_profit


# --- Example ---
jobs = [
    ("J1", 2, 80),
    ("J2", 3, 50),
    ("J3", 2, 90),
    ("J4", 4, 30),
    ("J5", 1, 60),
]

result, profit = job_sequencing(jobs)

print("Scheduled jobs:")
for slot, job_id, p in result:
    print(f"  Slot {slot}: {job_id}  (profit: {p})")
print(f"\nTotal profit: {profit}")