@echo off
REM Script para iniciar Backend y Frontend juntos en Windows CMD

echo.
echo ========================================
echo  Iniciando Fichas - Backend ^& Frontend
echo ========================================
echo.

REM Rutas
set ProjectRoot=%~dp0
set BackendDir=%ProjectRoot%backend
set FrontendDir=%ProjectRoot%frontend
set BackendPort=8000
set FrontendPort=5173
set npm=%ProjectRoot%tools\node-v20.10.0-win-x64\npm.cmd

echo [BACKEND] Iniciando en puerto %BackendPort%...
echo   Directorio: %BackendDir%
echo.

REM Terminal 1: Backend
start "Backend - FastAPI" cmd /k "cd /d %BackendDir% && python main.py"

timeout /t 2 /nobreak

echo [FRONTEND] Iniciando en puerto %FrontendPort%...
echo   Directorio: %FrontendDir%
echo.

REM Terminal 2: Frontend
start "Frontend - Vite" cmd /k "cd /d %FrontendDir% && %npm% run dev"

timeout /t 3 /nobreak

echo.
echo ========================================
echo  Servicios iniciados
echo ========================================
echo.
echo   Backend:  http://localhost:%BackendPort%
echo   Frontend: http://localhost:%FrontendPort%
echo.
echo   Abre http://localhost:%FrontendPort% en tu navegador
echo.
pause
