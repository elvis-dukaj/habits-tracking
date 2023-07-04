import click


@click.group()
def user():
    pass


@click.command()
def create(username: str, email: str):
    pass


@click.command()
def delete(username: str, email: str):
    pass


@click.command()
@click.option("--username", help="user to login")
def login(username: str):
    user_id = 1
    click.echo(f"user id: {user_id}")


user.add_command(create)
user.add_command(delete)
user.add_command(login)
