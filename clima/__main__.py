import click
import pandas as pd
import yaml

from . import __version__
from .graphics.bar_plots import (
    all_weather_bar_plot,
    bar_plot,
    barfrec_plot,
    gusts_bar_plot,
)
from .graphics.contour_map import contour_map
from .graphics.resume_table import generate_table
from .graphics.time_series import single_time_series, time_series
from .graphics.wind_direction import heat_map

f = open("logging.log", "w")
f.close()


@click.group()
@click.argument("station", type=click.STRING)
@click.pass_context
def cli(ctx, station: str):
    config_file = open("plot.config.yaml")
    plot_config = yaml.load(config_file, Loader=yaml.FullLoader)
    config_file.close()

    df = pd.read_csv(f"data/{station}/{station}_metars.csv")
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    ctx.obj = {
        "plot_config": plot_config,
        "station": station.lower(),
        "data": df,
    }


@cli.command()
def version():
    click.echo(f"{__version__}")


@cli.command()
@click.pass_context
def resume_table(ctx):
    station = ctx.obj["station"]
    generate_table(station)


@cli.command()
@click.pass_context
def wind_direction(ctx):
    station = ctx.obj["station"]
    columns = ["Month", "Day", "Hour", "Hour1_24", "Wind_direction"]

    config = ctx.obj["plot_config"]
    config = config[station][columns[-1].lower()]

    df = ctx.obj["data"][columns]
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
@click.pass_context
def wind_speed(ctx):
    station = ctx.obj["station"]
    columns = ["Month", "Day", "Hour", "Hour1_24", "Wind_speed"]

    config = ctx.obj["plot_config"]
    config = config[station][columns[-1].lower()]

    df = ctx.obj["data"][columns]
    label = "Velocidad del viento (kt)"

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
@click.pass_context
def wind_gust(ctx):
    station = ctx.obj["station"]
    columns = ["Year", "Month", "Day", "Hour", "Hour1_24", "Wind_gust"]

    config = ctx.obj["plot_config"]
    config = config[station][columns[-1].lower()]

    df = ctx.obj["data"][columns]
    label = "Ráfagas de viento (kt)"

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
    gusts_bar_plot(df)


@cli.command()
@click.pass_context
def temperature(ctx):
    station = ctx.obj["station"]
    columns = ["Month", "Day", "Hour", "Hour1_24", "Temperature"]

    config = ctx.obj["plot_config"]
    config = config[station][columns[-1].lower()]

    df = ctx.obj["data"][columns]
    label = "Temperatura absoluta (°C)"

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
@click.pass_context
def dewpoint(ctx):
    station = ctx.obj["station"]
    columns = ["Month", "Day", "Hour", "Hour1_24", "Dewpoint"]

    config = ctx.obj["plot_config"]
    config = config[station][columns[-1].lower()]

    df = ctx.obj["data"][columns]
    label = "Temperatura del punto rocío (°C)"

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
@click.pass_context
def pressure(ctx):
    station = ctx.obj["station"]
    columns = ["Month", "Day", "Hour", "Hour1_24", "Pressure"]

    config = ctx.obj["plot_config"]
    config = config[station][columns[-1].lower()]

    df = ctx.obj["data"][columns]
    label = "Presión atmosférica (inHg)"

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
@click.pass_context
def visibility(ctx):
    station = ctx.obj["station"]
    columns = ["Year", "Month", "Day", "Hour", "Hour1_24", "Visibility", "Cavok"]

    df = ctx.obj["data"][columns]

    barfrec_plot(df, station, "Cavok", bp_label="CAVOK", save_as="cavok")
    barfrec_plot(
        df,
        station,
        "Visibility",
        bp_label="Visibilidad reinante < 5000.0 m",
        save_as="visibility",
    )
    bar_plot(df, station, "Cavok", save_as="cavok")
    bar_plot(df, station, "Visibility", save_as="visibility")


@cli.command()
@click.pass_context
def weather(ctx):
    station = ctx.obj["station"]
    columns = [
        "Year",
        "Month",
        "Day",
        "Hour",
        "Hour1_24",
        "Weather_intensity",
        "Weather_description",
        "Weather_precipitation",
        "Weather_obscuration",
    ]

    df = ctx.obj["data"][columns]

    barfrec_plot(
        df,
        station,
        "Weather_description",
        weather="SH",
        bp_label="Chubascos de lluvia (SHRA)",
        save_as="shra",
    )
    barfrec_plot(
        df,
        station,
        "Weather_description",
        weather="TS",
        bp_label="Tormenta eléctrica (TS ó TSRA)",
        save_as="tsra",
    )
    barfrec_plot(
        df,
        station,
        "Weather_precipitation",
        weather="RA",
        bp_label="Lluvia (RA)",
        save_as="ra",
    )
    barfrec_plot(
        df,
        station,
        "Weather_precipitation",
        weather="DZ",
        bp_label="Llovizna (DZ)",
        save_as="dz",
    )
    barfrec_plot(
        df,
        station,
        "Weather_obscuration",
        weather="BR",
        bp_label="Neblina (BR)",
        save_as="br",
    )
    barfrec_plot(
        df,
        station,
        "Weather_obscuration",
        weather="FG",
        bp_label="Niebla (FG)",
        save_as="fg",
    )
    bar_plot(df, station, "Weather_description", weather="SH", save_as="sh")
    bar_plot(df, station, "Weather_description", weather="TS", save_as="ts")
    bar_plot(df, station, "Weather_precipitation", weather="RA", save_as="ra")
    bar_plot(df, station, "Weather_precipitation", weather="DZ", save_as="dz")
    bar_plot(df, station, "Weather_obscuration", weather="FG", save_as="fg")
    bar_plot(df, station, "Weather_obscuration", weather="BR", save_as="br")

    all_weather_bar_plot(df)


@cli.command()
@click.pass_context
def ceiling(ctx):
    station = ctx.obj["station"]
    columns = [
        "Year",
        "Month",
        "Day",
        "Hour",
        "Hour1_24",
        "Sky_layer1_height",
        "Sky_layer2_height",
        "Sky_layer3_height",
        "Sky_layer4_height",
    ]

    df = ctx.obj["data"][columns]

    barfrec_plot(
        df,
        station,
        "Sky_layer_height",
        bp_label="Techo de nubes < 1500 ft",
        save_as="ceiling",
    )
    bar_plot(df, station, "Sky_layer_height", save_as="ceiling")


if __name__ == "__main__":
    cli()
