# Team and Integrity Compliance

This report documents team details, contribution distributions, and academic integrity policies for the Z5008 Big Data Lab Project submission.

## 1. Project Type & Membership
*   **Project Type:** Individual project, as approved/submitted in the official project form.
*   **Student Name:** Akula Balakrishna
*   **IIT Madras Zanzibar ID / Credentials:** `akulabalakrishna0` (PhysioNet credentialed ID)

---

## 2. Contribution Summary
As an individual project, all components were developed, integrated, verified, and submitted by the single student author:
*   **Infrastructure:** Configured and validated the 11 container microservice architecture in Docker Compose.
*   **Data Ingestion:** Created the Kafka stream producer and consumer scripts.
*   **Lakehouse Integration:** Set up Apache Iceberg warehouse configurations and executed parquet to Iceberg schema migrations.
*   **Data Processing:** Built the Spark batch processing scripts (Bronze, Silver, Gold layers) and Spark Structured Streaming.
*   **Pipeline Orchestration:** Engineered the Airflow DAG (`icu_readmission_real_pipeline`).
*   **Model Training:** Wrote training pipelines logging to MLflow using Spark MLlib.
*   **Model Serving:** Built and serving the champion models using BentoML POST REST APIs.
*   **Monitoring & Testing:** Configured Prometheus and Grafana, wrote Pytest test suites, and executed load testing scripts.

---

## 3. Academic Integrity Declarations

### 3.1 AI-Assisted Development Declaration
AI-assisted tools, including ChatGPT and Antigravity, were used for debugging support, code review, documentation assistance, and command generation. All AI-assisted code and configuration changes were reviewed, tested, and understood by the project author before inclusion in the repository.

### 3.2 Open-Source Citations & Acknowledgments
The project integrates and references the following open-source frameworks:
*   **Apache Kafka:** Event streaming ingestion.
*   **Apache Spark:** Distributed data processing, streaming, and MLlib models.
*   **Apache Airflow:** Batch DAG workflow orchestration.
*   **Apache Iceberg:** ACID lakehouse table format.
*   **MinIO:** S3-compatible cloud object storage catalog.
*   **MLflow:** Experiment tracking and model registry storage.
*   **BentoML:** REST API model serving.
*   **Prometheus & Grafana:** Telemetry collection and visualization dashboards.
*   **scikit-learn:** Sklearn baseline models for MLflow comparison.
