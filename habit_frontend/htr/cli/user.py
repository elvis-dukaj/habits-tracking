import click

from htr.cli.cli import cli
from htr.client.habit_tracker import HabitTrackerClient


@cli.group("user")
@click.pass_obj
def user(habit_tracker_client: HabitTrackerClient):
    pass


@user.command()
@click.pass_obj
@click.option("--username", prompt=True, help="Username")
def create(client: HabitTrackerClient, username: str):
    user_id = client.add_user(username)
    click.echo(f"User {username} created with id: {user_id}")


@user.command()
@click.pass_obj
@click.option("--user-id", prompt=True, help="Username")
def delete(habit_tracker_client: HabitTrackerClient, user_id: int):
    habit_tracker_client.delete_user(user_id)
    click.echo(f"User {user_id} deleted")


@user.command()
@click.pass_obj
@click.option("--username", prompt=True, help="user to login")
def login(habit_tracker_client: HabitTrackerClient, username: str):
    user_id = habit_tracker_client.login(username)
    click.echo(f"User {username} has user_id {user_id}")
