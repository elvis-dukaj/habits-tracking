import click


@click.group()
@click.option("--user-id", "user_id", type=click.INT, help="user")
def habit(user_id: int):
    click.echo("habit group")


@habit.command()
@click.option("--with-periodicity", "periodicity", is_flag=False, type=click.INT,
              help="filter by periodicity")
def list(periodicity: int):
    click.echo(f"listening parameters with periodicity {periodicity}")


@habit.command()
@click.option("--task", help="short description of the task")
@click.option("--periodicity", type=click.INT, help="periodicity in days")
def create(task: str, periodicity: int):
    click.echo("create new habit")


@habit.command()
@click.option("--habit-id", type=click.INT, help="habit id to remove")
def delete():
    click.echo("delete new habit")


@habit.command()
@click.option("--habit-id", type=click.INT, help="habit id to remove")
def complete(habit_id: int):
    click.echo(f"complete new habit {habit_id}")


