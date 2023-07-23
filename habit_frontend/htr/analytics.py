import datetime

import numpy as np
import pandas as pd

from htr.schemas.habit_event import HabitEvent


def get_delta_times_grouped_by_consecutive_streak(completed_events: np.ndarray):
    partial_diffs = np.diff(completed_events).astype(np.int32)
    second_partial_diff = np.ediff1d(partial_diffs)
    return np.split(partial_diffs, np.where(second_partial_diff != 0)[0] + 1)


def transform_to_panda_dataframe(events: list[HabitEvent], periodicity: int) -> pd.DataFrame:
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    # print("completed_events: ", completed_events)

    deltas = np.diff(completed_events)
    # print("delta: ", deltas)

    streaks = (deltas <= np.timedelta64(periodicity, 'D')) * 1
    # print("streaks: ", streaks)

    if np.all(streaks == 1):
        return pd.DataFrame({
            "start date": [completed_events[0]],
            "end date": [completed_events[-1]],
            "streak": [len(completed_events) - 1]
        })

    if np.all(streaks == 0):
        print("all streak")
        return pd.DataFrame({
            "start date": [],
            "end date": [],
            "streak": []
        })

    change_in_streaks = np.diff(streaks)
    # print("change_in_streaks: ", change_in_streaks)

    streak_changes_index = np.nonzero(change_in_streaks)[0]
    # print("streak_changes_index: ", streak_changes_index)

    first_streak_change_index = streak_changes_index[0]
    last_streak_change_index = streak_changes_index[-1]

    should_add_index_0 = change_in_streaks[first_streak_change_index] == -1
    should_add_last_index = change_in_streaks[last_streak_change_index] == 1

    dtype = streak_changes_index.dtype
    prefix = np.array([0]) if should_add_index_0 else np.array([], dtype=dtype)
    postfix = np.array([len(completed_events) - 1]) if should_add_last_index else np.array([], dtype=dtype)

    idx = np.r_[prefix, streak_changes_index + 1, postfix]
    # print(f"idx: {idx}")

    df = pd.DataFrame({
        "start date": completed_events[idx][::2],
        "end date": completed_events[idx][1::2],
        "streak": np.diff(idx)[::2]
    })

    # print(f"data frame: {df}")
    return df


def get_delta_times_grouped_by_consecutive_streak2(completed_events: np.ndarray, periodicity: int):
    completed_events = np.concatenate(([completed_events[0] + datetime.timedelta(days=1)], completed_events))
    partial_diffs = np.diff(completed_events).astype(np.int32)
    # partial_diffs = (partial_diffs <= periodicity).astype(np.int32)
    print(f"partial_diffs {partial_diffs}")

    # second_partial_diffs = np.diff(partial_diffs)
    # print(f"second_partial_diffs {second_partial_diffs}")
    # grouped = np.split(completed_events, np.where(second_partial_diffs == 0)[0] + 1)
    # print(f"grouped {grouped}")
    return np.array([])


def calculate_streak_history(events: list[HabitEvent], periodicity: int):
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    grouped_by_periodicity = get_delta_times_grouped_by_consecutive_streak(completed_events)

    # remove all the broken streak
    print(f"grouped are: {grouped_by_periodicity}")


def calculate_record_streak(events: list[HabitEvent], periodicity: int) -> int:
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    grouped_by_periodicity = get_delta_times_grouped_by_consecutive_streak2(completed_events, periodicity)

    record_strike = 0
    for g in grouped_by_periodicity:
        # check if the streak was broken
        if g[0] > periodicity:
            continue

        record_strike = max(record_strike, g.shape[0])

    return record_strike


def calculate_current_streak(events: list[HabitEvent], periodicity: int) -> int:
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    partial_diff = np.flipud(np.ediff1d(completed_events).astype(np.int32))

    current_streak = 0
    for delta_time in partial_diff:
        if delta_time <= periodicity:
            current_streak += 1
            continue
        else:
            break

    return current_streak
