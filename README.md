# Z5008 Big Data Lab - Deliverable 3
## Real-Time Clinical Intelligence Platform for 30-Day ICU Readmission Prediction

### Short Project Summary
End-to-end big data and MLOps pipeline for 30-day ICU readmission prediction using local credentialed MIMIC-III data.

---

### Deliverable 3 Compliance Summary

| Requirement | Implementation Details |
| --- | --- |
| **Docker Compose all services** | Cluster orchestrated via `docker-compose.yml` defining all network services. |
| **Kafka real-data ingestion** | Pseudo real-time Python producer sending safe patient admission records. |
| **MinIO/lakehouse Bronze/Silver/Gold** | Dedicated layered buckets mapped locally storing processed data. |
| **Spark batch ETL** | PySpark Structured ETL pipelines extracting/transforming clinical data. |
| **Spark Structured Streaming** | Continuous windowed stream processing from Kafka `mimic-admissions` topic. |
| **Airflow DAG orchestration** | Fully integrated DAG `icu_readmission_real_pipeline` orchestrating the ETL. |
| **MLflow 5 runs and registry/artifacts** | Grid search with 5 models, registering the best (`LogisticRegression`). |
| **BentoML POST prediction API** | Async REST API accepting live JSON payloads and rendering risk. |
| **Real-data prediction payload** | Executed using valid clinical payload structures from the test split. |
| **10x load test** | API stressed properly reflecting ~24ms response latency. |
| **Prometheus/Grafana monitoring** | Endpoint telemetry actively scraped by Prometheus and configured. |
| **Pytest unit tests** | Validated core API prediction preprocessing logic safely. |
| **Raw data privacy and .gitignore** | Strict `.gitignore` implementations preventing leak of patient data. |

---

### 8-Layer Architecture
1. **Data source:** MIMIC-III local credentialed dataset.
2. **Ingestion:** Kafka producer using MIMIC-derived records.
3. **Storage:** MinIO/lakehouse-style Bronze, Silver, Gold zones.
4. **Processing:** Spark batch and Spark Structured Streaming.
5. **Orchestration:** Airflow DAG.
6. **ML training:** Gold features + MLflow experiment tracking with 5 model runs.
7. **Serving:** BentoML REST API.
8. **Monitoring:** Prometheus/Grafana evidence and API load test.

---

### Tool Stack

| Tool | Purpose |
| --- | --- |
| Python | Core programming language |
| Docker Compose | Container orchestration |
| Kafka & Zookeeper | Real-time event streaming |
| Spark 3.5.1 | Big Data Batch/Streaming processing |
| MinIO | S3-compatible Object Storage |
| Airflow | Workflow orchestration |
| MLflow | Experiment tracking & Model Registry |
| BentoML | Model Serving & REST API |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization dashboard |
| Pytest | Unit testing |

---

### Directory Structure

```text
dags/               # Airflow DAG configurations
src/ingestion/      # Kafka producers
src/spark_jobs/     # Spark batch processing (Bronze/Silver/Gold)
src/training/       # MLflow experiment grid search
src/serving/        # BentoML serving logic
src/monitoring/     # Prometheus configuration
reports/            # Automated evidence logs for Deliverable 3
scripts/            # API load testing automation
tests/              # Pytest unit tests
DELIVERABLE3_LIVE_DEMO_RUNBOOK.md # 8-minute demo runbook
```
*(Note: `data/raw` and `data/minio` are purposely ignored by Git).*

---

### Full Reproducible Local Commands

**Bring Up Infrastructure:**
```bash
docker compose up -d
docker compose ps
```

**Services and Ports:**
*   **Spark UI:** `http://localhost:8080`
*   **MLflow:** `http://localhost:5000`
*   **Airflow:** `http://localhost:8085`
*   **Prometheus:** `http://localhost:9090`
*   **Grafana:** `http://localhost:3001`
*   **BentoML API:** `http://localhost:3002`

---

### Bronze/Silver/Gold Commands

Use Spark cluster mode commands. 

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

**Gold Output Location:**
`data/minio/lakehouse/gold/readmission_features`

---

### MLflow Training Command

*(Using Git Bash locally):*
```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/training/train.py
```
**Evidence:** `reports/mlflow_5_runs_evidence.md`

---

### BentoML Command
```bash
python -m bentoml serve src.serving.service:svc --port 3002
```

---

### Prediction Command
```bash
curl -X POST http://localhost:3002/predict \
  -H "Content-Type: application/json" \
  -d @examples/readmission_prediction_payload.json
```
**Evidence:** `reports/bentoml_prediction_evidence.md`

---

### Load Test Command
```bash
python scripts/load_test_api.py
```
**Evidence:** `reports/api_10x_load_test_evidence.md`

---

### Kafka Commands

*Target Topic: `mimic-admissions`*

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
*(If container name differs, run `docker compose ps` and use the exact Kafka container name).*

---

### Spark Streaming Command
```bash
docker exec spark-master sh -lc "/opt/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --conf spark.jars.ivy=/tmp/.ivy2 \
  /opt/spark/work-dir/src/spark_jobs/streaming_kafka_demo.py"
```
**Evidence:** `reports/spark_structured_streaming_evidence.md`

---

### Airflow Command
```bash
docker exec z5008_readmission_project-airflow-webserver-1 airflow dags list
```
**Evidence:** `reports/airflow_evidence.md`

---

### Monitoring Evidence
- **Prometheus URL:** `http://localhost:9090`
- **Grafana URL:** `http://localhost:3001`
- **Evidence:** `reports/grafana_metrics_evidence.md`

---

### Tests
```bash
python -m pytest -q
```
**Evidence:** `reports/pytest_evidence.md`

---

### MIMIC-III Privacy Notice
- Raw MIMIC-III data is **not** included in this repository.
- Users must obtain credentialed access from PhysioNet.
- `data/raw`, `data/minio`, `mlflow_data`, `models`, and logs are strictly ignored.
- No patient-level raw records are committed to version control.

---

### Local Demo Optimization Note
The full local MIMIC-III dataset was audited. For laptop-safe Deliverable 3 execution, extremely large raw tables such as `CHARTEVENTS`, `NOTEEVENTS`, and `PROCEDUREEVENTS_MV` were deferred in the fast Bronze run, while remaining present locally and documented. The pipeline uses real MIMIC-derived data for Bronze/Silver/Gold, Kafka, MLflow, and BentoML demonstrations.

---

### Evidence Reports List
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

---

### Video Walkthrough
`DELIVERABLE3_LIVE_DEMO_RUNBOOK.md` contains the 8-minute live demo order.

---

### Final Submission Statement
This repository contains source code, Docker configuration, orchestration scripts, pipeline jobs, tests, runbook, and evidence reports only. Raw clinical data and generated lakehouse/model artifacts are intentionally excluded.
