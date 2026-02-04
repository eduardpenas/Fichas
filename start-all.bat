@echo off
REM Script para iniciar Backend y Frontend

echo ========================================
echo Instalando dependencias del backend...
echo ========================================
cd /d C:\Fichas
pip install -r requirements.txt

echo.
echo ========================================
echo Iniciando Backend (FastAPI en puerto 8000)...
echo ========================================
start "Backend FastAPI" cmd /k "cd C:\Fichas && python backend/main.py"

timeout /t 3 /nobreak

echo.
echo ========================================
echo Instalando dependencias del frontend...
echo ========================================
cd /d C:\Fichas\frontend
set PATH=C:\Fichas\tools\node-v20.10.0-win-x64;%PATH%
npm install

echo.
echo ========================================
echo Iniciando Frontend (Vite en puerto 5173)...
echo ========================================
start "Frontend Vite" cmd /k "cd C:\Fichas\frontend && set PATH=C:\Fichas\tools\node-v20.10.0-win-x64;%PATH% && npm run dev"

echo.
echo ========================================
echo Servicios iniciados:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:5173
echo ========================================
pause
