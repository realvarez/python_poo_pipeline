# Project - Base Data Pipeline
## Content
Base pipeline to be deployed in containers
This pipeline get data from a Postgres database, execute a cleansing process and save data in database

## Prepare the environment
To execute this code you will need a postgres database, to develop this process was used a dockerized
database postgresql 11.0.
Its recommended use a virtual environment, you could create a venv and then install the packages required to
the execution of code
```
python -m venv .
source venv/bin/activate
pip install -r requirements.txt
```
## Execution
To execute the process, you must create a .env file in app folder, you can copy the ".envexample" to use and complete 
with your database credentials.<br>

As an example, you could include "CREATE_DATA=True" in .env environment to create a fake dataset.

## Query to extract
The query used to data ingestion can be find in folder "app/utils/query"

```
select id,
       name,
       email,
       date_of_birth,
       address,
       purchase_amount,
       last_purchase
from raw_data
```