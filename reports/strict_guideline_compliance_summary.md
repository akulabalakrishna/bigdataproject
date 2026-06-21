# Z5008 Readmission Project - Strict Guideline Compliance Summary

This document summarizes the final read-only verification status of all components for the Big Data Lab Deliverable 3 submission.

---

## 1. Compliance Status Matrix

| Component | Status | Evidence / Verification Method | Reference Artifact / Report |
| :--- | :---: | :--- | :--- |
| **Docker Services** | ✅ PASS | `docker compose ps` shows 11/11 services UP. | [FINAL_PRESENTATION_COMMANDS.md](file:///E:/Z5008_Readmission_Project/FINAL_PRESENTATION_COMMANDS.md) |
| **BentoML API** | ✅ PASS | REST POST to `/predict` successfully returns risk scores. | [reports/bentoml_prediction_evidence.md](file:///E:/Z5008_Readmission_Project/reports/bentoml_prediction_evidence.md) |
| **Pytest Suite** | ✅ PASS | `python -m pytest` passes all tests with zero failures. | [reports/pytest_evidence.md](file:///E:/Z5008_Readmission_Project/reports/pytest_evidence.md) |
| **Airflow Orchestrator** | ✅ PASS | Web server (8090) and Scheduler (executing DAGs) are UP. | [reports/airflow_evidence.md](file:///E:/Z5008_Readmission_Project/reports/airflow_evidence.md) |
| **Kafka Ingestion** | ✅ PASS | Topic `mimic-admissions` active, producer/consumer streaming. | [reports/kafka_streaming_evidence.md](file:///E:/Z5008_Readmission_Project/reports/kafka_streaming_evidence.md) |
| **Spark MLlib Training**| ✅ PASS | Spark MLlib pipeline finished; metrics and parameters tracked. | [reports/spark_mllib_compliance_evidence.md](file:///E:/Z5008_Readmission_Project/reports/spark_mllib_compliance_evidence.md) |
| **MLflow Server** | ✅ PASS | Tracking server on port 5000 receives pipeline/Spark ML runs. | [reports/mlflow_final_evidence.md](file:///E:/Z5008_Readmission_Project/reports/mlflow_final_evidence.md) |
| **Model Registry** | ✅ PASS | Registered both Spark MLlib and Sklearn models in MLflow. | [reports/spark_mllib_compliance_evidence.md](file:///E:/Z5008_Readmission_Project/reports/spark_mllib_compliance_evidence.md) |
| **Apache Iceberg** | ✅ PASS | Physical metadata files (`v1.metadata.json`, snapshot & manifest `.avro`) confirmed. | [reports/iceberg_compliance_evidence.md](file:///E:/Z5008_Readmission_Project/reports/iceberg_compliance_evidence.md) |
| **Grafana Monitoring** | ✅ PASS | Analytics dashboard on port 3000 shows active scraped metrics. | [reports/grafana_metrics_evidence.md](file:///E:/Z5008_Readmission_Project/reports/grafana_metrics_evidence.md) |

---

## 2. Key Verification Command Summary & Results

### 2.1 BentoML Serve API
*   **Command:**
    ```powershell
    Invoke-RestMethod -Method Post -Uri "http://localhost:3002/predict" -ContentType "application/json" -InFile ".\examples\readmission_prediction_payload.json"
    ```
*   **Returned Output:**
    ```json
    {
      "risk_score": 0.042204848809428985,
      "prediction": 0,
      "threshold": 0.1,
      "model_name": "GradientBoosting",
      "status": "success"
    }
    ```

### 2.2 Pytest Validation
*   **Command:** `python -m pytest -v`
*   **Output:**
    ```text
    tests/test_features.py::test_readmission_logic PASSED
    tests/test_serving.py::test_bento_prediction_preprocessing PASSED
    ======================== 2 passed in 7.54s ========================
    ```

### 2.3 MLflow Spark MLlib Compliance Runs
*   **Command:**
    ```powershell
    docker exec airflow-scheduler python -c "import mlflow; mlflow.set_tracking_uri('http://mlflow:5000'); e=[x for x in mlflow.search_experiments() if x.name=='ICU_Readmission_SparkML_Compliance'][0]; d=mlflow.search_runs(experiment_ids=[e.experiment_id]); print(d[['run_id','status','tags.mlflow.runName']].to_string())"
    ```
*   **Output:**
    ```text
                                 run_id    status         tags.mlflow.runName
    0  9a5faf0908d7456fb58ceac16c768123  FINISHED       Register_Best_SparkML
    1  806a1ecac1014638a0c5b454b9ab294b  FINISHED        SparkML_RandomForest
    2  9ad47caa3e13470fb72717356d36f4a8  FINISHED  SparkML_LogisticRegression
    ```

### 2.4 Model Registry
*   **Command:**
    ```powershell
    docker exec airflow-scheduler python -c "import mlflow; mlflow.set_tracking_uri('http://mlflow:5000'); c=mlflow.tracking.MlflowClient(); print([(m.name,[v.version for v in m.latest_versions]) for m in c.search_registered_models()])"
    ```
*   **Output:**
    ```text
    [('ICU_Readmission_Real_Model', ['1']), ('ICU_Readmission_SparkML_Model', ['1'])]
    ```

### 2.5 Apache Iceberg Storage Layout
*   **Command:** `docker exec minio ls -R /data/lakehouse`
*   **Output Summary:**
    *   Bronze Table Path: `/data/lakehouse/iceberg-warehouse/bronze/admissions`
    *   Silver Table Path: `/data/lakehouse/iceberg-warehouse/silver/admissions_cleaned`
    *   Gold Table Path: `/data/lakehouse/iceberg-warehouse/gold/readmission_features`
    *   *Confirmed files:* `v1.metadata.json`, snapshot `.avro`, manifest `.avro`, and data `.parquet` files are fully present.

---

## 3. Conclusion & Privacy Compliance

*   **Privacy compliance:** Verified. `.gitignore` prevents tracking of raw clinical data and local database files.
*   **State validation:** The current deployment is verified as fully compliant and ready for final presentation.
