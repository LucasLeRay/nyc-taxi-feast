from typing import Sequence

import pandas as pd
from sklearn.model_selection import train_test_split as _train_test_split

from src.columns import TripsSource, WeatherSource
from src.config import config


def get_weather_dataset() -> pd.DataFrame:
    return pd.read_csv(
        config.data_path.weather,
        parse_dates=[WeatherSource.DATE]
    )


def get_trips_dataset() -> pd.DataFrame:
    return pd.read_csv(
        config.data_path.trips,
        parse_dates=[TripsSource.PICKUP_DATETIME, TripsSource.DROPOFF_DATETIME]
    )


def train_test_split(data: pd.DataFrame) -> Sequence[pd.DataFrame]:
    return _train_test_split(
        data,
        test_size=config.test_size,
        shuffle=False
    )
