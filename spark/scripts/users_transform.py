import os
from pyspark.sql import SparkSession
from dotenv import load_dotenv
from pathlib import Path
from pyspark.sql.functions import col, count, from_json, from_unixtime, sum, window
from pyspark.sql.types import IntegerType, LogType, StringType, StructField, StructType


# Load variable .env file
dotenv_path = Path('/opt/app/.env')
load_dotenv(dotenv_path=dotenv_path)

print("MASUK KE SPARK KAH MANIES?")

# Lnitialize variable service
SPARK_HOST_NAME = os.getenv("SPARK_MASTER_HOST_NAME")
SPARK_PORT = os.getenv("SPARK_MASTER_PORT")
MINIO_USERNAME = os.getenv("MINIO_USERNAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_PORT = os.getenv("MINIO_PORT")

# Configuration sparkSession and minio
spark = SparkSession.builder\
    .appName("Read file transaction parquet from minio")\
    .config("spark.hadoop.fs.s3a.endpoint", f"http://host.docker.internal:{MINIO_PORT}")\
    .config("spark.hadoop.fs.s3a.access.key", MINIO_USERNAME)\
    .config("spark.hadoop.fs.s3a.secret.key", MINIO_PASSWORD)\
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
    .config("spark.hadoop.fs.s3a.path, style.access", "true")\
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")\
    .getOrCreate()


parquet_path_files = "s3a://card-transactions/card-transactions/extract/users/*.parquet"

df = spark.read.parquet(parquet_path_files)
df.show()