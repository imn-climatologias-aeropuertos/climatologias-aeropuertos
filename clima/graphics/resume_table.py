import pandas as pd

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
    for i in range(1, 13):
        data_per_month = []
        month = df.query(f"Mes == {i}")
        
        # Fill the NaN values by the mean if the mean is >= 0.1 else 0.0
        for day in _days[i]:
            mean_prec = month[day].mean()
            month[day] = month[day].fillna(mean_prec if mean_prec >= 0.1 else 0.0)
        
        # Obtain the precipitation sum for every row (month by year) and its mean
        month["sum"] = month[_days[i]].sum(axis=1)
        data_per_month.append(month["sum"].mean())
        
        # Obtain the days with precipitation registered and its mean
        month['dias con lluvia'] = (month[_days[i]] != 0.0).T.sum()
        data_per_month.append(month["dias con lluvia"].mean())

        data.append(data_per_month)
    print(data)


def generate_table(station: str):
    station = station.lower()
    prec = pd.read_csv(f"data/{station}/{station}_prec.csv")
    tmax = pd.read_csv(f"data/{station}/{station}_max.csv")
    tmin = pd.read_csv(f"data/{station}/{station}_min.csv")
    
    _handle_precipitation(prec)
    # _handle_precipitation(tmax)
    # _handle_precipitation(tmin)
