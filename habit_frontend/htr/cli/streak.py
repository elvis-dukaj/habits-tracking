import datetime
from typing import Optional
import click
import plotext as plot
from operator import attrgetter
from collections import deque
from itertools import islice

from htr.cli.cli import cli
from htr.client.habit_tracker import HabitTrackerClient, Habit, HabitEvent


@cli.group()
@click.option("--user-id", "user_id", type=click.INT, envvar="HABIT_TRACKER_USER_ID", default=1,
              help="filter by habit id")
@click.pass_obj
def streak(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.set_current_user_id(user_id)


def sliding_window_iter(iterable, size):
    iterable = iter(iterable)
    window = deque(islice(iterable, size), maxlen=size)
    for item in iterable:
        yield tuple(window)
        window.append(item)
    if window:
        yield tuple(window)


def calculate_streaks(events: list[HabitEvent], periodicity: int):
    events.sort(key=attrgetter("completed_at"), reverse=True)
    streaks: int = 0

    for window in sliding_window_iter(events, 2):
        current = window[0]
        previous = window[1]

        delta: datetime.timedelta = current.completed_at - previous.completed_at
        delta_in_days: int = delta.days

        if delta_in_days <= periodicity:
            streaks += 1
        else:
            break

    return streaks


def calculate_all_streaks(habits: list[tuple[Habit, list[HabitEvent]]]) -> tuple[list[str], list[int]]:
    tasks: list[str] = [habit.task for habit, events in habits]
    streaks: list[int] = []

    for habit, events in habits:
        streaks.append(calculate_streaks(events, habit.periodicity))

    return tasks, streaks


@streak.command()
@click.option("--with-habit-id", "habit_id", is_flag=False, type=click.INT, help="filter by habit id")
@click.pass_obj
def display(habit_tracker_client: HabitTrackerClient, habit_id: Optional[int]):
    if habit_id is not None:
        habit = habit_tracker_client.get_habit_by_id(habit_id)
        events: list[HabitEvent] = habit_tracker_client.list_habit_events(habit.habit_id)
        streaks = calculate_streaks(events, habit.periodicity)
        click.echo(f"Habit {habit_id} has {streaks} streaks")
        return

    combined_habit_and_events: list[tuple[Habit, list[HabitEvent]]] = []

    habits = habit_tracker_client.list_habits()
    for habit in habits:
        events = habit_tracker_client.list_habit_events(habit.habit_id)
        combined_habit_and_events.append((habit, events))

    histogram = calculate_all_streaks(combined_habit_and_events)

    plot.simple_bar(histogram[0], histogram[1], title="progress of current streaks")
    plot.show()


@streak.command()
@click.option("--habit-id", required=True, type=click.INT, help="filter by habit id")
@click.pass_obj
def longest(habit_tracker_client: HabitTrackerClient, habit_id: int):
    click.echo(f"longest streak for {habit_id} is 2")
