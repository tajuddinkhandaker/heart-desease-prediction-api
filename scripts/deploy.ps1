# One-shot localhost deploy script
# Builds Docker image, starts container, waits for health check, opens browser

Write-Host "=== Heart Disease Prediction API - One-Shot Deploy ===" -ForegroundColor Cyan

# Step 1: Build the Docker image
Write-Host "`n[1/4] Building Docker image..." -ForegroundColor Yellow
docker compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

# Step 2: Start the container
Write-Host "`n[2/4] Starting container..." -ForegroundColor Yellow
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start container!" -ForegroundColor Red
    exit 1
}

# Step 3: Wait for health check
Write-Host "`n[3/4] Waiting for service to be ready..." -ForegroundColor Yellow
$maxRetries = 30
$retryCount = 0
while ($retryCount -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            Write-Host "Service is ready!" -ForegroundColor Green
            break
        }
    } catch {
        Start-Sleep -Seconds 2
        $retryCount++
        Write-Host "Waiting for service... ($retryCount/$maxRetries)" -ForegroundColor Gray
    }
}

if ($retryCount -eq $maxRetries) {
    Write-Host "Service did not start in time. Check logs with: docker compose logs" -ForegroundColor Red
    exit 1
}

# Step 4: Open browser
Write-Host "`n[4/4] Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8000/docs"

Write-Host "`n=== Deployment Complete! ===" -ForegroundColor Green
Write-Host "Swagger UI: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health:     http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "Info:       http://localhost:8000/info" -ForegroundColor Cyan
Write-Host "Predict:    http://localhost:8000/predict" -ForegroundColor Cyan
Write-Host "`nTo stop: docker compose down" -ForegroundColor Gray