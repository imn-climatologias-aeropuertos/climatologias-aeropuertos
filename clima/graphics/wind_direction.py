import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sbn

from clima.graphics import months

columns = ["Month", "Day", "Hour", "Wind_direction"]


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


def _hours_range(station: str):
    hours = []

    if station == "mrlm" or station == "mrpv":
        return [x for x in range(12, 25)]

    if station == "mroc":
        for i in range(7, 12):
            hours.append(i)

    if station == "mroc" or station == "mrlb":
        for i in range(12, 25):
            hours.append(i)

        for j in range(1, 7):
            hours.append(j)

    return hours


def heat_map(df: pd.DataFrame, station: str):
    df = df[columns]
    df["Hour0_24"] = df["Hour"].replace(0, 24)

    means_per_month = []
    cardinal_points_per_month = []

    # For every month, get data
    for i in range(1, 13):
        month = df.query(f"Month == {i}")
        means_per_hour = []
        cardinal_points_per_hour = []

        # For every hour, get the mean
        for j in _hours_range(station):
            hour = month.query(f"Hour0_24 == {j}")
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
    lhours = [i - 6 if i - 6 > 0 else i + 18 for i in _hours_range(station)]
    hours_labels = [
        f"{i}:00".replace("24", "00") if i > 9 else f"0{i}:00" for i in lhours
    ]

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
        cbar_kws={"label": "Dirección del viento (°)"},
    )
    fig.savefig(f"template/Figures/graphs/heatmap_wind_dir.png", format="png", dpi=600)
