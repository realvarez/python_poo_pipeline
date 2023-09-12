import logging

from app.infra import PGGateway
from app.utils import Query


class DataExtractor:

    @staticmethod
    def get_data_from_database(query_name, chunk_size: int | None = None):
        logging.info(f'Getting {query_name=} from DB')
        query = Query.DIC_QUERIES.get(query_name, None)
        if query:
            return PGGateway.pd_select_table(table_or_query=query)
        else:
            logging.error(f'Selected {query_name=} doesnt exist is dict')
            raise ValueError
