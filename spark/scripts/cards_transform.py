from base import *
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import BooleanType, IntegerType, StringType, StructField, StructType


spark = SparkSession.builder.getOrCreate()
load_config(spark.sparkContext)

# create schema for transactions data parquet
schema = StructType(
    [
        StructField('id', IntegerType(), nullable=False),
        StructField('client_id', IntegerType(), nullable=False),
        StructField('card_brand', StringType(), nullable=False),
        StructField('card_type', StringType(), nullable=False),
        StructField('card_number', StringType(), nullable=False),
        StructField('expires', StringType(), nullable=False),
        StructField('cvv', StringType(), nullable=True),
        StructField('has_chip', BooleanType(), nullable=False),
        StructField('num_cards_issued', StringType(), nullable=True),
        StructField('credit_limit', StringType(), nullable=False),
        StructField('acct_open_date', StringType(), nullable=True),
        StructField('year_pin_last_changed', IntegerType(), nullable=False),
        StructField('card_on_dark_web', StringType(), nullable=False)
    ]
)

# read data parquet from minio
data_frame = spark.read.parquet('s3a://card-transactions/extract/cards/*.parquet', header=True, schema=schema)

# reformat data card_brand, card_type, expires, credit_limit, acct_open_date, card_on_dark_web
df_reformat_card_lower = data_frame\
    .withColumn('card_brand', F.lower(data_frame['card_brand']))\
    .withColumn('card_type', F.lower(data_frame['card_type']))\
    .withColumn('card_on_dark_web', F.lower(data_frame['card_on_dark_web']))

df_reformat_expires = df_reformat_card_lower\
    .withColumn('expires', F.to_timestamp('expires', 'MM/yyyy'))

df_reformat_acct_open_date = df_reformat_expires\
    .withColumn('acct_open_date', F.to_timestamp('acct_open_date', 'MM/yyyy'))

df_reformat_credit_limit = df_reformat_acct_open_date\
    .withColumn('currency', F.regexp_extract(df_reformat_acct_open_date['credit_limit'], r"(\$)", 1))\
    .withColumn('credit_limit', F.regexp_extract(df_reformat_acct_open_date['credit_limit'], r"(-?\d+\.\d+|-?\d+)", 1))\
    .withColumn('credit_limit', F.col('credit_limit').cast("double"))

df_reformat = df_reformat_credit_limit\
    .withColumn('card_on_dark_web', F.when(F.col('card_on_dark_web') == 'no', False).otherwise(True))

# show schema and result reformating data
df_reformat.printSchema()
df_reformat.show()
null_counts = df_reformat.agg(
    *[F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in df_reformat.columns]
)

# show checking missing value all column
null_counts.show()

# configurations to postgres
jdbc_url = f'jdbc:postgresql://{POSTGRES_HOST_NAME}:{POSTGRES_PORT}/{POSTGRES_DB_WH}'
jdbc_properties = {
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD,
    'driver': 'org.postgresql.Driver',
    'stringtype': 'unspecified'
}

# write to table
df_reformat.write.mode('overwrite').jdbc(
    jdbc_url, 
    'public.cards_data', 
    properties=jdbc_properties)

print("DATA WRITE TO WAREHOUSE SUCCESS!!!")