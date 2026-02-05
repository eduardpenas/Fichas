# Script para iniciar Backend y Frontend juntos
# Uso: .\dev-start.ps1

Write-Host "
========================================
 Iniciando Fichas - Backend & Frontend
========================================
" -ForegroundColor Cyan

# Ruta del proyecto
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Backend
$BackendDir = Join-Path $ProjectRoot "backend"
$BackendPort = 8000

# Frontend
$FrontendDir = Join-Path $ProjectRoot "frontend"
$FrontendPort = 5173

# Node y NPM locales
$NodePath = Join-Path $ProjectRoot "tools\node-v20.10.0-win-x64"
$npm = Join-Path $NodePath "npm.cmd"

Write-Host "`n[BACKEND] Iniciando en puerto $BackendPort..." -ForegroundColor Green
Write-Host "  Directorio: $BackendDir`n" -ForegroundColor Gray

# Terminal 1: Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; python main.py" `
  -WindowStyle Normal

Start-Sleep -Seconds 2

Write-Host "[FRONTEND] Iniciando en puerto $FrontendPort..." -ForegroundColor Green
Write-Host "  Directorio: $FrontendDir`n" -ForegroundColor Gray

# Terminal 2: Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$FrontendDir'; & '$npm' run dev" `
  -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " ✓ Servicios iniciados" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "
 Backend:  http://localhost:$BackendPort
 Frontend: http://localhost:$FrontendPort

 Abre http://localhost:$FrontendPort en tu navegador
" -ForegroundColor Yellow
