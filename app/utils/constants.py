import sqlalchemy


class Constants:

    SCHEMA_TYPE_RAW_TABLE = {
        'id': sqlalchemy.types.Integer(),
        'name': sqlalchemy.types.VARCHAR(255),
        'email': sqlalchemy.types.VARCHAR(255),
        'date_of_birth': sqlalchemy.DateTime(),
        'address': sqlalchemy.types.VARCHAR(255),
        'purchase_amount': sqlalchemy.DECIMAL(precision=10, scale=2),
        'last_purchase': sqlalchemy.DateTime(),
    }

    SCHEMA_TYPE_CLEANED_TABLE = {
        'id': sqlalchemy.types.Integer(),
        'name': sqlalchemy.types.VARCHAR(255),
        'email': sqlalchemy.types.VARCHAR(255),
        'date_of_birth': sqlalchemy.DateTime(),
        'address': sqlalchemy.types.VARCHAR(255),
        'purchase_amount': sqlalchemy.DECIMAL(precision=10, scale=2),
        'last_purchase': sqlalchemy.DateTime(),
    }