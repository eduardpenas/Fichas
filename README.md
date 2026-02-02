# 📋 Generador de Fichas - Pipeline de Procesamiento

Sistema automatizado para procesar Anexos II, extraer datos de CVs en PDF, y generar fichas Word con plantillas personalizadas.

## 🎯 Descripción General

El programa realiza un pipeline completo de tres pasos:

1. **Procesar Anexo II** → Extrae datos de personal y colaboraciones desde un Excel → Genera JSONs
2. **Procesar CVs** → Lee PDFs de CVs, extrae experiencia profesional → Actualiza JSON de Personal
3. **Generar Fichas** → Crea documentos Word (Ficha 2.1 y 2.2) usando plantillas y JSONs

## 📁 Estructura del Proyecto

```
Fichas/
├── backend/
│   └── main.py                          # API FastAPI con endpoints
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUploader.tsx         # Carga de Anexo y CVs
│   │   │   ├── EditableTable.tsx        # Tabla editable de datos
│   │   │   └── ActionsPanel.tsx         # Botones de acciones
│   │   ├── api/
│   │   │   └── client.ts                # Cliente HTTP Axios
│   │   ├── App.tsx                      # Componente principal
│   │   └── main.tsx                     # Entry point
│   ├── package.json                     # Dependencias Node
│   ├── vite.config.ts                   # Config Vite
│   └── README.md                        # Documentación frontend
├── src/
│   ├── __init__.py
│   ├── main.py                          # Pipeline completo ejecutable desde consola
│   ├── validador.py                     # Validación automática de datos
│   ├── procesar_anexo.py               # Extrae datos del Anexo II → JSON
│   ├── procesar_cvs.py                 # Extrae CV data de PDFs → Actualiza JSON
│   ├── logica_fichas.py                # Genera fichas Word desde JSONs
│   └── utilidades_docx.py              # Funciones auxiliares para Word
├── inputs/
│   ├── Anexo_II_tipo_a_.xlsx           # Archivo principal del Anexo II
│   ├── cvs/                            # Carpeta con PDFs de CVs
│   ├── 2.1.docx                        # Plantilla Ficha 2.1 (Personal)
│   ├── 2.2.docx                        # Plantilla Ficha 2.2 (Colaboraciones)
│   ├── Excel_Personal_2.1.json         # JSON generado: Personal
│   ├── Excel_Colaboraciones_2.2.json   # JSON generado: Colaboraciones
│   └── Excel_Facturas_2.2.json         # JSON generado: Facturas
├── outputs/
│   ├── Ficha_2_1.docx                  # Documento generado: Personal
│   └── Ficha_2_2.docx                  # Documento generado: Colaboraciones
├── requirements.txt                    # Dependencias Python
├── test_validacion.py                  # Tests de validación
└── README.md                           # Este archivo
```

## 🚀 Instalación

### Requisitos Previos
- Python 3.11+
- pip (gestor de paquetes)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/eduardpenas/Fichas.git
cd Fichas
```

2. **Crear entorno virtual (opcional pero recomendado)**
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

3. **Instalar dependencias Backend (Python)**
```bash
pip install -r requirements.txt
```

4. **Instalar dependencias Frontend (Node.js)**
```bash
cd frontend
npm install
cd ..
```

## 📊 Pipeline de Uso

### Opción 1: Interfaz Web (Frontend + Backend) ⭐ RECOMENDADO

**Iniciar Backend (Terminal 1):**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Iniciar Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

**Acceder a la aplicación:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

**Flujo en la interfaz web:**
1. **Cargar Archivos** → Sube Anexo II y CVs
2. **Revisar Datos** → Visualiza la tabla de Personal
3. **Editar** → Modifica celdas si es necesario
4. **Procesar CVs** → Extrae experiencia de PDFs
5. **Validar** → Detecta errores e inconsistencias
6. **Generar Fichas** → Crea Ficha_2_1.docx y Ficha_2_2.docx

**Ventajas de usar el Frontend:**
- ✅ Interfaz gráfica intuitiva
- ✅ Edición en tiempo real de tablas
- ✅ Validación interactiva con alertas
- ✅ Gestión visual de archivos
- ✅ Mejor para usuarios no técnicos

---

### Opción 2: Ejecución desde Consola

**Comando único que ejecuta todo:**
```bash
cd Fichas
python src/main.py
```

Este comando:
1. Lee el archivo `inputs/Anexo_II_tipo_a_.xlsx`
2. Extrae datos de personal y colaboraciones → **genera JSONs**
3. Lee PDFs de `inputs/cvs/` y actualiza el JSON de Personal → **añade experiencia profesional**
4. **Valida** todos los datos automáticamente
5. Genera fichas Word usando plantillas → **crea `outputs/Ficha_2_1.docx` y `outputs/Ficha_2_2.docx`**

**Salida esperada:**
```
======================================================================
🚀 PIPELINE PRINCIPAL: GENERACIÓN DE FICHAS
======================================================================

📁 Directorio de entrada: C:\Fichas\inputs
📁 Directorio de salida: C:\Fichas\outputs

[1/3] Procesando Anexo II...
   ✅ Personal generado: 29 personas (JSON: Excel_Personal_2.1.json)
   ✅ Colaboraciones generado: 2 entidades (JSON: Excel_Colaboraciones_2.2.json)
   ✅ Facturas generado: 2 registros (JSON: Excel_Facturas_2.2.json)

[2/3] Procesando CVs...
   💾 JSON actualizado: 5 perfiles procesados.

[2.5/3] Validando datos...
   ✅ LISTO PARA GENERAR FICHAS

[3/3] Generando fichas con plantillas...
   ✅ Ficha 2.1 generada exitosamente
   ✅ Ficha 2.2 generada exitosamente

======================================================================
✅ Pipeline completado
======================================================================
```

**Ventajas de usar Consola:**
- ✅ Más rápido (sin interfaz gráfica)
- ✅ Automatizable en scripts
- ✅ Ideal para uso en servidores/cron jobs
- ✅ Para desarrolladores y usuarios avanzados

---

### Opción 3: API REST (FastAPI)

**Iniciar servidor:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Acceder a documentación interactiva:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Usar endpoints directamente (curl, Postman, Python, etc.):**
```bash
# Validar datos
curl -X POST http://localhost:8000/validate

# Generar fichas
curl -X POST http://localhost:8000/generate-fichas
```

---


**Iniciar el servidor:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Acceder a la documentación interactiva:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 Endpoints de la API

### 1. Health Check
```
GET /
```
Verifica si la API está funcionando.

**Respuesta:**
```json
{"mensaje": "¡Hola! La API de Fichas está funcionando 🚀"}
```

---

### 2. Subir Anexo II
```
POST /upload-anexo
Content-Type: multipart/form-data
file: <archivo xlsx>
```
Carga el Anexo II y lo procesa automáticamente.

**Respuesta exitosa:**
```json
{"status": "success", "message": "Anexo procesado y JSONs generados"}
```

---

### 3. Subir CVs
```
POST /upload-cvs
Content-Type: multipart/form-data
files: <múltiples archivos pdf>
```
Carga múltiples PDFs de CVs en la carpeta `inputs/cvs/`.

**Respuesta exitosa:**
```json
{"status": "success", "files": ["CV_Juan.pdf", "CV_Maria.pdf"]}
```

---

### 4. Procesar CVs
```
POST /process-cvs
```
Procesa los CVs en PDF, extrae experiencia profesional y actualiza el JSON de Personal.

**Respuesta exitosa:**
```json
{"status": "success", "message": "CVs leídos e integrados en el JSON"}
```

---

### 5. Obtener Datos de Personal
```
GET /personal
```
Devuelve el JSON con los datos de Personal procesados.

**Respuesta:**
```json
[
  {
    "Nombre": "Juan",
    "Apellidos": "García López",
    "Titulación 1": "Ingeniero Informático",
    "Coste horario (€/hora)": 50.0,
    "Horas totales": 100,
    "Coste total (€)": 5000.0,
    "EMPRESA 1": "Acme Corp",
    "PERIODO 1": "Enero 2020 - Diciembre 2022",
    "PUESTO 1": "Senior Developer",
    ...
  }
]
```

---

### 6. Actualizar Datos de Personal
```
POST /update-personal
Content-Type: application/json
[
  {
    "Nombre": "Juan",
    "Apellidos": "García López",
    ...modificaciones...
  }
]
```
Guarda los datos modificados (en JSON si existe, en Excel si no).

**Respuesta exitosa:**
```json
{"status": "success", "message": "JSON actualizado correctamente"}
```

---

### 7. Generar Fichas (⭐ Principal)
```
POST /generate-fichas
```
Genera los documentos Word finales (Ficha 2.1 y Ficha 2.2) usando las plantillas y los JSONs.

**Respuesta exitosa:**
```json
{
  "status": "success",
  "message": "Fichas generadas: Ficha_2_1.docx, Ficha_2_2.docx",
  "files": ["Ficha_2_1.docx", "Ficha_2_2.docx"]
}
```

## 📋 Flujo de Datos

```
ENTRADA                    PROCESAMIENTO                    SALIDA
─────────────────────────────────────────────────────────────────────

Anexo_II_tipo_a_.xlsx ──→ procesar_anexo.py ──→ Excel_Personal_2.1.json
                                              ├→ Excel_Colaboraciones_2.2.json
                                              └→ Excel_Facturas_2.2.json

CVs/*.pdf ────────────────→ procesar_cvs.py ───→ Excel_Personal_2.1.json
                                                 (actualizado con experiencia)

JSON files + Plantillas ──→ logica_fichas.py ──→ Ficha_2_1.docx
                                              └→ Ficha_2_2.docx
```

## 📝 Descripción de Módulos

### `procesar_anexo.py`
**Función:** `procesar_anexo()`

- Lee el archivo `Anexo_II_tipo_a_.xlsx`
- Extrae año fiscal, NIF y razón social desde la hoja "Datos solicitud"
- Procesa la hoja "Personal" para extraer nombres, horas, costes, titulaciones
- Procesa hojas de "C.Externas (Otros)" y "C.Externas (OPIS)" para colaboraciones
- **Salida:** Genera 3 archivos JSON en `inputs/`

### `procesar_cvs.py`
**Función:** `procesar_cvs()`

- Busca PDFs en `inputs/cvs/`
- Extrae el apartado "Experiencia" de cada CV
- Identifica empresa, puesto y período de cada experiencia laboral
- Traduce meses/años al español
- **Salida:** Actualiza `Excel_Personal_2.1.json` con:
  - EMPRESA 1, EMPRESA 2, EMPRESA 3
  - PUESTO 1, PUESTO 2, PUESTO 3
  - PERIODO 1, PERIODO 2, PERIODO 3
  - Puesto actual (del primero en el CV)

### `logica_fichas.py`
**Funciones principales:**
- `generar_ficha_2_1(json_path, plantilla_path, salida_path, año, acrónimo)`
  - Lee JSON de Personal
  - Rellena plantilla 2.1.docx con datos personalizados
  - Crea tablas formateadas
  - Genera cajas tituladas con experiencia y funciones
  
- `generar_ficha_2_2(json_colab, json_fact, plantilla_path, salida_path)`
  - Lee JSONs de Colaboraciones y Facturas
  - Rellena plantilla 2.2.docx
  - Crea tablas de identificación y costes

### `utilidades_docx.py`
Funciones auxiliares para:
- Formateo de euros (1.234,56 €)
- Manejo de celdas en tablas Word
- Colorado de celdas (gris para encabezados)
- Cambio de tamaños y fuentes
- Creación de cajas tituladas

## 🔧 Configuración

### Plantillas Word Requeridas
Los archivos `inputs/2.1.docx` y `inputs/2.2.docx` deben existir con la estructura base.

### Año Fiscal (Hardcoded)
En `src/main.py` y `backend/main.py`, el año se define como:
```python
anio = 2024
```
Modificar si es necesario.

### Acrónimo del Proyecto
```python
acronimo = 'ACR'
```
Modificar según el proyecto.

## 🐛 Requisitos Previos de Archivos

| Archivo | Ubicación | Requerido | Descripción |
|---------|-----------|-----------|-------------|
| Anexo_II_tipo_a_.xlsx | `inputs/` | ✅ SÍ | Archivo principal con datos |
| CVs (*.pdf) | `inputs/cvs/` | ✅ SÍ | Currículos en PDF |
| 2.1.docx | `inputs/` | ✅ SÍ | Plantilla Ficha 2.1 |
| 2.2.docx | `inputs/` | ✅ SÍ | Plantilla Ficha 2.2 |

## 📦 Dependencias

```
fastapi           # Framework API
uvicorn           # Servidor ASGI
python-multipart  # Manejo de archivos
pandas            # Procesamiento de datos
openpyxl          # Lectura/escritura Excel
pdfplumber        # Extracción de PDFs
python-docx       # Manipulación de documentos Word
```

Instalar con:
```bash
pip install -r requirements.txt
```

## 🚨 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pdfplumber'"
**Solución:** Instalar dependencias
```bash
pip install -r requirements.txt
```

### Error: "No se encontró ningún archivo 'Anexo...xlsx'"
**Solución:** Asegurar que `Anexo_II_tipo_a_.xlsx` existe en `inputs/`

### Error: "Permission denied" al generar fichas
**Solución:** Cerrar los archivos `.docx` en `outputs/` si están abiertos

### CVs no se procesan correctamente
**Solución:** 
- Verificar que los PDFs tienen estructura de CV standard con sección "Experiencia"
- Verificar que el nombre del archivo contiene al menos 2 palabras del nombre completo

## 📚 Ejemplos de Uso

### Desde Consola
```bash
# Ejecutar pipeline completo
python src/main.py

# Procesar solo Anexo
python src/procesar_anexo.py

# Procesar solo CVs
python src/procesar_cvs.py
```

### Desde API
```bash
# Iniciar servidor
cd backend
python -m uvicorn main:app --reload

# En otro terminal, hacer requests
curl -X POST http://localhost:8000/process-cvs
curl -X POST http://localhost:8000/generate-fichas
```

### Python Script
```python
from src.procesar_anexo import procesar_anexo
from src.procesar_cvs import procesar_cvs
from src.logica_fichas import generar_ficha_2_1, generar_ficha_2_2

# Ejecutar pipeline
procesar_anexo()
procesar_cvs()
generar_ficha_2_1('inputs/Excel_Personal_2.1.json', 'inputs/2.1.docx', 'outputs/Ficha_2_1.docx', 2024, 'ACR')
generar_ficha_2_2('inputs/Excel_Colaboraciones_2.2.json', 'inputs/Excel_Facturas_2.2.json', 'inputs/2.2.docx', 'outputs/Ficha_2_2.docx')
```

## 🔄 Flujo Recomendado de Trabajo

1. **Preparación:**
   - Colocar `Anexo_II_tipo_a_.xlsx` en `inputs/`
   - Colocar PDFs de CVs en `inputs/cvs/`
   - Asegurar que las plantillas `2.1.docx` y `2.2.docx` existen

2. **Procesamiento Automático:**
   ```bash
   python src/main.py
   ```

3. **Revisión de Datos:**
   - Revisar JSONs generados en `inputs/`
   - Comprobar que los CVs se procesaron correctamente

4. **Edición Manual (Opcional):**
   - Usar API para obtener datos: `GET /personal`
   - Modificar si es necesario: `POST /update-personal`

5. **Generación de Fichas:**
   - Si usas consola: ya hecho por `src/main.py`
   - Si usas API: `POST /generate-fichas`

6. **Resultado:**
   - Fichas generadas en `outputs/Ficha_2_1.docx` y `outputs/Ficha_2_2.docx`

## 📖 Más Información

- **GitHub:** https://github.com/eduardpenas/Fichas
- **Autor:** Eduard Peñas Balart
- **Última actualización:** Febrero 2026

---

**Estado del Proyecto:** En desarrollo activo ✅
