# Real-Time Clinical Intelligence Platform for 30-Day ICU Readmission Prediction
**Z5008 Big Data Lab · IIT Madras Zanzibar · Even Semester 2026**

---

## 1. Project Title
**Real-Time Clinical Intelligence Platform for 30-Day ICU Readmission Prediction**

---

## 2. Team Member Names and Roll Numbers
*   **Project Type:** Individual project, as approved/submitted in the official project form.
*   **Author:** Akula Balakrishna
*   **PhysioNet Credentialed Account ID:** `akulabalakrishna0`

---

## 3. Problem Statement
ICU readmissions significantly impact clinical outcomes and healthcare resource allocation. Patients readmitted within 30 days of discharge often face higher rates of clinical deterioration, and hospitals face high financial penalties. Predicting these readmission risks in real-time allows clinicians to intervene early, optimize bed management, and plan discharge transitions proactively.

---

## 4. Healthcare Domain and Dataset
*   **Domain:** Clinical Intelligence & Medical Informatics.
*   **Dataset:** MIMIC-III (Medical Information Mart for Intensive Care III) v1.4, containing de-identified clinical records of over 40,000 patient admissions to the Beth Israel Deaconess Medical Center.
*   **Data Integrity & Privacy:** All raw patient-level data files are strictly ignored by `.gitignore` and are not committed to GitHub.

---

## 5. Architecture Diagram
```text
                  ┌──────────────────────────────────────────────────┐
                  │                MIMIC-III SOURCE                  │
                  └────────────────────────┬─────────────────────────┘
                                           │ (Ingestion)
                                           ▼
                  ┌──────────────────────────────────────────────────┐
                  │                 APACHE KAFKA                     │
                  │        (Topic: mimic-admissions on 9092)         │
                  └────────────┬────────────────────────┬────────────┘
                               │                        │ (Streaming)
                               │ (Batch)                ▼
                               │            ┌────────────────────────┐
                               │            │  SPARK STRUCTURED      │
                               │            │  STREAMING (Console)   │
                               │            └────────────────────────┘
                               ▼
                  ┌──────────────────────────────────────────────────┐
                  │                      MinIO                       │
                  │      (lakehouse/iceberg-warehouse bucket)        │
                  │ ┌──────────────────────────────────────────────┐ │
                  │ │ Bronze Layer (Raw Parquet admissions)        │ │
                  │ ├──────────────────────────────────────────────┤ │
                  │ │ Silver Layer (Cleaned & standardized schema)  │ │
                  │ ├──────────────────────────────────────────────┤ │
                  │ │ Gold Layer (Aggregated feature engineering)  │ │
                  │ └──────────────────────────────────────────────┘ │
                  └────────────┬────────────────────────▲────────────┘
                               │                        │
                               ▼                        │
                  ┌─────────────────────────────────────┴────────────┐
                  │               APACHE AIRFLOW                     │
                  │        (DAG Orchestrator on Port 8090)           │
                  └────────────┬────────────────────────┬────────────┘
                               │                        │
                               ▼                        ▼
                  ┌────────────────────────┐┌────────────────────────┐
                  │      MLFLOW SERVER     ││      BentoML API       │
                  │  (Runs, Registry 5000) ││  (Prediction Serv 3002)│
                  └────────────┬───────────┘└───────────┬────────────┘
                               │                        │ (Scrape)
                               ▼                        ▼
                  ┌──────────────────────────────────────────────────┐
                  │              PROMETHEUS & GRAFANA                │
                  │          (Metrics and Dashboards 3000)           │
                  └──────────────────────────────────────────────────┘
```

---

## 6. Official 8-Layer Requirement Mapping

| Guideline Layer | Project Implementation |
|---|---|
| Streaming ingestion | Kafka topic `mimic-admissions` |
| Object storage | MinIO with Apache Iceberg |
| Processing | Spark batch and Structured Streaming |
| Orchestration | Apache Airflow |
| Model training | Spark MLlib |
| Experiment tracking | MLflow experiments and Model Registry |
| Model serving | BentoML REST API in Docker |
| Monitoring | Prometheus and Grafana |

---

## 7. Technology Stack
*   **Core Logic:** Python 3.10
*   **Microservice Runtime:** Docker & Docker Compose
*   **Streaming Platform:** Apache Kafka 3.7 (KRaft mode)
*   **Data Lakehouse warehouse:** MinIO S3 Object Storage
*   **ACID Table Engine:** Apache Iceberg 1.5
*   **Distributed Processing:** Apache Spark 3.5.1
*   **Orchestration Engine:** Apache Airflow 2.8.2
*   **Model Tracking:** MLflow 2.11.0
*   **Model Serving:** BentoML 1.2
*   **Operational Monitoring:** Prometheus 2.50 & Grafana 10.3
*   **Unit Tests:** Pytest 9.0

---

## 8. Prerequisites
*   Windows 10/11 with WSL2 enabled.
*   Docker Desktop running with at least 8GB RAM allocated.
*   Python 3.10+ installed locally on the host.

---

## 9. Environment Setup
Create a `.env` file in the root directory based on `.env.example` to define host paths and environment settings:
```powershell
Copy-Item .env.example .env
```
*(Verify that the paths mapped match your local filesystem parameters).*

---

## 10. `.env.example` Explanation
The `.env.example` file contains the microservices configuration parameters:
*   `PROJECT_BASE_PATH`: The absolute root path to the workspace directory.
*   `POSTGRES_USER` & `POSTGRES_PASSWORD`: The database authorization configurations.
*   `MINIO_ROOT_USER` & `MINIO_ROOT_PASSWORD`: Object storage root credentials.
*   `KAFKA_TOPIC`: Defaults to `mimic-admissions`.
*   `AIRFLOW_PORT`, `API_PORT`, `MLFLOW_PORT`, `GRAFANA_PORT`: The local port mappings.

---

## 11. Docker Compose Startup
Start the entire microservices environment using:
```powershell
docker compose up -d
docker compose ps
```
Verify that all 11 containers are in the `Up` state.

---

## 12. Service URLs

| Service | Local URL | Port | Container Name |
| :--- | :--- | :---: | :--- |
| **Airflow Web UI** | [http://localhost:8090](http://localhost:8090) | 8090 | `airflow-webserver` |
| **MLflow Server** | [http://localhost:5000](http://localhost:5000) | 5000 | `mlflow` |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | 9001 | `minio` |
| **Spark Master UI**| [http://localhost:8080](http://localhost:8080) | 8080 | `spark-master` |
| **BentoML Prediction**| [http://localhost:3002](http://localhost:3002) | 3002 | `api` |
| **Prometheus Server**| [http://localhost:9090](http://localhost:9090) | 9090 | `prometheus` |
| **Grafana UI** | [http://localhost:3000](http://localhost:3000) | 3000 | `grafana` |

---

## 13. Kafka Producer Command
Trigger the local producer to stream records from the raw dataset:
```powershell
python src/ingestion/kafka_producer.py
```
This command reads de-identified admissions and streams them to the `mimic-admissions` topic on `localhost:9092`.

---

## 14. Spark Batch Command
Run a production PySpark job directly on the Spark Cluster:
```powershell
docker exec -w /opt/airflow/project airflow-scheduler spark-submit `
  --master spark://spark-master:7077 `
  src/spark_jobs/gold_job.py
```
This batch script reads the Silver layer and writes feature vectors directly to the Gold Iceberg warehouse.

---

## 15. Spark Structured Streaming Command
Execute the streaming consumer in console query mode:
```powershell
docker exec -w /opt/airflow/project airflow-scheduler spark-submit `
  --jars /opt/airflow/project/jars/spark-sql-kafka-0-10_2.12-3.5.1.jar,/opt/airflow/project/jars/spark-token-provider-kafka-0-10_2.12-3.5.1.jar,/opt/airflow/project/jars/kafka-clients-3.4.1.jar,/opt/airflow/project/jars/commons-pool2-2.11.1.jar `
  src/spark_jobs/streaming_kafka_demo.py
```
This runs a 60-second streaming console aggregation on incoming Kafka records.

---

## 16. Airflow DAG Instructions
1. Navigate to the Airflow UI at `http://localhost:8090`.
2. Locate the DAG named `icu_readmission_real_pipeline`.
3. Unpause the DAG by clicking the toggle button.
4. Click the Trigger DAG button to manually execute the end-to-end processing and model training workflow.

---

## 17. Iceberg/MinIO Verification
Verify the physical metadata structure inside the object storage:
```powershell
docker exec minio ls -R /data/lakehouse/iceberg-warehouse
```
Confirm the presence of `v1.metadata.json`, snapshot `.avro`, and manifest `.avro` files indicating transaction consistency.

---

## 18. Spark MLlib Training Description
The training script executes distributed Model Training on the Gold Iceberg table data. It trains a **Logistic Regression** and a **Random Forest** classifier, evaluates performance using metrics (Accuracy, F1, AUC), and exports models to the local directory:
*   Logistic Regression: `models/spark_mllib/logisticregression`
*   Random Forest: `models/spark_mllib/randomforest`

---

## 19. MLflow Experiment and Registry
Verify tracked models and experiments logged under `ICU_Readmission_SparkML_Compliance` and `ICU_Real_Readmission_Enhanced`:
*   **Runs Check:**
    ```powershell
    docker exec airflow-scheduler python -c "import mlflow; mlflow.set_tracking_uri('http://mlflow:5000'); e=[x for x in mlflow.search_experiments() if x.name=='ICU_Readmission_SparkML_Compliance'][0]; d=mlflow.search_runs(experiment_ids=[e.experiment_id]); print(d[['run_id','status','tags.mlflow.runName']].to_string())"
    ```
*   **Registry Check:**
    ```powershell
    docker exec airflow-scheduler python -c "import mlflow; mlflow.set_tracking_uri('http://mlflow:5000'); c=mlflow.tracking.MlflowClient(); print([(m.name,[v.version for v in m.latest_versions]) for m in c.search_registered_models()])"
    ```

---

## 20. BentoML POST Example
Query the live champion model serving API:
```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:3002/predict" `
  -ContentType "application/json" `
  -InFile ".\examples\readmission_prediction_payload.json"
```

---

## 21. Prometheus and Grafana
Prometheus scrapes operational metrics exposed by the BentoML API. Access Grafana at `http://localhost:3000` (credentials: `admin` / `adminpassword`) and load the **"Clinical Readmission API Analytics"** dashboard to track request throughput, average response latency, and error counts.

---

## 22. Unit Tests
Run the project unit test suite:
```powershell
python -m pytest -v
```
This runs the local Pytest suite checking feature calculations and serving logic.

---

## 23. 10× Load Test
Benchmark the serving API using:
```powershell
python .\src\serving\load_test_api.py --url http://localhost:3002/predict --n 10
```
This evaluates service responsiveness across 10 sequential API calls.

---

## 24. Live Demonstration Order
1. Show system architecture structure.
2. Confirm container health (`docker compose ps`).
3. Demonstrate Airflow DAG workflow run.
4. Run the Kafka stream producer.
5. Demonstrate Spark Structured Streaming console consumer.
6. Verify lakehouse data layers on MinIO.
7. Confirm Apache Iceberg metadata layout.
8. Inspect MLflow training metrics.
9. Verify models inside the Model Registry.
10. Query the prediction API using BentoML.
11. Show Grafana metrics panel charts.
12. Run the 10x load test script.
13. Run the pytest test suite.

---

## 25. Results
*   **Lakehouse features generated:** 56,360 rows of gold features.
*   **Registered Models:** Successful model registry for clinical deployment.
*   **API performance:** latency boundaries average under `60ms` with zero failures.

---

## 26. Limitations
*   *Fast Run Constraints:* Large clinical tables (such as `CHARTEVENTS`) were deferred in local runs due to local memory limits.
*   *WSL2 Overhead:* Local developer execution requires high resource footprints.

---

## 27. AI-Assisted Development Declaration
AI-assisted tools, including ChatGPT and Antigravity, were used for debugging support, code review, documentation assistance, and command generation. All AI-assisted code and configuration changes were reviewed, tested, and understood by the project author before inclusion in the repository.

---

## 28. Open-Source Acknowledgements
We acknowledge and cite the creators of the following open-source technologies used in this pipeline:
*   **Apache Software Foundation:** Kafka, Spark, Airflow, and Iceberg.
*   **MinIO Inc:** Object storage.
*   **MLflow & BentoML:** Machine learning orchestration and serving.
*   **Prometheus & Grafana:** Monitoring and analytics.

---

## 29. Reproducibility Instructions
To reproduce the setup completely on another machine:
1. Clone this repository and check out `main`.
2. Configure `.env` using `.env.example`.
3. Put credentialed `ADMISSIONS.csv.gz` and other tables inside `data/raw/mimiciii/`.
4. Run `docker compose up -d` to spawn microservices.
5. Access the Airflow UI at `http://localhost:8090` and run the DAG to ingest data, execute Iceberg migrations, and train models.
6. Trigger Kafka streaming and query BentoML using the presentation commands.
