# Conectar Backend y Frontend

## Estado Actual ✓

El backend y frontend ya están configurados para comunicarse:

- **Backend**: FastAPI en `http://localhost:8000` con CORS habilitado
- **Frontend**: React + Vite en `http://localhost:5173`
- **Cliente API**: Axios configurado en `frontend/src/api/client.ts`

## Iniciar Ambos Servicios

### Opción 1: Script PowerShell (Recomendado para PowerShell)
```powershell
cd C:\Fichas
.\dev-start.ps1
```

### Opción 2: Script Batch (Para CMD)
```cmd
C:\Fichas\dev-start.bat
```

### Opción 3: Manual en 2 Terminales

**Terminal 1 - Backend:**
```bash
cd C:\Fichas\backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd C:\Fichas\frontend
C:\Fichas\tools\node-v20.10.0-win-x64\npm.cmd run dev
```

## URLs de Acceso

- **Frontend (UI)**: http://localhost:5173
- **Backend (API)**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

## Verificar Conexión

El frontend intentará conectar al backend al cargar. Si ves mensajes en la consola del navegador como:

```
[API] GET / ← Health Check
```

¡La conexión está funcionando! 🎉

## Endpoints Disponibles

El backend expone estos endpoints:

- `GET /` - Health check
- `GET /clientes` - Listar clientes
- `POST /upload-anexo` - Cargar archivo anexo
- `POST /upload-cvs` - Cargar CVs
- `POST /process-cvs` - Procesar CVs
- `POST /generate-fichas` - Generar fichas DOCX
- `GET /download-fichas` - Descargar fichas generadas
- Y muchos más en el backend

El cliente API en `frontend/src/api/client.ts` proporciona métodos para todos estos endpoints.

## Desarrollo

- Backend: Los cambios en `backend/main.py` requieren reinicio
- Frontend: Vite reinicia automáticamente con cambios en `frontend/src`

## Próximos Pasos

1. Verifica que ambos servicios inicien sin errores
2. Abre http://localhost:5173 en tu navegador
3. Comprueba la consola del navegador para logs del API
4. ¡Empieza a usar la aplicación!
