import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sbn

from clima.graphics import MONTHS
from clima.graphics import dpi, hours_range, local_time_list
from clima.logger_model import logger

months = [month[0:3].upper() for month in MONTHS]


def _cardinal_point(value: float):
    if value >= 337.5 or value < 22.5:
        return "N"
    elif value >= 22.5 and value < 67.5:
        return "NE"
    elif value >= 67.5 and value < 112.5:
        return "E"
    elif value >= 112.5 and value < 157.5:
        return "SE"
    elif value >= 157.5 and value < 202.5:
        return "S"
    elif value >= 202.5 and value < 247.5:
        return "SO"
    elif value >= 247.5 and value < 292.5:
        return "O"
    elif value >= 292.5 and value < 337.5:
        return "NO"
    else:
        raise ValueError("Not valid value.")


def heat_map(df: pd.DataFrame, station: str):

    means_per_month = []
    cardinal_points_per_month = []

    # For every month, get data
    logger.info("Getting the monthly DataFrames for wind direction heatmap")
    for i, month in enumerate(months, start=1):
        month_df = df.query(f"Month == {i}")
        means_per_hour = []
        cardinal_points_per_hour = []

        # For every hour, get the mean
        logger.info(f"Getting the hourly DataFrames and calculating the means values for month: {month}.")
        for j in hours_range(station):
            hour = month_df.query(f"Hour1_24 == {j}")
            mean = hour["Wind_direction"].mean()

            # Store the hourly means per month
            means_per_hour.append(mean)
            cardinal_points_per_hour.append(_cardinal_point(mean))

        # store the monthly values
        means_per_month.append(means_per_hour)
        cardinal_points_per_month.append(cardinal_points_per_hour)

    # Create numpy arrays
    means_array = np.array(means_per_month)
    cpoint_array = np.array(cardinal_points_per_month)

    # Get the list of operational hours per station
    hours_labels = local_time_list(hours_range(station))

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(11, 6))
    cmap = sbn.cm.rocket_r
    ax = sbn.heatmap(
        means_array,
        annot=cpoint_array,
        fmt="",
        cmap=cmap,
        yticklabels=months,
        xticklabels=hours_labels,
    )
    ax.set_xlabel("Hora", size=16)
    ax.set_ylabel("Mes", size=16)
    cbar = ax.collections[0].colorbar
    cbar.set_label("Dirección del viento (°)", size=16)
    
    if station.upper() in ["MROC", "MRLB"]:
        plt.xticks(rotation=45)

    plt.yticks(rotation=0)
    plt.subplots_adjust(
        bottom=0.12,
        top=0.94,
        left=0.1,
        right=1.0,
    )

    logger.info(f"Saving heat map figure for wind direction.")
    fig.savefig(f"template/Figures/graphs/heatmap_wind_dir.jpg", format="jpg", dpi=dpi)
