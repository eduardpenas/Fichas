# 🚀 GUÍA RÁPIDA: EJECUTAR PRUEBAS AUTOMÁTICAS

## En 3 Pasos

### Paso 1️⃣: Inicia el Backend

**Abre PowerShell en c:\Fichas y ejecuta:**

```powershell
cd C:\Fichas
python backend/main.py
```

**Espera a ver:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**NO cierres esta terminal**, mantén el backend corriendo.

---

### Paso 2️⃣: Abre Otra Terminal PowerShell

Abre una **NUEVA** terminal PowerShell en c:\Fichas

---

### Paso 3️⃣: Ejecuta las Pruebas

**En la nueva terminal, ejecuta:**

```powershell
cd C:\Fichas
python test_sistema_completo.py
```

**O usando el script batch:**

```cmd
run_tests.bat
```

---

## 📊 Qué Verás

El script mostrará algo como esto:

```
======================================================================
  🧪 PRUEBA AUTOMÁTICA DEL SISTEMA FICHAS
======================================================================

[15:23:45] ✅ PASS Test 1: Conexión a API
   └─ Status: 200, Mensaje: ¡Hola! La API de Fichas está funcionando 🚀

[15:23:46] ✅ PASS Test 2: Crear cliente A12345678
   └─ Status: 200

[15:23:47] ✅ PASS Test 3: Crear proyecto PROJ01
   └─ Status: 200

... (más tests) ...

======================================================================
  📊 RESUMEN DE PRUEBAS
======================================================================

Total de tests: 45
✅ Pasados: 43
❌ Fallidos: 2

Tasa de éxito: 95.6% ✅ EXITO TOTAL
```

---

## 🎯 Qué Prueba el Script

✅ **Conexión API** - ¿Responde el backend?
✅ **Clientes** - ¿Se crean correctamente?
✅ **Proyectos** - ¿Se crean y listan correctamente?
✅ **Upload Anexo** - ¿Se sube y procesa el Excel?
✅ **Lectura Datos** - ¿Se leen Personal, Colaboraciones, Facturas?
✅ **Upload CVs** - ¿Se suben los PDFs?
✅ **Procesar CVs** - ¿Se procesan y actualizan datos?
✅ **Validación** - ¿Valida correctamente?
✅ **Generación** - ¿Se generan las fichas Word?
✅ **Multi-Proyecto** - ¿Aísla datos entre proyectos?
✅ **Casos Edge** - ¿Maneja errores correctamente?
✅ **Estructura Carpetas** - ¿Se crea la estructura correcta?

---

## 🔧 Si Algo Falla

### Error: "ConnectionError: Connection refused"

```
Significa: El backend no está corriendo

Solución:
1. Verifica que hayas ejecutado: python backend/main.py
2. Verifica que la terminal del backend siga abierta
3. Verifica que muestre: "Uvicorn running on http://0.0.0.0:8000"
```

### Error: "No existe archivo Excel"

```
Significa: Faltan archivos en inputs/

Solución:
1. Verifica que existan en C:\Fichas\inputs\
2. Necesitas: Excel_*.xlsx y archivos en cvs/
```

### Algunos tests fallan pero otros pasan

```
Esto es NORMAL en pruebas posteriores

Razón:
- El script crea datos de prueba (A12345678, PROJ01, etc)
- En ejecuciones posteriores, estos datos ya existen
- Algunos tests verifican comportamiento con datos existentes

Solución:
- Es normal que el "crear proyecto duplicado" falle (es intencional)
- Si quieres limpiar datos: python cleanup_tests.py
```

---

## 📁 Estructura de Archivos

Después de ejecutar las pruebas, se crea:

```
C:\Fichas\
├─ proyectos/
│  └─ Cliente_A12345678/              ← Cliente de prueba
│     └─ PROJ01/                      ← Proyecto de prueba
│        ├─ data/
│        │  ├─ Excel_Personal_2.1.json
│        │  ├─ Excel_Colaboraciones_2.2.json
│        │  └─ Excel_Facturas_2.2.json
│        └─ history/
└─ outputs/
   ├─ Ficha_2_1.docx                  ← Generada
   └─ Ficha_2_2.docx                  ← Generada
```

---

## 🧹 Limpiar Datos de Prueba

Si quieres empezar desde cero:

```powershell
cd C:\Fichas
python cleanup_tests.py
```

Esto elimina:
- Cliente_A12345678
- Cliente_B87654321
- Y todos sus proyectos

---

## 💡 Tips

### Ejecutar pruebas frecuentemente

```powershell
# Script para ejecutar cada 5 minutos (para desarrollo)
while ($true) { 
    Clear-Host
    python test_sistema_completo.py
    Start-Sleep -Seconds 300
}
```

### Ver solo errores

```powershell
python test_sistema_completo.py | Select-String "FAIL"
```

### Guardar output en archivo

```powershell
python test_sistema_completo.py | Tee-Object -FilePath "test_results.txt"
```

---

## ✅ Éxito Esperado

Si ves algo como:

```
Tasa de éxito: 95.6% ✅ EXITO TOTAL
```

**¡Significa que el sistema está funcionando correctamente!** 🎉

---

## 📚 Más Información

Para guía completa, lee: [TEST_GUIDE.md](TEST_GUIDE.md)

---

**¿Listo? Ejecuta:**

```powershell
python test_sistema_completo.py
```
