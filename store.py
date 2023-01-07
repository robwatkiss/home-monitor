"""
This module fetches data from collect and stores it in BigQuery.
"""

import logging
import sys

import google.auth
from google.cloud import bigquery

from collect import get_current_state
from settings import BIGQUERY_DATASET, BIGQUERY_TABLE, GCP_PROJECT

# Set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)

DATASET_ID = f"{GCP_PROJECT}.{BIGQUERY_DATASET}"
TABLE_ID = f"{GCP_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"

def get_bq_client():
    # Get credentials
    credentials, project = google.auth.default()

    # Get BigQuery client
    return bigquery.Client(credentials=credentials, project=GCP_PROJECT)

def check_dataset_and_table_exist(client = None):
    if client is None:
        client = get_bq_client()

    # Check if dataset exists
    try:
        # Get dataset if it exists
        dataset = client.get_dataset(DATASET_ID)
    except Exception as e:
        logging.info('Dataset does not exist, creating it')
        logging.info(e)

        # Create dataset if it doesn't exist
        dataset = bigquery.Dataset(DATASET_ID)
        dataset = client.create_dataset(dataset)

    # Get or create table
    try:
        # Get table if it exists
        table = client.get_table(TABLE_ID)
    except Exception as e:
        logging.info('Table does not exist, creating it')
        logging.info(e)

        # Create table if it doesn't exist
        schema = [
            bigquery.SchemaField('location', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('location_id', 'INTEGER', mode='REQUIRED'),
            bigquery.SchemaField('measurement_type', 'STRING', mode='REQUIRED'),
            bigquery.SchemaField('measurement_value_float', 'FLOAT'),
            bigquery.SchemaField('measurement_value_string', 'STRING'),
            bigquery.SchemaField('timestamp', 'TIMESTAMP', mode='REQUIRED')
        ]
        table = bigquery.Table(TABLE_ID, schema=schema)
        table = client.create_table(table)

    return dataset, table

def store_current_state_in_bq():
    # Get BigQuery client
    client = get_bq_client()

    # Check if dataset and table exist
    dataset, table = check_dataset_and_table_exist(client)

    # Get current state
    current_state = get_current_state()

    # Insert data
    logging.info('Inserting data into BigQuery')
    errors = client.insert_rows(table, current_state)

    if errors == []:
        logging.info('Data inserted successfully')

    else:
        logging.error('Data insertion failed')
        logging.error(errors)