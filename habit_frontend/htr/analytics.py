import numpy as np

from htr.schemas.habit_event import HabitEvent


def calculate_record_streak(events: list[HabitEvent], periodicity: int) -> int:
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    partial_diff = np.ediff1d(completed_events).astype(np.int32)
    second_partial_diff = np.ediff1d(partial_diff)
    grouped_by_periodicity = np.split(partial_diff, np.where(second_partial_diff != 0)[0] + 1)

    record_strike = 0
    for g in grouped_by_periodicity:
        # check if the streak was broken
        if g[0] > periodicity:
            print(f"the periodicity {g[0]} was bigger than {periodicity}, not considering for the streak")
            continue

        record_strike = max(record_strike, g.shape[0])

    return record_strike


def calculate_current_streak(events: list[HabitEvent], periodicity: int) -> int:
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    partial_diff = np.ediff1d(completed_events).astype(np.int32)
    partial_diff = np.flipud(partial_diff)

    current_streak = 0
    for delta_time in partial_diff:
        print(f"evaluating {delta_time}")
        if delta_time <= periodicity:
            current_streak += 1
            continue
        else:
            break

    return current_streak
