# Kafka and Spark Structured Streaming Evidence

## Ingestion Architecture
- **Kafka Topic:** `mimic-admissions`
- **Kafka Bootstrap Server:** `kafka:29092` (internal), `localhost:9092` (external)
- **Spark Structured Streaming Consumer:** `src/spark_jobs/streaming_kafka_demo.py`
- **Data Ingestion Script:** `src/ingestion/kafka_producer.py`

## Execution Results

### 1. Ingestion of Real Patient Records
We ran the Kafka producer on the host machine to stream 20 real patient admission records from the MIMIC-III `ADMISSIONS.csv.gz` dataset:
```
Connecting to Kafka at ['localhost:9092']...
Connected to Kafka successfully.
Reading real data from E:/Z5008_Readmission_Project/data/raw/mimiciii/ADMISSIONS.csv.gz...
Sending to topic: mimic-admissions
Starting stream of 20 safety-filtered records...
Sent 20 records successfully...
============================================================
STREAMING COMPLETE
Sent 20 records successfully to mimic-admissions
============================================================
```

### 2. Spark Structured Streaming Consumer Processing
The Spark Structured Streaming job was executed inside the `airflow-scheduler` container. It processed the 20 incoming messages from the Kafka stream and aggregated them by `ADMISSION_TYPE`.

The streaming engine made the following progress on batch execution:
- **Input Rows Received:** 20
- **Aggregated Groups Outputted:** 4 distinct admission types (e.g., EMERGENCY, ELECTIVE, etc.)
- **Execution Status:** Successfully processed 20 events and terminated gracefully after the 60-second demonstration interval.

#### Micro-Batch Execution Log Snippet:
```json
{
  "id" : "5fef2a01-756d-4daf-be7c-4be0479ad163",
  "runId" : "8305605f-7289-41ec-acfa-874815daca30",
  "name" : "admission_counts",
  "timestamp" : "2026-06-21T18:33:36.658Z",
  "batchId" : 0,
  "numInputRows" : 20,
  "inputRowsPerSecond" : 0.0,
  "processedRowsPerSecond" : 1.2311480455524777,
  "stateOperators" : [ {
    "operatorName" : "stateStoreSave",
    "numRowsTotal" : 4,
    "numRowsUpdated" : 4,
    "memoryUsedBytes" : 1880
  } ],
  "sources" : [ {
    "description" : "KafkaV2[Subscribe[mimic-admissions]]",
    "startOffset" : null,
    "endOffset" : {
      "mimic-admissions" : {
        "0" : 20
      }
    },
    "numInputRows" : 20
  } ],
  "sink" : {
    "description" : "MemorySink",
    "numOutputRows" : 4
  }
}
```
