from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def run_streaming_demo():
    # Paths for container structure
    checkpoint_path = "/opt/spark/work-dir/data/streaming_demo/checkpoint"
    output_path = "/opt/spark/work-dir/data/streaming_demo/output"

    spark = SparkSession.builder \
        .appName("Kafka_Streaming_Demo") \
        .getOrCreate()

    # Define schema matching the Kafka stream
    schema = StructType([
        StructField("HADM_ID", IntegerType(), True),
        StructField("ADMISSION_TYPE", StringType(), True),
        StructField("ADMITTIME", StringType(), True),
        StructField("DISCHTIME", StringType(), True),
        StructField("INSURANCE", StringType(), True),
        StructField("DIAGNOSIS", StringType(), True)
    ])

    # Read from Kafka
    print("Connecting to Kafka stream 'mimic-admissions'...")
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "mimic-admissions") \
        .option("startingOffsets", "earliest") \
        .load()

    # Parse JSON data
    parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Simple aggregation for demo
    counts_df = parsed_df.groupBy("ADMISSION_TYPE").count()

    # Write to console for demo monitoring
    query_console = counts_df \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    # Write to memory for query proof
    query_memory = counts_df \
        .writeStream \
        .queryName("admission_counts") \
        .outputMode("complete") \
        .format("memory") \
        .start()

    print("Streaming started. Monitoring console output...")
    
    # Run for 60 seconds then stop for demo purposes
    query_console.awaitTermination(60)
    
    print("Demo interval finished. Stopping streaming queries.")
    query_console.stop()
    query_memory.stop()
    spark.stop()

if __name__ == "__main__":
    run_streaming_demo()
