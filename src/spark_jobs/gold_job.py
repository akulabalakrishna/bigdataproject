from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, lead, datediff, when, count, avg
import os

def run_gold_job():
    spark = SparkSession.builder \
        .appName("ICU_Gold_Job") \
        .getOrCreate()

    # Paths updated for Apache Spark container structure
    silver_path = "/opt/spark/work-dir/data/silver/mimiciii"
    gold_path = "/opt/spark/work-dir/data/gold/mimiciii"
    
    os.makedirs("/opt/spark/work-dir/data/gold", exist_ok=True)

    if not os.path.exists(f"{silver_path}/ADMISSIONS_CLEANED") or not os.path.exists(f"{silver_path}/PATIENTS_CLEANED"):
        print("ERROR: Mandatory tables missing in Silver layer.")
        spark.stop()
        return

    print("Loading mandatory cleaned tables...")
    admissions = spark.read.parquet(f"{silver_path}/ADMISSIONS_CLEANED")
    patients = spark.read.parquet(f"{silver_path}/PATIENTS_CLEANED")

    # Base Join: Admissions + Patients
    df = admissions.join(patients, "SUBJECT_ID", "inner")
    
    # Calculate Age at time of admission
    df = df.withColumn("AGE", (datediff("ADMITTIME", "DOB") / 365.25).cast("int"))
    
    # Filter out records where age is clearly invalid (MIMIC-III encodes ages >89 as 300)
    df = df.filter((col("AGE") >= 0) & (col("AGE") < 120))

    # Readmission Label Logic
    window = Window.partitionBy("SUBJECT_ID").orderBy("ADMITTIME")
    df = df.withColumn("NEXT_ADMITTIME", lead("ADMITTIME").over(window))
    df = df.withColumn("DAYS_TO_NEXT_ADMIT", datediff("NEXT_ADMITTIME", "DISCHTIME"))
    df = df.withColumn("READMISSION_30", when((col("DAYS_TO_NEXT_ADMIT") <= 30) & (col("DAYS_TO_NEXT_ADMIT") >= 0), 1).otherwise(0))

    # Optional Feature: Diagnosis Count
    if os.path.exists(f"{silver_path}/DIAGNOSES_ICD_CLEANED"):
        print("Adding Diagnosis features...")
        diagnoses = spark.read.parquet(f"{silver_path}/DIAGNOSES_ICD_CLEANED")
        diag_counts = diagnoses.groupBy("HADM_ID").agg(count("ICD9_CODE").alias("DIAG_COUNT"))
        df = df.join(diag_counts, "HADM_ID", "left").fillna(0, subset=["DIAG_COUNT"])
    
    # Optional Feature: Procedure Count
    if os.path.exists(f"{silver_path}/PROCEDURES_ICD_CLEANED"):
        print("Adding Procedure features...")
        procedures = spark.read.parquet(f"{silver_path}/PROCEDURES_ICD_CLEANED")
        proc_counts = procedures.groupBy("HADM_ID").agg(count("ICD9_CODE").alias("PROC_COUNT"))
        df = df.join(proc_counts, "HADM_ID", "left").fillna(0, subset=["PROC_COUNT"])

    # Optional Feature: ICU Stay Duration
    if os.path.exists(f"{silver_path}/ICUSTAYS_CLEANED"):
        print("Adding ICU features...")
        icustays = spark.read.parquet(f"{silver_path}/ICUSTAYS_CLEANED")
        icu_stats = icustays.groupBy("HADM_ID").agg(avg("LOS").alias("AVG_ICU_LOS"), count("ICUSTAY_ID").alias("ICU_STAY_COUNT"))
        df = df.join(icu_stats, "HADM_ID", "left").fillna(0, subset=["AVG_ICU_LOS", "ICU_STAY_COUNT"])

    # Select final features
    feature_cols = [
        "SUBJECT_ID", "HADM_ID", "ADMISSION_TYPE", "INSURANCE", 
        "RELIGION", "MARITAL_STATUS", "ETHNICITY", "GENDER", "AGE", "READMISSION_30"
    ]
    
    # Dynamically add optional features if they were joined
    if "DIAG_COUNT" in df.columns: feature_cols.append("DIAG_COUNT")
    if "PROC_COUNT" in df.columns: feature_cols.append("PROC_COUNT")
    if "AVG_ICU_LOS" in df.columns: feature_cols.append("AVG_ICU_LOS")
    if "ICU_STAY_COUNT" in df.columns: feature_cols.append("ICU_STAY_COUNT")

    final_features = df.select(*feature_cols)

    final_features.write.mode("overwrite").parquet(f"{gold_path}/READMISSION_FEATURES")
    print(f"Gold job complete: READMISSION_FEATURES saved to {gold_path}/READMISSION_FEATURES")

    spark.stop()

if __name__ == "__main__":
    run_gold_job()

