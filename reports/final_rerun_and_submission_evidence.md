# Final Rerun & Submission Evidence

**Timestamp:** 2026-06-17 17:00:21
**Commit Hash:** 91cae61f232639b06c447f8dcec57409afa50d6f

## System Health Audit
- **Spark UI (8080):** 200 OK
- **MLflow UI (5000):** 200 OK
- **Airflow UI (8085):** 302 Found
- **Prometheus (9090):** 302 Found
- **Grafana (3001):** 302 Found
- **BentoML (3002):** 200 OK

## ETL and Data Pipeline Pipeline
- **Bronze Layer (MinIO):** Generated 23 tables.
- **Silver Layer (MinIO):** Cleaned 23 tables.
- **Gold Layer (MinIO):** Engineered readmission features successfully generated.

## Streaming & Inference Flow
- **Kafka Topics:** mimic-admissions confirmed active.
- **Structured Streaming:** Spark successfully captured Kafka streams.
- **MLflow:** Training script completed successfully. LogisticRegression selected as champion.
- **Spark MLlib:** Training path script present and verifiable.
- **BentoML Post API:** Running on port 3002.
- **Load Test:** Completed 10x scale test, metrics exported to Prometheus/Grafana.
- **Orchestration:** Airflow pipeline DAG verified.

## Compliance & Code Quality
- **Pytest:** Integration tests passed.
- **Docker Compose:** Config validated securely.
- **Privacy Status:** RAW MIMIC-III data correctly ignored via .gitignore and lakehouse directories fully excluded. No sensitive formats tracked.

## Live Screenshot Capture Note
Screenshots were deferred to the host manual capture list via \eports/screenshot_capture_note.md\ due to terminal sandbox execution.

**STATEMENT OF PRIVACY COMPLIANCE:** No patient-level raw data, source archives, or generated lakehouse storage objects were committed to this repository. The project adheres to strict credentialed safety protocols.
