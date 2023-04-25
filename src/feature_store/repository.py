from pathlib import Path

import yaml
from feast import SnowflakeSource

from src.columns import SourceTrips
from src.config import config

FEATURE_STORE_PROJECT_PATH = Path(__file__).parent / "feature_store.yaml"

with open(FEATURE_STORE_PROJECT_PATH) as f:
    project = yaml.safe_load(f)

project_name = project["project"]
offline_store = project["offline_store"]

trips_source = SnowflakeSource(
    table=config.trips_source_table,
    timestamp_field=SourceTrips.PICKUP_DATETIME,
    created_timestamp_column="created"
)
