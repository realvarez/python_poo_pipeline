
class Query:
    RAW_EXTRACTION = 'select id, name, email, date_of_birth, address, purchase_amount, last_purchase from raw_data'

    DIC_QUERIES = {
        'raw_data': RAW_EXTRACTION
    }
