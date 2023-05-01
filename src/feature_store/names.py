from enum import auto

from src.columns import WeatherSource
from src.utils import StrEnum


class TripsFeatures(StrEnum):
    """Trips features columns"""
    PICKUP_HOUR = auto()
    PICKUP_DAY = auto()
    PICKUP_MONTH = auto()
    DISTANCE = auto()
    # It seems that it's not possible to rename a field
    MIN_TEMPERATURE = WeatherSource.TMIN
    MAX_TEMPERATURE = WeatherSource.TMAX


class FView(StrEnum):
    """Feature Views registered into store"""
    TEMPERATURE = auto()


class FService(StrEnum):
    """Feature Services registered into store"""
    TRIP_INFOS = auto()
