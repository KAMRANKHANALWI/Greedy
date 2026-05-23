def n_meetings(meetings):
    sorted_meetings = sorted(meetings, key= lambda x : x[2])
    
    selected_meeting = []
    last_end = -1
    
    for id, start, end in sorted_meetings:
        if start > last_end:
            # selected_meeting.append((id, start, end))
            selected_meeting.append((id))
            last_end = end
    
    return selected_meeting

meetings = [
    ("M1", 1, 3),
    ("M2", 2, 6),
    ("M3", 5, 7),
    ("M4", 3, 8),
    ("M5", 6, 9),
    ("M6", 8, 10),
]

print(n_meetings(meetings))

