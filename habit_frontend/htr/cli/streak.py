import datetime
from typing import Optional
import click
import plotext as plot
from operator import attrgetter

from htr.client.habit_tracker import HabitTrackerClient, Habit, HabitEvent


@click.group()
@click.option("--user-id", "user_id", type=click.INT, envvar="HABIT_TRACKER_USER_ID", default=1,
              help="filter by habit id")
@click.pass_obj
def streak(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.set_current_user_id(user_id)


def get_previous_month() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)


def order_events_by_completed_date(events: list[HabitEvent]) -> list[HabitEvent]:
    return events


def calculate_streaks(events: list[HabitEvent], periodicity: int):
    events.sort(key=attrgetter("completed_at"), reverse=True)
    print(f"after ordering {events}")
    streaks: int = 0

    for current, previous in zip(events[0::2], events[1::2]):
        print(f"current is {current}, previous is {previous}")
        delta = current.completed_at - previous.completed_at

        if delta.days <= periodicity:
            streaks += 1

    return streaks


def calculate_all_streaks(events: list[HabitEvent], periodicity: int) -> int:
    ordered_events = order_events_by_completed_date(events)
    print(f"after ordering {events}")
    streaks: int = 0

    for current, previous in zip(ordered_events[0::2], ordered_events[1::2]):
        delta = current.completed_at - previous.completed_at

        if delta.days <= periodicity:
            streaks += 1

    return streaks


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

    habits = habit_tracker_client.list_habits_by_user_id()
    streaks: list[int] = []

    for habit in habits:
        events_for_habit = habit_tracker_client.list_habit_events(habit.habit_id)
        streaks.append(calculate_all_streaks(events_for_habit, habit.periodicity))

    habit_events: list[HabitEvent] = habit_tracker_client.list_habit_events(habit_id)
    click.echo(f"Found {len(habit_events)} events: {habit_events}")

    habits = ["brush teeth", "jogging", "reading book", "climbing"]
    streaks = [3, 10, 1, 20]

    plot.simple_bar(habits, streaks, title="progress of current streaks")
    plot.show()


@streak.command()
@click.option("--habit-id", required=True, type=click.INT, help="filter by habit id")
@click.pass_obj
def longest(habit_tracker_client: HabitTrackerClient, habit_id: int):
    click.echo(f"longest streak for {habit_id} is 2")
