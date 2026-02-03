#!/usr/bin/env pwsh
<#
.SYNOPSIS
Script de Prueba Automática del Sistema Fichas
#>

Clear-Host
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  🧪 PRUEBA AUTOMÁTICA DEL SISTEMA FICHAS" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que la API esté corriendo
Write-Host "Verificando conexión con API..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -Method GET -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ API detectada en http://localhost:8000" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "❌ ERROR: La API no está corriendo" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor ejecuta primero:" -ForegroundColor Yellow
    Write-Host "  python backend/main.py" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Ejecutar las pruebas
Write-Host "Iniciando pruebas..." -ForegroundColor Cyan
Write-Host ""

python test_sistema_completo.py

Write-Host ""
Read-Host "Presiona Enter para salir"
