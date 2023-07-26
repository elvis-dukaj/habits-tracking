import datetime

import numpy as np
import pandas as pd
from tabulate import tabulate

from htr.schemas import Habit, HabitEvent


def get_expected_streaks(events: list[HabitEvent], periodicity: int) -> int:
    """
    Given a list of HabitEvents and the periodicity, calculate the maximum number of streaks that would be possible in
    the given data range.

    :param events: list of events
    :param periodicity: periodicity in days
    :return: number of maximum consecutive streaks in the given set of events
    """
    if len(events) < 2:
        return 0

    start_date: datetime.date = events[0].completed_at
    end_date: datetime.date = events[-1].completed_at

    elapsed = end_date - start_date
    elapsed_days = elapsed.days

    return elapsed_days // periodicity


def calculate_score(expected_streaks: int, actual_streak: int) -> float:
    """
    Calculate the score given the expected streaks and the actual ones
    :param expected_streaks:
    :param actual_streak:
    :return: the value is in percentage in the range [0, 1]
    """
    if expected_streaks == 0:
        return 0.0

    if actual_streak > expected_streaks:
        return 1.0

    return actual_streak / expected_streaks


def get_habit_events_history(events: list[HabitEvent], periodicity: int) -> pd.DataFrame:
    """
    Given a list of habits, sort them in a table with the following format:

    Start Date | End Date   | Streaks
    ---------- | ---------- | -------
    2023-01-01 | 2023-01-05 | 4

    :param events: list of events, ordered by date
    :param periodicity: the periodicity of the corresponding habit
    :return: a panda.DataFrame with the columns ["Start Date", "End Date", "Streaks"]
    """
    completed_events: np.ndarray = np.array([event.completed_at for event in events], dtype=np.datetime64)
    deltas = np.diff(completed_events)

    if len(deltas) == 0:
        return pd.DataFrame({
            "Start Date": [],
            "End Date": [],
            "Streak": [],
        })

    """
    
    The goal of the whole algorithm is given a list of dates and a periodicity, to find the indexes start date,
    end date where there is a streak in this range of dates (inclusive)
    
    0. let's have the following dates: 2023-01-01, 2023-01-02, 2023-01-03, 2023-01-05, 2023-01-07, 2023-01-08
       and a periodicity of 1 day
    1. let's calculate the differences in days: we will get: [1, 1, 2, 2, 1]
        1. we can immagine at the difference as it was the 1st derivative (it's not really
           a derivative as we are not dividing by the step) but the idea is the same.
    2. let's mark as True everything that is <= periodicity: [True, True, False, False, True]
    3. transform True to 1 and False to 0: streaks = [1, 1, 0, 0, 1]
        3a. if all are 1s than we are done: we have only streaks
        3b. if all are 0s than we are done: wh have no streaks
    4. we calculate the difference of the difference of the streaks: change_in_streaks = [0, -1, 0, 1]
    5. now we are interested in the first and in the last non zero values of change_in_streaks:
        first_streak_change_index = 1
        last_streak_change_index = 3
        
        change_in_streaks is very important because a change in the sign means a change between a streak or not streak.
        We can immagine this as the 2nd derivative of streaks. When the sign is positive means we are in a streak 
        sequence, when it is negative we are in a non-streak instance, when it is 0 we are changing between the two.
        
        5a. If the first element of the change_in_streaks is negative we need to take into consideration the 1st element
            because we are in a streak since the beginning of the first date
        5b. If the last element of the change_in_streaks is positive we need to take into consideration the last element
            because we are in a streak until the end
    6. We create an idx array that looks like: idx = [0, 2, 4, 5]
    7. This indexes represent a sequence of [(date-start, date-end)] and the difference of these indexes is the number
        of streaks. We are done!
    8. Our array is [(2023-01-01, 2023-01-03, 3), (2023-01-07, 2023-01-08, 1)]
    """

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
    """
    Return a string with the formatted table
    :param dataframe: data to print
    :return: string with the tabulated table
    """
    return tabulate(dataframe, headers='keys', tablefmt='psql', showindex=False)


def get_habit_events_statistic(events: list[HabitEvent], periodicity: int) -> pd.DataFrame:
    """
    Give  a list of HabitEvents and the periodicity. Get statistic on the events. A new pandas.DataFrame is returned
    having the following columns:
    Longest | Last | Median | Mean | Total Streaks | Expected Streaks | Score
    :param events:
    :param periodicity:
    :return: Longest is the longest strike, Last is the last completed streak (or current one), Median is the
             median of the streaks, Average is the mean of the streaks, "Total Streaks" is the total number of streaks
             in the given events list, "Expected Streaks" is the maximum number of streaks in the date and time range,
             Score is the ratio between "Total Streaks" and "Expected Streaks" where 1 is a score of 100% and 0 is a
             score of 0%
    """
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
    """
    Given a list of Habits and its associated events calculate the statistic for each Habit using. This function is
    using internally get_habit_events_statistic
    :param habits_and_events: a list of tuple, the first element is the habit and the second element is a list of the
                              associated events to that habit
    :return: A pandas.DataFrame with the following columns:
        - "Habit ID": the habit id
        - "Task": the habit task
        - "Periodicity": the habit periodicity
        - "Last Streak": the streaks count for the latest streak
        - "Longest Streak": the longest streak ever for the habit
        - "Average Streak": the average of the streaks
        - "Expected Streaks": the maximum number of possible streaks
        - "Score": the score from 0% to 100%
    """
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
