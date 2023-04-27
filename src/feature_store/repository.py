from datetime import timedelta

import pandas as pd
from feast import FeatureView, Field, RequestSource, SnowflakeSource
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Int64, UnixTimestamp

from src.columns import TripsSource, WeatherSource
from src.config import config
from src.feature_store.names import FView, TripsFeatures

weather_source = SnowflakeSource(
    table=config.weather_source_table,
    timestamp_field=WeatherSource.DATE,
    created_timestamp_column="created"
)

trip_input = RequestSource(
    name="trip_input",
    schema=[
        Field(name=TripsSource.PICKUP_DATETIME, dtype=UnixTimestamp),
        Field(name=TripsSource.PICKUP_LATITUDE, dtype=Float32),
        Field(name=TripsSource.PICKUP_LONGITUDE, dtype=Float32),
        Field(name=TripsSource.DROPOFF_LATITUDE, dtype=Float32),
        Field(name=TripsSource.DROPOFF_LONGITUDE, dtype=Float32),
    ],
)


@on_demand_feature_view(
    sources=[trip_input],
    schema=[
        Field(name=TripsFeatures.PICKUP_HOUR, dtype=Int64),
        Field(name=TripsFeatures.PICKUP_DAY, dtype=Int64),
        Field(name=TripsFeatures.PICKUP_MONTH, dtype=Int64),
    ]
)
def pickup_time_features(source: pd.DataFrame) -> pd.DataFrame:
    pickup_time = source[TripsSource.PICKUP_DATETIME]
    return pd.DataFrame({
        TripsFeatures.PICKUP_HOUR: pickup_time.dt.hour,
        TripsFeatures.PICKUP_DAY: pickup_time.dt.day,
        TripsFeatures.PICKUP_MONTH: pickup_time.dt.month,
    })


weather = FeatureView(
    name=FView.TEMPERATURE,
    ttl=timedelta(days=1),  # Get temperature of current day
    schema=[
        Field(name=TripsFeatures.MIN_TEMPERATURE, dtype=Float32),
        Field(name=TripsFeatures.MAX_TEMPERATURE, dtype=Float32),
    ],
    source=weather_source
)
