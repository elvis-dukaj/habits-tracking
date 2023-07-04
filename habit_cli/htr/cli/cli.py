import click

from htr.cli.user import user
from htr.cli.habit import habit
from htr.cli.streak import streak


@click.group()
@click.option("--endpoint", default="localhost:8000", help="server endpoint")
def cli(endpoint: str):
    click.echo("ciao")


cli.add_command(user)
cli.add_command(habit)
cli.add_command(streak)
