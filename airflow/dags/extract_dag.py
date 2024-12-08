from datetime import datetime
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from tasks.extracts.card_transaction import extract_transaction, extract_card, extract_user
from tasks.loads.card_transaction import load_stage_card_transaction, load_warehouse_card_transaction


@dag(
    dag_id='extract_transactions_card_dag',
    start_date=datetime(2010, 1, 1),
    catchup=True,
    description='Extraction from source',
    schedule_interval='@monthly'
)
def extract_transactions_card_dag():
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
        task_id='end_task',
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    start_task >> [extract_card_task, extract_user_task, extract_transaction_task] >> end_task


extract_transactions_card_dag()