from base import load_config
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import FloatType, IntegerType, StringType, StructField, StructType


spark = SparkSession.builder.getOrCreate()
load_config(spark.sparkContext)

# create schema for transactions data parquet
schema = StructType(
    [
        StructField('id', IntegerType(), nullable=False),
        StructField('current_age', IntegerType(), nullable=False),
        StructField('retirement_age', IntegerType(), nullable=False),
        StructField('birth_year', IntegerType(), nullable=False),
        StructField('birth_month', IntegerType(), nullable=False),
        StructField('gender', StringType(), nullable=False),
        StructField('address', StringType(), nullable=True),
        StructField('latitude', FloatType(), nullable=True),
        StructField('longitude', FloatType(), nullable=True),
        StructField('per_capita_income', StringType(), nullable=True),
        StructField('yearly_income', StringType(), nullable=True),
        StructField('total_debt', StringType(), nullable=True),
        StructField('credit_scode', IntegerType(), nullable=True),
        StructField('num_credit_cards', IntegerType(), nullable=True)
    ]
)

data_frame = spark.read.parquet('s3a://card-transactions/extract/users/*.parquet', header=True, schema=schema)

# reformat data gender, address, per_capita_income, yearly_income, total_debt
df_reformat_lower = data_frame\
    .withColumn('gender', F.lower(data_frame['gender']))\
    .withColumn('address', F.lower(data_frame['address']))

df_reformat_per_capita_income = df_reformat_lower\
    .withColumn('per_capita_income_currency', F.regexp_extract(df_reformat_lower['per_capita_income'], r"(\$)", 1))\
    .withColumn('per_capita_income', F.regexp_extract(df_reformat_lower['per_capita_income'], r"(-?\d+\.\d+|-?\d+)", 1))\
    .withColumn('per_capita_income', F.col('per_capita_income').cast("double"))

df_reformat_yearly_income = df_reformat_per_capita_income\
    .withColumn('yearly_income_currency', F.regexp_extract(df_reformat_per_capita_income['yearly_income'], r"(\$)", 1))\
    .withColumn('yearly_income', F.regexp_extract(df_reformat_per_capita_income['yearly_income'], r"(-?\d+\.\d+|-?\d+)", 1))\
    .withColumn('yearly_income', F.col('yearly_income').cast("double"))

df_reformat = df_reformat_yearly_income\
    .withColumn('total_debt_currency', F.regexp_extract(df_reformat_yearly_income['total_debt'], r"(\$)", 1))\
    .withColumn('total_debt', F.regexp_extract(df_reformat_yearly_income['total_debt'], r"(-?\d+\.\d+|-?\d+)", 1))\
    .withColumn('total_debt', F.col('total_debt').cast("double"))

# show schema and result reformating data
df_reformat.printSchema()
df_reformat.show()
null_counts = df_reformat.agg(
    *[F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c) for c in df_reformat.columns]
)

# show checking missing value all column
null_counts.show()

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
    'public.users_data', 
    properties=jdbc_properties)

print("DATA WRITE TO WAREHOUSE SUCCESS!!!")