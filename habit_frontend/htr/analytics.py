import datetime

import numpy as np
import pandas as pd
from tabulate import tabulate

from htr.schemas import Habit, HabitEvent


def get_expected_streaks(events: list[HabitEvent], periodicity: int) -> int:
    if len(events) < 2:
        return 0

    start_date: datetime.date = events[0].completed_at
    end_date: datetime.date = events[-1].completed_at

    elapsed = end_date - start_date
    elapsed_days = elapsed.days

    return elapsed_days // periodicity


def calculate_score(expected_streaks: int, actual_streak: int) -> float:
    if expected_streaks == 0:
        return 0.0

    if actual_streak > expected_streaks:
        return 1.0

    return actual_streak / expected_streaks


def get_habit_events_history(events: list[HabitEvent], periodicity: int) -> pd.DataFrame:
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    deltas = np.diff(completed_events)

    if len(deltas) == 0:
        return pd.DataFrame({
            "Start Date": [],
            "End Date": [],
            "Streak": [],
        })

    streaks = (deltas <= np.timedelta64(periodicity, 'D')) * 1

    if np.all(streaks == 1):
        return pd.DataFrame({
            "Start Date": [completed_events[0]],
            "End Date": [completed_events[-1]],
            "Streak": [len(completed_events) - 1]
        })

    if np.all(streaks == 0):
        return pd.DataFrame({
            "Start Date": [],
            "End Date": [],
            "Streak": []
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
        "Start Date": completed_events[idx][::2],
        "End Date": completed_events[idx][1::2],
        "Streak": np.diff(idx)[::2]
    })

    return df


def tabulate_dataframe(dataframe: pd.DataFrame):
    return tabulate(dataframe, headers='keys', tablefmt='psql', showindex=False)


def get_habit_events_statistic(events: list[HabitEvent], periodicity: int) -> pd.DataFrame:
    streak_history = get_habit_events_history(events, periodicity)

    expected_streaks = get_expected_streaks(events, periodicity)

    if streak_history.empty:
        return pd.DataFrame({
            "Longest": [0],
            "Last": [0],
            "Median": [0],
            "Mean": [0],
            "Total Streaks": [0],
            "Expected Streaks": [expected_streaks],
            "Score": [0]
        })

    longest = streak_history.max()["Streak"]
    last = streak_history.iloc[-1]["Streak"]
    median = streak_history.median()["Streak"]
    mean = streak_history.mean()["Streak"]
    total = streak_history["Streak"].sum()
    score = calculate_score(expected_streaks, total)

    stat = pd.DataFrame({
        "Longest": [longest],
        "Last": [last],
        "Median": [median],
        "Mean": [mean],
        "Total Streaks": [total],
        "Expected Streaks": [expected_streaks],
        "Score": [score]
    })

    return stat


def calculate_statistic(habits_and_events: list[tuple[Habit, list[HabitEvent]]]) -> pd.DataFrame:
    habit_id_series = pd.Series([habit.habit_id for habit, _ in habits_and_events])
    tasks = pd.Series([habit.task for habit, _ in habits_and_events])
    periodicities = pd.Series([habit.periodicity for habit, _ in habits_and_events])

    current_streaks_list: list[int] = []
    longest_streaks_list: list[int] = []
    average_streaks_list: list[float] = []
    expected_streak_list: list[int] = []
    scores_list: list[float] = []

    for habit, events in habits_and_events:
        if len(events) > 0:
            stat = get_habit_events_statistic(events, habit.periodicity)
            current_streaks_list.append(stat['Last'][stat.last_valid_index()])
            longest_streaks_list.append(stat['Longest'][stat.last_valid_index()])
            average_streaks_list.append(stat['Mean'][stat.last_valid_index()])
            # total_streaks = stat['Total Streaks'][stat.last_valid_index()]
            expected_streak_list.append(stat['Expected Streaks'][stat.last_valid_index()])
            scores_list.append(stat['Score'][stat.last_valid_index()])
        else:
            current_streaks_list.append(0)
            longest_streaks_list.append(0)
            average_streaks_list.append(0)
            expected_streak_list.append(0)
            scores_list.append(0)

    current_streaks: pd.Series = pd.Series(current_streaks_list)
    longest_streaks: pd.Series = pd.Series(longest_streaks_list)
    average_streaks: pd.Series = pd.Series(average_streaks_list)
    expected_streak: pd.Series = pd.Series(expected_streak_list)
    scores: pd.Series = pd.Series(scores_list)

    return pd.DataFrame({
        "Habit ID": habit_id_series,
        "Task": tasks,
        "Periodicity": periodicities,
        "Last Streak": current_streaks,
        "Longest Streak": longest_streaks,
        "Average Streak": average_streaks,
        "Expected Streaks": expected_streak,
        "Score": scores
    })
