import click


@click.group()
def user():
    pass


@user.command()
@click.option("--username", prompt=True, help="Username")
def create(username: str):
    click.echo(f"username {username} created with id 1")


@user.command()
@click.option("--user-id", prompt=True, help="Username")
def delete(user_id: int):
    click.echo(f"Deleting user {user_id}")


@user.command()
@click.option("--username", prompt=True, help="user to login")
def login(username: str):
    user_id = 1
    click.echo(f"user id: {user_id}")
