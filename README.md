# ICU Readmission Prediction Pipeline - Deliverable 2

## 📌 Project Title
**Z5008 Big Data Lab - ICU Readmission Prediction using MIMIC-III**

## 📖 Problem Statement
Hospital readmissions within 30 days are a major driver of healthcare costs and indicate potential gaps in initial care quality. This project builds an end-to-end Big Data and MLOps pipeline to predict 30-day hospital readmissions for ICU patients using the MIMIC-III clinical dataset.

## 🏗️ 8-Layer Architecture
1. **Data Sources**: MIMIC-III Database (Clinical Data, Demographics, Diagnoses, Procedures).
2. **Data Ingestion**: Kafka for streaming ingestion, local file loads for batch.
3. **Data Storage (Data Lake)**: MinIO object storage (S3-compatible) holding Bronze, Silver, and Gold layers.
4. **Data Processing**: Apache Spark for batch ETL and Structured Streaming.
5. **Orchestration**: Apache Airflow managing the DAGs and job scheduling.
6. **Machine Learning**: Scikit-Learn / XGBoost models trained on Gold features.
7. **Model Management**: MLflow tracking experiments, metrics, and model registry.
8. **Serving & Monitoring**: BentoML for model serving, Prometheus for metric scraping, Grafana for dashboarding.

## 🛠️ Tool Stack
| Category | Tool / Technology |
|----------|-------------------|
| **Programming Language** | Python 3.10 |
| **Big Data Processing** | Apache Spark 3.5.1 (PySpark) |
| **Data Lake Storage** | MinIO |
| **Streaming / Messaging** | Apache Kafka & Zookeeper |
| **Orchestration** | Apache Airflow |
| **ML Tracking & Registry** | MLflow |
| **Model Serving (API)** | BentoML |
| **Relational Database** | PostgreSQL 15 |
| **Monitoring & Dashboards** | Prometheus & Grafana |
| **Infrastructure** | Docker Compose |

## 📁 Directory Structure
```
.
├── dags/                  # Airflow pipeline definitions
├── dashboards/            # Grafana dashboard JSON exports
├── data/                  # Sample data instructions (Raw data ignored)
├── docker-compose.yml     # Infrastructure setup for all services
├── models/                # Saved ML artifacts (ignored by git)
├── notebooks/             # Exploratory Data Analysis notebooks
├── reports/               # Auto-generated profiling reports
├── screenshots/           # Evidence of working system
├── src/
│   ├── ingestion/         # Data check scripts and ingestion logic
│   ├── monitoring/        # Prometheus config
│   ├── serving/           # BentoML API definitions
│   ├── spark_jobs/        # Production Spark batch and streaming .py jobs
│   └── training/          # MLflow training scripts
└── tests/                 # Pytest unit tests
```

## ⚙️ Setup Instructions

### 1. Environment Variables
Copy `.env.example` to `.env` and fill in any required passwords.
```bash
cp .env.example .env
```

### 2. Infrastructure Setup
Start all services using Docker Compose:
```bash
docker compose up -d
```
> **Note**: Verify services are running with `docker ps`.

### 3. Dependencies
Install the Python requirements on your local host (or inside a virtual environment):
```bash
python -m pip install -r requirements.txt
```

---

## 🚀 Running the Pipeline

### 1. MinIO Check Command
To verify MinIO is accessible and buckets exist:
```bash
# Wait for MinIO to initialize, then visit http://localhost:9001
curl -I http://localhost:9000
```

### 2. Kafka Producer/Consumer Commands
To interact with Kafka inside the docker container:
```bash
# Create topic
docker exec -it kafka kafka-topics --create --topic icu_admissions --bootstrap-server localhost:9092

# Start Producer
docker exec -it kafka kafka-console-producer --topic icu_admissions --bootstrap-server localhost:9092

# Start Consumer
docker exec -it kafka kafka-console-consumer --topic icu_admissions --from-beginning --bootstrap-server localhost:9092
```

### 3. Spark Batch ETL (Bronze / Silver / Gold)
Process the data sequentially through the Medallion architecture:
```bash
# Bronze Layer: Ingest CSV to Parquet
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/src/spark_jobs/bronze_job.py

# Silver Layer: Clean and transform tables
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/src/spark_jobs/silver_job.py

# Gold Layer: Feature Engineering for Readmission
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/src/spark_jobs/gold_job.py
```

### 4. Spark Streaming Command
To run the Spark streaming job with the Kafka connector and a writable Ivy cache:
```bash
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --conf spark.jars.ivy=/tmp/.ivy2 \
  /opt/spark/work-dir/src/spark_jobs/streaming_kafka_demo.py
```

### 5. MLflow Startup & Training Command
MLflow is running via Docker. To train the model and track it:
```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/training/train.py
```

### 6. BentoML API Command
Start the BentoML service using the module path:
```bash
export PYTHONPATH=$PWD
python -m bentoml serve src.serving.service:svc --reload --host 0.0.0.0 --port 3000
```

### 7. Make a Prediction (Curl)
Test the deployed BentoML API:
```bash
curl -X POST http://localhost:3000/predict \
     -H "Content-Type: application/json" \
     -d '{"AGE": 65, "GENDER": "M", "ADMISSION_TYPE": "EMERGENCY", "INSURANCE": "Medicare", "RELIGION": "CATHOLIC", "MARITAL_STATUS": "MARRIED", "ETHNICITY": "WHITE", "DIAG_COUNT": 8, "PROC_COUNT": 3, "AVG_ICU_LOS": 4.5, "ICU_STAY_COUNT": 1}'
```

### 8. Load Test Command
Use the provided script to simulate traffic:
```bash
python src/serving/load_test_api.py
```

### 9. Run Unit Tests
To run the project tests locally:
```bash
python -m pytest tests -v
```

---

## 📊 Monitoring URLs
- **Spark Master UI**: [http://localhost:8080](http://localhost:8080)
- **Airflow Webserver**: [http://localhost:8085](http://localhost:8085)
- **MinIO Console**: [http://localhost:9001](http://localhost:9001)
- **MLflow UI**: [http://localhost:5000](http://localhost:5000)
- **BentoML Swagger UI**: [http://localhost:3000](http://localhost:3000)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Grafana**: [http://localhost:3001](http://localhost:3001)

---

## 📸 Screenshots List
Evidence of the working system is saved in the `screenshots/` directory:
- `airflow_dag.png`: Airflow pipeline execution.
- `mlflow_experiments.png`: MLflow tracking UI.
- `grafana_dashboard.png`: System monitoring dashboard.
- `spark_ui.png`: Spark job execution DAG.

---

## 🛡️ MIMIC-III Privacy Notice
**DO NOT UPLOAD RAW DATA.** The MIMIC-III dataset contains restricted clinical data governed by PhysioNet. All raw data files (`.csv.gz`, `.parquet`) and subsets in `data/raw`, `data/bronze`, `data/silver`, and `data/gold` are strictly excluded from version control via `.gitignore`. Users must obtain credentialed access from PhysioNet directly to download the dataset.

---

## 🤖 AI Tool Usage Declaration
AI tools (e.g., ChatGPT, Gemini) were utilized during the development of this project for:
- Writing PySpark data transformation boilerplate logic.
- Troubleshooting Docker network connectivity and volume mount issues.
- Generating unit test mock structures and `pytest` scaffolding.
- Structuring Markdown documentation (like this README).

---

## 🚑 Troubleshooting
- **Docker Compose Exit 137**: Increase Docker Desktop memory allocation to at least 8GB.
- **Spark Submit Ivy Error**: If Spark streaming fails to download Kafka dependencies, ensure you pass `--conf spark.jars.ivy=/tmp/.ivy2` so the container has a writable cache path.
- **Port Conflicts**: If port `5432` or `5000` is in use locally, change the port mappings in `docker-compose.yml` or stop local instances of PostgreSQL/MLflow.
