import click

from htr.client.habit_tracker import HabitTrackerClient


@click.group()
@click.option("--endpoint", envvar="HABIT_TRACKER_ENDPOINT", default="http://localhost:8000", help="server endpoint")
@click.pass_context
def cli(ctx, endpoint: str):
    ctx.obj = HabitTrackerClient(endpoint)
