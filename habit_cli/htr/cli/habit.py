import click


@click.group()
@click.option("--user-id", "user_id", type=click.INT, help="user")
def habit(user_id: int):
    click.echo("habit group")


@habit.command()
@click.option("--with-periodicity", "periodicity", type=click.INT,
              help="filter by periodicity")
def list(periodicity: int):
    habits = {
        0: {
            "task": "drink water",
            "description": "",
            "periodicity": 1
        },
        1: {
            "task": "bouldering",
            "description": "",
            "periodicity": 7
        },
        2: {
            "task": "read a book",
            "description": "",
            "periodicity": 7
        },
        3: {
            "task": "study german",
            "description": "",
            "periodicity": 1
        }
    }

    # print(tabulate(habits_id_list))
    click.echo(f"listening parameters with periodicity {periodicity}:\n{habits}")


@habit.command()
@click.option("--task", prompt=True, help="short description of the task")
@click.option("--description", prompt=True, help="short description of the task")
@click.option("--periodicity", prompt=True, type=click.INT, help="periodicity in days")
def create(task: str, description: str, periodicity: int):
    click.echo(f"create new habit: task {task}, description: {description}, periodicity: {periodicity}")


@habit.command()
@click.option("--habit-id", required=True, type=click.INT, help="habit id to remove")
def delete(habit_id: int):
    click.echo(f"delete new habit {habit_id}")


@habit.command()
@click.option("--habit-id", required=True, type=click.INT, help="habit id to remove")
def complete(habit_id: int):
    click.echo(f"complete new habit {habit_id}")
