import os
from dotenv import load_dotenv
from pathlib import Path
from pyspark import SparkContext


# Load variables from .env file
dotenv_path = Path('/opt/app/.env')
load_dotenv(dotenv_path=dotenv_path)

# Initialize variables for services
SPARK_HOST_NAME = os.getenv("SPARK_MASTER_HOST_NAME")
SPARK_PORT = os.getenv("SPARK_MASTER_PORT")
MINIO_USERNAME = os.getenv("MINIO_USERNAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_PORT = os.getenv("MINIO_PORT")

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.access.key", "admin")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "admin123")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")