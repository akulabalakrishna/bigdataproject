# Prometheus Metrics Evidence

`	ext
# HELP bentoml_api_server_request_total Total number of HTTP requests
# TYPE bentoml_api_server_request_total counter
bentoml_api_server_request_total{endpoint="/predict",http_response_code="200",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_total{endpoint="/predict",http_response_code="500",service_name="icu_readmission_service",service_version="not available"} 51.0
# HELP bentoml_api_server_request_in_progress Total number of HTTP requests in progress now
# TYPE bentoml_api_server_request_in_progress gauge
bentoml_api_server_request_in_progress{endpoint="/predict",service_name="icu_readmission_service",service_version="not available"} 0.0
# HELP bentoml_api_server_request_duration_seconds API HTTP request duration in seconds
# TYPE bentoml_api_server_request_duration_seconds histogram
bentoml_api_server_request_duration_seconds_sum{endpoint="/predict",http_response_code="200",service_name="icu_readmission_service",service_version="not available"} 1.4137264000310097
bentoml_api_server_request_duration_seconds_sum{endpoint="/predict",http_response_code="500",service_name="icu_readmission_service",service_version="not available"} 1.5317003000818659
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.005",service_name="icu_readmission_service",service_version="not available"} 0.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.01",service_name="icu_readmission_service",service_version="not available"} 0.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.025",service_name="icu_readmission_service",service_version="not available"} 1.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.05",service_name="icu_readmission_service",service_version="not available"} 4.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.075",service_name="icu_readmission_service",service_version="not available"} 10.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.1",service_name="icu_readmission_service",service_version="not available"} 10.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.25",service_name="icu_readmission_service",service_version="not available"} 10.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.5",service_name="icu_readmission_service",service_version="not available"} 10.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="0.75",service_name="icu_readmission_service",service_version="not available"} 10.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="1.0",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="2.5",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="5.0",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="7.5",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="10.0",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="200",le="+Inf",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_duration_seconds_count{endpoint="/predict",http_response_code="200",service_name="icu_readmission_service",service_version="not available"} 11.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.005",service_name="icu_readmission_service",service_version="not available"} 0.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.01",service_name="icu_readmission_service",service_version="not available"} 0.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.025",service_name="icu_readmission_service",service_version="not available"} 28.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.05",service_name="icu_readmission_service",service_version="not available"} 46.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.075",service_name="icu_readmission_service",service_version="not available"} 50.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.1",service_name="icu_readmission_service",service_version="not available"} 50.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.25",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.5",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="0.75",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="1.0",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="2.5",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="5.0",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="7.5",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="10.0",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_bucket{endpoint="/predict",http_response_code="500",le="+Inf",service_name="icu_readmission_service",service_version="not available"} 51.0
bentoml_api_server_request_duration_seconds_count{endpoint="/predict",http_response_code="500",service_name="icu_readmission_service",service_version="not available"} 51.0

`
