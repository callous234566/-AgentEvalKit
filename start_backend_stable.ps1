# Launch RAG Knowledge Base Assistant Backend (Stable)
# Features:
# 1. Auto-set HuggingFace mirror
# 2. Preload Embedding model to avoid first-request timeout
# 3. Disable dev --reload for stability
# 4. Auto-check environment

$env:HF_ENDPOINT="https://hf-mirror.com"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RAG Assistant - Backend Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python environment
$pythonPath = "D:\anaconda3\envs\ai_project\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "Error: Python not found: $pythonPath" -ForegroundColor Red
    Write-Host "Please check ai_project environment" -ForegroundColor Red
    exit 1
}

Write-Host "Python: $pythonPath" -ForegroundColor Green
Write-Host "HF Mirror: $env:HF_ENDPOINT" -ForegroundColor Yellow
Write-Host "URL: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host ""

# Check .env file
$envPath = Join-Path $PSScriptRoot ".env"
if (-not (Test-Path $envPath)) {
    Write-Host "Warning: .env not found" -ForegroundColor Yellow
    Write-Host "Copy .env.example to .env and set API key" -ForegroundColor Yellow
}

Write-Host "Starting backend..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Launch with stable params (no reload, longer timeout)
& $pythonPath -m uvicorn main:app `
    --host 127.0.0.1 `
    --port 8000 `
    --workers 1 `
    --timeout-keep-alive 120
