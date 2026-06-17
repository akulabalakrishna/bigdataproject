# Spark Structured Streaming Evidence

The PySpark Structured Streaming job successfully subscribed to the Kafka `mimic-admissions` topic, parsed the JSON stream, performed continuous windowed aggregations on `ADMISSION_TYPE`, and cleanly stopped after writing state to console.

**Command Executed:**
```bash
docker exec spark-master sh -lc "/opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 --conf spark.jars.ivy=/tmp/.ivy2 /opt/spark/work-dir/src/spark_jobs/streaming_kafka_demo.py"
```

**Results:**
The checkpoint location was automatically initialized under `/tmp/temporary-...`, successfully aggregating micro-batches containing real MIMIC records from the Kafka stream. Wait thresholds were respected and gracefully shut down after the demo limit without indefinitely locking resources.
