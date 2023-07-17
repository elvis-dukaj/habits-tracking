import datetime
from typing import Optional
import click
import plotext as plot

from htr.client.habit_tracker import HabitTrackerClient, HabitEvent


@click.group()
@click.option("--user-id", "user_id", type=click.INT, envvar="HABIT_TRACKER_USER_ID", help="filter by habit id")
@click.pass_obj
def streak(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.set_current_user_id(user_id)


def get_previous_month() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)


@streak.command()
@click.option("--with-habit-id", "habit_id", is_flag=False, type=click.INT, help="filter by habit id")
@click.pass_obj
# @click.option("--start-date", "start_date", is_flag=False, default=str(datetime.date.today()),
#               type=click.DateTime(formats=["%Y-%m-%d"]),
#               help="filter events from the start date")
# @click.option("--end-date", "end_date", is_flag=False,
#               type=click.DateTime(formats=["%Y-%m-%d"]),
#               default=str(get_previous_month()),
#               help="filter events from the start date")
def display(habit_tracker_client: HabitTrackerClient, habit_id: Optional[int]):
    habit_events: list[HabitEvent] = habit_tracker_client.list_habit_events(habit_id)
    click.echo(f"Found {len(habit_events)} events: {habit_events}")
    # # click.echo(f"with habit id {habit_id}, start_date: {start_date}, end_date: {end_date}")
    #
    # habits = ["brush teeth", "jogging", "reading book", "climbing"]
    # streaks = [3, 10, 1, 20]
    #
    # plot.simple_bar(habits, streaks, title="progress of current streaks")
    # plot.show()


@streak.command()
@click.option("--habit-id", required=True, type=click.INT, help="filter by habit id")
@click.pass_obj
def longest(habit_tracker_client: HabitTrackerClient, habit_id: int):
    click.echo(f"longest streak for {habit_id} is 2")
