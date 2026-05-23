def check_valid_string(s: str) -> bool:
    lo = 0   # min possible unmatched '('
    hi = 0   # max possible unmatched '('

    for ch in s:
        if ch == '(':
            lo += 1
            hi += 1
        elif ch == ')':
            lo -= 1
            hi -= 1
        else:  # ch == '*'
            lo -= 1   # best case: treat * as ')'
            hi += 1   # worst case: treat * as '('

        # Too many ')' — impossible to recover
        if hi < 0:
            return False

        # lo can't go below 0 — we can't have negative opens
        lo = max(lo, 0)

    # Valid if 0 open brackets is achievable
    return lo == 0


# --- Tests ---
cases = [
    ("()",    True),
    ("(*)",   True),
    ("(*))",  True),
    ("(*(",   False),
    ("",      True),   # empty string is valid
    (")*((",  False),
    ("(((*)", True),
    ("*",     True),
]

for s, expected in cases:
    result = check_valid_string(s)
    status = "✓" if result == expected else "✗"
    print(f"{status}  '{s}' → {result}")