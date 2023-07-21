import pytest
import responses

from htr.schemas.habit_event import HabitEvent
from htr.analytics import calculate_record_streak


def test_can_get_record_streaks():
    events_json = [
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-13"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-16"},  # 5
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-20"},  # X
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-23"},  # 1
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-01"},  # X
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-04"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-07"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-10"}  # 3
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]
    periodicity: int = 3
    expected_record_streak = 5

    record_streak = calculate_record_streak(events, periodicity)
    assert record_streak == expected_record_streak

#
# def test_can_get_current_streaks():
#     events_json = [
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-13"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-15"},  # 5
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-20"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-23"},  # 2
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-01"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},
#         {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"}  # 3
#     ]
#
#     events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]
#     periodicity: int = 3
#     expected_current_streak = 3
#
#     current_streak = calculate_current_streaks(events, periodicity)
#     assert current_streak == expected_current_streak
