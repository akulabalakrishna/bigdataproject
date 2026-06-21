
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name, lit

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "mimiciii"
BRONZE_DIR = PROJECT_ROOT / "data" / "minio" / "lakehouse" / "bronze" / "mimiciii"

PRIORITY_TABLES = [
    "ADMISSIONS",
    "PATIENTS",
    "ICUSTAYS",
    "DIAGNOSES_ICD",
    "PROCEDURES_ICD",
    "PRESCRIPTIONS",
    "LABEVENTS",
    "D_LABITEMS",
    "D_ICD_DIAGNOSES",
    "D_ICD_PROCEDURES",
    "TRANSFERS",
    "SERVICES",
    "DRGCODES",
    "CPTEVENTS",
    "MICROBIOLOGYEVENTS",
    "OUTPUTEVENTS",
    "INPUTEVENTS_CV",
    "INPUTEVENTS_MV",
    "DATETIMEEVENTS",
    "CALLOUT",
    "CAREGIVERS"
]

DEFERRED_LARGE_TABLES = {
    "CHARTEVENTS",
    "NOTEEVENTS",
    "PROCEDUREEVENTS_MV"
}

def clean_table_name(path):
    return path.name.replace(".csv.gz", "").replace(".csv", "").upper()

def main():
    spark = (
        SparkSession.builder
        .appName("ICU_Bronze_Job")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.files.maxPartitionBytes", "134217728")
        .getOrCreate()
    )

    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(RAW_DIR.glob("*.csv.gz"))
    file_map = {clean_table_name(f): f for f in files}

    ordered_tables = [t for t in PRIORITY_TABLES if t in file_map]
    remaining_tables = [
        t for t in sorted(file_map)
        if t not in ordered_tables and t not in DEFERRED_LARGE_TABLES
    ]

    tables_to_process = ordered_tables + remaining_tables

    print(f"Raw MIMIC files discovered: {len(files)}")
    print(f"Bronze tables selected for fast run: {len(tables_to_process)}")
    print(f"Deferred huge tables: {sorted(DEFERRED_LARGE_TABLES.intersection(file_map))}")

    for table in tables_to_process:
        src = str(file_map[table])
        out = str(BRONZE_DIR / table)

        print(f"Ingesting {table} to Bronze layer...")

        df = (
            spark.read
            .option("header", "true")
            .option("inferSchema", "false")
            .option("mode", "PERMISSIVE")
            .csv(src)
            .withColumn("bronze_ingestion_timestamp", current_timestamp())
            .withColumn("bronze_source_file", input_file_name())
            .withColumn("bronze_table_name", lit(table))
        )

        df.write.mode("ignore").parquet(out)
        print(f"Successfully saved {table} to {out}")

    marker = BRONZE_DIR / "_DEFERRED_LARGE_TABLES.txt"
    marker_text = (
        "Deferred for fast Deliverable 3 local run. Raw files remain available in data/raw/mimiciii:\n"
        + "\n".join(sorted(DEFERRED_LARGE_TABLES.intersection(file_map)))
        + "\n"
    )
    try:
        marker.unlink(missing_ok=True)
        marker.write_text(marker_text)
    except PermissionError:
        print(f"Warning: Could not write marker file (permission denied) — continuing.")

    print("Bronze fast run completed.")
    spark.stop()

if __name__ == "__main__":
    main()
