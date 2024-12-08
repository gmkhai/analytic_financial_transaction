import io
import pandas as pd
import requests
from airflow.models.variable import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook


def connection_save_to_minio(data_name: str, unique_1: int, unique_2: int, data_frame):
    """
    Connection minio storage for save data using parquet data
    :param data_name:table name
    :param unique_1: unique name 1 integer value
    :param unique_2: unique name 2 integer value
    :param data_frame: dataframe from source
    :return:
    """
    output_buffer = io.BytesIO()
    data_frame.to_parquet(output_buffer, engine='pyarrow', index=False)
    output_buffer.seek(0)
    s3_hook = S3Hook(aws_conn_id="storage_minio_conn")
    bucket_name = 'card-transactions'
    s3_key = f'/extract/{data_name}/{unique_1}-{unique_2}.parquet'
    s3_hook.load_bytes(
        bytes_data=output_buffer.getvalue(),
        bucket_name=bucket_name,
        key=s3_key,
        replace=True
    )

def extract_transaction(**kwargs):
    execution_date = kwargs.get("execution_date")
    month = execution_date.strftime("%m")
    years = execution_date.strftime("%Y")
    
    response = requests.get(f'http://fastapi:8000/transactions?date={month}-{years}')
    response_result = response.json()
    results = None
    if response_result.get("status_code") == 200:
        results = response_result.get("result")
    if results:
        data_frame = pd.DataFrame(results)
        connection_save_to_minio(data_name='transactions', unique_1=month, unique_2=years, data_frame=data_frame)
        Variable.set(key='var_extraction_transaction_date', value=execution_date)
        print(f"PUSH DATA TRANSACTIONS TO STORAGE SUCCESS!!!")

def extract_card():
    var_extraction_card_id = int(Variable.get("var_extraction_card_id", default_var=1))
    limit = 5000
    postgres_hook = PostgresHook(postgres_conn_id="postgres_card_transaction")
    query = """
        SELECT * 
        FROM cards
        ORDER BY id
        LIMIT %s
        OFFSET %s;
    """

    with postgres_hook.get_conn() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (limit, var_extraction_card_id))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data_frame = pd.DataFrame(results, columns=columns)
        if results:
            connection_save_to_minio(data_name='cards', unique_1=var_extraction_card_id, unique_2=var_extraction_card_id+limit, data_frame=data_frame)
            Variable.set(key='var_extraction_card_id', value=var_extraction_card_id+limit)
            print(f"PUSH DATA CARDS TO STORAGE SUCCESS!!!")

def extract_user():
    var_extraction_card_id = int(Variable.get("var_extraction_user_id", default_var=1))
    limit = 5000
    postgres_hook = PostgresHook(postgres_conn_id="postgres_card_transaction")
    query = """
        SELECT * 
        FROM users
        ORDER BY id
        LIMIT %s
        OFFSET %s;
    """

    with postgres_hook.get_conn() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (limit, var_extraction_card_id))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data_frame = pd.DataFrame(results, columns=columns)
        if results:
            connection_save_to_minio(data_name='users', unique_1=var_extraction_card_id, unique_2=var_extraction_card_id+limit, data_frame=data_frame)
            Variable.set(key='var_extraction_user_id', value=var_extraction_card_id+limit)
            print(f"PUSH DATA USERS TO STORAGE SUCCESS!!!")
    