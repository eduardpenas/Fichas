@echo off
REM Script simple para iniciar el frontend

echo Iniciando Frontend Vite...
echo.

cd /d "%~dp0frontend"
"%~dp0tools\node-v20.10.0-win-x64\npm.cmd" run dev

pause
