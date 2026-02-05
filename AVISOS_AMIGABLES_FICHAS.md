# Mejoras: Avisos Amigables para Fichas Selectivas

## Descripción del Cambio
Se ha mejorado la experiencia del usuario al generar fichas individuales. Ahora cuando no hay datos suficientes para generar una ficha, se muestra un aviso amigable en lugar de un error 400.

## Cambios Realizados

### Backend (main.py)

#### Endpoints `/generate-ficha-2-1-only` y `/generate-ficha-2-2-only`
**Cambio principal:** Retornan siempre HTTP 200, con un objeto JSON que indica si se pudo generar o no.

**Respuesta cuando SÍ se puede generar:**
```json
{
  "success": true,
  "status": "success",
  "message": "✅ Ficha 2.1 generada (5 personas)",
  "aviso": null,
  "file": "Ficha_2_1.docx"
}
```

**Respuesta cuando NO se puede generar (falta de datos):**
```json
{
  "success": false,
  "status": "error",
  "message": "❌ No se puede generar Ficha 2.1",
  "aviso": "No hay datos de personal. Cargue un Anexo primero.",
  "file": null
}
```

**Ejemplo 1: Intentar generar Ficha 2.2 en PLANEROPTI (sin colaboraciones/facturas)**
```json
{
  "success": false,
  "status": "error",
  "message": "❌ No se puede generar Ficha 2.2",
  "aviso": "No hay datos de colaboraciones o facturas.",
  "file": null
}
```

**Ejemplo 2: Intentar generar Ficha 2.1 sin datos de personal**
```json
{
  "success": false,
  "status": "error",
  "message": "❌ No se puede generar Ficha 2.1",
  "aviso": "No hay datos de personal. Cargue un Anexo primero.",
  "file": null
}
```

### Frontend (ActionsPanel.tsx)

#### Manejadores actualizados
- `handleGenerarFicha2_1Solo()`: Ahora verifica `response.data.success` y muestra avisos amigables
- `handleGenerarFicha2_2Solo()`: Ahora verifica `response.data.success` y muestra avisos amigables

#### Mejora visual de avisos
**Antes:**
- Avisos en fondo amarillo (advertencia genérica)

**Ahora:**
- Avisos en fondo rojo (es información de error, no una advertencia)
- Borde rojo izquierdo para mayor visibilidad
- Ícono de alerta prominente (⚠️)
- Mensaje claro: "Falta de datos para generar fichas"
- Sugerencia al usuario: "Cargue un Anexo o edite los datos existentes"

#### Mejora visual de opciones de descarga
**Antes:**
- Botones en fondo gris (indistinto)
- Título: "Descargar fichas individuales"

**Ahora:**
- Contenedor en fondo verde (éxito, datos disponibles)
- Borde verde
- Título claro: "Fichas disponibles para descargar"
- Botones mejorados con textos descriptivos:
  - "📄 Descargar solo Ficha 2.1 (Personal)"
  - "📄 Descargar solo Ficha 2.2 (Colaboraciones/Facturas)"

## Flujo de Usuario Mejorado

### Escenario 1: Ficha 2.1 disponible, Ficha 2.2 no disponible

1. Usuario selecciona proyecto PLANEROPTI
2. Hace clic en "Generar Fichas"
3. **Resultado:**
   - ✅ Ficha 2.1 se genera correctamente
   - ⚠️ Se muestra un aviso en rojo:
     > "⚠️ Falta de datos para generar fichas
     > • No hay datos de colaboraciones o facturas.
     > 💡 Cargue un Anexo o edite los datos existentes para poder generar todas las fichas"
   - ✅ Se muestra el botón "📄 Descargar solo Ficha 2.1 (Personal)"
   - ❌ NO se muestra el botón "📄 Descargar solo Ficha 2.2"

4. Usuario puede:
   - Descargar Ficha 2.1 haciendo clic en el botón
   - Editar datos de colaboraciones/facturas
   - Hacer clic de nuevo en "Generar Fichas" después de agregar datos

### Escenario 2: Sin datos de personal

1. Usuario intenta generar fichas sin haber cargado un Anexo
2. **Resultado:**
   - ❌ Se muestra un aviso en rojo:
     > "⚠️ Falta de datos para generar fichas
     > • No hay datos de personal. Cargue un Anexo primero.
     > • No hay datos de colaboraciones o facturas.
     > 💡 Cargue un Anexo o edite los datos existentes para poder generar todas las fichas"
   - ❌ NO se muestran botones de descarga
   - Usuario debe cargar primero un Anexo

### Escenario 3: Datos completos

1. Usuario selecciona proyecto GRANDES
2. Hace clic en "Generar Fichas"
3. **Resultado:**
   - ✅ Ambas fichas se generan correctamente
   - ❌ NO hay avisos rojos (todo está bien)
   - ✅ Se muestran ambos botones:
     - "📄 Descargar solo Ficha 2.1 (Personal)"
     - "📄 Descargar solo Ficha 2.2 (Colaboraciones/Facturas)"
   - ✅ También está disponible "⬇️ Descargar Fichas (ZIP)" para descargar todas

## Testing Manual

### Test 1: Generar fichas en PLANEROPTI
```bash
# Abrir navegador: http://localhost:5173
# 1. Seleccionar cliente: A31768138
# 2. Seleccionar proyecto: PLANEROPTI
# 3. Hacer clic en "Generar Fichas"
# Resultado esperado:
# - ✅ Mensaje de éxito para Ficha 2.1
# - ⚠️ Aviso rojo sobre falta de colaboraciones/facturas
# - ✅ Botón "📄 Descargar solo Ficha 2.1 (Personal)"
# - ❌ NO aparece botón para Ficha 2.2
```

### Test 2: Generar fichas en GRANDES
```bash
# Abrir navegador: http://localhost:5173
# 1. Seleccionar cliente: A31768138
# 2. Seleccionar proyecto: GRANDES
# 3. Hacer clic en "Generar Fichas"
# Resultado esperado:
# - ✅ Mensaje de éxito para Ficha 2.1
# - ✅ Mensaje de éxito para Ficha 2.2
# - ❌ NO hay avisos (todo está bien)
# - ✅ Botón "📄 Descargar solo Ficha 2.1 (Personal)"
# - ✅ Botón "📄 Descargar solo Ficha 2.2 (Colaboraciones/Facturas)"
```

### Test 3: Descargar Ficha 2.2 cuando no hay datos
```bash
# Desde el estado de PLANEROPTI (con aviso rojo)
# 1. Hacer clic en "📄 Descargar solo Ficha 2.2 (Colaboraciones/Facturas)"
# Resultado esperado:
# - ⚠️ Se muestra aviso: "No hay datos de colaboraciones o facturas."
# - ❌ No se descarga nada
# - Opcionalmente, el usuario ve el botón pero está deshabilitado
```

## Ventajas de estos cambios

1. **Mejor UX**: El usuario recibe mensajes claros en lugar de códigos de error
2. **Más flexibilidad**: El usuario puede descargar solo las fichas que necesita
3. **Guía al usuario**: Los avisos sugieren qué hacer siguiente
4. **Distinción visual**: Rojo para errores/falta de datos, verde para éxito
5. **Sin errores HTTP**: Todo retorna 200, los errores son lógicos (no técnicos)

## Compatibilidad

- ✅ Completamente compatible con flujos existentes
- ✅ No afecta a otros endpoints
- ✅ Funciona con `cliente_nif` y `proyecto_acronimo` opcionales
- ✅ Mantiene backward compatibility

## Próximas mejoras posibles

1. Deshabilitar botones de descarga si no hay datos (en lugar de solo no mostrarlos)
2. Agregar botón "Editar datos" junto a los avisos
3. Mostrar contador de registros: "5 personas", "3 colaboraciones", etc.
4. Permitir cargar datos parcialmente y regenerar solo fichas específicas
