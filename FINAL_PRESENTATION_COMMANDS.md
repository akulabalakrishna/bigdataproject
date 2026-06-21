# FINAL PRESENTATION RUNBOOK

This sheet contains the exact commands and URLs for the live demonstration sequence of the **Real-Time Clinical Intelligence Platform for 30-Day Hospital Readmission Prediction**.

## Live Demo Sequence (8 Minutes)

### 1. Show Infrastructure Status (30 Seconds)
Verify all microservices are healthy and running:
```powershell
docker compose ps
```

### 2. Show Airflow Orchestrated DAG (1 Minute)
Open the Airflow Web UI to demonstrate the successful execution of the complete batch ETL and training pipeline:
- **URL:** http://localhost:8090
- **Credentials:** `admin` / `adminpassword`
- **Actions to Show:**
  - Locate DAG: `icu_readmission_real_pipeline`
  - Show the Tree/Graph view with all tasks marked green (Success):
    - `data_check`
    - `bronze_job`
    - `silver_job`
    - `gold_job`
    - `train_model`

### 3. Browse Lakehouse Storage (1 Minute)
Demonstrate data persistence in the MinIO S3 object storage Lakehouse:
- **URL:** http://localhost:9001
- **Credentials:** `admin` / `adminpassword`
- **Folders to Show:**
  - Bucket: `lakehouse`
  - Navigate and explain:
    - `bronze/` - Raw parquet tables ingested (1.42 GB, 23 tables).
    - `silver/` - Cleaned & type-standardized parquet tables.
    - `gold/` - Feature store containing aggregated ML features (`readmission_features`).

### 4. Inspect MLflow Runs & Model Registry (1.5 Minutes)
Demonstrate experimentation tracking, metrics, and models registry:
- **URL:** http://localhost:5000
- **Actions to Show:**
  - Select experiment: **`ICU_Real_Readmission_Enhanced`**
  - Show the 5 classifier runs (LogisticRegression, RandomForest, DecisionTree, GaussianNB, GradientBoosting) and their logged metrics (F1, Accuracy, ROC-AUC).
  - Click on **Models** in the top navigation bar to display the registered model **`ICU_Readmission_Real_Model`** Version 1.

### 5. Send Real-Time Kafka Stream (1 Minute)
Ingest a live batch of clinical admissions using the stream producer:
```powershell
python src/ingestion/kafka_producer.py
```
*Note: This streams 20 real admission events into the topic `mimic-admissions`.*

### 6. Show Spark Structured Streaming (1 Minute)
Demonstrate the consumer aggregating incoming Kafka records in real-time:
```powershell
docker exec -w /opt/airflow/project airflow-scheduler spark-submit `
  --jars /opt/airflow/project/jars/spark-sql-kafka-0-10_2.12-3.5.1.jar,/opt/airflow/project/jars/spark-token-provider-kafka-0-10_2.12-3.5.1.jar,/opt/airflow/project/jars/kafka-clients-3.4.1.jar,/opt/airflow/project/jars/commons-pool2-2.11.1.jar `
  src/spark_jobs/streaming_kafka_demo.py
```
*Note: This runs a 60-second console aggregation query displaying counts by ADMISSION_TYPE.*

### 7. Call BentoML API for Live Prediction (1 Minute)
Query the active champion model serving API using a patient payload:
```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:3002/predict" `
  -ContentType "application/json" `
  -InFile ".\examples\readmission_prediction_payload.json"
```

### 8. View Grafana Dashboards (1 Minute)
Show real-time API operational metrics:
- **URL:** http://localhost:3000
- **Credentials:** `admin` / `adminpassword`
- **Actions to Show:**
  - Open Dashboard: **"Clinical Readmission API Analytics"**
  - Show the three active panels (API Request Count, Average Latency, HTTP Error Counts).

---

## Service URLs Quick Reference

| Service | Host URL | Port | Container Name |
| :--- | :--- | :--- | :--- |
| **Airflow** | [http://localhost:8090](http://localhost:8090) | 8090 | `airflow-webserver` |
| **MLflow** | [http://localhost:5000](http://localhost:5000) | 5000 | `mlflow` |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | 9001 | `minio` |
| **Spark Master UI** | [http://localhost:8080](http://localhost:8080) | 8080 | `spark-master` |
| **BentoML API** | [http://localhost:3002](http://localhost:3002) | 3002 | `api` |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | 9090 | `prometheus` |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | 3000 | `grafana` |
