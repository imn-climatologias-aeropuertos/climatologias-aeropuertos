import click
import pandas as pd

from . import __version__
from .graphics.contour_map import contour_map
from .graphics.resume_table import generate_table
from .graphics.time_series import single_time_series, time_series
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
    label = "Dirección del viento (°)"

    # heat_map(df, station)
    # contour_map(
    #     df,
    #     station,
    #     columns[-1],
    #     v_max=260,
    #     v_min=60,
    #     cbar_label=label,
    #     save_as=columns[-1].lower(),
    # )
    # time_series(
    #     df,
    #     station,
    #     columns[-1],
    #     v_min=50,
    #     yaxis_label=label,
    #     save_as=columns[-1].lower(),
    # )
    single_time_series(df, columns[-1], yaxis_label=label, save_as=columns[-1].lower())


@cli.command()
@click.argument("station", type=click.STRING)
def wind_speed(station: str):
    columns = ["Month", "Day", "Hour", "Wind_speed"]

    station = station.lower()
    data = pd.read_csv(f"data/{station}/{station}_metars.csv")
    df = data[columns]
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    # contour_map(
    #     df,
    #     station,
    #     columns[-1],
    #     v_max=18,
    #     v_min=2,
    #     cbar_ticks_num=10,
    #     cbar_label="Velocidad del viento (kt)",
    #     save_as=columns[-1].lower(),
    # )
    time_series(
        df,
        station,
        columns[-1],
        v_min=0,
        v_max=15,
        ytick_jump=3,
        hline=(),
        yaxis_label="Velocidad del viento (kt)",
        save_as=columns[-1].lower(),
    )


if __name__ == "__main__":
    cli()
