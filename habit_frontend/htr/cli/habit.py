import datetime
import pandas
from tabulate import tabulate
import click
from typing import Optional

from htr.cli.cli import cli
from htr.client.habit_tracker import HabitTrackerClient, Habit, HabitEvent
from htr.analytics import transform_to_panda_dataframe, get_habit_events_statistic, tabulate_dataframe


@cli.group()
@click.option("--user-id", "user_id", envvar="HABIT_TRACKER_USER_ID", type=click.INT, help="user", required=True)
@click.pass_obj
def habit(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.set_current_user_id(user_id)


@habit.command("list")
@click.option("--with-periodicity", "periodicity", required=False, type=click.INT, help="filter by periodicity")
@click.pass_obj
def list_habits(habit_tracker_client: HabitTrackerClient, periodicity: Optional[int] = None):
    habits: list[Habit] = habit_tracker_client.list_habits(periodicity)
    if len(habits) == 0:
        click.echo("No habits found")
        return

    df = pandas.DataFrame.from_records([dict(h) for h in habits])
    click.echo(tabulate(df, headers='keys', tablefmt='psql'))


@habit.command()
@click.option("--task", prompt=True, help="short description of the task")
@click.option("--periodicity", prompt=True, type=click.INT, help="periodicity in days")
@click.pass_obj
def create(habit_tracker_client: HabitTrackerClient, task: str, periodicity: int):
    habit_id = habit_tracker_client.create_habit(task, periodicity)
    click.echo(f"Habit {task} created with id {habit_id}")


@habit.command()
@click.option("--habit-id", required=True, type=click.INT, help="habit id to remove")
@click.pass_obj
def delete(habit_tracker_client: HabitTrackerClient, habit_id: int):
    habit_tracker_client.delete_habit(habit_id)
    click.echo(f"Habit '{habit_id}' deleted")


@habit.command()
@click.option("--habit-id", envvar="HABIT_TRACKER_HABIT_ID", prompt=True, required=True, type=click.INT,
              help="habit id to remove")
@click.option("--completed-date", "completed_date", required=True, prompt=True,
              type=click.DateTime(formats=["%Y-%m-%d"]),
              help="habit to mark as completed")
@click.pass_obj
def complete(habit_tracker_client: HabitTrackerClient, habit_id: int, completed_date: datetime.datetime):
    habit_tracker_client.mark_habit_completed(habit_id, completed_date.date())
    requested_habit = habit_tracker_client.get_habit_by_id(habit_id)
    click.echo(f"Habit '{requested_habit.task}' completed")


@habit.command()
@click.option("--habit-id", envvar="HABIT_TRACKER_HABIT_ID", prompt=True, required=True, type=click.INT,
              help="habit to view")
@click.pass_obj
def view(habit_tracker_client: HabitTrackerClient, habit_id: int):
    hbt = habit_tracker_client.get_habit_by_id(habit_id)
    click.echo(tabulate(hbt))


@habit.command()
@click.option("--habit-id", envvar="HABIT_TRACKER_HABIT_ID", prompt=True, required=True, type=click.INT,
              help="habit to view")
@click.pass_obj
def history(habit_tracker_client: HabitTrackerClient, habit_id: int):
    hbt = habit_tracker_client.get_habit_by_id(habit_id)
    events: list[HabitEvent] = habit_tracker_client.list_habit_events(hbt.habit_id)
    dataframe = transform_to_panda_dataframe(events, hbt.periodicity)

    if len(dataframe.index) == 0:
        click.echo("No data registered")
        return

    click.echo(tabulate_dataframe(dataframe))


@habit.command()
@click.option("--habit-id", envvar="HABIT_TRACKER_HABIT_ID", prompt=True, required=True, type=click.INT,
              help="habit to view")
@click.pass_obj
def statistic(habit_tracker_client: HabitTrackerClient, habit_id: int):
    hbt = habit_tracker_client.get_habit_by_id(habit_id)
    events: list[HabitEvent] = habit_tracker_client.list_habit_events(hbt.habit_id)
    dataframe = transform_to_panda_dataframe(events, hbt.periodicity)

    if len(dataframe.index) == 0:
        click.echo("No data registered")
        return

    click.echo(tabulate_dataframe(get_habit_events_statistic(dataframe)))
