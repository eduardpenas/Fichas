@echo off
REM Script para ejecutar las pruebas automáticas

cls
echo.
echo ================================================
echo  🧪 PRUEBA AUTOMÁTICA DEL SISTEMA FICHAS
echo ================================================
echo.

REM Verificar que la API esté corriendo
echo Verificando conexión con API...
curl -s http://localhost:8000/ > nul
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: La API no está corriendo
    echo.
    echo Por favor ejecuta primero:
    echo   python backend/main.py
    echo.
    exit /b 1
)

echo ✅ API detectada en http://localhost:8000
echo.

REM Ejecutar las pruebas
python test_sistema_completo.py

pause
