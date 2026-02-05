# Cambios: Avisos y Descargas Selectivas de Fichas

## Resumen
Se han implementado avisos amigables al usuario y opciones para descargar fichas individuales (solo Ficha 2.1 o solo Ficha 2.2) según la disponibilidad de datos.

## Cambios en el Backend (main.py)

### 1. Endpoint `/generate-fichas` - Actualizado
**Cambios:**
- Ahora retorna información detallada sobre qué fichas se pueden generar
- Captura avisos cuando faltan datos (colaboraciones, facturas, personal)
- Cuenta registros en los JSONs para determinar si hay datos válidos

**Nuevo Response:**
```json
{
  "status": "success",
  "message": "Fichas generadas: Ficha_2_1.docx",
  "files": ["Ficha_2_1.docx"],
  "avisos": [
    "Ficha 2.2: No hay datos de colaboraciones o facturas."
  ],
  "puede_generar_2_1": true,
  "puede_generar_2_2": false,
  "datos": {
    "personal": 5,
    "colaboraciones": 0,
    "facturas": 0
  }
}
```

### 2. Nuevo Endpoint `/generate-ficha-2-1-only` (POST)
**Propósito:** Generar solo la Ficha 2.1 (personal)

**Parámetros:**
- `cliente_nif` (query): NIF del cliente
- `proyecto_acronimo` (query): Acrónimo del proyecto
- `payload` (body): { cliente_nombre, cliente_nif, anio_fiscal }

**Response:**
```json
{
  "status": "success",
  "message": "Ficha 2.1 generada",
  "file": "Ficha_2_1.docx"
}
```

**Errores:**
- 400: No hay datos de personal o registro vacío
- 400: Plantilla no encontrada

### 3. Nuevo Endpoint `/generate-ficha-2-2-only` (POST)
**Propósito:** Generar solo la Ficha 2.2 (colaboraciones y facturas)

**Parámetros:**
- `cliente_nif` (query): NIF del cliente
- `proyecto_acronimo` (query): Acrónimo del proyecto
- `payload` (body): { cliente_nombre, cliente_nif, anio_fiscal }

**Response:**
```json
{
  "status": "success",
  "message": "Ficha 2.2 generada",
  "file": "Ficha_2_2.docx"
}
```

**Errores:**
- 400: No hay datos de colaboraciones o facturas
- 400: Plantilla no encontrada

## Cambios en el Frontend

### 1. ActionsPanel.tsx - Actualizado
**Nuevos estados:**
```typescript
const [generationAvisos, setGenerationAvisos] = useState<string[]>([]);
const [puede_generar_2_1, setPuedeGenerar2_1] = useState<boolean>(false);
const [puede_generar_2_2, setPuedeGenerar2_2] = useState<boolean>(false);
```

**Funciones nuevas:**
- `handleGenerarFicha2_1Solo()`: Genera solo Ficha 2.1
- `handleGenerarFicha2_2Solo()`: Genera solo Ficha 2.2

**Actualizaciones:**
- `handleGenerateFichas()`: Ahora captura avisos y disponibilidad de fichas del response

**UI Nuevo:**
1. **Avisos Condicionales** - Se muestran cuando hay avisos:
   ```
   ⚠️ Avisos sobre las fichas:
   - Ficha 2.2: No hay datos de colaboraciones o facturas.
   ```

2. **Opciones de Descarga Selectiva** - Se muestran cuando hay fichas disponibles:
   - Botón "📄 Solo Ficha 2.1" (si puede_generar_2_1 = true)
   - Botón "📄 Solo Ficha 2.2" (si puede_generar_2_2 = true)

### 2. api/client.ts - Actualizado
**Nuevos métodos:**
```typescript
generateFicha2_1Only: (clienteNif?: string, proyectoAcronimo?: string, payload?: any) => {...}
generateFicha2_2Only: (clienteNif?: string, proyectoAcronimo?: string, payload?: any) => {...}
```

## Flujo de Usuario

### Escenario 1: Proyecto con datos completos (GRANDES)
1. Usuario selecciona cliente y proyecto
2. Hace clic en "Generar Fichas"
3. ✅ Se generan ambas fichas (2.1 y 2.2)
4. ❌ No hay avisos
5. ✅ Aparecen ambos botones de descarga selectiva
6. Usuario puede descargar una o ambas fichas

### Escenario 2: Proyecto con datos parciales (PLANEROPTI)
1. Usuario selecciona cliente y proyecto
2. Hace clic en "Generar Fichas"
3. ✅ Se genera solo Ficha 2.1
4. ⚠️ Se muestra aviso: "Ficha 2.2: No hay datos de colaboraciones o facturas."
5. ✅ Aparece solo el botón "Solo Ficha 2.1"
6. Usuario puede:
   - Descargar Ficha 2.1
   - Editar datos de colaboraciones/facturas
   - Hacer clic en "Solo Ficha 2.2" para generar la ficha cuando tenga datos

### Escenario 3: Proyecto sin datos de personal
1. Usuario intenta generar fichas sin Anexo cargado
2. ❌ Se muestra error: "Ficha 2.1: No hay datos de personal. Cargue un Anexo primero."
3. ❌ No se puede descargar nada

## Testing

### Test Case 1: GRANDES (datos completos)
```bash
POST /generate-fichas?cliente_nif=A31768138&proyecto_acronimo=GRANDES
```
**Resultado esperado:**
- ✅ Ficha_2_1.docx y Ficha_2_2.docx generadas
- ✅ puede_generar_2_1 = true
- ✅ puede_generar_2_2 = true
- ✅ avisos = [] (vacío)

### Test Case 2: PLANEROPTI (datos parciales)
```bash
POST /generate-fichas?cliente_nif=A31768138&proyecto_acronimo=PLANEROPTI
```
**Resultado esperado:**
- ✅ Ficha_2_1.docx generada
- ❌ Ficha_2_2.docx NO generada
- ✅ puede_generar_2_1 = true
- ❌ puede_generar_2_2 = false
- ⚠️ avisos = ["Ficha 2.2: No hay datos de colaboraciones o facturas."]

### Test Case 3: Generar solo Ficha 2.1
```bash
POST /generate-ficha-2-1-only?cliente_nif=A31768138&proyecto_acronimo=PLANEROPTI
```
**Resultado esperado:**
- ✅ Ficha_2_1.docx generada
- message = "Ficha 2.1 generada"

### Test Case 4: Generar solo Ficha 2.2 (fallará sin datos)
```bash
POST /generate-ficha-2-2-only?cliente_nif=A31768138&proyecto_acronimo=PLANEROPTI
```
**Resultado esperado:**
- ❌ Error 400
- detail = "No hay datos de colaboraciones o facturas."

## Instalación/Activación

1. **Backend:**
   ```bash
   cd C:\Fichas\backend
   C:\Fichas\venv\Scripts\python.exe -m uvicorn main:app --reload
   ```

2. **Frontend:**
   ```bash
   cd C:\Fichas\frontend
   npm run dev
   ```

3. **Probar:**
   - Ir a http://localhost:5173
   - Seleccionar cliente A31768138
   - Seleccionar proyecto GRANDES o PLANEROPTI
   - Hacer clic en "Generar Fichas"
   - Ver avisos y opciones disponibles

## Notas Importantes

1. **Avisos dinámicos:** Los avisos se generan en tiempo de ejecución basados en los datos disponibles
2. **Botones condicionales:** Los botones de descarga selectiva solo aparecen si las fichas se pueden generar
3. **Validación previa:** Se recomienda usar "Validar Datos" antes de generar para verificar que los datos sean correctos
4. **Descarga directa:** Los usuarios pueden descargar directamente desde el frontend sin necesidad de procesos intermedios

## Compatibilidad

- ✅ Compatible con proyectos existentes
- ✅ Compatible con clientes sin proyecto
- ✅ Compatible con INPUT_DIR (modo legado)
- ✅ Mantiene backward compatibility con endpoints existentes
