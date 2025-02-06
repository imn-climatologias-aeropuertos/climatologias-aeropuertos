from typing import Dict, List

import pandas as pd


def _days_of_month(max_days: int):
    return [f"{day}" for day in range(1, max_days + 1)]


operation_hours_by_station: Dict[str, List[int]] = {
    "mroc": [i for i in range(7, 25)] + [i for i in range(1, 7)],
    "mrpv": [i for i in range(12, 25)],
    "mrlm": [i for i in range(12, 25)],
    "mrlb": [i for i in range(12, 25)] + [i for i in range(1, 7)],
}


def hours_range(station: str):
    hours = []

    if station == "mrlm" or station == "mrpv":
        return [i for i in range(12, 25)]

    if station == "mroc":
        for i in range(7, 12):
            hours.append(i)

    if station == "mroc" or station == "mrlb":
        for i in range(12, 25):
            hours.append(i)

        for i in range(1, 7):
            hours.append(i)

    return hours


def local_time_list(times: list):
    local_times = [i - 6 if i - 6 > 0 else i + 18 for i in times]
    return [f"{i}:00".replace("24", "00") if i > 9 else f"0{i}:00" for i in local_times]


def frange(start, stop, step):
    while start < stop:
        yield start
        start += step
        start = str("{:.2f}".format(start))
        start = float(start)


dpi = 150


MONTHS = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Setiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

DAYS_PER_MONTH = {
    1: _days_of_month(31),
    2: _days_of_month(28),
    3: _days_of_month(31),
    4: _days_of_month(30),
    5: _days_of_month(31),
    6: _days_of_month(30),
    7: _days_of_month(31),
    8: _days_of_month(31),
    9: _days_of_month(30),
    10: _days_of_month(31),
    11: _days_of_month(30),
    12: _days_of_month(31),
}

dpi = 100
