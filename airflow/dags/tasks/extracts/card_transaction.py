import io
import pandas as pd
import requests
from airflow.models.variable import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime


def connection_save_to_minio(data_name: str, month: int, years: int, data_frame):
    """
    Connection minio storage for save data using parquet data
    :param data_name:table name
    :param month: monthly integer value
    :param years: years integer value
    :param data_frame: dataframe from source
    :return:
    """
    output_buffer = io.BytesIO()
    data_frame.to_parquet(output_buffer, engine='pyarrow', index=False)
    output_buffer.seek(0)
    s3_hook = S3Hook(aws_conn_id="storage_minio_conn")
    bucket_name = 'card-transaction'
    s3_key = f'/card-transaction/extract/{data_name}/{month}-{years}.parquet'
    s3_hook.load_bytes(
        bytes_data=output_buffer.getvalue(),
        bucket_name=bucket_name,
        key=s3_key,
        replace=True
    )


def extract_transaction(**kwargs):
    # execution_date = kwargs.get("execution_date")
    # month = execution_date.strftime("%m")
    # years = execution_date.strftime("%Y")
    #
    # response = requests.get(f'http://fastapi:8000/transactions?date={month}-{years}')
    # response_result = response.json()
    # results = None
    # if response_result.get("status_code") == 200:
    #     results = response_result.get("results")
    #
    # if results:
    #     data_frame = pd.read_json(results)
    #     connection_save_to_minio(data_name='transactions', month=month, years=years, data_frame=data_frame)
    #     Variable.set(key='var_extraction_transaction_date', value=execution_date)
    print("YTAMPIL PRLIS")

def extract_card():
    print("HAHAHAH")


def extract_user():
    print("HIHIIHI")