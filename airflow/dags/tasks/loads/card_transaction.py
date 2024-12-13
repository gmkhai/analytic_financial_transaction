import io
import pandas as pd
import requests
from airflow.models.variable import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_card_transaction():
    response = requests.get(f'http://fastapi:8000/hit-dbt?unique_command=project_akhir_dbt')
    response_result = response.json()
    if response_result.get("status_code") == 200:
        print(f"PUSH DATA TRANSACTIONS TO USING DBT SUCCESS!!!")
    else:
        print(f"PUSH DATA TRANSACTIONS TO USING DBT SUCCESS!!!")