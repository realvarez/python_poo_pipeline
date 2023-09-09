import logging

import pandas as pd
from sqlalchemy import create_engine
from app.infra import EnvConfig


class MetaPGGateway(type):
    _pg_credentials = EnvConfig.pg_credentials
    _engine_connection = None

    @property
    def engine_connection(cls):
        if not cls._engine_connection:
            cls._engine_connection = create_engine(cls.connection_string)
            logging.info("Created postgres engine")
        return cls._engine_connection

    @property
    def connection_string(cls) -> str:
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            user=cls._pg_credentials.get("username"),
            password=cls._pg_credentials.get("password"),
            host=cls._pg_credentials.get("host"),
            port=cls._pg_credentials.get("port"),
            database=cls._pg_credentials.get("db")
        )


class PGGateway(metaclass=MetaPGGateway):

    @classmethod
    def pd_insert_sql(cls, table: str, df: pd.DataFrame, columns_type: dict = None, replace_table: bool = False):
        logging.info(f'Executing insert {table=} into database')
        df.to_sql(
            name=table,
            con=cls.engine_connection,
            dtype=columns_type,
            replace=replace_table
        )
        logging.info(f'Insert complete')

    @classmethod
    def pd_select_table(cls, table_or_query: str):
        return pd.read_sql(
            sql=table_or_query,
            con=cls.engine_connection
        )