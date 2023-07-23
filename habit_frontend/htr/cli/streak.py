from typing import Optional
from tabulate import tabulate
import click
import plotext as plot

from htr.cli.cli import cli
from htr.client.habit_tracker import HabitTrackerClient
from htr.schemas.habit import Habit
from htr.schemas.habit_event import HabitEvent

from htr.analytics import (
    calculate_current_streak,
    calculate_streak_history,
    transform_to_panda_dataframe
)


@cli.group()
@click.option("--user-id", type=click.INT, envvar="HABIT_TRACKER_USER_ID", default=1,
              help="filter by habit id")
@click.pass_obj
def streak(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.set_current_user_id(user_id)


def calculate_all_streaks(habits: list[tuple[Habit, list[HabitEvent]]]) -> list[int]:
    streaks: list[int] = []

    for habit, events in habits:
        streaks.append(calculate_current_streak(events, habit.periodicity))

    return streaks


@streak.command()
@click.option("--with-habit-id", "habit_id", is_flag=False, type=click.INT, help="filter by habit id")
@click.pass_obj
def display(habit_tracker_client: HabitTrackerClient, habit_id: Optional[int]):
    if habit_id is not None:
        habit = habit_tracker_client.get_habit_by_id(habit_id)
        events: list[HabitEvent] = habit_tracker_client.list_habit_events(habit.habit_id)
        dataframe = transform_to_panda_dataframe(events, habit.periodicity)
        click.echo(tabulate(dataframe, headers='keys', tablefmt='psql'))
        return

    combined_habit_and_events: list[tuple[Habit, list[HabitEvent]]] = []

    habits = habit_tracker_client.list_habits()
    for habit in habits:
        events = habit_tracker_client.list_habit_events(habit.habit_id)
        combined = (habit, events)
        combined_habit_and_events.append(combined)

    tasks: list[str] = [habit.task for habit in habits]
    current_streak = calculate_all_streaks(combined_habit_and_events)

    plot.simple_bar(tasks, current_streak, title="progress of current streaks")
    plot.show()


@streak.command()
@click.option("--with-habit-id", "habit_id", type=click.INT, help="filter by habit id")
@click.pass_obj
def longest(habit_tracker_client: HabitTrackerClient, habit_id: Optional[int]):
    if habit_id is None:
        habit_id = 3

    habit = habit_tracker_client.get_habit_by_id(habit_id)
    events: list[HabitEvent] = habit_tracker_client.list_habit_events(habit.habit_id)
    streaks = calculate_streaks(events, habit.periodicity)

    calculate_streak_history(events, 3)
    click.echo(f"Habit {habit_id} has {streaks} streaks")
    return
