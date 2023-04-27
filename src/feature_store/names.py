from enum import auto

from src.columns import WeatherSource
from src.utils import StrEnum


class TripsFeatures(StrEnum):
    """Trips features columns"""
    PICKUP_HOUR = auto()
    PICKUP_DAY = auto()
    PICKUP_MONTH = auto()
    # It seems that it's not possible to rename a field, so the same as
    # weather dataset is used.
    MIN_TEMPERATURE = WeatherSource.TMIN
    MAX_TEMPERATURE = WeatherSource.TMAX


class FView(StrEnum):
    """Feature Views registered into store"""
    TEMPERATURE = auto()
