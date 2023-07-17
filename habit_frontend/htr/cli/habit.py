import datetime

import click

from htr.client.habit_tracker import HabitTrackerClient, Habit


@click.group()
@click.option("--user-id", "user_id", envvar="HABIT_TRACKER_USER_ID", type=click.INT, help="user")
@click.pass_obj
def habit(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.set_current_user_id(user_id)


@habit.command()
@click.option("--with-periodicity", "periodicity", type=click.INT, help="filter by periodicity")
@click.pass_obj
def list(habit_tracker_client: HabitTrackerClient, periodicity: int):
    habits: list[Habit] = habit_tracker_client.list_habits_by_periodicity(periodicity)
    if len(habits) == 0:
        click.echo("No habits found")
        return

    click.echo(f"Found {len(habits)} habits: \n")
    for habit_response in habits:
        click.echo(f" habit[{habit_response.habit_id}] ")
        click.echo(f"  user_id: {habit_response.user_id}")
        click.echo(f"  task: '{habit_response.task}'")
        click.echo(f"  periodicity: {habit_response.periodicity}\n")


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
    click.echo(f"habit {habit_id} was deleted")


@habit.command()
@click.option("--habit-id", required=True, type=click.INT, help="habit id to remove")
@click.option("--completed-date", "completed_date", required=True, type=click.DateTime(),
              help="habit id to remove")
@click.pass_obj
def complete(habit_tracker_client: HabitTrackerClient, habit_id: int, completed_date: datetime.datetime):
    habit_tracker_client.mark_habit_completed(habit_id, completed_date.date())
    click.echo(f"habit {habit_id} was marked as completed")
