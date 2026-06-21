# ================================================================
# Z5008 Big Data Lab — Infrastructure Health Check Script
# ================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Auditing Real-Time Clinical Intelligence Stack Health Status" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# 1. Docker Compose status
Write-Host "`n[1/3] Docker Compose Container Status:" -ForegroundColor Yellow
docker compose ps

# Helper function to check TCP connection
function Test-Port ($HostName, $Port, $ServiceName) {
    $conn = New-Object System.Net.Sockets.TcpClient
    $success = $false
    try {
        $asyncResult = $conn.BeginConnect($HostName, $Port, $null, $null)
        $success = $asyncResult.AsyncWaitHandle.WaitOne(2000, $false)
        if ($success) {
            $conn.EndConnect($asyncResult)
        }
    } catch {
        # ignore
    } finally {
        if ($conn.Connected) {
            $conn.Close()
            $success = $true
        }
    }
    if ($success) {
        Write-Host "  [+] Service '$ServiceName' on port $Port is REACHABLE." -ForegroundColor Green
        return $true
    } else {
        Write-Host "  [-] Service '$ServiceName' on port $Port is UNREACHABLE." -ForegroundColor Red
        return $false
    }
}

# Helper function to check HTTP status
function Test-HttpEndpoint ($Url, $ServiceName) {
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        $statusCode = $response.StatusCode
        if ($statusCode -eq 200 -or $statusCode -eq 302 -or $statusCode -eq 401) {
            Write-Host "  [+] HTTP endpoint '$ServiceName' ($Url) responded with status $statusCode." -ForegroundColor Green
            return $true
        } else {
            Write-Host "  [-] HTTP endpoint '$ServiceName' ($Url) responded with unexpected status $statusCode." -ForegroundColor Yellow
            return $false
        }
    } catch {
        # Check if it was a 401 Unauthorized or similar (which means server is alive)
        if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
            $statusCode = [int]$_.Exception.Response.StatusCode
            Write-Host "  [+] HTTP endpoint '$ServiceName' ($Url) responded with status $statusCode." -ForegroundColor Green
            return $true
        }
        Write-Host "  [-] HTTP endpoint '$ServiceName' ($Url) failed to respond: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# 2. Port Connectivity Check
Write-Host "`n[2/3] Performing TCP Port Connectivity Audit..." -ForegroundColor Yellow
$postgresOk = Test-Port "localhost" 5432 "PostgreSQL"
$minioOk = Test-Port "localhost" 9000 "MinIO S3 API"
$minioConsoleOk = Test-Port "localhost" 9001 "MinIO Web Console"
$kafkaOk = Test-Port "localhost" 9092 "Kafka Broker (External)"
$sparkMasterOk = Test-Port "localhost" 7077 "Spark Master (Internal)"
$sparkUiOk = Test-Port "localhost" 8080 "Spark Master Web UI"
$mlflowOk = Test-Port "localhost" 5000 "MLflow UI"
$airflowOk = Test-Port "localhost" 8090 "Airflow Webserver UI"
$apiOk = Test-Port "localhost" 3002 "BentoML API Port"
$prometheusOk = Test-Port "localhost" 9090 "Prometheus Web UI"
$grafanaOk = Test-Port "localhost" 3000 "Grafana Web UI"

# 3. HTTP Endpoints Detailed Audit
Write-Host "`n[3/3] Performing HTTP Endpoint Audit..." -ForegroundColor Yellow

if ($minioConsoleOk) {
    Test-HttpEndpoint "http://localhost:9001" "MinIO Console UI"
}
if ($sparkUiOk) {
    Test-HttpEndpoint "http://localhost:8080" "Spark Master Web UI"
}
if ($mlflowOk) {
    Test-HttpEndpoint "http://localhost:5000" "MLflow UI"
}
if ($airflowOk) {
    Test-HttpEndpoint "http://localhost:8090" "Airflow Web UI"
}
if ($apiOk) {
    Test-HttpEndpoint "http://localhost:3002/livez" "BentoML API Health"
}
if ($prometheusOk) {
    Test-HttpEndpoint "http://localhost:9090" "Prometheus UI"
    Test-HttpEndpoint "http://localhost:9090/api/v1/targets" "Prometheus Targets API"
}
if ($grafanaOk) {
    Test-HttpEndpoint "http://localhost:3000/api/health" "Grafana API Health"
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Health Audit Complete." -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
