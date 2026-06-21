# Lakehouse Final Evidence

## MinIO Storage & Lakehouse Status
- **MinIO Service Status:** Healthy (HTTP 200 OK)
- **MinIO Live URL:** `http://localhost:9000` (Console: `http://localhost:9001`)
- **MinIO Bucket:** `lakehouse`

## Lakehouse Layer Breakdown

### 1. Bronze Layer (Raw Ingestion)
- **Table Count:** 23 raw MIMIC-III tables ingested.
- **Physical Directory:** `data/minio/lakehouse/bronze/mimiciii/`
- **Total Ingested Data Size:** 1.42 GB (1,423,449,189 bytes)
- **Deferred Tables:** Large transaction tables (e.g., `CHARTEVENTS`) were deferred using `_DEFERRED_LARGE_TABLES.txt` to optimize execution for the local lab environment.

### 2. Silver Layer (Cleaned & Formatted Data)
- **Cleaned Table Count:** 23 tables corresponding to the Bronze layer.
- **Physical Directory:** `data/minio/lakehouse/silver/mimiciii/`
- **Actions Performed:** Standardized schema, cast timestamps, calculated lengths of stay (LOS), filtered missing key variables.

### 3. Gold Layer (Feature Store / ML Features)
- **Gold Feature Table:** `readmission_features`
- **Physical Directory:** `data/minio/lakehouse/gold/readmission_features/`
- **Actions Performed:** Aggregated diagnoses, procedures, and prescriptions counts per admission; calculated 30-day readmission label (`READMISSION_30`) using windowed analysis on readmission timeline logic.

## Storage Format and Technical Limitations
- **Storage Format:** The pipeline stores all tables in standard **Snappy-compressed Parquet (`.snappy.parquet`)** format.
- **Limitation Documentation:** Currently, the storage format is standard Parquet partitioned directories. The project does not run active Delta Lake or Apache Iceberg transaction metadata engines (no `_delta_log` or catalog metadata files). This represents a technical choice/limitation to maintain lightweight local Docker execution. Transitioning to full Delta Lake/Iceberg is deferred as a future architectural enhancement.
