from typing import Optional
import click
import plotext as plot


@click.command()
@click.option("--user-id", "user_id", type=click.INT, help="filter by habit id")
@click.option("--habit-id", "habit_id", type=click.INT, help="filter by habit id")
@click.option("--show-progress", "show_progress", is_flag=True, help="filter by habit id")
# @click.option("--start-date", type=click.DateTime, default=datetime., help="filter events from the start date")
# @click.option("--end-date", type=click.DateTime, help="filter events from the start date")
def streak(user_id: int, habit_id: int, show_progress: Optional[bool]):
    if show_progress:
        display_progress()

    click.echo(f"streak for user {user_id}")


# @streak.command()
# @click.option("--habit-id", "habit_id", is_flag=False, type=click.INT, help="filter by habit id")
def display_progress():
    habits = ["brush teeth", "jogging", "reading book", "climbing"]
    streaks = [3, 10, 1, 20]

    plot.simple_bar(habits, streaks, title="progress of current streaks")
    plot.show()
#
#
# @click.command()
# @click.option("--habit-id", type=click.INT, help="filter by habit id")
# def longest(habit_id: int):
#     pass
