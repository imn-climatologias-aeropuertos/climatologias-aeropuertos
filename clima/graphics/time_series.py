import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from clima.graphics import DAYS_PER_MONTH
from clima.graphics import MONTHS as months
from clima.graphics import dpi, frange, hours_range, local_time_list
from clima.logger_model import logger


def reduce_list(l: list, max=13):
    new = []
    if len(l) > max:
        for val in l:
            if l.index(val) % 2 == 0:
                new.append(val)
        return new
    return l


def time_series(
    df: pd.DataFrame,
    station: str,
    variable: str,
    yaxis_label="",
    save_as="",
    config={"min": 0, "max": 260, "tick_jump": 50, "hline": [5, 6, 8, 9, 10]},
):
    sns.set()
    fig, _axs = plt.subplots(figsize=(16, 18), nrows=4, ncols=3)
    axs = _axs.flatten()

    hours = hours_range(station)
    if station == "mroc":
        hours_array = np.array([hours.index(x) + 1 for x in hours])
    else:
        hours_array = np.array([hours.index(x) + 6 for x in hours])

    logger.info(
        f"Getting the monthly DataFrames for time series, variable: {variable}."
    )
    for month in months:
        month_i = months.index(month) + 1
        ax_i = months.index(month)
        month_means = []
        month_df = df.query(f"Month == {month_i}")

        logger.info(
            f"Getting the hourly DataFrames for month {month} and calculating the mean values."
        )
        for hour in hours:
            hour_df = month_df.query(f"Hour1_24 == {hour}")
            mean = hour_df[variable].mean()
            month_means.append(mean)

        month_means_array = np.array(month_means)
        arr_len = len(hours_array)

        # print(month, month_means_array.shape, month_means_array.reshape(len(hours_array), 1))
        # print(hours_array.reshape(len(hours_array), 1))
        data = np.hstack(
            (hours_array.reshape(arr_len, 1), month_means_array.reshape(arr_len, 1))
        )
        month_df = pd.DataFrame(data, columns=["hour", "var"])
        # print(month_df.head())

        logger.info(
            f"Generating the time series for month {month} of variable {variable}."
        )
        im = sns.lineplot(
            x="hour",
            y="var",
            data=month_df,
            ax=axs[month_i - 1],
            hue_norm=(config["min"], config["max"]),
        )
        if month_i in config["hline"]:
            axs[ax_i].plot(
                list(hours_array),
                [180 for x in range(len(hours_array))],
                "--",
                c="r",
                lw=1.0,
            )
        axs[ax_i].set_title(month, weight="bold", size=16)
        axs[ax_i].set_xticks(reduce_list(list(hours_array)))
        axs[ax_i].set_xlabel("")
        axs[ax_i].set_ylabel(yaxis_label, size=16)
        # axs[ax_i].set_yticks(
        #     list(frange(config["min"], config["max"], config["tick_jump"]))
        # )
        axs[ax_i].set_yticks(
            np.arange(config["min"], config["max"], config["tick_jump"])
        )
        # axs[ax_i].set_yticks(
        #     [x for x in range(config["min"], config["max"], config["tick_jump"])]
        # )

        if month_i in [2, 3, 5, 6, 8, 9, 11, 12]:
            axs[ax_i].set_yticklabels([])
            axs[ax_i].set_ylabel("")

        if month_i in [1, 2, 3, 7, 8, 9]:
            axs[ax_i].set_xticklabels([])
        else:
            axs[ax_i].set_xticklabels(
                [
                    hour.replace(":00", "")
                    for hour in local_time_list(reduce_list(hours))
                ]
            )

    fig.subplots_adjust(
        bottom=0.05, top=0.95, left=0.08, right=0.95, wspace=0.2, hspace=0.2
    )

    logger.info(f"Saving time series figure for variable {variable}.")
    fig.savefig(
        f"template/Figures/graphs/time_series_{save_as}.png", format="png", dpi=dpi
    )


def single_time_series(df: pd.DataFrame, variable: str, yaxis_label="", save_as=""):

    month_means = np.zeros(12)
    logger.info(f"Extracting data for single time series (monthly) for {variable}.")
    for i in range(12):
        j = i + 1
        month_df = df.query(f"Month == {j}")
        month_means[i] = month_df[variable].mean()

    sns.set()
    fig, ax = plt.subplots(figsize=(10, 6))
    im = sns.lineplot(x=range(12), y=month_means, ax=ax)
    im.set_xticks(list(range(12)))
    im.set_xticklabels([m[0:3].upper() for m in months])
    im.set_ylabel(yaxis_label)

    logger.info(f"Saving single time series figure for variable {variable}.")
    fig.savefig(
        f"template/Figures/graphs/single_time_series_{save_as}.png",
        format="png",
        dpi=dpi,
    )
