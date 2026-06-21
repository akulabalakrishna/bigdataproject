# Grafana Dashboard Final Evidence

## Service Access URLs
- **Prometheus UI:** `http://localhost:9090` (Internal Status: Ready)
- **Grafana UI:** `http://localhost:3000` (Internal Status: Healthy)
- **BentoML API Port:** `http://localhost:3002/metrics` (Prometheus Metrics Target)

## Confirmed Dashboard Panels

The dashboard **"Clinical Readmission API Analytics"** (UID: `readmission_api_dashboard`) has been successfully loaded and configured in Grafana with the following three key performance visualization panels:

### 1. BentoML API Request Count
- **Panel ID:** 1
- **Panel Type:** Time Series (`timeseries`)
- **Metric Query:**
  ```promql
  sum(rate(request_duration_seconds_count[5m])) by (endpoint) or sum(rate(http_request_duration_seconds_count[5m])) by (handler)
  ```
- **Description:** Tracks the volume of incoming API prediction requests per second, grouped by API endpoint handler, to analyze overall platform throughput.

### 2. BentoML API Average Latency (seconds)
- **Panel ID:** 2
- **Panel Type:** Time Series (`timeseries`)
- **Metric Query:**
  ```promql
  (sum(rate(request_duration_seconds_sum[5m])) by (endpoint) / sum(rate(request_duration_seconds_count[5m])) by (endpoint)) or (sum(rate(http_request_duration_seconds_sum[5m])) by (handler) / sum(rate(http_request_duration_seconds_count[5m])) by (handler))
  ```
- **Description:** Calculates and visualizes the rolling average response latency in seconds to monitor the responsiveness and runtime speed of the model serving layer.

### 3. BentoML API HTTP Error Counts
- **Panel ID:** 3
- **Panel Type:** Time Series (`timeseries`)
- **Metric Query:**
  ```promql
  sum(rate(http_request_duration_seconds_count{status=~"[45].*"}[5m])) by (status) or sum(rate(request_duration_seconds_count{status=~"[45].*"}[5m])) by (status) or vector(0)
  ```
- **Description:** Monitors client-side (4xx) and server-side (5xx) HTTP error rates. It defaults to showing `0` when there are no errors, providing immediate visual confirmation of server stability.

## Presentation View Instructions
1. Open your web browser and navigate to `http://localhost:3000`.
2. Log in using `admin` / `adminpassword` (configured in your `.env` file).
3. Search for the dashboard named **"Clinical Readmission API Analytics"**.
4. The dashboard will automatically update every 5 seconds, displaying real-time metrics collected from the BentoML endpoint via Prometheus.
5. If the panels are empty or flat, execute the load test script (`python src/serving/load_test_api.py --n 100`) to generate active request traffic and display the corresponding spike in the panels.
