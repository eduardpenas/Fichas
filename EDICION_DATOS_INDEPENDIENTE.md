# ✅ Edición de Datos sin Dependencia de Anexo

## Cambio Principal

Se ha modificado `DataEditor.tsx` para que las tablas de edición:
1. **Siempre estén disponibles** - No dependen de que el usuario haya cargado un Anexo
2. **Muestren la estructura correcta** - Tienen todas las columnas con los atributos esperados
3. **Permitan agregar filas** - El usuario puede crear nuevos registros manualmente
4. **Permitan eliminar filas** - El usuario puede quitar registros

## Cambios Realizados

### 1. Estructura de Columnas Predefinida
Se agregó `COLUMN_DEFINITIONS` que define exactamente qué columnas debe tener cada tabla:

```typescript
const COLUMN_DEFINITIONS: Record<string, string[]> = {
  personal: [
    'Nombre', 'Apellidos', 'Titulación 1', 'Titulación 2',
    'Coste horario (€/hora)', 'Horas totales', 'Coste total (€)',
    'Coste IT (€)', 'Horas IT', 'Departamento', 'Puesto actual',
    'Coste I+D (€)', 'Horas I+D', 'EMPRESA 1', 'PERIODO 1', 'PUESTO 1',
    'EMPRESA 2', 'PERIODO 2', 'PUESTO 2', 'EMPRESA 3', 'PERIODO 3', 'PUESTO 3'
  ],
  colaboraciones: [
    'Razón social', 'NIF', 'NIF 2', 'Entidad contratante',
    'País de la entidad', 'Localidad', 'Provincia', 'País de realización'
  ],
  facturas: [
    'Entidad', 'Nombre factura', 'Importe (€)'
  ],
};
```

### 2. Función createEmptyRow()
Crea una fila vacía con la estructura correcta:

```typescript
const createEmptyRow = (dataType: 'personal' | 'colaboraciones' | 'facturas') => {
  const columns = COLUMN_DEFINITIONS[dataType];
  const emptyRow: any = {};
  columns.forEach(col => {
    emptyRow[col] = '';
  });
  return emptyRow;
};
```

### 3. Manejo de Datos Vacíos
Cuando no hay datos (archivo no existe):
- Se inicializa con un array vacío `[]`
- Se muestra un mensaje: "No hay datos. Haz clic en '➕ Agregar fila' para crear nuevos registros."
- El usuario puede hacer clic en "➕ Agregar fila" para empezar a crear

### 4. Nuevas Funciones en la Tabla

#### handleAddRow()
Agrega una nueva fila vacía a la tabla:
```typescript
const handleAddRow = () => {
  const newRow = createEmptyRow(dataType);
  const newData = [...displayData, newRow];
  setDisplayData(newData);
  setHasChanges(true);
};
```

#### handleDeleteRow(rowIndex)
Elimina una fila específica:
```typescript
const handleDeleteRow = (rowIndex: number) => {
  const newData = displayData.filter((_, idx) => idx !== rowIndex);
  setDisplayData(newData);
  setHasChanges(true);
};
```

### 5. Mejoras Visuales

#### Cuando la tabla está vacía:
```
┌──────────────────────────────────────┐
│ No hay datos.                        │
│ Haz clic en "➕ Agregar fila" para  │
│ crear nuevos registros.              │
│                                      │
│       [➕ Agregar fila]              │
└──────────────────────────────────────┘
```

#### Cuando hay datos:
- **Columna #**: Número de fila (gris)
- **Columnas de datos**: Editables al hacer clic
- **Columna ✕**: Botón para eliminar la fila
- **Botón ➕ Agregar fila**: Para agregar nuevas filas
- **Botón 💾 Guardar Cambios**: Para guardar todos los cambios

## Casos de Uso

### Caso 1: Usuario sin Anexo cargado
1. Usuario selecciona cliente y proyecto
2. Hace clic en "✏️ Personal (Ficha 2.1)"
3. La tabla está vacía
4. Usuario hace clic en "➕ Agregar fila"
5. Aparece una fila vacía con todas las columnas
6. Usuario edita cada celda haciendo clic
7. Usuario puede agregar más filas
8. Hace clic en "💾 Guardar Cambios"
9. Los datos se guardan
10. Usuario puede generar fichas

### Caso 2: Usuario con datos parciales (PLANEROPTI)
1. Usuario tiene datos de personal
2. No tiene colaboraciones (porque el Anexo no las tenía)
3. Usuario hace clic en "✏️ Colaboraciones (Ficha 2.2)"
4. La tabla está vacía (pero con las columnas correctas)
5. Usuario agrega colaboraciones manualmente
6. Guarda
7. Ahora puede generar Ficha 2.2

### Caso 3: Usuario con Anexo completo
1. Usuario carga un Anexo con todos los datos
2. Hace clic en "✏️ Personal (Ficha 2.1)"
3. Ve todos los datos del Anexo
4. Puede editar registros
5. Puede agregar más registros
6. Puede eliminar registros que no necesita
7. Guarda
8. Genera las fichas

## Comportamiento de la UI

### Tabla con datos:
```
┌────┬──────────────┬──────────┬─────────────────┬─────┐
│ #  │ Nombre       │ Apellido │ Titulación 1    │  ✕  │
├────┼──────────────┼──────────┼─────────────────┼─────┤
│ 1  │ ANGEL        │ ZAMARRON │ INGENIERO AGRO. │  ✕  │
│ 2  │ ANTONIO      │ FERREIRO │ ING.TÉC. IND.   │  ✕  │
│ 3  │              │          │                 │  ✕  │  ← Nueva fila vacía
└────┴──────────────┴──────────┴─────────────────┴─────┘
```

### Botones de control:
```
3 registro(s) • Hay cambios sin guardar

[➕ Agregar fila]        [❌ Cancelar] [💾 Guardar Cambios]
```

## Edición de Celdas

1. **Hacer clic en una celda** → Se abre editor de texto
2. **Escribir nuevo valor** → Se actualiza en vivo
3. **Presionar Enter o click fuera** → Se guarda y se cierra el editor
4. **Presionar Escape** → Se cancela la edición

## Guardado de Datos

Cuando el usuario hace clic en "💾 Guardar Cambios":
1. Se envían todos los datos al backend
2. Se guarda el JSON actualizado
3. Se muestra un mensaje: "✅ Datos de Personal guardados (3 registros)"
4. Los cambios se confirman

## Validación

- ✅ Las tablas siempre tienen las columnas correctas
- ✅ Los datos se guardan en los JSONs correspondientes
- ✅ Se permite editar incluso si no hay Anexo
- ✅ Se pueden agregar registros manualmente
- ✅ Se pueden eliminar registros
- ✅ Los cambios se rastrean (Hay cambios sin guardar)

## Flujo Completo

```
Usuario abre editor
        ↓
¿Hay datos? 
    ↙      ↘
  SI       NO
  ↓        ↓
Mostrar   Mostrar
tabla     vacío
  ↓        ↓
  └─────→ Usuario puede:
         - Editar celdas
         - Agregar filas (➕)
         - Eliminar filas (✕)
           ↓
        ¿Hay cambios?
            ↓
         Guardar (💾)
            ↓
        ✅ Datos salvos
```

## Archivos Modificados

- **frontend/src/components/DataEditor.tsx**
  - Agregado: `COLUMN_DEFINITIONS` constante
  - Agregado: `createEmptyRow()` función
  - Agregado: `handleAddRow()` método
  - Agregado: `handleDeleteRow()` método
  - Mejorado: Manejo de datos vacíos
  - Mejorado: Visualización de tabla con números de fila y columna de eliminar

## Próximas Mejoras Posibles

1. ✅ Validación de datos antes de guardar
2. ✅ Importar datos desde CSV
3. ✅ Plantillas de filas (copiar fila anterior)
4. ✅ Búsqueda y filtrado en tablas grandes
5. ✅ Columnas de ancho ajustable
6. ✅ Selección múltiple y operaciones en lote
