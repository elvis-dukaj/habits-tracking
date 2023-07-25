from typing import Optional

import pandas
import click
import pandas as pd

from htr.cli.cli import cli as htr_cli
from htr.client.habit_tracker import HabitTrackerClient
from htr.schemas.habit import Habit
from htr.schemas.habit_event import HabitEvent

from htr.analytics import transform_to_panda_dataframe, get_habit_events_statistic, tabulate_dataframe


@htr_cli.group()
@click.option("--user-id", type=click.INT, envvar="HABIT_TRACKER_USER_ID", help="filter by habit id")
@click.pass_obj
def statistic(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.set_current_user_id(user_id)


@statistic.command(name="all")
@click.option("--order-by", type=click.Choice(['habit', 'current', 'longest', 'mean', 'periodicity']), default='habit')
@click.option("--ascending", is_flag=True, default=True)
@click.pass_obj
def show_all(habit_tracker_client: HabitTrackerClient, order_by: str, ascending: bool):
    habits = habit_tracker_client.list_habits()

    habit_id_series = pandas.Series([habit.habit_id for habit in habits], name="habit id")
    tasks = pandas.Series([habit.task for habit in habits], name="Task")
    periodicities = pandas.Series([habit.periodicity for habit in habits], name="Periodicity")

    current_streaks_list: list[int] = []
    longest_streaks_list: list[int] = []
    average_streaks_list: list[float] = []

    for habit in habits:
        events = habit_tracker_client.list_habit_events(habit.habit_id)
        if len(events) > 0:
            df = transform_to_panda_dataframe(events, habit.habit_id)
            stat = get_habit_events_statistic(df)
            current_streaks_list.append(stat['Last'][stat.last_valid_index()])
            longest_streaks_list.append(stat['Longest'][stat.last_valid_index()])
            average_streaks_list.append(stat['Mean'][stat.last_valid_index()])
        else:
            current_streaks_list.append(0)
            longest_streaks_list.append(0)
            average_streaks_list.append(0)

    current_streaks: pandas.Series = pandas.Series(current_streaks_list)
    longest_streaks: pandas.Series = pandas.Series(longest_streaks_list)
    average_streaks: pandas.Series = pandas.Series(average_streaks_list)

    df = pandas.DataFrame({
        "Habit ID": habit_id_series,
        "Task": tasks,
        "Periodicity": periodicities,
        "Current Streak": current_streaks,
        "Longest Streak": longest_streaks,
        "Average Streak": average_streaks,
    })

    if order_by == 'current':
        click.echo(tabulate_dataframe(df.sort_values(by=['Current Streak'], ascending=ascending)))

    if order_by == 'longest':
        click.echo(tabulate_dataframe(df.sort_values(by=['Longest Streak'], ascending=ascending)))

    if order_by == 'mean':
        click.echo(tabulate_dataframe(df.sort_values(by=['Average Streak'], ascending=ascending)))

    if order_by == 'periodicity':
        click.echo(tabulate_dataframe(df.sort_values(by=['Periodicity'], ascending=ascending)))

    if order_by == 'habit':
        click.echo(tabulate_dataframe(df.sort_values(by=['Habit ID'], ascending=ascending)))
