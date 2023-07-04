import click


@click.group()
@click.option("--user-id", type=click.INT, help="user")
@click.option("--list", help="list all habits")
@click.option("--with-periodicity", type=click.INT, help="filter by periodicity")
def habit():
    pass


@click.command()
@click.option("--task", help="short description of the task")
@click.option("--periodicity", type=click.INT, help="periodicity in days")
def create(task: str, periodicity: int):
    pass


@click.command()
@click.option("--habit-id", type=click.INT, help="habit id to remove")
def delete():
    pass


@click.command()
@click.option("--habit-id", type=click.INT, help="habit id to remove")
def complete():
    pass


habit.add_command(create)
habit.add_command(delete)
habit.add_command(complete)
