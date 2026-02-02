# 🚀 Guía Rápida - Inicio en 5 Minutos

## Opción 1: Windows - Doble clic (Más fácil) ⭐

```
1. Abre el archivo: start-dev.bat
2. Se abrirán dos ventanas automáticamente
3. Espera 5 segundos a que cargue todo
4. Abre http://localhost:5173 en tu navegador
```

## Opción 2: Terminal Única (PowerShell/CMD)

```powershell
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2 (nueva) - Frontend
cd frontend
npm run dev
```

## Opción 3: Consola (Sin interfaz)

```bash
python src/main.py
```

---

## ✅ Verificar que todo funciona

### Backend OK:
- Abre http://localhost:8000/docs
- Deberías ver la documentación de la API

### Frontend OK:
- Abre http://localhost:5173
- Deberías ver la interfaz gráfica

---

## 📋 Flujo de uso (Frontend)

### Paso 1: Cargar Anexo
1. Haz clic en "Cargar Anexo"
2. Selecciona tu archivo `Anexo_II_tipo_a_.xlsx`
3. Espera a que aparezca ✅

### Paso 2: Cargar CVs
1. Haz clic en "Cargar CVs"
2. Selecciona todos los PDF de CVs
3. Espera a que aparezca ✅

### Paso 3: Ver datos
- En la tabla ves todos los registros de Personal
- Puedes clickear en cualquier celda para editar
- Cambios locales (no guardados aún)

### Paso 4: Procesar CVs
- Haz clic en "🔍 Procesar CVs"
- Extrae experiencia profesional de los PDFs
- Actualiza automáticamente la tabla

### Paso 5: Validar
- Haz clic en "✅ Validar Datos"
- Detecta errores e inconsistencias
- Muestra resumen en el panel

### Paso 6: Generar Fichas
- Haz clic en "📄 Generar Fichas"
- Crea Ficha_2_1.docx y Ficha_2_2.docx
- Los archivos están en `outputs/`

---

## 🛠️ Requisitos Instalados

✅ Python 3.11+
✅ pip
✅ Node.js 16+ (necesario para el frontend)
✅ npm

Si falta algo:
- Python: https://python.org/downloads
- Node.js: https://nodejs.org/en/download

---

## 🆘 Problemas Comunes

### Error: "npm not found"
```powershell
# Instala Node.js desde https://nodejs.org
# Luego en el terminal:
cd frontend
npm install
```

### Error: "Connection refused" en Frontend
- Verifica que el backend está corriendo en http://localhost:8000

### Error: CORS en consola del navegador
- El backend necesita CORS habilitado (ya está configurado)

### Las tablas están vacías
- Primero carga el Anexo II
- Espera a que se procese (verás ✅)

---

## 📞 Soporte

- 🔗 Docs: http://localhost:8000/docs
- 📖 README: [Ver README.md](README.md)
- 💬 Issues: GitHub Issues

---

**¡Ya estás listo! Comienza cargando tu Anexo II** 📄
