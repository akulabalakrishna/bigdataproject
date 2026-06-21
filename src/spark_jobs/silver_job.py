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

    base_dir = os.environ.get("PROJECT_PATH", "/opt/spark/work-dir")
    lakehouse_path = f"{base_dir}/data/minio/lakehouse"
    bronze_path = f"{lakehouse_path}/bronze/mimiciii"
    silver_path = f"{lakehouse_path}/silver/mimiciii"
    
    os.makedirs(silver_path, exist_ok=True)

    # Mandatory check
    if not os.path.exists(f"{bronze_path}/ADMISSIONS") or not os.path.exists(f"{bronze_path}/PATIENTS"):
        print("ERROR: Mandatory tables (ADMISSIONS/PATIENTS) missing in Bronze.")
        spark.stop()
        return

    tables = [d for d in os.listdir(bronze_path) if os.path.isdir(os.path.join(bronze_path, d))]
    
    for table in tables:
        print(f"Cleaning {table}...")
        df = spark.read.parquet(f"{bronze_path}/{table}")
        
        if table == "ADMISSIONS":
            df = df.withColumn("ADMITTIME", to_timestamp("ADMITTIME")) \
                   .withColumn("DISCHTIME", to_timestamp("DISCHTIME")) \
                   .withColumn("DEATHTIME", to_timestamp("DEATHTIME"))
        elif table == "PATIENTS":
            df = df.withColumn("DOB", to_timestamp("DOB")) \
                   .withColumn("DOD", to_timestamp("DOD"))
        elif table == "ICUSTAYS":
            df = df.withColumn("INTIME", to_timestamp("INTIME")) \
                   .withColumn("OUTTIME", to_timestamp("OUTTIME"))
                   
        out_path = f"{silver_path}/{table}_CLEANED"
        df.write.mode("ignore").parquet(out_path)
        print(f"Done: {table}_CLEANED")

    print(f"Silver job complete. Cleaned tables saved to {silver_path}")
    spark.stop()

if __name__ == "__main__":
    run_silver_job()

