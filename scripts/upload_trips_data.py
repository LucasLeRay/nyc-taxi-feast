from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from src.config import config

DATA_FOLDER = Path(__file__).parents[1] / "data"
NYC_TAXI_DATASET_FILENAME = "nyc-taxi-2015.csv"

SAMPLE_COUNT = 10_000  # Number of rows to upload to warehouse


def main():
    engine = get_snowflake_engine()
    data = get_dataset()
    upload_data(data, engine=engine)


def get_dataset() -> pd.DataFrame:
    nyc_taxi_data_path = DATA_FOLDER / NYC_TAXI_DATASET_FILENAME
    return pd.read_csv(nyc_taxi_data_path).sample(n=SAMPLE_COUNT)


def get_snowflake_engine() -> Engine:
    connector = config.snowflake_connector
    snowflake_url = URL.create(
        drivername="snowflake",
        username=connector.user,
        password=connector.password,
        host=connector.account,
        database=connector.database,
        query={
            "warehouse": connector.warehouse,
            "role": connector.role
        }
    )

    engine = create_engine(snowflake_url)
    with engine.connect() as conn:
        conn.execute(f"USE SCHEMA {connector.database}.{connector.schema}")

    return engine


def upload_data(data: pd.DataFrame, engine: Engine):
    data.to_sql(
        name=config.trips_source_table,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi"
    )


if __name__ == "__main__":
    main()
