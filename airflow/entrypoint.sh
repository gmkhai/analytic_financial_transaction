#!/bin/bash
airflow db init
echo "AUTH_ROLE_PUBLIC = 'Admin'" >> webserver_config.py
airflow users create \
    --username airflow \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password airflow
airflow connections add 'postgres_main' \
    --conn-type 'postgres' \
    --conn-login $POSTGRES_USER \
    --conn-password $POSTGRES_PASSWORD \
    --conn-host $POSTGRES_CONTAINER_NAME \
    --conn-port $POSTGRES_PORT \
    --conn-schema $POSTGRES_DB
airflow connections add 'storage_minio_conn' \
    --conn-type 'aws' \
    --conn-login $MINIO_USERNAME \
    --conn-password $MINIO_PASSWORD \
    --conn-extra '{"endpoint_url": "host.docker.internal:$MINIO_PORT"}'
export SPARK_FULL_HOST_NAME="spark://$SPARK_MASTER_HOST_NAME"
airflow connections add 'spark_main' \
    --conn-type 'spark' \
    --conn-host $SPARK_FULL_HOST_NAME \
    --conn-port $SPARK_MASTER_PORT
airflow webserver
