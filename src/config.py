import os
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv

ROOT_PATH = Path(__file__).parents[1]
ENV_PATH = ROOT_PATH / ".env"


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

        self.weather_source_table = "NYC_TAXI_WEATHER"


config = _Config()
