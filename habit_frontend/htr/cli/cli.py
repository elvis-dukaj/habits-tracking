import click
import os

from htr.cli.user import user
from htr.cli.habit import habit
from htr.cli.streak import streak


@click.group()
@click.option("--endpoint", envvar="HABIT_TRACKER_ENDPOINT", default="localhost:8080", help="server endpoint")
def cli(endpoint: str):
    click.echo(f"endpoint is {endpoint}")


cli.add_command(user)
cli.add_command(habit)
cli.add_command(streak)
