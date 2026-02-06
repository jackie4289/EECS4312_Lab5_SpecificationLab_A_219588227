## Student Name: Jackie Lin 
## Student ID: 219588227

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    if meeting_duration <= 0:
        return []

    work_start = 9 * 60
    work_end = 17 * 60
    if meeting_duration > (work_end - work_start):
        return []

    def to_minutes(t: str) -> int:
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    blocked = []
    for ev in events:
        s = to_minutes(ev["start"])
        e = to_minutes(ev["end"])
        if e <= work_start or s >= work_end:
            continue
        if s < work_start:
            s = work_start
        if e > work_end:
            e = work_end
        if s < e:
            # Treat event end as inclusive for meeting start times.
            e_block = e + 1 if e < work_end else e
            blocked.append((s, e_block))

    # Lunch break blocks all overlapping slots (12:00–13:00)
    blocked.append((12 * 60, 13 * 60))

    if blocked:
        blocked.sort()
        merged = []
        for s, e in blocked:
            if not merged or s > merged[-1][1]:
                merged.append([s, e])
            else:
                if e > merged[-1][1]:
                    merged[-1][1] = e
    else:
        merged = []

    latest_start = work_end - meeting_duration
    slots = []
    idx = 0
    for start in range(work_start, latest_start + 1, 15):
        end = start + meeting_duration
        while idx < len(merged) and merged[idx][1] <= start:
            idx += 1
        if idx < len(merged) and end > merged[idx][0]:
            continue
        slots.append(f"{start // 60:02d}:{start % 60:02d}")

    return slots
