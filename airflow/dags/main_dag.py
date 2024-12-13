from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime


@dag(
    dag_id='main_trigger_dag',
    description='Trigger DAGs for run dag extract, transform, and load',
    schedule_interval='@monthly',
    start_date=datetime(2014, 12, 1),
    catchup=False
)
def main_trigger_dag():
    start_task = EmptyOperator(
        task_id='start_task'
    )

    trigger_extract_dag_task = TriggerDagRunOperator(
        task_id='trigger_extract_dag_task',
        trigger_dag_id='extract_transactions_card_dag',
        wait_for_completion=True
    )

    trigger_tranform_dag_task = TriggerDagRunOperator(
        task_id='trigger_tranform_dag_task',
        trigger_dag_id='transform_transactions_card_dag',
        wait_for_completion=True
    )

    trigger_load_dag_task = TriggerDagRunOperator(
        task_id='trigger_load_dag_task',
        trigger_dag_id='load_transactions_card_dag',
        wait_for_completion=True
    )

    end_task = EmptyOperator(
        task_id='end_task',
    )

    start_task >> trigger_extract_dag_task >> trigger_tranform_dag_task >> trigger_load_dag_task >> end_task


main_trigger_dag()