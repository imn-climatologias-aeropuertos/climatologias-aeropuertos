import click
import pandas as pd

from . import __version__
from .graphics.contour_map import contour_map
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
    columns = ["Month", "Day", "Hour", "Wind_direction"]

    station = station.lower()
    data = pd.read_csv(f"data/{station}/{station}_metars.csv")
    df = data[columns]
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    heat_map(df, station)
    contour_map(
        df,
        station,
        columns[-1],
        v_max=260,
        v_min=60,
        cbar_label="Dirección del viento (°)",
        save_as=columns[-1].lower(),
    )


if __name__ == "__main__":
    cli()
