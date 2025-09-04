# Docker Compose Management Script for Windows
# Usage: .\docker.ps1 [command]

param(
    [Parameter(Mandatory=$false)]
    [string]$Command = "help"
)

$COMPOSE_FILE = "docker-compose.yml"
$OVERRIDE_FILE = "docker-compose.override.yml"

# Check if .env.docker exists
if (-not (Test-Path ".env.docker")) {
    Write-Host "❌ .env.docker file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.docker to .env and configure your environment variables."
    exit 1
}

# Function to check if Docker is running
function Test-Docker {
    try {
        docker info | Out-Null
    } catch {
        Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
        exit 1
    }
}

# Function to show usage
function Show-Usage {
    Write-Host ">>> Code Snippet Explainer - Docker Management" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\docker.ps1 [command]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  up             Start all services"
    Write-Host "  down           Stop all services"
    Write-Host "  build          Build all services"
    Write-Host "  rebuild        Rebuild all services from scratch"
    Write-Host "  logs           Show logs from all services"
    Write-Host "  logs-backend   Show logs from backend service"
    Write-Host "  logs-frontend  Show logs from frontend service"
    Write-Host "  shell-backend  Enter backend container shell"
    Write-Host "  shell-frontend Enter frontend container shell"
    Write-Host "  clean          Remove all containers and volumes"
    Write-Host "  help           Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\docker.ps1 up           # Start the application"
    Write-Host "  .\docker.ps1 logs         # View all logs"
    Write-Host "  .\docker.ps1 down         # Stop the application"
}

# Main command handling
switch ($Command) {
    "up" {
        Test-Docker
        Write-Host ">>> Starting Code Snippet Explainer..." -ForegroundColor Green
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE up -d
        Write-Host "[OK] Services started!" -ForegroundColor Green
        Write-Host "[WEB] Frontend: http://localhost:5173" -ForegroundColor Blue
        Write-Host "[API] Backend API: http://localhost:8000" -ForegroundColor Blue
        Write-Host "[DOC] API Docs: http://localhost:8000/docs" -ForegroundColor Blue
    }

    "down" {
        Write-Host "[STOP] Stopping services..." -ForegroundColor Yellow
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE down
        Write-Host "[OK] Services stopped!" -ForegroundColor Green
    }

    "build" {
        Test-Docker
        Write-Host "[BUILD] Building services..." -ForegroundColor Yellow
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE build
        Write-Host "[OK] Build complete!" -ForegroundColor Green
    }

    "rebuild" {
        Test-Docker
        Write-Host "[REBUILD] Rebuilding services from scratch..." -ForegroundColor Yellow
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE down -v
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE build --no-cache
        Write-Host "[OK] Rebuild complete!" -ForegroundColor Green
    }

    "logs" {
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE logs -f
    }

    "logs-backend" {
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE logs -f backend
    }

    "logs-frontend" {
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE logs -f frontend
    }

    "shell-backend" {
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE exec backend /bin/bash
    }

    "shell-frontend" {
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE exec frontend /bin/sh
    }

    "clean" {
        Write-Host "[CLEAN] Cleaning up containers and volumes..." -ForegroundColor Yellow
        docker-compose -f $COMPOSE_FILE -f $OVERRIDE_FILE down -v --remove-orphans
        docker system prune -f
        Write-Host "[OK] Cleanup complete!" -ForegroundColor Green
    }

    default {
        Show-Usage
    }
}
