# 🧪 Guía de Pruebas Automáticas - Sistema Fichas

## Descripción

Este script ejecuta **12 grupos de pruebas** sobre el sistema Fichas para verificar:

✅ Conexión a la API
✅ Gestión de clientes
✅ Gestión de proyectos
✅ Upload de Anexo (Excel)
✅ Lectura de datos (Personal, Colaboraciones, Facturas)
✅ Upload de CVs
✅ Procesamiento de CVs
✅ Validación de datos
✅ Generación de fichas Word
✅ Multi-proyecto (mismo cliente, múltiples proyectos)
✅ Casos edge (errores esperados)
✅ Estructura de carpetas

---

## 📋 Requisitos Previos

### 1. Backend Ejecutándose

Abre una terminal PowerShell y ejecuta:

```powershell
cd C:\Fichas
python backend/main.py
```

Deberías ver:
```
INFO:     Started server process [XXXX]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. Frontend Ejecutándose (Opcional)

```powershell
cd C:\Fichas\frontend
npm run dev
```

**Nota**: Las pruebas automáticas NO necesitan el frontend, solo la API.

### 3. Archivos de Prueba Disponibles

El script usa archivos existentes en `inputs/`:

```
C:\Fichas\inputs\
├─ Excel_Personal_2.1.xlsx          ← Usado para Upload Anexo
├─ Excel_Colaboraciones_2.2.xlsx
├─ Excel_Facturas_2.2.xlsx
├─ cvs\
│  ├─ Alejandro Navalon Fernandez.pdf
│  ├─ Beatriz Redondo Gomez.pdf
│  ├─ ... (más PDFs)
└─ 2.1.docx                         ← Plantilla
   2.2.docx                         ← Plantilla
```

---

## 🚀 Cómo Ejecutar

### Opción 1: Desde CMD (recomendado)

```cmd
cd C:\Fichas
run_tests.bat
```

### Opción 2: Desde PowerShell

```powershell
cd C:\Fichas
.\run_tests.ps1
```

### Opción 3: Directamente con Python

```powershell
cd C:\Fichas
python test_sistema_completo.py
```

---

## 📊 Interpretación de Resultados

### Colores de Output

- 🟢 **Verde (✅ PASS)**: Test pasó correctamente
- 🔴 **Rojo (❌ FAIL)**: Test falló
- 🟡 **Amarillo**: Mensajes informativos
- 🔵 **Azul**: Encabezados de secciones

### Ejemplo de Output

```
[15:23:45] ✅ PASS Test 1: Conexión a API
   └─ Status: 200, Mensaje: ¡Hola! La API de Fichas está funcionando 🚀

[15:23:46] ✅ PASS Test 2: Crear cliente A12345678
   └─ Status: 200

[15:23:47] ❌ FAIL Test 3: Upload Anexo a PROJ01
   └─ Status: 500, Error: Archivo no encontrado
```

### Resumen Final

```
================================================================================
  📊 RESUMEN DE PRUEBAS
================================================================================

Total de tests: 45
✅ Pasados: 43
❌ Fallidos: 2

Tasa de éxito: 95.6% ✅ EXITO TOTAL
```

---

## 🔍 Qué Prueba Cada Sección

### 1️⃣ CONEXIÓN A API
- Verifica que el backend esté activo y responda

### 2️⃣ GESTIÓN DE CLIENTES
- Lista clientes
- Crea cliente A12345678
- Verifica que aparece en la lista

### 3️⃣ GESTIÓN DE PROYECTOS
- Crea proyecto PROJ01
- Lista proyectos del cliente
- Crea proyecto PROJ02

### 4️⃣ UPLOAD DE ANEXO
- Sube un Excel con datos
- Verifica que se guardan en `Cliente_A12345678/PROJ01/data/`
- Genera 3 JSONs: Personal, Colaboraciones, Facturas

### 5️⃣ LECTURA DE DATOS
- GET /personal → Debe retornar registros
- GET /colaboraciones → Debe retornar registros
- GET /facturas → Debe retornar registros

### 6️⃣ UPLOAD DE CVs
- Sube 3 PDFs desde inputs/cvs/
- Verifica que se guardan correctamente

### 7️⃣ PROCESAR CVs
- Ejecuta procesamiento de CVs
- Actualiza Excel_Personal_2.1.json con experiencias

### 8️⃣ VALIDACIÓN
- Valida datos de Personal, Colaboraciones, Facturas
- Verifica que la validación es exitosa

### 9️⃣ GENERACIÓN DE FICHAS
- Genera Ficha_2_1.docx
- Genera Ficha_2_2.docx
- Verifica que los archivos se crean en outputs/

### 🔟 MULTI-PROYECTO
- Crea proyecto TESTPROJ
- Verifica que existen 3 proyectos para el cliente
- Confirma aislamiento de datos

### 1️⃣1️⃣ CASOS EDGE
- Intenta crear proyecto duplicado
- Crea proyecto sin Anexo
- Verifica que retorna lista vacía

### 1️⃣2️⃣ ESTRUCTURA DE CARPETAS
- Verifica estructura: Cliente_A12345678/PROJ01/data/
- Verifica existencia de JSONs generados

---

## 🐛 Troubleshooting

### Error: "ConnectionError: Connection refused"
```
Solución: El backend no está ejecutándose
→ Ejecuta: python backend/main.py
```

### Error: "No existe archivo: inputs/Excel_*.xlsx"
```
Solución: Faltan archivos de prueba
→ Verifica que existen en inputs/
```

### Error: "Upload Anexo: Status 500"
```
Solución: El archivo Excel está corrupto o tiene formato incorrecto
→ Verifica que sea un Excel .xlsx válido
```

### Algunos tests fallan pero otros pasan
```
Esto es normal en ejecuciones posteriores porque:
- Puede fallar el "crear cliente duplicado" (es intencional)
- Puede haber datos residuales de ejecuciones anteriores

→ El script limpia datos de prueba al inicio
```

---

## 📈 Casos de Éxito Esperados

### ✅ Éxito Total (95-100%)
Significa que el sistema está funcionando correctamente:
- Todos los endpoints responden
- Datos se guardan y leen correctamente
- Estructura de carpetas se crea correctamente

### ⚠️ Mayoría Pasó (80-94%)
Indica problemas menores:
- Algunos casos edge pueden fallar (normal)
- Posibles datos residuales de pruebas anteriores
- Recomendación: Limpiar carpetas y reintentar

### ❌ Fallos Críticos (<80%)
Indica problemas serios:
- Backend no responde correctamente
- Errores en endpoints
- Problemas de permisos de carpetas

---

## 🔧 Opciones de Personalización

Edita `test_sistema_completo.py` para cambiar:

```python
# Línea 23-28: Datos de prueba
self.test_data = {
    "cliente1": "A12345678",      # ← Cambiar NIF
    "cliente2": "B87654321",      # ← Cambiar NIF
    "proyecto1": "PROJ01",         # ← Cambiar proyecto
    "proyecto2": "PROJ02",
    "proyecto3": "TESTPROJ"
}
```

---

## 📝 Logs del Script

El script genera logs detallados:

```
[15:23:45] ✅ PASS Test 1: Conexión a API
[15:23:46] 📥 Limpiando datos de prueba...
[15:23:46]    Eliminada carpeta: c:\Fichas\proyectos\Cliente_A12345678
[15:23:47] ✅ PASS Test 2: Listar clientes (lista vacía)
...
```

Cada línea tiene timestamp para debugging.

---

## 🎯 Ejecución Frecuente

**Recomendación**: Ejecuta las pruebas:
- ✅ Después de cambios en código
- ✅ Antes de desplegar a producción
- ✅ Para validar que nada se rompió
- ✅ Para documentar comportamiento

---

## 📞 Soporte

Si las pruebas fallan:

1. **Revisa los logs del backend**
   ```powershell
   # Terminal donde corre el backend debe mostrar errores
   ```

2. **Verifica la estructura de carpetas**
   ```powershell
   dir c:\Fichas\proyectos\
   ```

3. **Ejecuta una prueba manual**
   ```powershell
   curl http://localhost:8000/
   ```

4. **Reinicia el backend**
   ```powershell
   # CTRL+C en terminal del backend
   # Ejecuta nuevamente: python backend/main.py
   ```

---

**¡Listo! Ahora puedes ejecutar todas las pruebas automáticamente. 🚀**
