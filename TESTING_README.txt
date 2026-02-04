📋 ARCHIVOS DE PRUEBA CREADOS
═══════════════════════════════════════════════════════════════

He creado un sistema completo de pruebas automáticas para el sistema Fichas.

ARCHIVOS NUEVOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 test_sistema_completo.py
   └─ Script principal de pruebas
   └─ Realiza 12 grupos de pruebas (45+ tests)
   └─ Valida: API, Clientes, Proyectos, Uploads, Lectura, Validación, etc.
   └─ Colores en output para fácil lectura
   └─ Resumen automático de resultados

🚀 run_tests.bat
   └─ Script batch para Windows
   └─ Verifica que el backend esté corriendo
   └─ Ejecuta el script de pruebas
   └─ Uso: run_tests.bat

📜 run_tests.ps1
   └─ Script PowerShell
   └─ Igual que .bat pero con mejor integración PowerShell
   └─ Uso: .\run_tests.ps1

🧹 cleanup_tests.py
   └─ Limpia datos de prueba generados
   └─ Elimina Cliente_A12345678 y Cliente_B87654321
   └─ Útil para ejecutar pruebas limpias
   └─ Uso: python cleanup_tests.py

📖 TEST_GUIDE.md
   └─ Guía completa de pruebas
   └─ Explica qué prueba cada sección
   └─ Troubleshooting
   └─ Interpretación de resultados

🎯 TESTING_QUICK_START.md
   └─ Guía rápida (3 pasos)
   └─ Para empezar inmediatamente
   └─ Tips y errores comunes


CÓMO EMPEZAR (3 pasos):
═════════════════════════════════════════════════════════════

PASO 1: Inicia el Backend
────────────────────────
1. Abre PowerShell en c:\Fichas
2. Ejecuta:
   python backend/main.py
3. Espera a ver:
   INFO:     Uvicorn running on http://0.0.0.0:8000

PASO 2: Abre Otra Terminal
─────────────────────────
1. Abre una NUEVA terminal PowerShell
2. Ve a c:\Fichas:
   cd C:\Fichas

PASO 3: Ejecuta las Pruebas
──────────────────────────
Elige UNA de estas opciones:

Opción A (recomendado):
  python test_sistema_completo.py

Opción B (con script batch):
  run_tests.bat

Opción C (PowerShell):
  .\run_tests.ps1


QUÉ PRUEBA EL SCRIPT:
═════════════════════════════════════════════════════════════

✅ Conexión a API
✅ Gestión de Clientes
✅ Gestión de Proyectos
✅ Upload de Anexo (Excel)
✅ Lectura de Datos (Personal, Colaboraciones, Facturas)
✅ Upload de CVs (PDFs)
✅ Procesamiento de CVs
✅ Validación de Datos
✅ Generación de Fichas Word (2.1 y 2.2)
✅ Multi-Proyecto (mismo cliente, múltiples proyectos)
✅ Casos Edge (errores esperados)
✅ Estructura de Carpetas


RESULTADO ESPERADO:
═════════════════════════════════════════════════════════════

Deberías ver algo como:

  [15:23:45] ✅ PASS Test 1: Conexión a API
  [15:23:46] ✅ PASS Test 2: Crear cliente A12345678
  ...
  
  Total de tests: 45
  ✅ Pasados: 43
  ❌ Fallidos: 2
  
  Tasa de éxito: 95.6% ✅ EXITO TOTAL


ERRORES COMUNES:
═════════════════════════════════════════════════════════════

❌ "ConnectionError: Connection refused"
   → El backend no está corriendo
   → Verifica Paso 1 arriba

❌ "No existe archivo Excel"
   → Faltan archivos en inputs/
   → Verifica que existan Excel_*.xlsx

❌ Algunos tests fallan
   → Es NORMAL en ejecuciones posteriores
   → Causa: datos de prueba anteriores
   → Solución: python cleanup_tests.py


ARCHIVOS GENERADOS DURANTE LAS PRUEBAS:
═════════════════════════════════════════════════════════════

El script crea automáticamente:

C:\Fichas\proyectos\
  └─ Cliente_A12345678/           ← Cliente de prueba
     ├─ PROJ01/                   ← Proyecto 1
     │  ├─ data/
     │  │  ├─ Excel_Personal_2.1.json
     │  │  ├─ Excel_Colaboraciones_2.2.json
     │  │  └─ Excel_Facturas_2.2.json
     │  └─ history/
     ├─ PROJ02/                   ← Proyecto 2
     │  ├─ data/
     │  └─ history/
     └─ TESTPROJ/                 ← Proyecto 3
        ├─ data/
        └─ history/

C:\Fichas\outputs\
  ├─ Ficha_2_1.docx               ← Generada
  └─ Ficha_2_2.docx               ← Generada


LIMPIAR DATOS DE PRUEBA:
═════════════════════════════════════════════════════════════

Si quieres empezar desde cero:

  python cleanup_tests.py

Esto elimina:
  - Cliente_A12345678
  - Cliente_B87654321
  - Todos sus proyectos


PRÓXIMAS ACCIONES:
═════════════════════════════════════════════════════════════

1. 🚀 Ejecuta: python test_sistema_completo.py
2. 📊 Revisa los resultados
3. 📖 Lee TEST_GUIDE.md si necesitas más detalles
4. 🔄 Ejecuta regularmente durante desarrollo


COMANDOS ÚTILES:
═════════════════════════════════════════════════════════════

# Ejecutar pruebas
python test_sistema_completo.py

# Limpiar datos de prueba
python cleanup_tests.py

# Ver solo errores
python test_sistema_completo.py | findstr "FAIL"

# Guardar resultados
python test_sistema_completo.py > test_results.txt


¡YA ESTÁ TODO LISTO!
═════════════════════════════════════════════════════════════

Ejecuta las pruebas ahora:

  cd C:\Fichas
  python test_sistema_completo.py

📚 Para más info: TEST_GUIDE.md o TESTING_QUICK_START.md
