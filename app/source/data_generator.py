import logging

import pandas as pd
from faker import Faker
from app.infra import PGGateway
from app.utils import Constants


class DataGenerator:
    def __init__(self):
        self.fake = Faker("es-CL")
        self.seed = 0
        Faker.seed(self.seed)

    def generate_dummy_data(self, rows: int = 1000):
        logging.info(f'Generating {rows} rows of data with {self.seed=}')
        data = pd.DataFrame()
        data['id'] = [int(_) for _ in range(rows)]
        data['name'] = [str(self.fake.name()) for _ in range(rows)]
        data['email'] = [str(self.fake.email()) for _ in range(rows)]
        data['date_of_birth'] = [str(self.fake.date_of_birth(minimum_age=18, maximum_age=40)) for _ in range(rows)]
        data['address'] = [str(self.fake.address()) for _ in range(rows)]
        data['purchase_amount'] = [
            float(self.fake.pricetag().replace(u"$\xa0", "").replace(".", "")) for _ in range(rows)
        ]
        data['last_purchase'] = [str(self.fake.date_between(start_date='-1y')) for _ in range(rows)]
        return data

    @staticmethod
    def insert_data(fake_data: pd.DataFrame):
        logging.info(f'Saving fake data into the database')
        PGGateway.pd_insert_sql(
            table='raw_data',
            df=fake_data,
            columns_type=Constants.SCHEMA_TYPE_RAW_TABLE,
            replace_table=True
        )

