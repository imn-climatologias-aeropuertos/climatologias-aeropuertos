import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from clima.graphics import DAYS_PER_MONTH, MONTHS, dpi, hours_range, local_time_list
from clima.logger_model import logger

months = list(MONTHS)


def contour_map(
    df: pd.DataFrame,
    station: str,
    variable: str,
    cbar_label="",
    save_as="",
    config={"max": 100, "min": 0, "ticks_num": 9},
):
    fig, _axs = plt.subplots(figsize=(16, 18), nrows=4, ncols=3)
    axs = _axs.flatten()
    cmap = mpl.cm.rainbow

    suptitle_varname = (
        f"las {cbar_label.lower()}"
        if "Ráfagas" in cbar_label
        else f"la {cbar_label.lower()}"
    )
    fig.suptitle(
        f"Distribución diaria de {suptitle_varname} por mes",
        size=20,
        y=0.99,
    )

    hours = hours_range(station)
    if station == "mroc":
        hours_array = np.array([hours.index(x) + 1 for x in hours])
    else:
        hours_array = np.array([hours.index(x) + 6 for x in hours])

    # Get the month df
    logger.info(
        f"Getting the monthly DataFrames for contour map, variable: {variable}."
    )
    for i, month in enumerate(months, start=1):
        month_means = []
        month_df = df.query(f"Month == {i}")

        # Get the day df for every month
        # logger.info(f"Getting the dayly DataFrames for month {month}.")
        for day in DAYS_PER_MONTH[i]:
            day = int(day)
            day_means = []
            day_df = month_df.query(f"Day == {day}")

            # Get the hour df for every day
            # logger.info(
            #     f"Getting the hourly DataFrames for day {day} and calculating the mean values."
            # )
            for hour in hours:
                hour_df = day_df.query(f"Hour1_24 == {hour}")
                mean = hour_df[variable].mean()
                day_means.append(mean)

            month_means.append(day_means)

        month_means_array = np.array(month_means)
        days_array = np.array(list(map(int, DAYS_PER_MONTH[i])))

        logger.info(
            f"Generating the contour map for month {month} of variable {variable}."
        )
        X, Y = np.meshgrid(days_array, hours_array)
        Z = month_means_array.T
        # plt.yticks(hours_array.tolist(), local_time_list(hours))
        im = axs[i - 1].contourf(
            X, Y, Z, cmap=cmap, vmax=config["max"], vmin=config["min"]
        )
        axs[i - 1].set_yticks(list(hours_array))

        # yticklabels hidden for more right plots
        # if i in [1, 4, 7, 10]:
        #     axs[i - 1].set_yticklabels(local_time_list(hours))
        #     axs[i -1].set_ylabel("Hora", size=16)
        # else:
        #     axs[i - 1].set_yticklabels([])

        axs[i - 1].set_yticklabels(local_time_list(hours))
        axs[i - 1].set_ylabel("Hora local", size=16)

        # set the title for every plot (the month name)
        axs[i - 1].set_title(month, size=15)
        axs[i - 1].set_xlabel("Día del mes", size=14)
        # axs[i -1].set_ylabel("Hora", size=16)

    cbar_ax = fig.add_axes([0.85, 0.25, 0.02, 0.5])
    if variable == "Pressure":
        # bounds = list(frange(config["min"], config["max"], config["ticks_num"]))
        bounds = np.arange(config["min"], config["max"], config["ticks_num"])
    else:
        bounds = list(
            map(
                int,
                np.linspace(config["min"], config["max"], config["ticks_num"]).tolist(),
            )
        )
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="both")
    cb = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax)
    cb.set_label(label=cbar_label, size=25)
    cb.ax.tick_params(labelsize=18)
    fig.subplots_adjust(
        bottom=0.05,
        top=0.95,
        left=0.1,
        right=0.8,
        wspace=0.25,
        hspace=0.25,
    )

    logger.info(f"Saving contour map figure for variable {variable}.")
    fig.savefig(
        f"template/Figures/graphs/contourmap_{save_as}.jpg", format="jpg", dpi=dpi
    )
