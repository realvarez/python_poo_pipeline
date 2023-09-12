import logging
from datetime import datetime, date
from app.infra import EnvConfig
from app.source import DataGenerator, DataProcess
from app.source import DataExtractor


def create_fake_data():
    datagen = DataGenerator()
    fake_data = datagen.generate_dummy_data()
    datagen.insert_data(fake_data)


def main():
    logging.basicConfig(
        filename=None,
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.DEBUG
    )
    EnvConfig()
    if EnvConfig.env.get('CREATE_DATA', True):
        create_fake_data()
    print('0asd')
    data = DataExtractor.get_data_from_database(query_name='raw_data')
    DataProcess.execute_process(data)


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    logging.info(f"Time Execution: {end_time-start_time}")
