from pyspark.sql import SparkSession
from base import load_config




spark = SparkSession.builder.getOrCreate()
load_config(spark.sparkContext)

data_frame = spark.read.parquet('s3a://card-transactions/extract/users/*.parquet')
data_frame.show()