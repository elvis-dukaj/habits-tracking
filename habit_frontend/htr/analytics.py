import datetime
from typing import Optional

import numpy as np
import pandas as pd
from tabulate import tabulate

from htr.schemas import HabitEvent


def get_delta_times_grouped_by_consecutive_streak(completed_events: np.ndarray):
    partial_diffs = np.diff(completed_events).astype(np.int32)
    second_partial_diff = np.ediff1d(partial_diffs)
    return np.split(partial_diffs, np.where(second_partial_diff != 0)[0] + 1)


def transform_to_panda_dataframe(events: list[HabitEvent], periodicity: int) -> pd.DataFrame:
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    deltas = np.diff(completed_events)

    if len(deltas) == 0:
        return pd.DataFrame({
            "start date": [],
            "end date": [],
            "streak": []
        })

    streaks = (deltas <= np.timedelta64(periodicity, 'D')) * 1

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

    streak_changes_index = np.nonzero(change_in_streaks)[0]

    first_streak_change_index = streak_changes_index[0]
    last_streak_change_index = streak_changes_index[-1]

    should_add_index_0 = change_in_streaks[first_streak_change_index] == -1
    should_add_last_index = change_in_streaks[last_streak_change_index] == 1

    dtype = streak_changes_index.dtype
    prefix = np.array([0]) if should_add_index_0 else np.array([], dtype=dtype)
    postfix = np.array([len(completed_events) - 1]) if should_add_last_index else np.array([], dtype=dtype)

    idx = np.r_[prefix, streak_changes_index + 1, postfix]

    df = pd.DataFrame({
        "start date": completed_events[idx][::2],
        "end date": completed_events[idx][1::2],
        "streak": np.diff(idx)[::2]
    })

    return df


def tabulate_dataframe(dataframe: pd.DataFrame):
    return tabulate(dataframe, headers='keys', tablefmt='psql', showindex=False)


def get_habit_events_statistic(dataframe: pd.DataFrame):
    col = 'streak'
    statistics_frame = pd.DataFrame({
        "Longest": dataframe.max()[col],
        "Last": dataframe[col][dataframe.last_valid_index()],
        "Median": dataframe.median()[col],
        "Mean": dataframe.mean()[col]
    }, index=[0])

    return statistics_frame
