# 🎨 Vista Previa del Frontend

## 📋 Interfaz Principal (http://localhost:5173)

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                            ┃
┃  📋 Gestor de Fichas                                     ┃
┃  Sistema de gestión de datos y generación automática   ┃
┃                                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─ ALERTAS ─────────────────────────────────────────────────┐
│ ✅ Anexo procesado: Personal generado: 29 personas     × │
│ ⚠️ Validación completada: 1 advertencia detectada       × │
└───────────────────────────────────────────────────────────┘

┌─ 1️⃣ CARGAR ARCHIVOS ──────────────────────────────────────┐
│                                                            │
│  Anexo II (Excel)                                        │
│  ┌──────────────────────────────────────┐               │
│  │ Seleccionar archivo... ▼             │ [Cargar]      │
│  └──────────────────────────────────────┘               │
│  ✓ Anexo_II_tipo_a_.xlsx                                │
│                                                            │
│  CVs (PDF)                                               │
│  ┌──────────────────────────────────────┐               │
│  │ Seleccionar archivos... ▼            │ [Cargar 5]    │
│  └──────────────────────────────────────┘               │
│  ✓ CV_Juan.pdf                                           │
│  ✓ CV_Maria.pdf                                          │
│  ... +3 más                                              │
│                                                            │
└───────────────────────────────────────────────────────────┘

┌─ 2️⃣ REVISAR Y EDITAR DATOS ──────────────────────────────┐
│                                                            │
│  📊 Tabla de Personal (Ficha 2.1)                       │
│  Edita los datos haciendo clic en cada celda            │
│                                                            │
│  [🔄 Actualizar] [➕ Agregar Fila] [💾 Guardar]         │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Acciones │ Nombre    │ Apellidos    │ Titulación    │ │
│  ├──────────┼───────────┼──────────────┼───────────────┤ │
│  │ [🗑️]    │ Juan      │ García López │ Ingeniero [✏️]│ │
│  │ [🗑️]    │ María     │ López Ruiz   │ Abogada       │ │
│  │ [🗑️]    │ Carlos    │ Martínez     │ Médico        │ │
│  │ ...       │ ...       │ ...          │ ...           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Total: 29 registros | Columnas: 12                     │
│                                                            │
└───────────────────────────────────────────────────────────┘

┌─ 3️⃣ PROCESAR Y GENERAR ────────────────────────────────────┐
│                                                            │
│  [🔍 Procesar CVs]  [✅ Validar Datos]  [📄 Generar Fichas] │
│                                                            │
│  ┌─ RESULTADO DE VALIDACIÓN ──────────────────────────┐ │
│  │                                                      │ │
│  │ ✅ LISTO PARA GENERAR FICHAS                       │ │
│  │                                                      │ │
│  │ Personal:                                          │ │
│  │   Errores: 0 | Advertencias: 1                    │ │
│  │   ⚠️ 24 personas sin experiencia laboral          │ │
│  │                                                      │ │
│  │ Colaboraciones:                                    │ │
│  │   Errores: 0 | Advertencias: 0                    │ │
│  │                                                      │ │
│  └────────────────────────────────────────────────────┘ │
│                                                            │
└───────────────────────────────────────────────────────────┘

┌─ FOOTER ──────────────────────────────────────────────────┐
│ 🚀 Gestor de Fichas v1.0 - Sistema de procesamiento    │
│ API: http://localhost:8000 | Frontend: http://localhost │
└───────────────────────────────────────────────────────────┘
```

---

## 🖱️ Interacciones Principales

### 1. Cargar Anexo
```
Usuario:        "Quiero cargar el Anexo II"
Acción:         Hace clic en input file, selecciona Excel
Sistema:        ✅ Procesa Anexo
Resultado:      Genera 3 JSONs (Personal, Colaboraciones, Facturas)
Feedback:       "✅ Anexo procesado: Personal generado: 29 personas"
```

### 2. Editar Tabla
```
Usuario:        "Quiero cambiar el nombre de Juan"
Acción:         Hace clic en celda "Juan"
Sistema:        Muestra input editable
Usuario:        Tipea "Juan Carlos" y presiona Tab/Enter
Sistema:        Guarda cambio localmente
Feedback:       ✓ Celda se actualiza
```

### 3. Procesar CVs
```
Usuario:        Hace clic en "🔍 Procesar CVs"
Sistema:        Lee PDFs de inputs/cvs/
             Extrae experiencia laboral
             Actualiza tabla con nuevos datos
Feedback:       "✅ CVs procesados: 5 perfiles actualizados"
Resultado:      Tabla muestra EMPRESA 1-3, PUESTO 1-3, PERIODO 1-3
```

### 4. Validar Datos
```
Usuario:        Hace clic en "✅ Validar Datos"
Sistema:        Ejecuta validador.py
             Analiza campos, formatos, consistencias
             Genera reporte de errores/advertencias
Feedback:       Panel de validación muestra resultados
Posibles:       ✅ OK para procesar
             ⚠️ Advertencias detectadas
             ❌ Errores críticos detectados
```

### 5. Generar Fichas
```
Usuario:        Hace clic en "📄 Generar Fichas"
Sistema:        Verifica validación = OK
             Crea Ficha_2_1.docx (Personal)
             Crea Ficha_2_2.docx (Colaboraciones)
Feedback:       "✅ Fichas generadas: Ficha_2_1.docx, Ficha_2_2.docx"
Resultado:      Archivos disponibles en outputs/
```

---

## 📊 Componentes de la Interfaz

### FileUploader
```
┌─────────────────────────────────┐
│ 📁 Cargar Archivos              │
├─────────────────────────────────┤
│                                 │
│ Anexo II (Excel)               │
│ [Seleccionar archivo...] [▼]   │
│ [Cargar Anexo]                 │
│ ✓ Anexo_II_tipo_a_.xlsx         │
│                                 │
│ CVs (PDF)                       │
│ [Seleccionar archivos...] [▼]  │
│ [Cargar CVs (5)]                │
│ ✓ CV_Juan.pdf, CV_Maria.pdf...  │
│                                 │
└─────────────────────────────────┘
```

### EditableTable
```
┌────────────────────────────────────┐
│ 📊 Tabla de Personal (Ficha 2.1)  │
│ [🔄] [➕] [💾]                     │
├────────────────────────────────────┤
│ Acciones │ Nombre │ Apellidos │... │
├──────────┼────────┼──────────┼────┤
│ [🗑️]    │ Juan   │ García   │    │
│ [🗑️]    │ María  │ López    │    │
│ ...      │ ...    │ ...      │... │
├────────────────────────────────────┤
│ Total: 29 registros | Cols: 12    │
└────────────────────────────────────┘
```

### ActionsPanel
```
┌───────────────────────────────────────┐
│ ⚙️ Acciones                          │
├───────────────────────────────────────┤
│                                       │
│ [🔍 Procesar CVs]                    │
│ [✅ Validar Datos]                   │
│ [📄 Generar Fichas]                  │
│                                       │
│ ┌─ VALIDACIÓN ──────────────────────┐ │
│ │ ✅ LISTO PARA GENERAR FICHAS      │ │
│ │ Personal:                         │ │
│ │  - Errores: 0                    │ │
│ │  - Advertencias: 1               │ │
│ └─────────────────────────────────┘ │
│                                       │
└───────────────────────────────────────┘
```

---

## 🎯 Estados de la Aplicación

### Estado 1: Inicial (Sin datos)
```
- Campos vacíos
- Tabla: "No hay datos disponibles. Carga el Anexo primero."
- Botones: Todos funcionales
```

### Estado 2: Datos cargados
```
- Tabla poblada con Personal
- Campos editables (click en celdas)
- Botones "Procesar", "Validar", "Generar" activos
```

### Estado 3: Validación en progreso
```
- Loader visible ("Procesando...")
- Interfaz bloqueada
- Pantalla oscurecida
```

### Estado 4: Validación completa
```
- Panel de validación visible
- Resumen de errores/advertencias
- Botón "Generar Fichas" activo si no hay errores críticos
```

### Estado 5: Fichas generadas
```
- Alerta: "✅ Fichas generadas"
- Archivos disponibles en outputs/
- UI completa nuevamente funcional
```

---

## 🎨 Paleta de Colores

```
Primario:      #3b82f6 (Azul) - Headers, botones principales
Secundario:    #10b981 (Verde) - Botones de éxito
Danger:        #ef4444 (Rojo) - Errores, eliminar
Warning:       #f59e0b (Naranja) - Advertencias
Info:          #06b6d4 (Cian) - Información

Fondo:         #f9fafb (Gris muy claro)
Texto:         #111827 (Gris muy oscuro)
Bordes:        #d1d5db (Gris medio)
```

---

## 📱 Responsive Design

```
Desktop (≥1024px)              Tablet (768-1024px)      Mobile (≤768px)
┌──────────────────┐          ┌──────────────┐         ┌────────────┐
│ Header           │          │ Header       │         │ Header     │
├──────────────────┤          ├──────────────┤         ├────────────┤
│ Alertas (lado)   │          │ Alertas      │         │ Alertas    │
│ Uploader         │          │ (stack)      │         │ (stack)    │
│ Tabla (scroll)   │          │ Uploader     │         │ Uploader   │
│ Acciones (3 col) │          │ Tabla        │         │ Tabla      │
│ (lado)           │          │ (scroll)     │         │ (scroll)   │
│                  │          │ Acciones     │         │ Acciones   │
└──────────────────┘          │ (1 col)      │         │ (1 col)    │
                               └──────────────┘         └────────────┘
```

---

## ⌨️ Atajos de Teclado (Potencial futuro)

```
Ctrl+S          → Guardar cambios
Ctrl+V          → Validar
Ctrl+G          → Generar fichas
Ctrl+U          → Cargar archivo
Enter (en tabla)→ Guardar y siguiente celda
Tab             → Siguiente celda
```

---

## 📝 Mensajes de Usuario

### Éxito ✅
```
"✅ Anexo procesado: Personal generado: 29 personas"
"✅ CVs cargados: 5 archivos procesados"
"✅ Validación exitosa - Todos los datos son correctos"
"✅ Fichas generadas: Ficha_2_1.docx, Ficha_2_2.docx"
```

### Advertencia ⚠️
```
"⚠️ Por favor selecciona un archivo Excel (.xlsx)"
"⚠️ 24 personas sin experiencia laboral documentada"
"⚠️ Validación completada: 0 errores, 1 advertencia"
```

### Error ❌
```
"❌ Selecciona un archivo Anexo"
"❌ Solo se aceptan archivos PDF"
"❌ Error cargando datos: Connection refused"
"❌ No se puede procesar: Hay 2 errores críticos"
```

---

## 🚀 Próximo: Mejoras de UX

- [ ] Animaciones suaves en transiciones
- [ ] Indicador de progreso (0-100%)
- [ ] Histórico de cambios con undo/redo
- [ ] Búsqueda y filtros en tabla
- [ ] Exportar tabla a Excel
- [ ] Vista previa de fichas
- [ ] Tema oscuro (Dark Mode)
- [ ] Notificaciones de escritorio

