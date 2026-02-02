# 🎨 Frontend - Gestor de Fichas

Interfaz web moderna para gestionar datos y generar fichas automáticamente.

## 🚀 Instalación

### Requisitos
- Node.js 16+ y npm/yarn

### Pasos

```bash
cd frontend
npm install
npm run dev
```

La aplicación estará disponible en: **http://localhost:5173**

## 📦 Dependencias

- **React 18** - UI Library
- **TypeScript** - Tipado estático
- **Vite** - Build tool moderno
- **Tailwind CSS** - Estilos
- **Axios** - Cliente HTTP

## 📁 Estructura

```
src/
├── components/
│   ├── FileUploader.tsx      # Subida de Anexo y CVs
│   ├── EditableTable.tsx     # Tabla editable de datos
│   └── ActionsPanel.tsx      # Botones de procesamiento
├── api/
│   └── client.ts             # Cliente HTTP
├── App.tsx                   # Componente principal
├── main.tsx                  # Entry point
└── index.css                 # Estilos Tailwind
```

## 🔌 Características

### 1. Carga de Archivos
- Subir Anexo II (Excel)
- Subir múltiples CVs (PDF)

### 2. Edición de Datos
- Tabla editable de Personal
- Editar celdas in-place
- Agregar/eliminar filas
- Guardar cambios

### 3. Acciones
- **Procesar CVs** - Extrae experiencia de PDFs
- **Validar Datos** - Detecta errores e inconsistencias
- **Generar Fichas** - Crea Ficha_2_1.docx y Ficha_2_2.docx

## 🔗 Conexión con Backend

El frontend se conecta al backend FastAPI en `http://localhost:8000` usando Axios.

**Endpoints utilizados:**
- `POST /upload-anexo`
- `POST /upload-cvs`
- `POST /process-cvs`
- `GET /personal`
- `POST /update-personal`
- `POST /validate`
- `POST /generate-fichas`

## 📱 Flujo de Uso

1. **Cargar Anexo II** → Procesa datos iniciales
2. **Cargar CVs** → Sube los PDFs
3. **Revisar Datos** → Ve la tabla de Personal
4. **Editar** → Modifica celdas si es necesario
5. **Procesar CVs** → Extrae experiencia de PDFs
6. **Validar** → Detecta errores/inconsistencias
7. **Generar Fichas** → Crea documentos finales

## 🐛 Troubleshooting

### Error: "Cannot GET /personal"
- Verifica que el backend está corriendo: `cd backend && python -m uvicorn main:app --reload`

### Error: CORS
- El frontend y backend están en puertos diferentes (5173 vs 8000)
- El backend ya tiene CORS habilitado en `backend/main.py`

### Tabla vacía
- Primero carga el Anexo II usando el componente FileUploader

## 📚 Desarrollo

### Scripts disponibles
```bash
npm run dev       # Iniciar servidor de desarrollo
npm run build     # Compilar para producción
npm run preview   # Preview de producción
```

### Agregar nuevas funcionalidades
1. Crear componente en `src/components/`
2. Agregar endpoint en `src/api/client.ts`
3. Importar y usar en `src/App.tsx`

## 🎯 Mejoras Futuras

- [ ] Descarga de fichas generadas
- [ ] Historial de cambios
- [ ] Búsqueda y filtros en tablas
- [ ] Exportar datos a Excel
- [ ] Autenticación de usuarios
- [ ] Dark mode
- [ ] Soporte multiidioma
