# Load from environment variables
import os
from dotenv import load_dotenv
load_dotenv()

TADO_USERNAME = os.getenv('TADO_USERNAME')
TADO_PASSWORD = os.getenv('TADO_PASSWORD')

GCP_PROJECT = os.getenv('GCP_PROJECT')

BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET')
BIGQUERY_TABLE = os.getenv('BIGQUERY_TABLE')