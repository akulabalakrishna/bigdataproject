# Deliverable 3: Big Data Lakehouse Pipeline & Real-Time Analytics
## LIVE DEMO RUNBOOK & VIDEO CHECKLIST

This runbook contains the exact commands required to demonstrate all 8 architectural layers using the full local MIMIC-III dataset.

---

### 1. Environment Startup
Start all Docker containers (Postgres, MinIO, Zookeeper, Kafka, Spark Master/Worker, MLflow, Airflow, Prometheus, Grafana).
```bash
docker compose up -d
docker compose ps
```

### 2. Dataset Audit (Real Data Proof)
Show that the full MIMIC-III dataset is being used locally without committing it.
```bash
# Verify raw dataset files exist and are not in Git
ls -lh data/raw/mimiciii
git status
```

### 3. Spark Batch ETL (Lakehouse: Bronze/Silver/Gold)
Execute the PySpark ETL jobs. They will dynamically read the full MIMIC-III data and write to the MinIO `lakehouse` bucket.
```bash
# Run Bronze Job (Ingest to Lakehouse)
export PROJECT_PATH=$(pwd) && python src/spark_jobs/bronze_job.py

# Run Silver Job (Clean and Format)
export PROJECT_PATH=$(pwd) && python src/spark_jobs/silver_job.py

# Run Gold Job (Feature Engineering)
export PROJECT_PATH=$(pwd) && python src/spark_jobs/gold_job.py
```

### 4. MinIO/Lakehouse Verification
Show the processed data in MinIO bucket storage.
Open your browser to the MinIO Console:
* **URL:** http://localhost:9001
* **Credentials:** admin / adminpassword
* **Action:** Navigate to the `lakehouse` bucket and show the `bronze`, `silver`, and `gold` folders.

### 5. Airflow DAG Demo
Show the orchestrator. The DAG invokes the Spark batch jobs and ML training.
Open your browser to the Airflow UI:
* **URL:** http://localhost:8085
* **Credentials:** admin / adminpassword
* **Action:** Trigger the `icu_readmission_real_pipeline` DAG and show the graph view executing successfully.

### 6. Kafka & Spark Structured Streaming Demo
Demonstrate real-time streaming of hospital admissions.
Open two terminal windows.
**Terminal 1 (Start Spark Streaming Consumer):**
```bash
export PROJECT_PATH=$(pwd) && python src/spark_jobs/streaming_kafka_demo.py
```
**Terminal 2 (Start Kafka Producer):**
```bash
python src/ingestion/kafka_producer.py
```
*Action:* Watch Terminal 1 aggregate the incoming admission streams dynamically.

### 7. MLflow Training (5 Runs) & Registry
Train multiple machine learning models on the gold dataset and log them to MLflow.
```bash
export PROJECT_PATH=$(pwd) && python src/training/train.py
```
Open your browser to MLflow UI:
* **URL:** http://localhost:5000
* **Action:** Show the 5 different model runs (Logistic Regression, Random Forest, Decision Tree, GaussianNB, XGBoost), compare metrics, and show the registered Champion Model.

### 8. BentoML API Serving
Serve the best trained model via BentoML REST API.
```bash
# Optional: run bentoml build to package it
bentoml serve src.serving.service:svc --reload
```
*Wait for the server to start on http://localhost:3000.*

### 9. API Prediction (Real Gold-Layer Row)
Send a POST request with real patient features.
Open another terminal:
```bash
curl -X POST "http://localhost:3000/predict" \
     -H "Content-Type: application/json" \
     -d '{"AGE": 65, "GENDER": "M", "ADMISSION_TYPE": "EMERGENCY", "INSURANCE": "Medicare", "RELIGION": "CATHOLIC", "MARITAL_STATUS": "MARRIED", "ETHNICITY": "WHITE", "DIAG_COUNT": 8, "PROC_COUNT": 3, "AVG_ICU_LOS": 4.5, "ICU_STAY_COUNT": 1}'
```

### 10. 10x Load Test
Execute the load test to prove the REST API's scalability.
```bash
python src/serving/load_test_api.py --n 1000
```
*Action:* Show the throughput and latency metrics in the console output.

### 11. Prometheus/Grafana Evidence
Show the real-time monitoring of the infrastructure and API.
Open your browser to the Grafana UI:
* **URL:** http://localhost:3001
* **Credentials:** admin / admin
* **Action:** Open the dashboard and display the 3 real-time metrics (e.g., API requests, latency, CPU/Memory).

---

## 8-Minute Video Walkthrough Checklist
- [ ] **0:00 - 1:00:** Architecture Overview & Dataset Audit (`data/raw/mimiciii`).
- [ ] **1:00 - 2:00:** Docker Compose up & Airflow DAG execution.
- [ ] **2:00 - 3:00:** PySpark Bronze/Silver/Gold ETL proof and MinIO Lakehouse bucket browsing.
- [ ] **3:00 - 4:00:** Kafka Producer & Spark Structured Streaming console output.
- [ ] **4:00 - 5:00:** MLflow UI, showing 5 distinct experiment runs and Model Registry champion.
- [ ] **5:00 - 6:00:** BentoML serving startup and cURL prediction demo.
- [ ] **6:00 - 7:00:** Load Test execution showing throughput metrics.
- [ ] **7:00 - 8:00:** Grafana Dashboard showing real-time load test spikes and system health.

## Strict Rubric Evidence

**Spark MLlib Path Command:**
```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/training/train_spark_mllib.py
```

**Lakehouse Readiness Report:**
`reports/lakehouse_delta_iceberg_readiness.md`

**Privacy Check Commands:**
```bash
git status --ignored --short data/raw/mimiciii/ADMISSIONS.csv.gz
git status --ignored --short data/minio/lakehouse/bronze/mimiciii/ADMISSIONS
```
