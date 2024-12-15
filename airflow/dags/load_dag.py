from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
from tasks.loads.card_transaction import load_card_transaction


@dag(
    dag_id = "load_transactions_card_dag",
    description='Extraction from source',
    schedule_interval=None,
    start_date=datetime(2014, 12, 1)
)
def load_transactions_card_dag():
    start_task = EmptyOperator(
        task_id='start_task'
    )

    load_datamart_task = PythonOperator(
        task_id='load_datamart_task',
        python_callable=load_card_transaction
    )

    end_task = EmptyOperator(
        task_id='end_task',
	trigger_rule=TriggerRule.ALL_SUCCESS
    )

    start_task >> load_datamart_task >> end_task

load_transactions_card_dag()
