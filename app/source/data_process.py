import logging
import string
import re
import datetime
from unicodedata import normalize

import pandas as pd

from app.infra import PGGateway
from app.source import DataExtractor
from app.utils import Constants


class StringProcess:

    @staticmethod
    def remove_especial_characters(_str) -> str:
        str_normalized = normalize(
            'NFC',
            re.sub(
                r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
                r"\1",
                normalize("NFD", _str), 0, re.I
            )
        )
        return str_normalized if isinstance(_str, str) else None

    @staticmethod
    def verify_email(_email: str) -> str | None:
        if isinstance(_email, str):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', _email):
                return _email


class DateProcess:

    @staticmethod
    def verify_past_date(input_date) -> datetime.date | None:
        try:
            _date = input_date
            today = datetime.date.today()
            if _date:
                return _date if _date < today else today
            else:
                return
        except AttributeError:
            logging.error(f'Cant parse {input_date=} as date')
            return


class DataProcess:

    @staticmethod
    def process_name(name: str) -> str:
        return StringProcess.remove_especial_characters(
            string.capwords(name)
        )

    @staticmethod
    def process_address(address: str) -> str:
        return string.capwords(
            address.replace("\n", ", ")
        )

    @staticmethod
    def process_email(email: str) -> str:
        return StringProcess.verify_email(email.lower())

    @staticmethod
    def process_purchase_date(date) -> str:
        return DateProcess.verify_past_date(date)

    @staticmethod
    def process_amount(amount: int) -> int:
        return abs(amount)

    @staticmethod
    def apply_cleaning(df: pd.DataFrame) -> pd.DataFrame:
        try:
            df['name'] = df['name'].apply(DataProcess.process_name)
            df['address'] = df['address'].apply(DataProcess.process_address)
            df['email'] = df['email'].apply(DataProcess.process_email)
            df['purchase_amount'] = df['purchase_amount'].apply(DataProcess.process_amount)
            df['last_purchase'] = df['last_purchase'].apply(DataProcess.process_purchase_date)
            return df
        except AttributeError as err:
            logging.error(f"Error in cleaning {err=}")
            exit()
        except KeyError as err:
            logging.error(f"Error in cleaning {err=}")
            exit()

    @staticmethod
    def execute_process(df: pd.DataFrame):
        df = DataProcess.apply_cleaning(df)
        PGGateway.pd_insert_sql(
            table="cleaned_data",
            df=df,
            columns_type=Constants.SCHEMA_TYPE_CLEANED_TABLE
        )