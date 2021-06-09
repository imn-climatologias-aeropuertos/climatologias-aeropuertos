from decimal import ROUND_HALF_UP, Decimal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from clima.graphics import DAYS_PER_MONTH, MONTHS, dpi
from clima.logger_model import logger

months = list(MONTHS)
months.append("Anual")


def _handle_precipitation(df: pd.DataFrame):
    data = []
    total_prec_days = 0
    total_prec = 0.0

    for i, month in enumerate(months[:-1], start=1):
        data_per_month = []
        month_df = df.query(f"Mes == {i}")

        # Fill the NaN values by the mean if the mean is >= 0.1 else 0.0
        for day in DAYS_PER_MONTH[i]:
            mean_prec = month_df[day].mean()
            month_df[day] = month_df[day].fillna(mean_prec if mean_prec >= 0.1 else 0.0)

        # Obtain the precipitation sum for every row (month by year) and its mean
        logger.info(f"Obtaining precipitation sum for month: {month}")
        month_df["sum"] = month_df[DAYS_PER_MONTH[i]].sum(axis=1)
        mean_prec = float(
            Decimal(month_df["sum"].mean()).quantize(Decimal(".1"), ROUND_HALF_UP)
        )
        data_per_month.append(mean_prec)
        total_prec += mean_prec

        # Obtain the days with precipitation registered and its mean
        logger.info(f"Obtaining days with precipitation for month: {month}")
        month_df["days with prec"] = (month_df[DAYS_PER_MONTH[i]] != 0.0).T.sum()
        mean_days_with_prec = int(
            Decimal(month_df["days with prec"].mean()).quantize(
                Decimal("1."), ROUND_HALF_UP
            )
        )
        data_per_month.append(mean_days_with_prec)
        total_prec_days += mean_days_with_prec

        data.append(data_per_month)

    data.append([round(total_prec, 1), total_prec_days])
    return data


def _handle_tmax(df: pd.DataFrame):
    data = []
    extreme_tmax = 0.0
    mean_tmax = 0.0

    for i, month in enumerate(months[:-1], start=1):
        data_per_month = []
        month_df = df.query(f"Mes == {i}")

        # Fill the NaN values by the mean
        for day in DAYS_PER_MONTH[i]:
            day_mean = month_df[day].mean()
            month_df[day] = month_df[day].fillna(day_mean)

        # Obtain the tmax extreme and mean per every month (same month) by year
        logger.info(f"Obtaining mean tmax for month: {month}")
        month_df["tmax"] = month_df[DAYS_PER_MONTH[i]].max(axis=1)
        mean_tmax_of_month = float(
            Decimal(month_df["tmax"].mean()).quantize(Decimal(".1"), ROUND_HALF_UP)
        )
        logger.info(f"Obtaining extreme tmax for month: {month}")
        extreme_tmax_of_month = float(
            Decimal(month_df["tmax"].max()).quantize(Decimal(".1"), ROUND_HALF_UP)
        )

        data_per_month.append(extreme_tmax_of_month)
        data_per_month.append(mean_tmax_of_month)

        if extreme_tmax_of_month > extreme_tmax:
            extreme_tmax = extreme_tmax_of_month
        mean_tmax += mean_tmax_of_month

        data.append(data_per_month)

    data.append(
        [
            extreme_tmax,
            float(Decimal(mean_tmax / 12).quantize(Decimal(".1"), ROUND_HALF_UP)),
        ]
    )

    return data


def _handle_tmin(df: pd.DataFrame):
    data = []
    extreme_tmin = 100.0
    mean_tmin = 0.0

    for i, month in enumerate(months[:-1], start=1):
        data_per_month = []
        month_df = df.query(f"Mes == {i}")

        # Fill the NaN values by the mean
        for day in DAYS_PER_MONTH[i]:
            day_mean = month_df[day].mean()
            month_df[day] = month_df[day].fillna(day_mean)

        # Obtain the tmin extreme and mean per every month (same month) by year
        logger.info(f"Obtaining mean tmin for month: {month}")
        month_df["tmin"] = month_df[DAYS_PER_MONTH[i]].min(axis=1)
        mean_tmin_of_month = float(
            Decimal(month_df["tmin"].mean()).quantize(Decimal(".1"), ROUND_HALF_UP)
        )
        logger.info(f"Obtaining extreme tmin for month: {month}")
        extreme_tmin_of_month = float(
            Decimal(month_df["tmin"].min()).quantize(Decimal(".1"), ROUND_HALF_UP)
        )

        data_per_month.append(extreme_tmin_of_month)
        data_per_month.append(mean_tmin_of_month)

        if extreme_tmin_of_month < extreme_tmin:
            extreme_tmin = extreme_tmin_of_month
        mean_tmin += mean_tmin_of_month

        data.append(data_per_month)

    data.append(
        [
            extreme_tmin,
            float(Decimal(mean_tmin / 12).quantize(Decimal(".1"), ROUND_HALF_UP)),
        ]
    )

    return data


def _generate_climogram(station: str, data: list):
    df = pd.DataFrame(
        np.array(data),
        columns=[
            "Mes",
            "Tmax_extrema",
            "Tmin_extrema",
            "Tmax_media",
            "Tmin_media",
            "Precipitacion",
            "Dias_con_pcp",
        ],
    )

    df["Tmax_extrema"] = df["Tmax_extrema"].astype(float)
    df["Tmin_extrema"] = df["Tmin_extrema"].astype(float)
    df["Tmax_media"] = df["Tmax_media"].astype(float)
    df["Tmin_media"] = df["Tmin_media"].astype(float)
    df["Precipitacion"] = df["Precipitacion"].astype(float)
    df["Dias_con_pcp"] = df["Dias_con_pcp"].astype(int)

    sns.set()
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(
        x="Mes",
        y="Precipitacion",
        data=df,
        color="royalblue",
        ax=ax,
        label="Precipitación",
    )
    ax.set(ylabel="Precipitación (mm)")
    ax.set_xlabel(None)
    ax_hanldes, ax_labels = ax.get_legend_handles_labels()
    # ax.legend(loc="upper left")
    ax2 = ax.twinx()
    ax2.set(
        ylabel="Temperatura (°C)",
        ylim=(int(df["Tmin_media"].min() - 3), int(df["Tmax_media"].max()) + 3),
    )
    ax2.grid(False)
    sns.set_style("ticks")
    tmax = sns.lineplot(
        x="Mes",
        y="Tmax_media",
        data=df,
        color="red",
        ax=ax2,
        lw=5,
        label="Temperatura máxima",
    )
    tmin = sns.lineplot(
        x="Mes",
        y="Tmin_media",
        data=df,
        color="blue",
        ax=ax2,
        lw=5,
        label="Temperatura mínima",
    )
    ax2_hanldes, ax2_labels = ax2.get_legend_handles_labels()
    all_handles = ax_hanldes + ax2_hanldes
    ax.set_xticklabels([lab[:3].upper() for lab in df["Mes"].tolist()])
    sns.set()
    ax2.legend(handles=all_handles, loc="upper left", framealpha=0.9)
    # ax.tick_params(axis='y')
    fig.savefig("template/Figures/graphs/climograma.png", format="png", dpi=dpi)


LATEX_HEADER = """
\\begin{table}[htb]
\caption{Resumen de variables meteorológicas, \icaoCode{} \\resumeYearsRange{}.}
\label{table:resumen}
\\begin{center}
\\begin{tabular}{>{\centering}p{0.12\\textwidth}>
{\centering}p{0.1\\textwidth}>
{\centering}p{0.1\\textwidth}>
{\centering}p{0.1\\textwidth}>
{\centering}p{0.1\\textwidth}>
{\centering}p{0.1\\textwidth}>
{\centering\\arraybackslash}p{0.1\\textwidth}}
\headrow
\\textbf{Mes} & \\textbf{Temperatura máxima extrema (°C)} & \\textbf{Temperatura mínima extrema (°C)} & \\textbf{Temperatura máxima media (°C)} & \\textbf{Temperatura mínima media (°C)} & \\textbf{Precipitación total media (mm)} & \\textbf{Media de días con precipitación}\\\\
"""

LATEX_FOOTER = """
\hline  % Please only put a hline at the end of the table
\end{tabular}
\end{center}

\\begin{tablenotes}
\item \\textbf{Palabras clave:} \\airportName{}, cambio de viento, cimatología aeronáutica, mínimos operativos, variables meteorológicas.
\end{tablenotes}
\end{table}
"""


def generate_table(station: str):
    station = station.lower()
    logger.info("Reading data from CSV files.")
    prec = pd.read_csv(f"data/{station}/{station}_prec.csv")
    tmax = pd.read_csv(f"data/{station}/{station}_max.csv")
    tmin = pd.read_csv(f"data/{station}/{station}_min.csv")

    prec_data = _handle_precipitation(prec)
    tmax_data = _handle_tmax(tmax)
    tmin_data = _handle_tmin(tmin)

    data = []
    latex_table = ""
    for m, tx, tn, pcp in zip(months, tmax_data, tmin_data, prec_data):
        month_data = [
            m,
            str(tx[0]),
            str(tn[0]),
            str(tx[1]),
            str(tn[1]),
            str(pcp[0]),
            str(pcp[1]),
        ]

        data.append(month_data)

    for month_data in data[:-1]:
        latex_table += " & ".join(month_data) + "\\\\\n"
    latex_table += "\\textbf{" + "} & \\textbf{".join(data[-1]) + "}\\\\\n"

    f = open("template/Tables/table01.tex", "w")
    f.write(LATEX_HEADER)
    f.write(latex_table)
    f.write(LATEX_FOOTER)
    f.close()

    _generate_climogram(station, data[:-1])
