import click
import pandas as pd
import yaml

from . import __version__
from .graphics.bar_plots import bar_plot
from .graphics.contour_map import contour_map
from .graphics.resume_table import generate_table
from .graphics.time_series import single_time_series, time_series
from .graphics.wind_direction import heat_map

f = open("logging.log", "w")
f.close()

config_file = open("plot.config.yaml")
PLOT_CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)
config_file.close()


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
    config = PLOT_CONFIG[station][columns[-1].lower()]

    station = station.lower()
    df = pd.read_csv(f"data/{station}/{station}_metars.csv", usecols=columns)
    df["Hour1_24"] = df["Hour"].replace(0, 24)
    label = "Dirección del viento (°)"

    heat_map(df, station)
    contour_map(
        df,
        station,
        columns[-1],
        cbar_label=label,
        save_as=columns[-1].lower(),
        config=config["contour_map"],
    )
    time_series(
        df,
        station,
        columns[-1],
        yaxis_label=label,
        save_as=columns[-1].lower(),
        config=config["time_series"],
    )
    single_time_series(df, columns[-1], yaxis_label=label, save_as=columns[-1].lower())


@cli.command()
@click.argument("station", type=click.STRING)
def wind_speed(station: str):
    columns = ["Month", "Day", "Hour", "Wind_speed"]
    config = PLOT_CONFIG[station][columns[-1].lower()]

    station = station.lower()
    df = pd.read_csv(f"data/{station}/{station}_metars.csv", usecols=columns)
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    contour_map(
        df,
        station,
        columns[-1],
        cbar_label="Velocidad del viento (kt)",
        save_as=columns[-1].lower(),
        config=config["contour_map"],
    )
    time_series(
        df,
        station,
        columns[-1],
        yaxis_label="Velocidad del viento (kt)",
        save_as=columns[-1].lower(),
        config=config["time_series"],
    )


@cli.command()
@click.argument("station", type=click.STRING)
def visibility(station: str):
    columns = ["Year", "Month", "Day", "Hour", "Visibility", "Cavok"]

    station = station.lower()
    df = pd.read_csv(f"data/{station}/{station}_metars.csv", usecols=columns)
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    bar_plot(df, station, "Cavok")
    bar_plot(df, station, "Visibility")


@cli.command()
@click.argument("station", type=click.STRING)
def weather(station: str):
    columns = [
        "Year",
        "Month",
        "Day",
        "Hour",
        "Weather_description",
        "Weather_precipitation",
        "Weather_obscuration",
    ]

    station = station.lower()
    df = pd.read_csv(f"data/{station}/{station}_metars.csv", usecols=columns)
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    bar_plot(df, station, "Weather_description", weather="SH")
    bar_plot(df, station, "Weather_precipitation", weather="RA")
    bar_plot(df, station, "Weather_obscuration", weather="BR")


if __name__ == "__main__":
    cli()
