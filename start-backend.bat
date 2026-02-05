@echo off
REM Script simple para iniciar el backend

echo Iniciando Backend FastAPI...
echo.

cd /d "%~dp0backend"
python main.py

pause
