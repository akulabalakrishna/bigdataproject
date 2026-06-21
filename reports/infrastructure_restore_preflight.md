# Infrastructure Restore Preflight Report

**Timestamp:** 2026-06-21T10:50:00+03:00
**Project:** Real-Time Clinical Intelligence Platform for 30-Day Hospital Readmission Prediction
**Author:** AI Coding Assistant

---

## 1. Files Found
During the initial inspection phase, the following core repository files and assets were identified inside the project directory:

*   **Application Source Code:**
    *   [src/ingestion/data_check.py](file:///e:/Z5008_Readmission_Project/src/ingestion/data_check.py)
    *   [src/ingestion/kafka_producer.py](file:///e:/Z5008_Readmission_Project/src/ingestion/kafka_producer.py)
    *   [src/spark_jobs/bronze_job.py](file:///e:/Z5008_Readmission_Project/src/spark_jobs/bronze_job.py)
    *   [src/spark_jobs/silver_job.py](file:///e:/Z5008_Readmission_Project/src/spark_jobs/silver_job.py)
    *   [src/spark_jobs/gold_job.py](file:///e:/Z5008_Readmission_Project/src/spark_jobs/gold_job.py)
    *   [src/spark_jobs/streaming_kafka_demo.py](file:///e:/Z5008_Readmission_Project/src/spark_jobs/streaming_kafka_demo.py)
    *   [src/training/train.py](file:///e:/Z5008_Readmission_Project/src/training/train.py)
    *   [src/training/train_spark_mllib.py](file:///e:/Z5008_Readmission_Project/src/training/train_spark_mllib.py)
    *   [src/serving/service.py](file:///e:/Z5008_Readmission_Project/src/serving/service.py)
    *   [src/serving/load_test_api.py](file:///e:/Z5008_Readmission_Project/src/serving/load_test_api.py)
    *   [scripts/load_test_api.py](file:///e:/Z5008_Readmission_Project/scripts/load_test_api.py)
    *   [dags/readmission_dag.py](file:///e:/Z5008_Readmission_Project/dags/readmission_dag.py)
    *   [tests/test_features.py](file:///e:/Z5008_Readmission_Project/tests/test_features.py)
    *   [tests/test_serving.py](file:///e:/Z5008_Readmission_Project/tests/test_serving.py)
    *   [examples/readmission_prediction_payload.json](file:///e:/Z5008_Readmission_Project/examples/readmission_prediction_payload.json)
*   **Documentation & Scripts:**
    *   [README.md](file:///e:/Z5008_Readmission_Project/README.md)
    *   [DELIVERABLE3_LIVE_DEMO_RUNBOOK.md](file:///e:/Z5008_Readmission_Project/DELIVERABLE3_LIVE_DEMO_RUNBOOK.md)
    *   [.env](file:///e:/Z5008_Readmission_Project/.env) (Local file preserved)
    *   [.env.example](file:///e:/Z5008_Readmission_Project/.env.example)
*   **External Assets:**
    *   `infrastructure.zip` located in `C:\Users\HP\Downloads\infrastructure.zip`

---

## 2. Files Missing / Requiring Creation
To satisfy the course's infrastructure requirements, the following files must be restored, updated, or created at the project root or relevant subdirectories:

*   **Config Directory:**
    *   `config/prometheus.yml` (Scraper endpoints configuration)
    *   `config/grafana-datasources.yml` (Prometheus datasource provisioning)
    *   `config/grafana-dashboards.yml` (Dashboard provisioning configuration)
    *   `config/spark-defaults.conf` (Spark packages and S3/Iceberg configs)
    *   `config/init-db.sql` (Initialization for `airflow` and `mlflow` PostgreSQL schemas)
*   **Airflow & API Containers:**
    *   `airflow/Dockerfile` (Airflow container with Spark and project requirements)
    *   `api/Dockerfile` (BentoML Model Serving API container)
    *   `requirements-airflow.txt` (Python packages for Airflow tasks)
    *   `requirements-api.txt` (Python packages for BentoML service)
*   **Docker Orchestration:**
    *   `docker-compose.yml` (Unified container composition orchestrating 12 services)
*   **Execution & Control Scripts:**
    *   `scripts/start_infrastructure.ps1` (PowerShell launch orchestrator)
    *   `scripts/stop_infrastructure.ps1` (PowerShell shutdown script)
    *   `scripts/check_infrastructure.ps1` (PowerShell health check script)

---

## 3. Docker Resources Found
The host environment was audited for Docker networks, volumes, images, and container states.

*   **Daemon Status:** Docker Desktop is running and fully accessible.
*   **Containers:** Currently, no containers exist on the host (`docker ps -a` returned empty).
*   **Networks:**
    *   Standard bridge, host, and none networks are present.
    *   Existing network `icu_readmission_network` and `bigdata-net` were detected from previous builds.
*   **Potential Reusable Volumes:**
    The following volumes were discovered from prior project states and can potentially be mapped to preserve data:
    *   `clinical-platform_postgres_data` / `infrastructure_postgres_data`
    *   `clinical-platform_minio_data` / `infrastructure_minio_data`
    *   `clinical-platform_kafka_data` / `infrastructure_kafka_data`
    *   `clinical-platform_prometheus_data` / `infrastructure_prometheus_data`
    *   `clinical-platform_grafana_data` / `infrastructure_grafana_data`
    *   `clinical-platform_airflow_logs` / `infrastructure_airflow_logs`

---

## 4. Port Conflicts
We mapped the default host ports configured in the yml to verify availability:
*   `5432` (PostgreSQL) - Checked. No host processes currently listening.
*   `9000` & `9001` (MinIO S3 & Console) - Checked. Available.
*   `9092` (Kafka External) - Checked. Available.
*   `8080` & `8081` (Spark Master & Worker UI) - Checked. Available.
*   `5000` (MLflow UI) - Checked. Available.
*   `8090` (Airflow Web UI) - Checked. Available.
*   `3002` (BentoML API UI) - Checked. Available.
*   `9090` (Prometheus UI) - Checked. Available.
*   `3000` (Grafana UI) - Checked. Available.

---

## 5. Planned Changes
We plan to restore the entire infrastructure with the following architecture:
1.  **Shared Network:** Map all containers to a single bridge network named `icu_readmission_network`.
2.  **Environment Variables:** Decouple all passwords and server URIs via the local `.env` and `.env.example`.
3.  **Kafka Configuration:** Use a modern KRaft mode Kafka setup (Apache Kafka 3.7.0) with an internal listener at `kafka:29092` for containers and an external listener at `localhost:9092` for the host Windows environment.
4.  **MinIO Buckets:** Automate the creation of `lakehouse`, `mlflow-artifacts`, and `checkpoints` buckets using a startup initialization container.
5.  **Lakehouse Support:** Configure Apache Spark 3.5.1 with Apache Iceberg catalog integrations in `config/spark-defaults.conf`.
6.  **BentoML Container:** Create a custom image to build and package `src/serving/service.py` to expose `/predict`.
7.  **Airflow Custom Container:** Build an Airflow image containing `pyspark`, `mlflow`, `scikit-learn`, `joblib`, and other requirements so Airflow can execute training and ETL steps successfully.
8.  **Prometheus Scraping:** Configure scraping rules targeting Prometheus itself and the BentoML API endpoints.

---

## 6. Risks & Mitigation
*   **Risk 1: Version Mismatch in Spark & Lakehouse Jars:**
    *   *Mitigation:* Explicitly pin the packages for `iceberg-spark-runtime-3.5_2.12:1.5.0` and its companion Hadoop AWS dependencies in `spark-defaults.conf`.
*   **Risk 2: Port 3000 Conflicts with Other Services:**
    *   *Mitigation:* Grafana is mapped to port `3000` while BentoML is mapped to `3002` to avoid host conflicts.
*   **Risk 3: Lost Local Run States:**
    *   *Mitigation:* Named volumes are configured inside the `docker-compose.yml` to prevent data deletion when containers stop.
*   **Risk 4: Windows Execution Policies:**
    *   *Mitigation:* Scripts are written to run with standard PowerShell flags, and the runbook commands will detail bypassing policies using `-ExecutionPolicy Bypass`.
