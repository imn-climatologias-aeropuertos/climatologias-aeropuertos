import re
from typing import List

from decimal import ROUND_HALF_UP, Decimal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from clima.graphics import DAYS_PER_MONTH, dpi, MONTHS, hours_range, local_time_list

from clima.logger_model import logger


def bar_plot_selective(
    df: pd.DataFrame,
    station: str,
    variable: str,
    use_months: List[int],
    bp_label="",
    weather="",
    save_as="",
):
    df = df.query(f"Month in {use_months}")
    df["Hour1_24"] = df["Hour"].replace(0, 24)

    hours = hours_range(station)
    # means = np.arange(len(hours))
    means = np.empty([len(hours)], dtype=float)
    years = df["Year"].unique()

    # logger.info(
    #     f"Getting the hourly DataFrames for bar plot, variable: {variable}, and calculating the means."
    # )
    for hour in hours:
        index = hours.index(hour)
        hour_df = df.query(f"Hour1_24 == {hour}")
        count = 0

        if variable == "Visibility":
            mean = np.count_nonzero(hour_df[variable] <= 5000.0)
        elif variable in ["Weather_description", "Weather_obscuration"]:
            hour_df = hour_df.query('Weather_intensity != "VC"')
            count = np.count_nonzero(hour_df[variable] == weather)
        elif variable == "Weather_precipitation":
            if weather == "RA":
                hour_df = hour_df.query(
                    'Weather_description != "SH" and Weather_description != "TS"'
                )
            count = np.count_nonzero(hour_df[variable] == weather)
        elif "Sky_layer" in variable:
            cols = [
                "Sky_layer1_height",
                "Sky_layer2_height",
                "Sky_layer3_height",
                "Sky_layer4_height",
            ]
            count = np.count_nonzero(hour_df[cols] <= 1500.0)
        else:
            raise ValueError(f"Invalid variable {variable}.")

        # means[index] = Decimal(mean).quantize(Decimal("1."), ROUND_HALF_UP)
        # means[index] = Decimal(mean).quantize(Decimal("1."))
        means[index] = count / (len(use_months) * len(years))
    print(means)

    sns.set_theme()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(x=np.arange(0, len(hours)), y=means, color="royalblue", ax=ax)
    # ax.set_yticks(np.arange(0, 31, 5))
    ax.set_xlabel("Hora local", size=16)
    if bp_label:
        ax.set_ylabel(f"Número de ocurrencias de {bp_label}", size=16)
    else:
        ax.set_ylabel(f"Número de ocurrencias", size=16)
    ax.set_xticklabels(local_time_list(hours))

    if station in ["mroc", "mrlb"]:
        plt.xticks(rotation=90)

    # logger.info(
    #     f"Saving bar plot figure for variable {variable}" + ": {weather}."
    #     if weather != ""
    #     else "."
    # )
    plt.subplots_adjust(
        bottom=0.15,
        top=0.94,
        left=0.1,
        right=0.95,
    )

    ax.set_title(f"Distribución horaria de ocurrencias de {bp_label}", size=18)
    plt.show()
    # fig.savefig(
    #     f"template/Figures/graphs/bar_plot_{save_as}.jpg", format="jpg", dpi=dpi
    # )
