# ================================================================
# Z5008 Big Data Lab — Infrastructure Startup Control Script
# ================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Starting Real-Time Clinical Intelligence Stack Infrastructure" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# 1. Verify Docker is running
Write-Host "[1/5] Checking Docker daemon status..." -ForegroundColor Yellow
$dockerStatus = docker desktop status 2>&1
if ($dockerStatus -like "*running*") {
    Write-Host "Docker Desktop is running." -ForegroundColor Green
} else {
    Write-Host "Docker is not running. Attempting to start Docker Desktop..." -ForegroundColor Yellow
    docker desktop start
    Start-Sleep -Seconds 15
    $check = docker desktop status 2>&1
    if ($check -notlike "*running*") {
        Write-Host "ERROR: Docker Desktop could not be started. Please launch it manually." -ForegroundColor Red
        Exit 1
    }
    Write-Host "Docker Desktop successfully started." -ForegroundColor Green
}

# 2. Validate Compose configuration
Write-Host "[2/5] Validating Docker Compose configuration..." -ForegroundColor Yellow
docker compose config > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: docker-compose.yml configuration validation failed." -ForegroundColor Red
    Exit 1
}
Write-Host "docker-compose.yml is valid." -ForegroundColor Green

# 3. Build custom containers
Write-Host "[3/5] Building custom containers (Airflow & BentoML API)..." -ForegroundColor Yellow
docker compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker Compose build failed." -ForegroundColor Red
    Exit 1
}
Write-Host "Custom containers built successfully." -ForegroundColor Green

# 4. Start foundational services in dependency order
Write-Host "[4/5] Starting foundational services (Postgres, MinIO, Kafka)..." -ForegroundColor Yellow
docker compose up -d postgres minio kafka
Start-Sleep -Seconds 5

Write-Host "Waiting for database and object store to pass health checks..." -ForegroundColor Yellow
for ($i=0; $i -lt 12; $i++) {
    $pgHealth = docker inspect --format='{{json .State.Health.Status}}' postgres 2>$null
    $minioHealth = docker inspect --format='{{json .State.Health.Status}}' minio 2>$null
    
    if ($pgHealth -like "*healthy*" -and $minioHealth -like "*healthy*") {
        Write-Host "PostgreSQL and MinIO are healthy." -ForegroundColor Green
        break
    }
    Write-Host "Waiting..." -ForegroundColor DarkGray
    Start-Sleep -Seconds 5
}

# Ingest MinIO init buckets
docker compose up -d minio-init
Start-Sleep -Seconds 2

# Start Spark Cluster
Write-Host "Starting Spark cluster (Master and Worker)..." -ForegroundColor Yellow
docker compose up -d spark-master spark-worker
Start-Sleep -Seconds 3

# Start MLflow
Write-Host "Starting MLflow tracking server..." -ForegroundColor Yellow
docker compose up -d mlflow
Start-Sleep -Seconds 3

# Initialize and start Airflow
Write-Host "Starting Airflow Database Migration and User Init..." -ForegroundColor Yellow
docker compose up -d airflow-init
Start-Sleep -Seconds 10

Write-Host "Starting Airflow Webserver and Scheduler..." -ForegroundColor Yellow
docker compose up -d airflow-webserver airflow-scheduler
Start-Sleep -Seconds 5

# Start BentoML API
Write-Host "Starting BentoML Prediction REST API..." -ForegroundColor Yellow
docker compose up -d api
Start-Sleep -Seconds 3

# Start Prometheus and Grafana Monitoring
Write-Host "Starting Prometheus and Grafana monitoring tools..." -ForegroundColor Yellow
docker compose up -d prometheus grafana
Start-Sleep -Seconds 5

# 5. Output running status and URLs
Write-Host "[5/5] Checking service status..." -ForegroundColor Yellow
docker compose ps

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  INFRASTRUCTURE SERVICES STARTED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  Service endpoints available at:" -ForegroundColor Yellow
Write-Host "  - Spark UI:        http://localhost:8080" -ForegroundColor White
Write-Host "  - Spark Worker:    http://localhost:8081" -ForegroundColor White
Write-Host "  - MLflow UI:       http://localhost:5000" -ForegroundColor White
Write-Host "  - MinIO Console:   http://localhost:9001 (S3 Port: 9000)" -ForegroundColor White
Write-Host "  - Airflow Web UI:  http://localhost:8090 (admin/adminpassword)" -ForegroundColor White
Write-Host "  - BentoML API:     http://localhost:3002" -ForegroundColor White
Write-Host "  - Prometheus:      http://localhost:9090" -ForegroundColor White
Write-Host "  - Grafana UI:      http://localhost:3000 (admin/adminpassword)" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Green
