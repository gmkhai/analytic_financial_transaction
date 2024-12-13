from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta


datetime_days_ago = datetime.now() - timedelta(days=1)

@dag(
    dag_id = "transform_transactions_card_dag",
    description='Extraction from source',
    schedule_interval=None,
    start_date=datetime(2014, 12, 1)
)
def transform_transactions_card_dag():
    stark_task = EmptyOperator(
        task_id='start_task',
    )

    transform_transaction_task = SparkSubmitOperator(
        task_id='transform_transaction_task',
        application="/spark/transactions_transform.py",
        jars="/opt/spark/jars/hadoop-aws-3.3.4.jar,/opt/spark/jars/aws-java-sdk-bundle-1.12.565.jar,/opt/spark/jars/postgresql-42.2.18.jar",
        conn_id='spark_main'
    )

    tranform_card_task = SparkSubmitOperator(
        task_id='transform_card_task',
        application="/spark/cards_transform.py",
        jars="/opt/spark/jars/hadoop-aws-3.3.4.jar,/opt/spark/jars/aws-java-sdk-bundle-1.12.565.jar,/opt/spark/jars/postgresql-42.2.18.jar",
        conn_id='spark_main'
    )

    tranform_user_task = SparkSubmitOperator(
        task_id='tranform_user_task',
        application="/spark/users_transform.py",
        jars="/opt/spark/jars/hadoop-aws-3.3.4.jar,/opt/spark/jars/aws-java-sdk-bundle-1.12.565.jar,/opt/spark/jars/postgresql-42.2.18.jar",
        conn_id='spark_main'
    )

    end_task = EmptyOperator(
        task_id='end_task',
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    stark_task >> [transform_transaction_task, tranform_card_task, tranform_user_task] >> end_task

transform_transactions_card_dag()