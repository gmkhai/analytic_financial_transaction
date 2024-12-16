import os
from dotenv import load_dotenv
from pathlib import Path
from pyspark import SparkContext


# Load variables from .env file
dotenv_path = Path('/opt/.env')
load_dotenv(dotenv_path=dotenv_path)

# Initialize variables for services
SPARK_HOST_NAME = os.getenv("SPARK_MASTER_HOST_NAME")
SPARK_PORT = os.getenv("SPARK_MASTER_PORT")
MINIO_HOST_NAME = os.getenv("MINIO_CONTAINER_NAME")
MINIO_USERNAME = os.getenv("MINIO_USERNAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_PORT = os.getenv("MINIO_PORT")
POSTGRES_HOST_NAME = os.getenv("POSTGRES_CONTAINER_NAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB_WH = os.getenv("POSTGRES_DB_WH")


def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.access.key", f"{MINIO_USERNAME}")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.secret.key", f"{MINIO_PASSWORD}")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.endpoint", f"http://{MINIO_HOST_NAME}:{MINIO_PORT}")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")