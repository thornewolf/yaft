import click
from sqlmodel import Session, select

from . import db, models


@click.group()
def cli():
    pass


@cli.command()
def hello():
    click.echo("Hello World!")


@cli.command()
@click.option("--count", default=1, help="Number of times to greet.")
@click.argument("name")
def greet(count, name):
    for _ in range(count):
        click.echo(f"Hello, {name}!")


@cli.command()
def add_users():
    click.echo("Adding users")
    with Session(db.engine) as session:
        user_1 = models.User(username="john", email="", hashed_password="123456")
        user_2 = models.User(username="mary", email="", hashed_password="654321")
        session.add(user_1)
        session.add(user_2)
        session.commit()


@cli.command()
def list_users():
    click.echo("Listing users")
    with Session(db.engine) as session:
        statement = select(models.User)
        users = session.exec(statement)
        for user in users:
            click.echo(f"{user.id} - {user.username} - {user.email} - {user}")


if __name__ == "__main__":
    db.create_db_and_tables()
    cli()
