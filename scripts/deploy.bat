@echo off
REM One-shot localhost deploy script (Windows Batch)
REM Builds Docker image, starts container, waits for health check, opens browser

echo === Heart Disease Prediction API - One-Shot Deploy ===

REM Step 1: Build the Docker image
echo.
echo [1/4] Building Docker image...
docker compose build
if %ERRORLEVEL% neq 0 (
    echo Build failed!
    exit /b 1
)

REM Step 2: Start the container
echo.
echo [2/4] Starting container...
docker compose up -d
if %ERRORLEVEL% neq 0 (
    echo Failed to start container!
    exit /b 1
)

REM Step 3: Wait for health check
echo.
echo [3/4] Waiting for service to be ready...
timeout /t 5 /nobreak >nul
:check_health
curl -s http://localhost:8000/health >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Waiting for service...
    timeout /t 2 /nobreak >nul
    goto check_health
)
echo Service is ready!

REM Step 4: Open browser
echo.
echo [4/4] Opening browser...
start http://localhost:8000/docs

echo.
echo === Deployment Complete! ===
echo Swagger UI: http://localhost:8000/docs
echo Health:     http://localhost:8000/health
echo Info:       http://localhost:8000/info
echo Predict:    http://localhost:8000/predict
echo.
echo To stop: docker compose down