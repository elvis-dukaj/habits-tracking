import click
import os

from htr.client.habit_tracker import HabitTrackerClient
from htr.cli.user import user
from htr.cli.habit import habit
from htr.cli.streak import streak


@click.group()
@click.option("--endpoint", envvar="HABIT_TRACKER_ENDPOINT", default="http://localhost:8000", help="server endpoint")
@click.pass_context
def cli(ctx, endpoint: str):
    ctx.obj = HabitTrackerClient(endpoint)
    click.echo(f"endpoint is {endpoint}")


cli.add_command(user)
cli.add_command(habit)
cli.add_command(streak)
