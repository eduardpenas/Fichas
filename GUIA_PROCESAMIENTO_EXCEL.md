# 📖 GUÍA: Procesamiento Robusto de Anexo II

## ¿Qué cambió?

El procesamiento de la hoja **Personal** ahora es mucho más robusto y puede manejar variaciones en la estructura del Excel sin fallar.

## Flujo de Procesamiento

```
Excel (Anexo II)
    ↓
[Lectura de headers multi-nivel]
    ↓
[Búsqueda flexible de columnas]
    ↓ Detecta año fiscal automáticamente
    ↓ Busca: Nombre, Titulación, Horas IT, Coste IT
    ↓
[Filtrado de datos válidos]
    ↓ Solo personas con Horas > 0 O Coste > 0
    ↓
[Generación de JSON]
    ↓
Excel_Personal_2.1.json (29 personas en este caso)
```

## Ejemplo Práctico

### Entrada (Excel)
```
Sheet "Personal", Rows 12-13 (headers):
┌─────────────────────────────────────────────┐
│ Nombre  │ Titulación │ 2024 (Horas IT) │ 2024 (Coste IT) │ ...
├─────────────────────────────────────────────┤
│ Juan    │ Ingeniero  │ 100             │ 4362            │
│ María   │ Máster     │ 80              │ 3490            │
│ Pedro   │ -          │ 0               │ 0               │ ← Excluido
│ ...
└─────────────────────────────────────────────┘
```

### Procesamiento
```
1. Lee headers: detecta que son multi-nivel
2. Busca columnas:
   ✓ Nombre encontrado
   ✓ Titulación encontrada
   ✓ Horas IT (2024) encontradas
   ✓ Coste IT (2024) encontrado
3. Filtra:
   - Pedro excluido (0 horas Y 0 coste)
   - Juan y María incluidos
4. Calcula:
   - Coste horario = Coste / Horas
   - Juan: 4362 / 100 = €43.62/hora
```

### Salida (JSON)
```json
[
  {
    "Nombre": "JUAN",
    "Apellidos": "...",
    "Titulación 1": "Ingeniero",
    "Coste horario (€/hora)": 43.62,
    "Horas totales": 100.0,
    "Coste total (€)": 4362,
    "Coste IT (€)": 4362,
    "Horas IT": 100.0,
    ...
  },
  ...
]
```

## Características Principales

### 1. Detección Automática de Año Fiscal
```
No necesitas decirle al programa qué año procesar.
Si los datos tienen 2024, 2025, 2026, etc., el código busca 2024.

Si no encuentra 2024:
  ⚠️ Te dice qué años SÍ tiene el archivo
  
Ejemplo de log:
  WARN - No se encontraron Horas/Coste IT para año 2024
  Anos disponibles: ['2022', '2023', '2026']
```

### 2. Búsqueda Flexible de Columnas
```
Case-insensitive: NOMBRE = Nombre = nombre ✓
Parcial: "horas" + "it" = busca esa combinación

Funciona con:
  - "Horas Imputadas IT"
  - "HORAS_IT"
  - "2024 Horas IT"
  - Cualquier variación razonable
```

### 3. Validación Inteligente
```
Antes de procesar, valida:
  ✓ ¿Existe columna Nombre?
  ✓ ¿Existe Horas IT para 2024?
  ✓ ¿Existe Coste IT para 2024?

Si faltan → Crea archivo vacío (no rompe el programa)
Si OK → Procesa normalmente
```

### 4. Logs Detallados
```
Cada paso importante se registra:
  - Dimensiones del Excel
  - Columnas detectadas
  - Registros antes/después de filtrar
  - Resultado final (N personas, archivo creado)
```

## Casos Especiales

### Personal Sheet Vacío
```
El programa:
  1. Detecta que no hay datos
  2. Crea archivo JSON vacío con estructura
  3. El botón "Generar Ficha 2.1" muestra gris
  4. El usuario puede editar manualmente en la UI
```

### Columna Titulación Faltante
```
El programa:
  1. Detecta que no existe
  2. Usa string vacío ""
  3. Genera Personal normal
  4. Campo "Titulación 1" está vacío
  5. El usuario puede editarlo en la UI
```

### Excel con Estructura Ligeramente Diferente
```
Si las columnas están en otro lugar pero tienen nombres reconocibles:
  → El código las encuentra igual (búsqueda flexible)
  
Si los headers NO están en filas 12-13:
  → Esto SÍ causa problema (asume esas filas)
  → Contacta si necesitas soporte para estructura radicalmente diferente
```

## Flujo de Uso para el Usuario

### Escenario 1: Todo Normal ✅
```
1. Usuario sube Excel (Anexo II)
2. Backend procesa automáticamente
3. Detecta 29 personas, crea JSON
4. Frontend muestra tabla con datos
5. Usuario puede editar si necesita
```

### Escenario 2: Personal Vacío o Sin Datos ⚠️
```
1. Usuario sube Excel
2. Backend detecta que Personal no tiene datos
3. Crea archivo JSON vacío
4. Frontend muestra: "No hay datos de Personal (edita manualmente)"
5. Usuario puede agregar personas manualmente
```

### Escenario 3: Estructura Inesperada ⚠️⚠️
```
1. Usuario sube Excel con estructura radicalmente diferente
2. Backend intenta procesar
3. Si encuentra las columnas → OK (búsqueda flexible)
4. Si NO encuentra → Crea archivo vacío + logs claros
5. Usuario ve los logs y entiende qué faltó
```

## Debugging

Si algo no funciona, revisa los logs:

```bash
# Ejecutar procesamiento directamente con logs
python -c "from src.procesar_anexo import procesar_anexo; procesar_anexo()"
```

Los logs te dirán:
- ✓ Qué columnas detectó
- ✓ Cuántos registros procesó
- ✗ Qué columnas faltaron (si es el caso)

Ejemplo:
```
👤 Procesando Personal...
   Dimensiones originales: 39 filas x 35 columnas
   Año fiscal objetivo: 2024
   Buscando columnas de interés...
      OK - Nombre encontrado: ('Nombre', 'Unnamed: 2_level_1')
      ❌ No se encontró Titulación
      ✓ Horas IT (2024) encontradas
      ✓ Coste IT (2024) encontrado
   Extrayendo datos...
   Registros antes de filtrar: 39
   Registros después de filtrar: 29
   OK - Personal generado: 29 personas
```

## Resumen de Mejoras

| Problema Anterior | Solución Nueva |
|-------------------|----------------|
| Crash si estructura diferente | Búsqueda flexible + validación |
| Error "Series object" | Manejo explícito de casos vacíos |
| Logs confusos | Logs detallados en cada paso |
| Año hardcoded | Detección automática |
| Fallos silenciosos | Archivo vacío + logs claros |

## Preguntas Frecuentes

**P: ¿Qué pasa si mi Excel no tiene headers en filas 12-13?**
A: Eso aún asume el formato estándar. Si necesitas otro, contacta para soporte.

**P: ¿Y si tengo datos de 2025 en lugar de 2024?**
A: El código buscará 2024. Si no existe, te mostrará:
```
WARN - No se encontraron Horas/Coste IT para año 2024
Anos disponibles: ['2025', '2026']
```
En ese caso, actualiza tu Excel a 2024 o contacta para cambiar el año.

**P: ¿Puedo editar los datos manualmente después?**
A: SÍ. La UI permite editar toda la tabla de Personal incluso después de subir Excel.

**P: ¿Qué es "Coste horario"?**
A: Se calcula como `Coste Total / Horas Totales`. Ejemplo: €5000 / 100 horas = €50/hora

**P: ¿Cómo corrijo datos incorrectos?**
A: 
1. En la UI: Edita directamente en la tabla (ya implementado)
2. En Excel: Corrije y sube el archivo nuevo
3. Combinado: Sube Excel + edita manualmente lo que necesites

---

**Última actualización**: 2024
**Version**: v2 (Robusta)
