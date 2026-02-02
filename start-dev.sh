#!/bin/bash
# Script para iniciar Backend y Frontend

echo "🚀 Iniciando Fichas - Backend y Frontend"
echo ""

# Función para limpiar al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup EXIT INT TERM

# Iniciar Backend
echo "📦 Iniciando Backend (FastAPI) en http://localhost:8000"
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 3

# Iniciar Frontend
echo "🎨 Iniciando Frontend (React+Vite) en http://localhost:5173"
cd ../frontend
npm run dev &
FRONTEND_PID=$!
sleep 3

echo ""
echo "✅ Servicios iniciados:"
echo "   🔗 Frontend: http://localhost:5173"
echo "   🔗 Backend:  http://localhost:8000"
echo "   🔗 API Docs: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener ambos servicios"
echo ""

# Esperar a que se cierren
wait
