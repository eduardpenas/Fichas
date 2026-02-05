@echo off
REM Script para iniciar Backend y Frontend simultáneamente

echo.
echo ===================================
echo  INICIANDO SISTEMA FICHAS
echo ===================================
echo.

REM Configurar Node.js portátil
set PATH=C:\Fichas\tools\node-v20.10.0-win-x64;%PATH%

REM Iniciar Backend en una ventana separada
echo [Backend] Iniciando en puerto 8000...
start "Backend - FastAPI" cmd /k "cd C:\Fichas && C:/Fichas/venv/Scripts/python.exe backend/main.py"

REM Esperar un poco para que el backend inicie
timeout /t 3 /nobreak

REM Iniciar Frontend en una ventana separada
echo [Frontend] Iniciando en puerto 5173...
start "Frontend - Vite" cmd /k "cd C:\Fichas\frontend && npm install & npm run dev"

REM Mostrar instrucciones
echo.
echo ===================================
echo  SISTEMA INICIADO
echo ===================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Presione cualquier tecla para cerrar esta ventana...
pause
