## Student Name: Jackie Lin
## Student ID: 219588227

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
import random
from solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:00" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert slots[1] == "10:00"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots



#Extra 5 tests

def test_back_to_back_events_merge():
    events = [
        {"start": "10:00", "end": "10:30"},
        {"start": "10:30", "end": "11:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:00" in slots


def test_duration_longer_than_workday():
    events = []
    slots = suggest_slots(events, meeting_duration=500, day="2026-02-01")

    assert slots == []


def test_duration_equals_workday_blocked_by_lunch():
    events = []
    slots = suggest_slots(events, meeting_duration=480, day="2026-02-01")

    assert slots == []


def test_non_15_minute_duration():
    events = []
    slots = suggest_slots(events, meeting_duration=20, day="2026-02-01")

    assert "09:00" in slots
    assert "09:15" in slots
    assert "12:00" not in slots


def test_duplicate_events_no_change():
    events = [
        {"start": "10:00", "end": "10:30"},
        {"start": "10:00", "end": "10:30"},
    ]
    slots_dup = suggest_slots(events, meeting_duration=30, day="2026-02-01")
    slots_single = suggest_slots([{"start": "10:00", "end": "10:30"}], meeting_duration=30, day="2026-02-01")

    assert slots_dup == slots_single


def test_friday_no_starts_after_1500():
    """
    Requirement:
    On Fridays, meetings must not start after 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="Fri")

    assert "15:00" in slots
    assert "15:15" not in slots
    assert "16:00" not in slots


def test_event_partially_outside_work_hours_blocks_overlap_only():
    """
    Boundary case:
    Event clipping at work-start should still block overlapping morning slots.
    """
    events = [{"start": "08:30", "end": "09:30"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" not in slots
    assert "09:15" not in slots
    assert "09:45" in slots


def test_last_possible_start_non_friday_is_included():
    """
    Boundary case:
    The latest valid non-Friday start should be included.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=60, day="Thu")

    assert "16:00" in slots


def test_last_possible_start_friday_is_1500():
    """
    Boundary case:
    Friday latest start is capped at 15:00.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=15, day="Friday")

    assert "15:00" in slots
    assert "15:15" not in slots


def test_zero_or_negative_duration_returns_empty():
    """
    Invalid input:
    Non-positive duration should return no slots.
    """
    assert suggest_slots([], meeting_duration=0, day="Mon") == []
    assert suggest_slots([], meeting_duration=-30, day="Mon") == []


def test_invalid_time_format_raises_value_error():
    """
    Invalid input:
    Malformed time strings should fail fast.
    """
    events = [{"start": "9:xx", "end": "10:00"}]
    with pytest.raises(ValueError):
        suggest_slots(events, meeting_duration=30, day="Mon")


def test_missing_event_key_raises_key_error():
    """
    Invalid input:
    Missing required event fields should raise KeyError.
    """
    events = [{"start": "09:00"}]
    with pytest.raises(KeyError):
        suggest_slots(events, meeting_duration=30, day="Mon")


def test_randomized_event_order_invariance():
    """
    Randomized robustness:
    Event ordering should not affect output.
    """
    base_events = [
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "11:30"},
        {"start": "14:15", "end": "15:00"},
        {"start": "15:30", "end": "16:00"},
    ]
    expected = suggest_slots(base_events, meeting_duration=30, day="Tue")

    shuffled = base_events[:]
    random.Random(4312).shuffle(shuffled)
    actual = suggest_slots(shuffled, meeting_duration=30, day="Tue")

    assert actual == expected


def test_event_covering_workday_returns_empty():
    """
    Edge case:
    A full-day event during work hours leaves no availability.
    """
    events = [{"start": "09:00", "end": "17:00"}]
    slots = suggest_slots(events, meeting_duration=15, day="Mon")

    assert slots == []


def test_event_ending_at_work_start_does_not_block_0900():
    """
    Boundary case:
    Event ending right at 09:00 should not remove morning availability.
    """
    events = [{"start": "08:00", "end": "09:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="Mon")

    assert "09:00" in slots


def test_event_starting_at_work_end_does_not_block_afternoon():
    """
    Boundary case:
    Event starting at 17:00 should not affect workday slots.
    """
    events = [{"start": "17:00", "end": "18:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="Mon")

    assert "16:30" in slots


def test_friday_day_parsing_is_case_and_space_insensitive():
    """
    Edge case:
    Friday constraint should apply with mixed case and surrounding whitespace.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="  fRiDay  ")

    assert "15:00" in slots
    assert "15:15" not in slots


def test_short_friday_label_triggers_cutoff():
    """
    Edge case:
    One-letter Friday shorthand should trigger Friday cutoff.
    """
    slots = suggest_slots([], meeting_duration=30, day="F")
    assert "15:00" in slots
    assert "15:15" not in slots


def test_lunch_boundary_start_1115_allowed_for_45_minutes():
    """
    Boundary case:
    A meeting ending exactly at 12:00 should be allowed.
    """
    events = []
    slots = suggest_slots(events, meeting_duration=45, day="Mon")

    assert "11:15" in slots
    assert "11:30" not in slots


def test_invalid_clock_values_raise_value_error():
    """
    Invalid input:
    Out-of-range hour/minute values should raise ValueError.
    """
    with pytest.raises(ValueError):
        suggest_slots([{"start": "25:00", "end": "10:00"}], meeting_duration=30, day="Mon")
    with pytest.raises(ValueError):
        suggest_slots([{"start": "09:75", "end": "10:00"}], meeting_duration=30, day="Mon")


def test_non_string_event_time_raises_type_error():
    """
    Invalid input:
    Non-string event times should raise TypeError.
    """
    with pytest.raises(TypeError):
        suggest_slots([{"start": None, "end": "10:00"}], meeting_duration=30, day="Mon")


def test_iso_date_friday_enforces_cutoff():
    """
    Clarified behavior:
    ISO date strings do not trigger Friday-specific logic.
    """
    slots = suggest_slots([], meeting_duration=30, day="2026-02-06")
    assert "15:15" in slots


def test_cross_midnight_event_blocks_same_day_afternoon():
    """
    Invalid input:
    End-before-start events are rejected.
    """
    with pytest.raises(ValueError):
        suggest_slots([{"start": "14:00", "end": "13:00"}], meeting_duration=30, day="Mon")


def test_boolean_duration_raises_type_error():
    """
    Invalid input:
    Boolean duration is rejected even though bool is a subtype of int.
    """
    with pytest.raises(TypeError):
        suggest_slots([], meeting_duration=True, day="Mon")
