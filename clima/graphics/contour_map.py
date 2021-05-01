import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from clima.graphics import DAYS_PER_MONTH
from clima.graphics import MONTHS as months
from clima.graphics import hours_range, local_time_list
from clima.logger_model import logger


def contour_map(
    df: pd.DataFrame,
    station: str,
    variable: str,
    v_max=100,
    v_min=0,
    cbar_ticks_num=9,
    cbar_label="",
    save_as="",
):
    fig, _axs = plt.subplots(figsize=(16, 18), nrows=4, ncols=3)
    axs = _axs.flatten()
    cmap = mpl.cm.rainbow

    hours = hours_range(station)
    if station == "mroc":
        hours_array = np.array([hours.index(x) + 1 for x in hours])
    else:
        hours_array = np.array([hours.index(x) + 6 for x in hours])
    # plt.yticks(hours_array.tolist(), local_time_list(hours))

    # Get the month df
    logger.info("Getting the monthly DataFrames.")
    for month in months:
        month_i = months.index(month) + 1
        month_means = []
        month_df = df.query(f"Month == {month_i}")

        # Get the day df for every month
        logger.info(f"Getting the dayly DataFrames for month {month}.")
        for day in DAYS_PER_MONTH[month_i]:
            day = int(day)
            day_means = []
            day_df = month_df.query(f"Day == {day}")

            # Get the hour df for every day
            logger.info(
                f"Getting the hourly DataFrames for day {day} and calculating the mean values."
            )
            for hour in hours:
                hour_df = day_df.query(f"Hour1_24 == {hour}")
                mean = hour_df[variable].mean()
                day_means.append(mean)

            month_means.append(day_means)

        month_means_array = np.array(month_means)
        # if station == "mroc":
        #     hours_array = np.array([hours.index(x) + 1 for x in hours])
        # else:
        #     hours_array = np.array([hours.index(x) + 6 for x in hours])
        days_array = np.array(list(map(int, DAYS_PER_MONTH[month_i])))

        logger.info(
            f"Generating the contour map for month {month} of variable {variable}."
        )
        X, Y = np.meshgrid(days_array, hours_array)
        Z = month_means_array.T
        # plt.yticks(hours_array.tolist(), local_time_list(hours))
        im = axs[month_i - 1].contourf(X, Y, Z, cmap=cmap, vmax=v_max, vmin=v_min)
        axs[month_i - 1].set_yticks(list(hours_array))
        
        # yticklabels hidden for more right plots
        if month_i in [1, 4, 7, 10]:
            axs[month_i - 1].set_yticklabels(local_time_list(hours))
        else:
            axs[month_i - 1].set_yticklabels([])
        
        # set the title for every plot (the month name)
        axs[month_i - 1].set_title(month, weight="bold", size=16)

    cbar_ax = fig.add_axes([0.85, 0.25, 0.02, 0.5])
    bounds = list(map(int, np.linspace(int(v_min), int(v_max), cbar_ticks_num).tolist()))
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="both")
    cb = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax)
    cb.set_label(label=cbar_label, size=20)
    fig.subplots_adjust(
        bottom=0.05, top=0.95, left=0.1, right=0.8, wspace=0.2, hspace=0.2
    )

    logger.info(f"Saving contour map figure for variable {variable}.")
    fig.savefig(
        f"template/Figures/graphs/contourmap_{save_as}.png", format="png", dpi=300
    )
