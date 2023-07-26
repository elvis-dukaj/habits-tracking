import click

from htr.cli.cli import cli as htr_cli
from htr.client.habit_tracker import HabitTrackerClient
from htr.schemas import Habit, HabitEvent
from htr.analytics import tabulate_dataframe, calculate_statistic


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
    habits_and_events: list[tuple[Habit, list[HabitEvent]]] = []
    habits = habit_tracker_client.list_habits()

    for habit in habits:
        events = habit_tracker_client.list_habit_events(habit.habit_id)
        habits_and_events.append((habit, events))

    df = calculate_statistic(habits_and_events)

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
