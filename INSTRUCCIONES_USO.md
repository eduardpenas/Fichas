# 🎯 INSTRUCCIONES DE USO - Procesamiento Robusto

## Inicio Rápido

### 1️⃣ Antes de Empezar
- Tienes el frontend corriendo en `http://localhost:5174`
- Tienes el backend corriendo en `http://localhost:8000`
- Tienes un archivo Anexo II (Excel) preparado

### 2️⃣ Flujo Estándar

```
1. Seleccionar Cliente
   └─ Va a carpeta Cliente_{NIF} o crea nueva

2. Subir Anexo II (Excel)
   └─ Backend procesa automáticamente
   └─ Detecta año fiscal (2024)
   └─ Extrae Personal, Colaboraciones, Facturas

3. Ver resultados en el formulario
   └─ Personal: 29 personas (ejemplo)
   └─ Colaboraciones: 2 entidades
   └─ Facturas: 2 registros

4. Editar si necesitas
   └─ La tabla es 100% editable
   └─ Cambios se guardan automáticamente

5. Generar Fichas
   └─ Ficha 2.1 (Personal) ✓
   └─ Ficha 2.2 (Colaboraciones) ✓
   └─ Descargar en WORD
```

---

## Cuando la Magia Ocurre 🪄

### Procesamiento Automático del Personal Sheet

```
Excel (.xlsx)
    │
    ├─ Lee headers en filas 12-13 (multi-nivel)
    │
    ├─ BUSCA dinámicamente:
    │  ├─ Columna "Nombre" (case-insensitive)
    │  ├─ Columna "Titulación"
    │  ├─ Año fiscal 2024 en el primer nivel
    │  ├─ "Horas IT" para 2024
    │  └─ "Coste IT" para 2024
    │
    ├─ VALIDA:
    │  ├─ ¿Existen todas las columnas necesarias?
    │  ├─ ¿Hay al menos una persona con datos?
    │  └─ ¿Se puede calcular el coste horario?
    │
    ├─ FILTRA:
    │  ├─ Excluye personas sin nombre
    │  ├─ Excluye personas con 0 horas Y 0 coste
    │  └─ Mantiene: Nombre, Titulación, Horas, Coste
    │
    ├─ CALCULA:
    │  ├─ Coste horario = Coste total / Horas totales
    │  └─ Evita división por cero
    │
    └─ GENERA:
       └─ Excel_Personal_2.1.json (29 personas ✓)
```

---

## 📋 Qué Pasa en Cada Escenario

### ✅ Escenario Ideal: Todo funciona
```
Excel sube → Backend procesa → 29 personas generadas → Ves en UI

Log que ves:
👤 Procesando Personal...
   Dimensiones originales: 39 filas x 35 columnas
   OK - Nombre encontrado
   OK - Titulación encontrada
   OK - Horas IT (2024) encontradas
   OK - Coste IT (2024) encontrado
   Registros antes de filtrar: 39
   Registros después de filtrar: 29
   OK - Personal generado: 29 personas
```

### ⚠️ Escenario: Personal Sin Datos
```
Excel sin personas → Backend procesa → Archivo vacío → Botón gris en UI

Log que ves:
👤 Procesando Personal...
   Registros antes de filtrar: 0
   WARN - No hay registros validos con datos
   Archivo vacio creado

Frontend muestra:
"No hay datos de Personal (edita manualmente)"
```

### ⚠️ Escenario: Falta Columna Titulación
```
Excel sin Titulación → Backend procesa → Datos igual, campo vacío

Log que ves:
👤 Procesando Personal...
   OK - Nombre encontrado
   WARN - No se encontró columna 'Titulación'
   OK - Horas IT (2024) encontradas
   OK - Coste IT (2024) encontrado
   OK - Personal generado: 29 personas

Frontend muestra:
[Tabla con Titulación 1 vacío]
```

### ⚠️ Escenario: Año Diferente (2025)
```
Excel solo tiene 2025 → Backend procesa → Archivo vacío

Log que ves:
👤 Procesando Personal...
   WARN - No se encontraron Horas/Coste IT para año 2024
   Anos disponibles: ['2025', '2026']
   Archivo vacio creado

Solución:
1. Actualiza el Excel a 2024, O
2. Contacta para cambiar el año procesado
```

---

## 🎨 Interfaz Gráfica

### Tabla Personal (Editable)

```
┌─────────────────────────────────────────────────────────────────┐
│ Nombre    │ Apellidos │ Titulación 1 │ Horas │ Coste │ Coste/h │
├─────────────────────────────────────────────────────────────────┤
│ JUAN      │ PÉREZ     │ Ing. Inf.    │ 100  │ 5000 │ 50.00   │
│ MARÍA     │ GARCÍA    │ Máster       │ 80   │ 3600 │ 45.00   │
│ PEDRO     │ MARTINEZ  │ Grado        │ 120  │ 4800 │ 40.00   │
│           │           │              │      │      │         │ ← Editable
└─────────────────────────────────────────────────────────────────┘

Editar:
- Click en cualquier celda → Puedes cambiar valor
- Presiona Enter → Se guarda
- Los cambios se mantienen
```

### Botones de Acción

```
[📤 Subir Anexo II] → Inicia procesamiento
    └─ Detecta año fiscal
    └─ Busca columnas automáticamente
    └─ Genera JSONs
    └─ Carga tabla

[✏️ Editar] → Habilita edición de tabla
    └─ Click en celdas
    └─ Cambios en vivo
    └─ Sin guardar (se guarda al generar Ficha)

[📄 Generar Ficha 2.1] → Crea WORD con datos
    └─ Usa datos actuales (Excel + ediciones)
    └─ Descarga como Ficha_Personal_2.1.docx
    └─ Listo para enviar al cliente
```

---

## 🔧 Debugging

Si algo no funciona como esperado:

### Opción 1: Ver logs en tiempo real
```bash
# En otra terminal, ve al directorio
cd c:\Fichas

# Sube un Excel para ver los logs
python -c "from src.procesar_anexo import procesar_anexo; procesar_anexo()"
```

Los logs te dirán exactamente dónde está el problema.

### Opción 2: Revisar archivo JSON generado
```bash
# Abre el archivo con un editor
cat inputs/Excel_Personal_2.1.json

# O en Windows
type inputs\Excel_Personal_2.1.json
```

Verás exactamente qué datos se extrajeron.

### Opción 3: Contactar con información
Cuando contactes, proporciona:
- El log completo del procesamiento
- El archivo Excel que causó el problema
- Lo que esperabas vs. lo que pasó

---

## 📌 Tips & Trucos

### Tip 1: Validar Structure Antes de Subir
```
Asegúrate que tu Excel tenga:
✓ Hoja "Personal" con datos
✓ Headers en filas 12-13 (multi-nivel)
✓ Columna "Nombre"
✓ Columna "Titulación" (opcional pero recomendado)
✓ Columnas para 2024 (Horas IT, Coste IT)
```

### Tip 2: Si Falta un Campo
```
No pasa nada. El código:
1. Te avisa en los logs
2. Usa valor vacío para ese campo
3. Continúa procesando

Ejemplo:
- Sin Titulación → Campo "Titulación 1" vacío
- Sin Personal → Archivo JSON vacío
- Sin 2024 → Archivo JSON vacío

IMPORTANTE: Siempre crear el archivo (vacío si es necesario)
para que el resto del programa funcione.
```

### Tip 3: Editar Después de Subir
```
1. Sube Excel → Genera datos automáticamente
2. Edita tabla en la UI → Cambios locales
3. Genera Ficha → Usa datos editados

NO necesitas re-subir Excel si solo necesitas
cambios pequeños en la tabla.
```

### Tip 4: Múltiples Años
```
Si tu Excel tiene 2024 Y 2025:
→ El código extrae SOLO 2024

Si necesitas otros años:
→ Abre una issue o contacta
→ Se puede adaptar fácilmente
```

---

## 🚨 Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "No hay datos" | Personal vacío o sin horas/coste | Verifica Excel, agrega datos |
| "Archivo vacío" | Falta columna Nombre/Horas/Coste | Verifica estructura Excel |
| "0 personas" | Todos tienen horas=0 y coste=0 | Verifica valores en Excel |
| "Coste horario incorrecto" | Horas = 0 (división por cero) | Edita manualmente en UI |
| "Año incorrecto" | Excel tiene 2025, buscamos 2024 | Actualiza Excel a 2024 |

---

## ✅ Checklist Antes de Enviar a Cliente

- [ ] ¿Subiste el Excel correcto?
- [ ] ¿Se generaron los datos correctamente?
- [ ] ¿Verificaste la tabla (29 personas)?
- [ ] ¿Editaste campos si necesitabas?
- [ ] ¿Descargaste la Ficha 2.1 en WORD?
- [ ] ¿Revisaste que todo se vea correctamente?
- [ ] ¿Generaste también Ficha 2.2 (Colaboraciones)?
- [ ] ¿Verificaste que los importes cuadren?

---

## 🎓 Resumen Rápido

```
ANTES: Procesamiento frágil, crash si estructura diferente
AHORA: Búsqueda flexible, valida antes de procesar, logs claros

RESULTADO: 29 personas extraídas correctamente ✅
TIEMPO: Automático, casi instantáneo
EDICIÓN: Totalmente editable después en la UI
FORMATO: WORD (Ficha 2.1) listo para enviar
```

---

**Versión**: v2.0 (Robust Processing)
**Estado**: ✅ Listo para Producción
**Último Update**: 2024
