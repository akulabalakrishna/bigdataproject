# Real-Time Clinical Intelligence Platform for 30-Day ICU Readmission Prediction
**Z5008 Big Data Lab · IIT Madras Zanzibar · Even Semester 2026**

## 1. Project Overview
This project presents an end-to-end Big Data and MLOps system designed for 30-day ICU readmission prediction. The platform operates safely using locally stored, credentialed MIMIC-III clinical datasets to power an automated real-time stream processing and model serving ecosystem.

## 2. Problem Statement
ICU readmissions pose a significant burden on healthcare systems, driving up operational costs and negatively impacting patient survival outcomes. Predicting whether an ICU patient will be readmitted within 30 days of discharge allows healthcare providers to implement targeted interventions, optimize bed allocations, and elevate the overall standard of proactive care.

## 3. System Architecture
The platform is constructed on a scalable, 8-layer architecture:
*   **Data Source:** MIMIC-III local credentialed dataset.
*   **Streaming Ingestion:** Kafka.
*   **Object Storage / Lakehouse:** MinIO-backed Bronze, Silver, and Gold zones.
*   **Processing:** Apache Spark batch processing and Structured Streaming.
*   **Orchestration:** Apache Airflow.
*   **Model Training & Tracking:** Gold features, ML training, MLflow runs, registry, and artifacts.
*   **Serving:** BentoML REST API.
*   **Monitoring:** Prometheus and Grafana.

## 4. Architecture Flow
```text
MIMIC-III Data
→ Kafka Producer
→ MinIO/Lakehouse Bronze Layer
→ Spark Silver Cleaning
→ Spark Gold Feature Engineering
→ MLflow Model Training
→ BentoML Prediction API
→ Prometheus/Grafana Monitoring
```

## 5. Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming logic |
| **Docker Compose** | Containerized service orchestration |
| **Kafka & Zookeeper** | Real-time event streaming layer |
| **Spark 3.5.1** | Distributed Batch and Streaming engine |
| **MinIO** | S3-compatible Object Storage |
| **Airflow** | Pipeline and DAG orchestration |
| **MLflow** | Experiment tracking & Model Registry |
| **BentoML** | Model Serving & REST API |
| **Prometheus** | Metrics collection |
| **Grafana** | Live telemetry visualization dashboard |
| **Pytest** | Application unit testing |

## 6. Repository Structure
```text
dags/               # Airflow DAG orchestrations
src/ingestion/      # Kafka producers
src/spark_jobs/     # Spark batch and streaming processes
src/training/       # Model training scripts via MLflow
src/serving/        # BentoML API definitions
src/monitoring/     # Prometheus configuration
reports/            # Automated evidence logs and compliance reports
scripts/            # API load testing and automation utilities
tests/              # Pytest unit tests
DELIVERABLE3_LIVE_DEMO_RUNBOOK.md # Demonstration runbook
.env.example        # Environment variables template
docker-compose.yml  # Network orchestrator configuration
README.md           # Project documentation
```

## 7. Full System Capabilities

| Capability | Status |
| :--- | :--- |
| Docker Compose launches services | ✅ |
| Kafka streams MIMIC-derived records | ✅ |
| Bronze/Silver/Gold lakehouse layers are generated | ✅ |
| Spark batch jobs run as production `.py` files | ✅ |
| Spark Structured Streaming demo is included | ✅ |
| Airflow DAG orchestrates the pipeline | ✅ |
| MLflow tracks at least 5 experiment runs | ✅ |
| BentoML API accepts POST prediction requests | ✅ |
| Real prediction payload is supported | ✅ |
| 10x load test script is included | ✅ |
| Prometheus/Grafana monitoring evidence is included | ✅ |
| Unit tests are included | ✅ |
| MIMIC-III raw data is protected by `.gitignore` | ✅ |

## 8. Setup Instructions

**Bring Up Infrastructure:**
```bash
docker compose up -d
docker compose ps
```

**Service URLs:**
*   **Spark UI:** `http://localhost:8080`
*   **MLflow UI:** `http://localhost:5000`
*   **Airflow UI:** `http://localhost:8085`
*   **MinIO Console:** `http://localhost:9001`
*   **Prometheus:** `http://localhost:9090`
*   **Grafana:** `http://localhost:3001`
*   **BentoML API:** `http://localhost:3002`

## 9. Running the Pipeline

**Bronze Job:**
```bash
docker exec -d spark-master sh -lc '
cd /opt/spark/work-dir &&
mkdir -p outputs/logs &&
nohup /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --driver-memory 2g \
  --executor-memory 2g \
  --conf spark.sql.shuffle.partitions=4 \
  src/spark_jobs/bronze_job.py \
  > outputs/logs/bronze_run.log 2>&1 &
'
```

**Silver Job:**
```bash
docker exec -d spark-master sh -lc '
cd /opt/spark/work-dir &&
mkdir -p outputs/logs &&
nohup /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --driver-memory 2g \
  --executor-memory 2g \
  --conf spark.sql.shuffle.partitions=4 \
  src/spark_jobs/silver_job.py \
  > outputs/logs/silver_run.log 2>&1 &
'
```

**Gold Job:**
```bash
docker exec -d spark-master sh -lc '
cd /opt/spark/work-dir &&
mkdir -p outputs/logs &&
nohup /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --driver-memory 2g \
  --executor-memory 2g \
  --conf spark.sql.shuffle.partitions=4 \
  src/spark_jobs/gold_job.py \
  > outputs/logs/gold_run.log 2>&1 &
'
```
*Gold Output Location:* `data/minio/lakehouse/gold/readmission_features`

## 10. Kafka Streaming Demo

**Producer:**
```bash
python src/ingestion/kafka_producer.py
```

**Consumer:**
```bash
docker exec z5008_readmission_project-kafka-1 kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic mimic-admissions \
  --from-beginning \
  --max-messages 5
```
*(Note: If the Kafka container name differs, run `docker compose ps` and use the actual Kafka container name).*

## 11. Spark Structured Streaming Demo
```bash
docker exec spark-master sh -lc "/opt/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --conf spark.jars.ivy=/tmp/.ivy2 \
  /opt/spark/work-dir/src/spark_jobs/streaming_kafka_demo.py"
```

## 12. Model Training and MLflow
```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/training/train.py
```
*Evidence:* `reports/mlflow_5_runs_evidence.md`

## 13. BentoML API
**Serve Model:**
```bash
python -m bentoml serve src.serving.service:svc --port 3002
```

**Prediction Payload:**
```bash
curl -X POST http://localhost:3002/predict \
  -H "Content-Type: application/json" \
  -d @examples/readmission_prediction_payload.json
```
*Evidence:* `reports/bentoml_prediction_evidence.md`

## 14. Load Test
```bash
python scripts/load_test_api.py
```
*Evidence:* `reports/api_10x_load_test_evidence.md`

## 15. Airflow Orchestration
```bash
docker exec z5008_readmission_project-airflow-webserver-1 airflow dags list
```
*Evidence:* `reports/airflow_evidence.md`

## 16. Monitoring
*   **Prometheus:** `http://localhost:9090`
*   **Grafana:** `http://localhost:3001`

*Evidence:* `reports/grafana_metrics_evidence.md`

## 17. Tests
```bash
python -m pytest -q
```
*Evidence:* `reports/pytest_evidence.md`

## 18. Evidence Reports
The following project evidence reports document operational executions and architectural compliance natively generated during runtime:
*   `reports/final_guideline_crosswalk.md`
*   `reports/deliverable3_strict_guideline_compliance_checklist.md`
*   `reports/deliverable3_pipeline_compatibility_audit.md`
*   `reports/mlflow_5_runs_evidence.md`
*   `reports/bentoml_prediction_evidence.md`
*   `reports/api_10x_load_test_evidence.md`
*   `reports/kafka_real_data_ingestion_evidence.md`
*   `reports/spark_structured_streaming_evidence.md`
*   `reports/airflow_evidence.md`
*   `reports/grafana_metrics_evidence.md`
*   `reports/pytest_evidence.md`

## 19. MIMIC-III Data Privacy Notice
*   **Raw MIMIC-III data is not included in this repository.**
*   Users must obtain credentialed access directly from PhysioNet.
*   `data/raw`, `data/minio`, `mlflow_data`, `models`, logs, and large artifacts are intentionally ignored via Git.
*   No patient-level raw records are committed.
*   Only source code, configs, scripts, tests, runbook, and evidence reports are pushed.

## 20. Local Demo Optimization Note
The full local MIMIC-III dataset was thoroughly audited. For laptop-safe execution, extremely large raw tables such as `CHARTEVENTS`, `NOTEEVENTS`, and `PROCEDUREEVENTS_MV` were deferred in the fast local Bronze run, while remaining present locally and fully documented. The pipeline still completely demonstrates real MIMIC-derived data flow through Kafka, lakehouse layers, Spark jobs, MLflow, and BentoML.

## 21. AI Tool Usage Declaration
AI coding assistants were used for documentation drafting, debugging guidance, and code review support. All generated code was reviewed, executed, and comprehensively validated by the project author.
