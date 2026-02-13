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
    if isinstance(meeting_duration, bool) or not isinstance(meeting_duration, int):
        raise TypeError("meeting_duration must be an integer number of minutes")
    if meeting_duration <= 0:
        return []

    work_start = 9 * 60
    work_end = 17 * 60
    if meeting_duration > (work_end - work_start):
        return []

    def to_minutes(t: str) -> int:
        if not isinstance(t, str):
            raise TypeError("event times must be strings in HH:MM format")
        parts = t.split(":")
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            raise ValueError(f"invalid time format: {t!r}")
        h = int(parts[0])
        m = int(parts[1])
        if h < 0 or h > 23 or m < 0 or m > 59:
            raise ValueError(f"invalid clock time: {t!r}")
        return h * 60 + m

    def is_friday(day_value: str) -> bool:
        if not isinstance(day_value, str):
            raise TypeError("day must be a string")
        day_key = day_value.strip().lower()
        # Do not infer weekday from dates to avoid timezone/date-interpretation ambiguity.
        friday_labels = {"f", "fr", "fri", "friday", "viernes", "vendredi", "freitag", "venerdi"}
        return day_key in friday_labels

    blocked = []
    for ev in events:
        if not isinstance(ev, dict):
            raise TypeError("each event must be a dict with start/end keys")
        s = to_minutes(ev["start"])
        e = to_minutes(ev["end"])
        if e < s:
            raise ValueError("event end time must be greater than or equal to start time")
        if e <= work_start or s >= work_end:
            continue
        if s < work_start:
            s = work_start
        if e > work_end:
            e = work_end
        if s < e:
            # Treat event intervals as half-open [start, end): starting exactly at event end is allowed.
            blocked.append((s, e))

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
    # Additional constraint: on Fridays, meetings cannot start after 15:00.
    if is_friday(day):
        friday_latest_start = 15 * 60
        if friday_latest_start < latest_start:
            latest_start = friday_latest_start
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
