from base import load_config
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import IntegerType, StringType, StructField, StructType


spark = SparkSession.builder.getOrCreate()
load_config(spark.sparkContext)

# create schema for transactions data parquet
schema = StructType(
    [
        StructField('id', IntegerType(), nullable=False),
        StructField('date', StringType(), nullable=False),
        StructField('client_id', IntegerType(), nullable=False),
        StructField('card_id', IntegerType(), nullable=False),
        StructField('amount', StringType(), nullable=False), # reformating valuee amount
        StructField('merchant_id', IntegerType(), nullable=False),
        StructField('merchant_city', StringType(), nullable=True),
        StructField('merchant_state', StringType(), nullable=True),
        StructField('zip', StringType(), nullable=True), # null fill with online
        StructField('use_chip', StringType(), nullable=True)
    ]
)

# read data parquet from minio
data_frame = spark.read.parquet('s3a://card-transactions/extract/transactions/*.parquet', header=True, schema=schema)

# reformat data schema date, amount, and zip
df_reformat_date = data_frame\
    .withColumn('date', F.to_timestamp('date'))

df_reformat_zip = df_reformat_date\
    .withColumn('zip', F.col('zip').cast('int'))\
    .withColumn('zip', F.col('zip').cast('string'))

df_reformat_fillnull = df_reformat_zip\
    .withColumn('merchant_state', F.when(F.col('merchant_state') == '', 'online').otherwise(F.col('merchant_state')))

df_reformat_fillna = df_reformat_fillnull\
    .fillna({'zip':'online'})

df_reformat_lower = df_reformat_fillna\
    .withColumn('merchant_city', F.lower(df_reformat_fillna['merchant_city']))\
    .withColumn('merchant_state', F.lower(df_reformat_fillna['merchant_state']))\
    .withColumn('use_chip', F.lower(df_reformat_fillna['use_chip']))

# reformat amount column
df_reformat = df_reformat_lower\
    .withColumn('currency', F.regexp_extract(df_reformat_lower['amount'], f"(\$)", 1))\
    .withColumn('amount', F.regexp_extract(df_reformat_lower['amount'], f"(\d+\.\d+|\d+)", 1))

# show schema and result reformating data
df_reformat.printSchema()
df_reformat.show()

# configurations to postgres
jdbc_url = f'jdbc:postgresql://postgres:5432/datawarehouse'
jdbc_properties = {
    'user': 'airflow',
    'password': 'final_project123',
    'driver': 'org.postgresql.Driver',
    'stringtype': 'unspecified'
}

# write to table
df_reformat.write.mode('overwrite').jdbc(
    jdbc_url, 
    'public.transactions_data', 
    properties=jdbc_properties)

print("DATA WRITE TO WAREHOUSE SUCCESS!!!")