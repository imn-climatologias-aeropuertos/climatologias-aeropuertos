import click
import pandas as pd

from . import __version__
from .graphics.resume_table import generate_table
from .graphics.wind_direction import heat_map

f = open("logging.log", "w")
f.close()


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo(f"{__version__}")


@cli.command()
@click.argument("station", type=click.STRING)
def resume_table(station: str):
    station = station.lower()
    generate_table(station)


@cli.command()
@click.argument("station", type=click.STRING)
def wind_direction(station: str):
    station = station.lower()
    data = pd.read_csv(f"data/{station}/{station}_metars.csv")

    heat_map(data, station)


if __name__ == "__main__":
    cli()
