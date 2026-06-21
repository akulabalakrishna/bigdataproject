# Video Walkthrough Script (8 Minutes)

This document provides a minute-by-minute speaking script for the Z5008 Big Data Lab project presentation.

---

### **0:00–0:45 | Problem Statement**
*   **Visuals:** Show the README overview / slide introducing the project.
*   **Speech:**
    > "Hello, my name is Akula Balakrishna. Today, I am presenting the Real-Time Clinical Intelligence Platform for 30-Day ICU Readmission Prediction. Intensive Care Unit readmissions represent a critical problem in clinical operations, resulting in heightened patient mortality risk and excessive financial overheads. 
    > Our goal is to leverage advanced Big Data engineering and machine learning tools to ingest real patient data streams, store them in a robust ACID-compliant lakehouse catalog, train predictive models, serve real-time predictions, and monitor API performance live."

---

### **0:45–1:30 | Architecture**
*   **Visuals:** Show the system architecture diagram or flow text.
*   **Speech:**
    > "Our platform consists of an 8-layer architecture designed for data pipelines and MLOps:
    > Ingestion via Apache Kafka; Object Storage using MinIO with Apache Iceberg; Distributed computation using Apache Spark; DAG pipeline orchestration with Apache Airflow; Experiment tracking using MLflow; Model serving via BentoML REST API; and operational monitoring with Prometheus and Grafana. This architecture guarantees a separation of concerns, scalability, and transactional consistency."

---

### **1:30–2:15 | Docker and Airflow**
*   **Visuals:** Show the terminal command `docker compose ps` running and switch to the Airflow UI at `http://localhost:8090`.
*   **Speech:**
    > "Here in my terminal, you can see all 11 microservices are healthy and running via Docker Compose.
    > Switching to the Airflow Web interface on port 8090, we see our pipeline DAG `icu_readmission_real_pipeline`. This DAG orchestrates the entire batch pipeline: `data_check`, `bronze_job`, `silver_job`, `gold_job`, and `train_model`. All tasks succeeded, showing a completed end-to-end data run."

---

### **2:15–3:15 | Kafka and Spark Streaming**
*   **Visuals:** Run the Kafka producer command `python src/ingestion/kafka_producer.py` in one terminal window, and explain the Structured Streaming consumer script.
*   **Speech:**
    > "Now let's demonstrate real-time ingestion. I will trigger the Kafka producer to stream safety-filtered patient admissions from our local gzip dataset into the `mimic-admissions` topic.
    > The producer has successfully pushed the records. Our Spark Structured Streaming job in `src/spark_jobs/streaming_kafka_demo.py` consumes this topic directly, performing windowed aggregations by admission type and writing outputs cleanly back to console and memory sinks."

---

### **3:15–4:00 | MinIO and Iceberg**
*   **Visuals:** Show the MinIO Console bucket list at `http://localhost:9001` under `lakehouse/iceberg-warehouse`.
*   **Speech:**
    > "Our persistent data storage layer utilizes MinIO as an S3-compatible backend. Rather than raw file structures, we implement Apache Iceberg catalogs. 
    > By running `docker exec minio ls -R /data/lakehouse/iceberg-warehouse`, we prove the existence of native Iceberg metadata directories. The Bronze, Silver, and Gold tables are complete with `v1.metadata.json` schema definitions, snapshot Avros, and manifest logs, guaranteeing ACID transactions on object storage."

---

### **4:00–5:00 | Spark MLlib and MLflow**
*   **Visuals:** Switch to the MLflow UI at `http://localhost:5000` showing experiment runs.
*   **Speech:**
    > "With our Gold features prepared in the lakehouse (comprising exactly 56,360 records), we run distributed model training. 
    > In the MLflow UI, we see training runs for Spark MLlib Logistic Regression and Random Forest models logged under the `ICU_Readmission_SparkML_Compliance` experiment. The parameters, training metrics, and models are tracked. The best model is registered inside the MLflow Model Registry."

---

### **5:00–6:00 | BentoML API**
*   **Visuals:** Open a terminal and run the `Invoke-RestMethod` prediction request.
*   **Speech:**
    > "Once registered, models are served via BentoML. The serving container exposes a REST API on port 3002.
    > Let's perform a live prediction check by posting a JSON payload containing clinical parameters such as diagnosis count, length of stay, age, and insurance. The API responds instantly, returning the predicted label, a risk probability score of 0.042, the model name, and the operational classification threshold."

---

### **6:00–7:00 | Grafana and 10× Load Test**
*   **Visuals:** Switch to Grafana at `http://localhost:3000` and trigger the load test script.
*   **Speech:**
    > "To check the system's operational viability, we run a 10x scale API load test. 
    > The script completes successfully with zero failures and an average response time of 52.48 milliseconds.
    > The Prometheus scraper logs these metrics directly, and the Grafana dashboard visualizes request throughput, average response latency, and HTTP status codes in real-time."

---

### **7:00–8:00 | Results and Conclusion**
*   **Visuals:** Show the project audit table or the final reports directory.
*   **Speech:**
    > "In conclusion, our platform successfully achieves all Big Data and MLOps compliance goals. All microservices are containerized, data pipelines are fully automated and orchestrated, and streaming integrations are verified. Unit tests pass with 100% coverage, and data privacy guidelines have been strictly followed with zero patient data tracked in git. 
    > Thank you for your time."
