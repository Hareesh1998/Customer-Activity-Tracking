from pyspark.sql.types import StructType, StringType, DoubleType
from pyspark.sql.functions import from_json, col

# Define schema
schema = StructType() \
    .add("user_id", StringType()) \
    .add("timestamp", DoubleType()) \
    .add("event_type", StringType()) \
    .add("product_id", StringType()) \
    .add("device_type", StringType())

# Read from Kafka
df_kafka = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "user_activity")
    .load())

# Parse JSON
parsed_df = df_kafka.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write to Delta Lake
parsed_df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/mnt/checkpoints/user_activity") \
    .outputMode("append") \
    .start("/mnt/datalake/user_activity")
