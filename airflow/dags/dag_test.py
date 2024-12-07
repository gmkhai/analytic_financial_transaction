from datetime import datetime
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from tasks.extracts.card_transaction import extract_transaction, extract_card, extract_user
from tasks.loads.card_transaction import load_stage_card_transaction, load_warehouse_card_transaction


@dag(
    dag_id='ini_test',
    start_date=datetime.now(), #datetime(2009, 12, 1),
    description="Assignment ETL Spark",
    schedule_interval='1 * * * *'
)
def transaction_card_dag():
    start_task = EmptyOperator(
        task_id='start_task',
    )

    extract_transaction_task = PythonOperator(
        task_id='extract_transaction_task',
        python_callable=extract_transaction
    )

    extract_card_task = PythonOperator(
        task_id='extract_card_task',
        python_callable=extract_card
    )

    extract_user_task = PythonOperator(
        task_id='extract_user_task',
        python_callable=extract_user
    )

    end_task = EmptyOperator(
        task_id='end_task'
    )

    # load_stage_task = PythonOperator(
    #     task_id='load_stage_task',
    #     python_callable=load_stage_card_transaction
    # )

    # load_warehouse_task = PythonOperator(
    #     task_id='load_warehouse_task',
    #     python_callable=load_warehouse_card_transaction
    # )


    start_task >> [extract_card_task, extract_user_task, extract_transaction_task] >> end_task


transaction_card_dag()