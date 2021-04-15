import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from ..logger_model import logger

def _days_of_month(max_days: int):
    return [f"{day}" for day in range(1, max_days + 1)]

_days = {
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

def _handle_precipitation(df: pd.DataFrame):
    data = []
    total_prec_days = 0
    total_prec = 0
    
    for i in range(1, 13):
        data_per_month = []
        month = df.query(f"Mes == {i}")
        
        # Fill the NaN values by the mean if the mean is >= 0.1 else 0.0
        for day in _days[i]:
            mean_prec = month[day].mean()
            month[day] = month[day].fillna(mean_prec if mean_prec >= 0.1 else 0.0)
        
        # Obtain the precipitation sum for every row (month by year) and its mean
        logger.info(f"Obtaining precipitation sum for month: {i}")
        month["sum"] = month[_days[i]].sum(axis=1)
        mean_prec = float(Decimal(month["sum"].mean()).quantize(Decimal(".1"), ROUND_HALF_UP))
        data_per_month.append(mean_prec)
        total_prec += mean_prec
        
        # Obtain the days with precipitation registered and its mean
        logger.info(f"Obtaining days with precipitation for month: {i}")
        month['days with prec'] = (month[_days[i]] != 0.0).T.sum()
        mean_days_with_prec = int(Decimal(month["days with prec"].mean()).quantize(Decimal("1."), ROUND_HALF_UP))
        data_per_month.append(mean_days_with_prec)
        total_prec_days += mean_days_with_prec

        data.append(data_per_month)
    
    data.append([round(total_prec, 1), total_prec_days])
    return data


def generate_table(station: str):
    station = station.lower()
    logger.info("Reading data from CSV files.")
    prec = pd.read_csv(f"data/{station}/{station}_prec.csv")
    tmax = pd.read_csv(f"data/{station}/{station}_max.csv")
    tmin = pd.read_csv(f"data/{station}/{station}_min.csv")
    
    prec_data = _handle_precipitation(prec)
    # _handle_precipitation(tmax)
    # _handle_precipitation(tmin)
