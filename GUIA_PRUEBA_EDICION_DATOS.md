# 🧪 Guía de Prueba - Edición de Datos Independiente

## Pruebas Recomendadas

### Test 1: Agregar datos sin Anexo

**Precondición:** Cliente A31768138, Proyecto PLANEROPTI (o cualquiera sin datos)

**Pasos:**
1. Abre http://localhost:5173
2. Selecciona Cliente: A31768138
3. Selecciona Proyecto: PLANEROPTI
4. Haz clic en "✏️ Personal (Ficha 2.1)"
5. Verás:
   ```
   No hay datos. Haz clic en "➕ Agregar fila" 
   para crear nuevos registros.
   
   [➕ Agregar fila]
   ```
6. Haz clic en "➕ Agregar fila"
7. Aparece una tabla con 1 fila vacía:
   ```
   # | Nombre | Apellidos | Titulación 1 | ... | ✕
   1 | [vacio]| [vacio]   | [vacio]      | ... | ✕
   ```
8. Haz clic en la celda "Nombre"
9. Escribe un nombre, por ejemplo: "JUAN"
10. Presiona Enter
11. La celda se actualiza y se cierra el editor
12. Continúa llenando otros campos
13. Si quieres agregar más filas, haz clic en "➕ Agregar fila"
14. Cuando termines, haz clic en "💾 Guardar Cambios"
15. Verás el mensaje: "✅ Datos de Personal guardados (X registros)"

**Resultado esperado:**
- ✅ Se pueden agregar datos manualmente
- ✅ Se pueden editar celdas
- ✅ Se guardan los cambios en el JSON
- ✅ No requiere Anexo

---

### Test 2: Editar datos existentes

**Precondición:** Cliente A31768138, Proyecto GRANDES (con datos de Anexo)

**Pasos:**
1. Selecciona Cliente: A31768138
2. Selecciona Proyecto: GRANDES
3. Haz clic en "✏️ Personal (Ficha 2.1)"
4. Verás la tabla con todos los datos del Anexo
5. Haz clic en una celda para editarla
6. Cambia el valor, por ejemplo: Nombre de "ANGEL" a "JUAN"
7. Presiona Enter
8. Haz clic en "➕ Agregar fila" para agregar una nueva persona
9. Haz clic en "✕" de una fila para eliminarla
10. Cuando termines, haz clic en "💾 Guardar Cambios"

**Resultado esperado:**
- ✅ Se cargan todos los datos
- ✅ Se pueden editar celdas
- ✅ Se pueden agregar filas
- ✅ Se pueden eliminar filas
- ✅ Se guardan todos los cambios

---

### Test 3: Completar datos parciales

**Precondición:** Cliente A31768138, Proyecto PLANEROPTI

**Pasos:**
1. Selecciona Cliente: A31768138
2. Selecciona Proyecto: PLANEROPTI
3. Haz clic en "✏️ Colaboraciones (Ficha 2.2)"
4. Verás tabla vacía (sin datos de Anexo)
5. Haz clic en "➕ Agregar fila"
6. Llena los datos de una colaboración:
   - Razón social: "ACCENTURE SERVICES"
   - NIF: "A12345678"
   - País de la entidad: "España"
   - etc.
7. Agrega más colaboraciones si quieres
8. Haz clic en "💾 Guardar Cambios"
9. Repite con "✏️ Facturas (Ficha 2.2)"
10. Agrega facturas manualmente
11. Guarda los cambios
12. Ahora haz clic en "Generar Fichas"
13. Debería generar ambas fichas (2.1 y 2.2)

**Resultado esperado:**
- ✅ Se pueden agregar datos de colaboraciones manualmente
- ✅ Se pueden agregar datos de facturas manualmente
- ✅ Al generar fichas después, se incluyen los datos editados
- ✅ Ficha 2.2 se genera correctamente con los datos agregados

---

### Test 4: Cancelar sin guardar

**Precondición:** Cualquier editor abierto con cambios

**Pasos:**
1. Abre un editor de datos
2. Haz cambios (agrega, edita, elimina filas)
3. Verás: "Hay cambios sin guardar"
4. Haz clic en "❌ Cancelar"
5. Se cierra el editor sin guardar

**Resultado esperado:**
- ✅ Los cambios se descartan
- ✅ El editor se cierra
- ✅ Los datos antiguos se conservan

---

### Test 5: Validar estructura de columnas

**Prueba manual:**
Abre la consola del navegador (F12) y verifica que `COLUMN_DEFINITIONS` tiene:
- `personal`: 23 columnas
- `colaboraciones`: 8 columnas
- `facturas`: 3 columnas

**En la consola:**
```javascript
// Ejecuta esto en DevTools:
console.log(Object.keys(COLUMN_DEFINITIONS));
// Debería mostrar: ["personal", "colaboraciones", "facturas"]
```

---

## Checklist de Validación

- [ ] Test 1: Agregar datos sin Anexo ✓
- [ ] Test 2: Editar datos existentes ✓
- [ ] Test 3: Completar datos parciales ✓
- [ ] Test 4: Cancelar sin guardar ✓
- [ ] Test 5: Validar estructura ✓

---

## Puntos Clave a Verificar

1. **Tabla vacía:**
   - ✅ Se muestra mensaje de "No hay datos"
   - ✅ Se muestra botón "➕ Agregar fila"
   - ✅ Al hacer clic, aparece 1 fila vacía

2. **Tabla con datos:**
   - ✅ Se cargan todos los datos correctamente
   - ✅ Las columnas coinciden con la estructura definida
   - ✅ Se puede editar cada celda
   - ✅ Se puede agregar filas nuevas
   - ✅ Se puede eliminar filas

3. **Guardado:**
   - ✅ Al hacer clic "Guardar", se envía al backend
   - ✅ Se muestra mensaje de éxito
   - ✅ Los datos se guardan en el JSON correspondiente

4. **Integración:**
   - ✅ Los datos agregados se pueden usar para generar fichas
   - ✅ Los datos se mantienen entre sesiones
   - ✅ Se pueden editar nuevamente después de guardar

---

## Mensajes de Error a Esperar

### Si no hay permisos de escritura:
```
❌ Error al guardar: Permission denied
```

### Si los datos son inválidos:
```
❌ Error al guardar: Invalid JSON
```

### Si la carpeta no existe:
```
✅ Datos de Personal guardados (1 registros)
(El sistema crea la carpeta automáticamente)
```

---

## URLs Clave

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Datos:** c:\Fichas\proyectos\Cliente_{nif}\{proyecto}\data\

---

## Información Útil

### Clientes y Proyectos de Prueba

```
Cliente: A31768138
├── Proyecto: GRANDES
│   └── Datos: Completos (Personal, Colaboraciones, Facturas)
│
└── Proyecto: PLANEROPTI
    └── Datos: Parciales (Solo Personal)
```

### Estructura JSON

**Excel_Personal_2.1.json:**
```json
[
  {
    "Nombre": "JUAN",
    "Apellidos": "PEREZ",
    "Titulación 1": "INGENIERO",
    "Coste horario (€/hora)": 50,
    ...
  }
]
```

**Excel_Colaboraciones_2.2.json:**
```json
[
  {
    "Razón social": "ACCENTURE",
    "NIF": "A12345678",
    ...
  }
]
```

**Excel_Facturas_2.2.json:**
```json
[
  {
    "Entidad": "ACCENTURE",
    "Nombre factura": "Personal 2024",
    "Importe (€)": 1000.50
  }
]
```

---

## Conclusión

El editor de datos ahora es **completamente independiente del Anexo**. El usuario puede:
1. Crear datos desde cero
2. Editar datos cargados del Anexo
3. Completar datos parciales
4. Eliminar datos innecesarios
5. Generar fichas con los datos editados

¡Toda la flexibilidad que el usuario necesita! 🎉
