import os
from types import SimpleNamespace

from dotenv import load_dotenv

from src.directories import directories

ENV_PATH = directories.root_dir / ".env"


class _Config:
    def __init__(self):
        if ENV_PATH.exists():
            load_dotenv(ENV_PATH)

        self.snowflake_connector = SimpleNamespace(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            role=os.environ["SNOWFLAKE_ROLE"],
            warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
            database=os.environ["SNOWFLAKE_DATABASE"],
            schema=os.environ["SNOWFLAKE_SCHEMA"],
        )

        self.data_path = SimpleNamespace(
            trips=directories.data_dir / "nyc-taxi-2015.csv",
            weather=directories.data_dir / "nyc-weather-2015.csv",
        )

        self.weather_source_table = "NYC_TAXI_WEATHER"

        self.test_size = .2
        self.target = "duration"


config = _Config()
