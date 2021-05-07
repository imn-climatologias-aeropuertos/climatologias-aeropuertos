import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from clima.graphics import DAYS_PER_MONTH, MONTHS, hours_range

time_ranges = {19: 9, 13: 6, 24: 12}


def _handle_cavok(df: pd.DataFrame, hrange: int):
    day_sum = df["Cavok"].sum()

    if day_sum >= time_ranges[hrange]:
        return 1

    return 0


def _handle_visibility(df: pd.DataFrame):
    unique_vals = df["Visibility"].unique()
    ocurrences = np.count_nonzero(unique_vals < 5000.0)

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
        < 1500.0
    )

    if ocurrences > 0:
        return 1

    return 0


def _handle_weather(df: pd.DataFrame, variable: str, weather: str):
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

    for month in months:
        month_sum = 0

        for year in years:
            month_df = df.query(f"Year == {year} and Month == {month}")

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

        month_means[month - 1] = month_sum / len(years)
    frecs = 100 * month_means / len(DAYS_PER_MONTH[month])
    print(month_means, frecs)

    sns.set()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(
        x=months - 1, y=month_means, color="royalblue", ax=ax, label=bp_label
    )
    ax.set(ylabel="No. ocurrencias mensuales")
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
    ax.set_xticklabels([m[:3].upper() for m in MONTHS])
    sns.set()
    ax2.legend(handles=all_handles, loc="upper left", framealpha=0.9)

    fig.savefig(f"template/Figures/graphs/barfrec_plot_{save_as}.png", format="png", dpi=600)
