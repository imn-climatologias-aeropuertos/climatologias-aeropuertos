import pandas as pd

def generate_table(station: str):
    station = station.lower()
    prec = pd.read_csv(f"data/{station}/{station}_prec.csv")
    tmax = pd.read_csv(f"data/{station}/{station}_max.csv")
    tmin = pd.read_csv(f"data/{station}/{station}_min.csv")
    print(prec.head(10))
    print(tmax.head(10))
    print(tmin.head(10))