from operator import attrgetter

import numpy as np

from htr.schemas.habit import Habit
from htr.schemas.habit_event import HabitEvent


def convert_habit_event_in_np(events: list[HabitEvent]) -> np.ndarray:
    date_lists = [event.completed_at for event in events]
    print("dates: ", date_lists)
    return np.array(date_lists, dtype="datetime64")


def calculate_streaks(events: list[HabitEvent], periodicity: int):
    arr = convert_habit_event_in_np(events)
    print("numpy array: ", arr)
    print("numpy array diffs: ", np.diff(arr))


