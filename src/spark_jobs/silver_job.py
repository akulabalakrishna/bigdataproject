from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, datediff, expr
import os

def run_silver_job():
    spark = SparkSession.builder \
        .appName("ICU_Silver_Job") \
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

    bronze_path = "/opt/spark/work-dir/data/bronze/mimiciii"
    silver_path = "/opt/spark/work-dir/data/silver/mimiciii"
    
    os.makedirs("/opt/spark/work-dir/data/silver", exist_ok=True)

    # Mandatory check
    if not os.path.exists(f"{bronze_path}/ADMISSIONS") or not os.path.exists(f"{bronze_path}/PATIENTS"):
        print("ERROR: Mandatory tables (ADMISSIONS/PATIENTS) missing in Bronze.")
        spark.stop()
        return

    # Clean ADMISSIONS
    print("Cleaning ADMISSIONS...")
    admissions = spark.read.parquet(f"{bronze_path}/ADMISSIONS")
    admissions = admissions.withColumn("ADMITTIME", to_timestamp("ADMITTIME")) \
                           .withColumn("DISCHTIME", to_timestamp("DISCHTIME")) \
                           .withColumn("DEATHTIME", to_timestamp("DEATHTIME"))
    admissions.write.mode("overwrite").parquet(f"{silver_path}/ADMISSIONS_CLEANED")

    # Clean PATIENTS
    print("Cleaning PATIENTS...")
    patients = spark.read.parquet(f"{bronze_path}/PATIENTS")
    patients = patients.withColumn("DOB", to_timestamp("DOB")) \
                       .withColumn("DOD", to_timestamp("DOD"))
    patients.write.mode("overwrite").parquet(f"{silver_path}/PATIENTS_CLEANED")

    # Clean optional tables if they exist
    optional_tables = ["ICUSTAYS", "DIAGNOSES_ICD", "PROCEDURES_ICD"]
    for table in optional_tables:
        if os.path.exists(f"{bronze_path}/{table}"):
            print(f"Cleaning {table}...")
            df = spark.read.parquet(f"{bronze_path}/{table}")
            if table == "ICUSTAYS":
                df = df.withColumn("INTIME", to_timestamp("INTIME")) \
                       .withColumn("OUTTIME", to_timestamp("OUTTIME"))
            df.write.mode("overwrite").parquet(f"{silver_path}/{table}_CLEANED")
        else:
            print(f"INFO: {table} not found in Bronze, skipping Silver cleaning.")

    print(f"Silver job complete. Cleaned tables saved to {silver_path}")
    spark.stop()

if __name__ == "__main__":
    run_silver_job()

