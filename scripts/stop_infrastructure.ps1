# ================================================================
# Z5008 Big Data Lab — Infrastructure Stop Control Script
# ================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Stopping Real-Time Clinical Intelligence Stack Containers" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Stop containers without removing them or their volumes
Write-Host "Stopping all running services..." -ForegroundColor Yellow
docker compose stop

if ($LASTEXITCODE -eq 0) {
    Write-Host "Services stopped successfully." -ForegroundColor Green
    Write-Host "Docker volumes and data are fully preserved." -ForegroundColor Green
} else {
    Write-Host "WARNING: Docker Compose stop encountered an error." -ForegroundColor Red
}
Write-Host "================================================================" -ForegroundColor Cyan
