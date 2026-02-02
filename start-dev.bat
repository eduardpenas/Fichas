@echo off
REM Script para iniciar Backend y Frontend en Windows

echo 🚀 Iniciando Fichas - Backend y Frontend
echo.

REM Iniciar Backend en una ventana nueva
echo 📦 Iniciando Backend (FastAPI) en http://localhost:8000
cd backend
start "Backend - Fichas" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..
timeout /t 3 /nobreak

REM Iniciar Frontend en una ventana nueva
echo 🎨 Iniciando Frontend (React+Vite) en http://localhost:5173
cd frontend
start "Frontend - Fichas" cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak

echo.
echo ✅ Servicios iniciados:
echo    🔗 Frontend: http://localhost:5173
echo    🔗 Backend:  http://localhost:8000
echo    🔗 API Docs: http://localhost:8000/docs
echo.
echo Cierra las ventanas para detener los servicios
echo.
pause
