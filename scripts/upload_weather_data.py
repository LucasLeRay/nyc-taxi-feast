from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine.base import Engine

from src.config import config
from src.data import get_weather_dataset


def main():
    engine = get_snowflake_engine()
    data = get_weather_dataset().assign(created=datetime.now())
    upload_data(data, engine=engine)


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
        name=config.weather_source_table,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi"
    )


if __name__ == "__main__":
    main()
