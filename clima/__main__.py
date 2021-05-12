import click
import pandas as pd
import yaml

from . import __version__
from .graphics.bar_plots import bar_plot, barfrec_plot, all_weather_bar_plot
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

    barfrec_plot(df, station, "Cavok", bp_label="CAVOK", save_as="cavok")
    barfrec_plot(
        df,
        station,
        "Visibility",
        bp_label="Visibilidad reinante < 5000.0 m",
        save_as="visibility",
    )


@cli.command()
@click.argument("station", type=click.STRING)
def weather(station: str):
    columns = [
        "Year",
        "Month",
        "Day",
        "Hour",
        "Weather_intensity",
        "Weather_description",
        "Weather_precipitation",
        "Weather_obscuration",
    ]

    station = station.lower()
    df = pd.read_csv(f"data/{station}/{station}_metars.csv", usecols=columns)
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    #barfrec_plot(
    #    df,
    #    station,
    #    "Weather_description",
    #    weather="SH",
    #    bp_label="Chubascos de lluvia (SHRA)",
    #    save_as="shra",
    #)
    #barfrec_plot(
    #    df,
    #    station,
    #    "Weather_description",
    #    weather="TS",
    #    bp_label="Tormenta eléctrica (TS ó TSRA)",
    #    save_as="tsra",
    #)
    #barfrec_plot(
    #    df,
    #    station,
    #    "Weather_precipitation",
    #    weather="RA",
    #    bp_label="Lluvia (RA)",
    #    save_as="ra",
    #)
    #barfrec_plot(
    #    df,
    #    station,
    #    "Weather_precipitation",
    #    weather="DZ",
    #    bp_label="Llovizna (DZ)",
    #    save_as="dz",
    #)
    #barfrec_plot(
    #    df,
    #    station,
    #    "Weather_obscuration",
    #    weather="BR",
    #    bp_label="Neblina (BR)",
    #    save_as="br",
    #)
    #barfrec_plot(
    #    df,
    #    station,
    #    "Weather_obscuration",
    #    weather="FG",
    #    bp_label="Niebla (FG)",
    #    save_as="fg",
    #)
    bar_plot(df, station, "Weather_description", weather="TS", save_as="ts")
    bar_plot(df, station, "Weather_precipitation", weather="RA", save_as="ra")
    bar_plot(df, station, "Weather_obscuration", weather="BR", save_as="br")

@cli.command()
@click.argument("station", type=click.STRING)
def all_weather(station: str):
    columns = [
        "Year",
        "Month",
        "Day",
        "Weather_intensity",
        "Weather_description",
        "Weather_precipitation",
    ]

    station = station.lower()
    df = pd.read_csv(f"data/{station}/{station}_metars.csv", usecols=columns)
    
    all_weather_bar_plot(df, station)


@cli.command()
@click.argument("station", type=click.STRING)
def cloud_height(station: str):
    columns = [
        "Year",
        "Month",
        "Day",
        "Hour",
        "Sky_layer1_height",
        "Sky_layer2_height",
        "Sky_layer3_height",
        "Sky_layer4_height",
    ]

    station = station.lower()
    df = pd.read_csv(f"data/{station}/{station}_metars.csv", usecols=columns)
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    # barfrec_plot(df, station, "Sky_layer_height", bp_label="Techo de nubes", save_as="ceiling")
    bar_plot(df, station, "Sky_layer_height")


if __name__ == "__main__":
    cli()
