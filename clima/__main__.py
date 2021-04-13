import click

from . import __version__
from .graphics.resume_table import generate_table


@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo(f"{__version__}")

@cli.command()
@click.argument('station', type=click.STRING)
def resume_table(station: str):
    generate_table(station)

if __name__ == "__main__":
    cli()