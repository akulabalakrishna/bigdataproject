from pyspark.sql import SparkSession
import os

def run_bronze_job():
    spark = SparkSession.builder \
        .appName("ICU_Bronze_Job") \
        .config("spark.sql.parquet.int96RebaseModeInWrite", "LEGACY") \
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY") \
        .config("spark.sql.parquet.int96RebaseModeInRead", "LEGACY") \
        .config("spark.sql.parquet.datetimeRebaseModeInRead", "LEGACY") \
        .getOrCreate()

    # Explicitly set configs in the session as well
    spark.conf.set("spark.sql.parquet.int96RebaseModeInWrite", "LEGACY")
    spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
    spark.conf.set("spark.sql.parquet.int96RebaseModeInRead", "LEGACY")
    spark.conf.set("spark.sql.parquet.datetimeRebaseModeInRead", "LEGACY")

    # Paths updated for Apache Spark container structure

    raw_path = "/opt/spark/work-dir/data/raw/mimiciii"
    bronze_path = "/opt/spark/work-dir/data/bronze/mimiciii"
    
    os.makedirs("/opt/spark/work-dir/data/bronze", exist_ok=True)

    # Complete subset tables to process
    complete_tables = [
        "ADMISSIONS", "PATIENTS", "DIAGNOSES_ICD", "PROCEDURES_ICD", 
        "ICUSTAYS", "D_ICD_DIAGNOSES", "D_ITEMS", "D_LABITEMS"
    ]
    
    # Incomplete/Optional tables to skip for now
    incomplete_tables = ["LABEVENTS", "PRESCRIPTIONS", "CHARTEVENTS"]
    
    for table in complete_tables:
        file_path = f"{raw_path}/{table}.csv.gz"
        if os.path.exists(file_path):
            print(f"Ingesting {table} to Bronze layer...")
            df = spark.read.csv(file_path, header=True, inferSchema=True)
            df.write.mode("overwrite").parquet(f"{bronze_path}/{table}")
            print(f"Successfully saved {table} to {bronze_path}/{table}")
        else:
            print(f"WARNING: {table}.csv.gz not found at {file_path}. Skipping optional table.")

    for table in incomplete_tables:
        print(f"WARNING: Skipping {table} (Incomplete/Optional in Subset Mode).")

    spark.stop()

if __name__ == "__main__":
    run_bronze_job()

