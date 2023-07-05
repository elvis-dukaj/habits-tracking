import datetime
from typing import Optional
import click
import plotext as plot


@click.group()
@click.option("--user-id", "user_id", type=click.INT, help="filter by habit id")
# @click.option("--habit-id", "habit_id", type=click.INT, help="filter by habit id")
# @click.option("--show-progress", "show_progress", is_flag=True, help="filter by habit id")
# @click.option("--start-date", type=click.DateTime, default=datetime., help="filter events from the start date")
# @click.option("--end-date", type=click.DateTime, help="filter events from the start date")
def streak(user_id: int):
    click.echo(f"streak for user {user_id}")


def get_previous_month() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)


@streak.command()
@click.option("--with-habit-id", "habit_id", is_flag=False, type=click.INT, help="filter by habit id")
@click.option("--start-date", "start_date", is_flag=False, default=str(datetime.date.today()),
              type=click.DateTime(formats=["%Y-%m-%d"]),
              help="filter events from the start date")
@click.option("--end-date", "end_date", is_flag=False,
              type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(get_previous_month()),
              help="filter events from the start date")
def display(habit_id: Optional[int], start_date: Optional[datetime.date], end_date: Optional[datetime.date]):
    click.echo(f"with habit id {habit_id}, start_date: {start_date}, end_date: {end_date}")

    habits = ["brush teeth", "jogging", "reading book", "climbing"]
    streaks = [3, 10, 1, 20]

    plot.simple_bar(habits, streaks, title="progress of current streaks")
    plot.show()


@streak.command()
@click.option("--habit-id", required=True, type=click.INT, help="filter by habit id")
def longest(habit_id: int):
    click.echo(f"longest streak for {habit_id} is 2")
