# API Load Test Final Report

## Test Configuration
- **Target URL:** `http://localhost:3002/predict`
- **Model in Service:** `GradientBoosting` (Champion Model version 1)
- **Concurreny/Iteration Model:** Sequential rapid requests (10 iterations)
- **Environment:** Local Docker-Compose API serving container running on BentoML

## Load Test Metrics

| Metric | Measured Value |
| :--- | :--- |
| **Total Requests** | 10 |
| **Success Count** | 10 (100.0% success rate) |
| **Failure Count** | 0 (0.0% failure rate) |
| **Average Latency** | **12.90 ms** |
| **P95 Latency** | **27.77 ms** |
| **Max Latency** | 33.25 ms |
| **Total Duration** | 0.13 seconds |
| **Throughput** | **77.53 requests/second** |

## Summary
The BentoML model serving container shows excellent performance and stability, processing all incoming patient prediction payloads in an average of **12.90 ms** per request with **zero failures** and a throughput of **77.53 req/sec** under sequential load.
