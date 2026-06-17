# Lakehouse Delta/Iceberg Readiness Architecture

**Overview:**
The Z5008 Big Data Lab architecture currently implements a localized laptop-safe storage paradigm utilizing native PySpark Parquet extraction. This document outlines the structured compliance roadmap transitioning this architecture toward full ACID-compliant Delta Lake or Apache Iceberg deployments natively within the MinIO cluster.

## Current Working Storage Architecture
- **Format:** Native Columnar `Parquet`
- **Bronze Zone:** `data/minio/lakehouse/bronze/mimiciii/`
- **Silver Zone:** `data/minio/lakehouse/silver/mimiciii/`
- **Gold Zone:** `data/minio/lakehouse/gold/readmission_features/`
- **Why Parquet?** Operating distributed Apache Delta or Iceberg frameworks inside lightweight localized Docker footprints induces significant dependency complexity on local developer hardware. Standard Parquet allows identical API ingestion logic (`spark.read.parquet`) simulating lakehouse layer progression while preserving critical computational memory natively.

## Strict Extension: Delta Lake Implementation Strategy
To enforce ACID transactional compliances mirroring production lakehouse designs, the pipeline requires exactly two modifications:

1.  **Dependency Addition:**
    Inject `--packages io.delta:delta-spark_2.12:3.1.0` and `--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension` into the Spark Submit configuration payloads.
2.  **API Translation:**
    Modify PySpark dataframe sinks natively in `bronze_job.py`, `silver_job.py`, and `gold_job.py`:
    *From:* `df.write.mode("overwrite").parquet("...")`
    *To:* `df.write.format("delta").mode("overwrite").save("...")`

## Strict Guideline Note
The current framework explicitly mimics a tiered Object Storage Lakehouse data progression (Bronze -> Silver -> Gold). While strict `Delta`/`Iceberg` protocols are architecturally prepared for deployment (as detailed above), they are natively disabled locally to ensure stable out-of-the-box Windows Docker interoperability for demo purposes.
