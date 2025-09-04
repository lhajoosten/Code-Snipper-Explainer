# Health Check Script for Docker Setup (Windows)
# Usage: .\health-check.ps1

Write-Host "[CHECK] Checking Code Snippet Explainer services..." -ForegroundColor Cyan

# Function to check service
function Test-Service {
    param(
        [string]$Url,
        [string]$ServiceName
    )

    Write-Host -NoNewline "Checking $ServiceName... "

    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec 5 -ErrorAction Stop
        Write-Host "[OK] UP" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[ERROR] DOWN" -ForegroundColor Red
        return $false
    }
}

# Check services
$backendOk = Test-Service -Url "http://localhost:8000/health" -ServiceName "Backend API"
$frontendOk = Test-Service -Url "http://localhost:5173" -ServiceName "Frontend"

Write-Host ""
Write-Host "[SUMMARY] Health Check Summary:" -ForegroundColor Blue

if ($backendOk) {
    Write-Host "Backend API: " -NoNewline; Write-Host "Running" -ForegroundColor Green
} else {
    Write-Host "Backend API: " -NoNewline; Write-Host "Not running" -ForegroundColor Red
}

if ($frontendOk) {
    Write-Host "Frontend: " -NoNewline; Write-Host "Running" -ForegroundColor Green
} else {
    Write-Host "Frontend: " -NoNewline; Write-Host "Not running" -ForegroundColor Red
}

if ($backendOk -and $frontendOk) {
    Write-Host ""
    Write-Host "[SUCCESS] All services are running!" -ForegroundColor Green
    Write-Host "[WEB] Frontend: http://localhost:5173" -ForegroundColor Blue
    Write-Host "[API] Backend API: http://localhost:8000" -ForegroundColor Blue
    Write-Host "[DOC] API Docs: http://localhost:8000/docs" -ForegroundColor Blue
    exit 0
} else {
    Write-Host ""
    Write-Host "[WARNING] Some services are not running." -ForegroundColor Yellow
    Write-Host "Try running: .\docker.ps1 up"
    exit 1
}
