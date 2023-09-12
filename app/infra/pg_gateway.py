import logging
from typing import Iterator
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from app.infra import EnvConfig


class MetaPGGateway(type):
    _engine_connection = None
    _engine_connection_stream = None
    @property
    def engine_connection(cls):
        if not cls._engine_connection:
            cls._engine_connection = create_engine(cls.connection_string)
            logging.info("Created postgres engine")
        return cls._engine_connection

    @property
    def engine_connection_stream(cls):
        if not cls._engine_connection_stream:
            cls._engine_connection_stream = create_engine(
                cls.connection_string
            ).connect().execution_options(stream_results=True)
            logging.info("Created postgres engine")
        return cls._engine_connection

    @property
    def pg_credentials(cls) -> dict:
        return EnvConfig.pg_credentials

    @property
    def connection_string(cls) -> str:
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            user=cls.pg_credentials.get("username"),
            password=cls.pg_credentials.get("password"),
            host=cls.pg_credentials.get("host"),
            port=cls.pg_credentials.get("port"),
            database=cls.pg_credentials.get("db")
        )


class PGGateway(metaclass=MetaPGGateway):

    @classmethod
    def pd_insert_sql(cls, table: str, df: pd.DataFrame, columns_type: dict = None, replace_table: bool = False):
        logging.info(f'Executing insert {table=} into database')
        df.to_sql(
            name=table,
            con=cls.engine_connection,
            dtype=columns_type,
            index=False,
            if_exists="replace" if replace_table else "append"
        )
        logging.info(f'Insert complete')

    @classmethod
    def pd_select_table(cls, table_or_query: str) -> pd.DataFrame:
        return pd.read_sql(
            sql=table_or_query,
            con=cls.engine_connection
        )