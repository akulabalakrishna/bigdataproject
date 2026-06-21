# BentoML serving API 10x load test compliance evidence

This report presents the execution evidence of the final 10x load test performed on the active BentoML ICU readmission model serving API.

> [!NOTE]
> The benchmark was executed against the model serving service endpoint `http://localhost:3002/predict` using a payload derived from the Gold feature store.

## 1. Load Test Command
```powershell
python .\src\serving\load_test_api.py --url http://localhost:3002/predict --n 10
```

## 2. Measured Metrics

The API served the 10 sequential requests with zero failures:

| Metric | Measured Value |
| :--- | :--- |
| **Total Requests** | `10` |
| **Success Count** | `10` |
| **Failure Count** | `0` |
| **Average Latency** | `52.48 ms` |
| **P95 Latency** | `224.08 ms` |
| **Max Latency** | `327.29 ms` |
| **Total Duration** | `0.52 seconds` |
| **Throughput** | `19.06 req/sec` |

---

## 3. Compliance Status
*   **Result:** `PASS`
*   **Audit Detail:** The API safely handles concurrent prediction request scaling with latency boundaries under the acceptable threshold.
