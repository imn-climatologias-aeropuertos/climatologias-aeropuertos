from decimal import ROUND_HALF_UP, Decimal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from clima.graphics import DAYS_PER_MONTH, MONTHS, hours_range, local_time_list
from clima.logger_model import logger

time_ranges = {19: 9, 13: 6, 24: 12}


def _handle_cavok(df: pd.DataFrame, hrange: int):
    day_sum = df["Cavok"].sum()

    if day_sum >= time_ranges[hrange]:
        return 1

    return 0


def _handle_visibility(df: pd.DataFrame):
    unique_vals = df["Visibility"].unique()
    ocurrences = np.count_nonzero(unique_vals <= 5000.0)

    if ocurrences > 0:
        return 1

    return 0


def _handle_cloud(df: pd.DataFrame):
    ocurrences = np.count_nonzero(
        df[
            [
                "Sky_layer1_height",
                "Sky_layer2_height",
                "Sky_layer3_height",
                "Sky_layer4_height",
            ]
        ]
        <= 1500.0
    )

    if ocurrences > 5:
        return 1

    return 0


def _handle_weather(df: pd.DataFrame, variable: str, weather: str):
    df = df.query('Weather_intensity != "VC"')
    
    if weather == "RA":
        df = df.query('Weather_description != "SH" and Weather_description != "TS"')

    if weather == "FG":
        df = df.query('Weather_intensity != "VC"')

    ocurrences = np.count_nonzero(df[variable] == weather)

    if ocurrences > 0:
        return 1

    return 0


def barfrec_plot(
    df: pd.DataFrame,
    station: str,
    variable: str,
    weather="",
    bp_label="",
    save_as="",
):
    years = df["Year"].unique()
    months = np.arange(1, 13)
    month_means = np.arange(12)
    hrange = len(hours_range(station))

    logger.info(
        f"Getting the monthly DataFrames for bar-frecuencies plot, variable: {variable}."
    )
    for month in months:
        month_sum = 0

        logger.info(
            f"Getting the yearly DataFrames for bar-frecuencies plot, variable: {variable}."
        )
        for year in years:
            month_df = df.query(f"Year == {year} and Month == {month}")

            logger.info(
                f"Getting the dayly DataFrames for bar-frecuencies plot, variable: {variable}, and calculating the means."
            )
            for day in DAYS_PER_MONTH[month]:
                day_df = month_df.query(f"Day == {day}")

                if variable == "Cavok":
                    month_sum += _handle_cavok(day_df, hrange)
                elif variable == "Visibility":
                    month_sum += _handle_visibility(day_df)
                elif "Sky_layer" in variable:
                    month_sum += _handle_cloud(day_df)
                else:
                    month_sum += _handle_weather(day_df, variable, weather)

        month_means[month - 1] = Decimal(month_sum / len(years)).quantize(
            Decimal("1."), ROUND_HALF_UP
        )
    frecs = 100 * month_means / len(DAYS_PER_MONTH[month])
    print(month_means, frecs)

    sns.set()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(
        x=months - 1, y=month_means, color="royalblue", ax=ax, label=bp_label
    )
    ax.set(ylabel="No. de días con ocurrencia de fenomeno")
    ax.set_xlabel(None)
    ax_hanldes, ax_labels = ax.get_legend_handles_labels()
    ax2 = ax.twinx()
    ax2.set(
        ylabel="Frecuencia de ocurrencia %",
        ylim=(
            int(frecs.min() - 5) if int(frecs.min() - 5) > 0 else 0,
            int(frecs.max() + 5) if int(frecs.max() + 5) <= 100 else 100,
        ),
    )
    ax2.grid(False)
    sns.set_style("ticks")
    frecuencies = sns.lineplot(
        x=months - 1,
        y=frecs,
        color="red",
        ax=ax2,
        lw=5,
        label="Frecuencias",
    )
    ax2_hanldes, ax2_labels = ax2.get_legend_handles_labels()
    all_handles = ax_hanldes + ax2_hanldes
    ax.set_yticks(np.arange(0, 31, 5))
    ax2.set_yticks(np.arange(0, 101, 10))
    ax.set_xticklabels([m[:3].upper() for m in MONTHS])
    sns.set()
    ax2.legend(handles=all_handles, loc="upper left", framealpha=0.9)

    logger.info(f"Saving bar-frecuencies plot figure for variable {variable}.")
    fig.savefig(
        f"template/Figures/graphs/barfrec_plot_{save_as}.png", format="png", dpi=600
    )


def bar_plot(df: pd.DataFrame, station: str, variable: str, weather="", save_as=""):    
    hours = hours_range(station)
    means = np.arange(len(hours))
    years = df["Year"].unique()

    logger.info(
        f"Getting the hourly DataFrames for bar plot, variable: {variable}, and calculating the means."
    )
    for hour in hours:
        index = hours.index(hour)
        hour_df = df.query(f"Hour1_24 == {hour}")

        if variable == "Cavok":
            mean = hour_df[variable].sum() / (12 * len(years))
        elif variable == "Visibility":
            vis_df = hour_df.query(f"{variable} <= 5000.0")
            mean = vis_df["Visibility"].sum() / (12 * len(years))
        elif variable in ["Weather_description", "Weather_obscuration"]:
            mean = np.count_nonzero(hour_df[variable] == weather) / (12 * len(years))
        elif variable == "Weather_precipitation":
            if weather == "RA":
                hour_df = hour_df.query(
                    'Weather_description != "SH" and Weather_description != "TS"'
                )
            mean = np.count_nonzero(hour_df[variable] == weather) / (12 * len(years))
        elif "Sky_layer" in variable:
            cols = [
                "Sky_layer1_height",
                "Sky_layer2_height",
                "Sky_layer3_height",
                "Sky_layer4_height",
            ]
            mean = np.count_nonzero(hour_df[cols] <= 1500.0) / (12 * len(years))
        else:
            raise ValueError(f"Invalid variable {variable}.")

        means[index] = Decimal(mean).quantize(Decimal("1."), ROUND_HALF_UP)

    sns.set()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(x=np.arange(0, len(hours)), y=means, color="royalblue", ax=ax)
    ax.set_yticks(np.arange(0, 31, 5))
    ax.set_xticklabels(local_time_list(hours))
    ax.set_ylabel("No. de días con ocurrencia de fenómeno")

    if station in ["mroc", "mrlb"]:
        plt.xticks(rotation=90)

    logger.info(f"Saving bar plot figure for variable {variable}" + ": {weather}." if weather != "" else ".")
    fig.savefig(f"template/Figures/graphs/bar_plot_{save_as}.png", format="png", dpi=600)