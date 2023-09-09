import logging
from datetime import datetime, date
from app.infra import EnvConfig
from app.source import DataGenerator
from app.source import DataExtractor


def create_fake_data():
    datagen = DataGenerator()
    fake_data = datagen.generate_dummy_data()
    datagen.insert_data(fake_data)


def main():
    today_date = date.today()
    logging.basicConfig(
        filename=None,#f"pipeline{today_date}.log",
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.DEBUG
    )
    EnvConfig()
    if EnvConfig.env.get('CREATE_DATA', True):
        create_fake_data()

    data = DataExtractor.get_data_from_database(query_name='raw_data')


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    logging.info(f"Time Execution: {start_time-end_time}")
