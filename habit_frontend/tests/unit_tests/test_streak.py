import pytest
import responses

from htr.schemas.habit_event import HabitEvent
from htr.analytics import calculate_streaks


def test_can_get_current_streaks():
    events_json = [
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-02"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-03"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-05"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-06"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-08"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-09"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-11"},
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    calculate_streaks(events, 3)
