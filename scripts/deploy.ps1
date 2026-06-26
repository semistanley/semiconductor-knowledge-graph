<#
Semiconductor KG Platform - One-Click Deploy
Usage: .\scripts\deploy.ps1 [-Build] [-Pipeline] [-NoSeed] [-Logs]
#>
param(
    [switch]$Build,
    [switch]$Pipeline,
    [switch]$NoSeed,
    [switch]$Logs
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Semiconductor KG Platform - Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Docker
Write-Host "[1/5] Checking Docker..." -ForegroundColor Yellow
try {
    docker info 2>$null | Out-Null
    Write-Host "  Docker is ready" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# 2. Check .env
Write-Host "[2/5] Checking config..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "  .env created from .env.example" -ForegroundColor Yellow
    Write-Host "  Please edit .env and fill in:" -ForegroundColor Yellow
    Write-Host "    - DEEPSEEK_API_KEY: your DeepSeek API key" -ForegroundColor Yellow
    Write-Host "    - NEO4J_PASSWORD: Neo4j password" -ForegroundColor Yellow
    Write-Host "    - FLASK_SECRET_KEY: Flask secret key" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Edit .env then press Enter to continue"
}

$envContent = Get-Content ".env" -Raw -ErrorAction SilentlyContinue
if ($envContent -match "your_deepseek_api_key_here|change_me") {
    Write-Host "  [WARNING] .env still has placeholder values!" -ForegroundColor Red
    Write-Host "  Make sure DEEPSEEK_API_KEY is set to a valid key." -ForegroundColor Red
    Read-Host "Press Enter to continue anyway, or Ctrl+C to abort"
} else {
    Write-Host "  .env config OK" -ForegroundColor Green
}

# 3. Pull / Build
Write-Host "[3/5] Preparing images..." -ForegroundColor Yellow
if ($Build) {
    Write-Host "  Building Docker images..." -ForegroundColor Yellow
    docker compose build
} else {
    Write-Host "  Pulling base images..." -ForegroundColor Yellow
    docker compose pull mysql neo4j 2>$null
}

# 4. Start
Write-Host "[4/5] Starting services..." -ForegroundColor Yellow
if ($Build) {
    if ($Pipeline) {
        docker compose --profile pipeline up -d --build
    } else {
        docker compose up -d --build
    }
} else {
    if ($Pipeline) {
        docker compose --profile pipeline up -d
    } else {
        docker compose up -d
    }
}

# 5. Wait
Write-Host "[5/5] Waiting for services to be ready..." -ForegroundColor Yellow
Write-Host "  (First run may take 2-5 min for image download + DB init + Neo4j seeding)"
Write-Host "  Check progress in Docker Desktop."
Write-Host ""

if ($Logs) {
    Write-Host "  Streaming web service logs..." -ForegroundColor Cyan
    docker compose logs -f web
}

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deploy Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Home:        http://localhost:5000" -ForegroundColor White
Write-Host "  AI Chat:     http://localhost:5000/app" -ForegroundColor White
Write-Host "  Doc Ingest:  http://localhost:5000/ingest" -ForegroundColor White
Write-Host "  News:        http://localhost:5000/news" -ForegroundColor White
Write-Host ""
Write-Host "  Neo4j:       http://localhost:7474 (user: neo4j)" -ForegroundColor Gray
Write-Host "  MySQL:       localhost:3307 (user: kg_user)" -ForegroundColor Gray
Write-Host ""
Write-Host "Pipeline (auto doc ingestion):" -ForegroundColor Yellow
Write-Host "  1) Drop PDF/DOCX/TXT into automation/inbox/" -ForegroundColor Gray
Write-Host "  2) Run: docker compose run --rm web python automation/pipeline.py" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to exit"
