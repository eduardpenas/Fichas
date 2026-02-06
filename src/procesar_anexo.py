import pandas as pd
import os
import re
import json
import warnings

warnings.filterwarnings("ignore")

def separar_nombre_completo(nombre_completo):
    """Separa nombre y apellidos según la lógica requerida."""
    partes = str(nombre_completo).strip().split()
    if len(partes) == 3:
        return pd.Series({"Apellidos": " ".join(partes[1:]), "Nombre": partes[0]})
    elif len(partes) >= 4:
        return pd.Series({"Apellidos": " ".join(partes[2:]), "Nombre": " ".join(partes[:2])})
    else:
        return pd.Series({"Apellidos": "", "Nombre": str(nombre_completo)})

def buscar_archivo_anexo(input_dir):
    """Busca cualquier excel que contenga 'Anexo' en el nombre."""
    for file in os.listdir(input_dir):
        if "anexo" in file.lower() and file.endswith(".xlsx") and not file.startswith("~$"):
            return os.path.join(input_dir, file)
    return None

def extraer_anio_fiscal_clean(archivo_anexo):
    """
    Extrae el año fiscal de forma clean desde la pestaña 'Datos Solicitud'.
    
    Busca la fila que contiene 'EJERCICIO FISCAL DE LA SOLICITUD' y extrae
    la fecha que le sigue (en cualquier formato: dd/mm/aaaa, aaaa-mm-dd, etc.)
    sacando de esa fecha el año.
    
    Args:
        archivo_anexo: Path al archivo Excel
    
    Returns:
        anio_fiscal (int): Año fiscal extraído, o 2024 como fallback
    """
    try:
        df = pd.read_excel(archivo_anexo, sheet_name="Datos solicitud", header=None)
        
        # Buscar la fila que contiene "EJERCICIO FISCAL"
        for i, row in df.iterrows():
            # Convertir fila a strings y buscar patrón
            row_str = [str(cell).upper() if pd.notna(cell) else "" for cell in row]
            
            # Buscar la celda que contiene "EJERCICIO FISCAL"
            for j, cell in enumerate(row_str):
                if "EJERCICIO FISCAL" in cell and "SOLICITUD" in cell:
                    # Encontramos la celda, ahora buscamos la fecha en las siguientes celdas
                    # La fecha suele estar 2-5 columnas a la derecha
                    for offset in range(2, 8):  # Expandido a 8 para más flexibilidad
                        if j + offset < len(row):
                            valor = str(row.iloc[j + offset]).strip()
                            
                            # Buscar formatos: dd/mm/aaaa o aaaa-mm-dd o aaaa-mm-dd hh:mm:ss
                            # Formato 1: dd/mm/aaaa
                            match_fecha = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', valor)
                            if match_fecha:
                                anio = int(match_fecha.group(3))  # El año es el tercer grupo
                                return anio
                            
                            # Formato 2: aaaa-mm-dd (con o sin hora)
                            match_fecha_iso = re.search(r'(20\d{2})[/-](\d{1,2})[/-](\d{1,2})', valor)
                            if match_fecha_iso:
                                anio = int(match_fecha_iso.group(1))  # El año es el primer grupo
                                return anio
        
        # Si no se encuentra, usar 2024 como default
        return 2024
    
    except Exception as e:
        # En caso de error, usar 2024 como default silenciosamente
        return 2024

def procesar_anexo(archivo_especifico=None, cliente_nif=None, proyecto_acronimo=None):
    """
    Procesa el archivo anexo especificado, o busca uno disponible.
    
    Args:
        archivo_especifico: Nombre del archivo a procesar (ej: 'Anexo_Subido.xlsx').
                           Si es None, busca el primer archivo que contenga 'anexo' en el nombre.
        cliente_nif: NIF del cliente. Si se proporciona con proyecto_acronimo, los JSONs se guardan en la carpeta del proyecto.
                    Si es None, se guardan en INPUT_DIR.
        proyecto_acronimo: Acrónimo del proyecto. Requerido si se proporciona cliente_nif.
    """
    print("--- 🔄 PROCESANDO ANEXO II (VERSIÓN FINAL) ---")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    
    # Determinar dónde guardar los archivos de salida
    if cliente_nif and proyecto_acronimo:
        # Guardar en carpeta del proyecto
        PROYECTOS_DIR = os.path.join(BASE_DIR, 'proyectos')
        client_dir = os.path.join(PROYECTOS_DIR, f'Cliente_{cliente_nif}')
        project_dir = os.path.join(client_dir, proyecto_acronimo.upper())
        output_dir = os.path.join(project_dir, 'data')
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Modo PROYECTO: Guardando en {output_dir}")
        print(f"   ✓ Directorio creado/verificado: {os.path.exists(output_dir)}")
    elif cliente_nif:
        # Guardar en carpeta del cliente (compatibilidad hacia atrás)
        PROYECTOS_DIR = os.path.join(BASE_DIR, 'proyectos')
        client_dir = os.path.join(PROYECTOS_DIR, f'Cliente_{cliente_nif}')
        output_dir = os.path.join(client_dir, 'data')
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Modo CLIENTE: Guardando en {output_dir}")
        print(f"   ✓ Directorio creado/verificado: {os.path.exists(output_dir)}")
    else:
        # Guardar en INPUT_DIR (compatibilidad con comportamiento anterior)
        output_dir = INPUT_DIR
        print(f"📁 Modo INPUT_DIR: Guardando en {output_dir}")
    
    # Si se especifica un archivo, úsalo directamente
    if archivo_especifico:
        archivo_anexo = os.path.join(INPUT_DIR, archivo_especifico)
        print(f"📌 Procesando archivo específico: {archivo_especifico}")
        if not os.path.exists(archivo_anexo):
            print(f"❌ ERROR: Archivo no encontrado: {archivo_anexo}")
            return
    else:
        # Si no, busca cualquier archivo que contenga 'anexo'
        archivo_anexo = buscar_archivo_anexo(INPUT_DIR)
        if not archivo_anexo:
            print(f"❌ ERROR: No se encontró ningún archivo 'Anexo...xlsx' en {INPUT_DIR}")
            return
    
    print(f"📖 Leyendo: {os.path.basename(archivo_anexo)}")
    print(f"📁 Ruta completa: {archivo_anexo}")

    # 1. DETECTAR DATOS GENERALES (AÑO, NIF, RAZÓN SOCIAL)
    # Extraer año fiscal de forma clean desde Datos Solicitud
    anio_fiscal = extraer_anio_fiscal_clean(archivo_anexo)
    nif_solicitante = ""
    entidad_solicitante = ""  # Sin valor por defecto, se dejará vacío si no se encuentra
    
    try:
        df_datos = pd.read_excel(archivo_anexo, sheet_name="Datos solicitud", header=None)
        
        print(f"   📖 Leyendo hoja 'Datos solicitud' ({len(df_datos)} filas)")
        
        # Convertir a string y buscar patrones
        for i, row in df_datos.iterrows():
            # Convertir cada celda a string de forma segura, manejando NaN
            row_str = [str(cell).upper() if pd.notna(cell) else "" for cell in row]
            row_original = [str(cell) if pd.notna(cell) else "" for cell in row]
            
            # Buscar NIF Solicitante
            for idx, cell in enumerate(row_str):
                if "NIF" in cell and ("ENTIDAD" in cell or "SOLICITANTE" in cell):
                    # Buscar el valor en las siguientes columnas
                    for offset in range(1, 5):
                        if idx + offset < len(row):
                            val = str(row_original[idx + offset]).strip()
                            if val and val.upper() != "NAN" and len(val) > 4:
                                nif_solicitante = val
                                print(f"      ✅ NIF encontrado: {nif_solicitante}")
                                break
                
                # Buscar Razón Social / Entidad Solicitante (mejorado)
                # Patrones: RAZÓN SOCIAL, RAZON SOCIAL, DENOMINACIÓN, DENOMINACION, ENTIDAD SOLICITANTE
                cell_clean = cell.replace("\n", " ").strip()
                
                is_razon_social = "RAZÓN SOCIAL" in cell_clean or "RAZON SOCIAL" in cell_clean
                is_denominacion = "DENOMINACIÓN" in cell_clean or "DENOMINACION" in cell_clean
                is_entidad = ("ENTIDAD" in cell_clean and "SOLICITANTE" in cell_clean and "NIF" not in cell_clean)
                
                if is_razon_social or is_denominacion or is_entidad:
                    # Buscar el valor en las siguientes columnas
                    for offset in range(1, 6):  # Aumentar rango a 6 para mayor cobertura
                        if idx + offset < len(row):
                            val = str(row_original[idx + offset]).strip()
                            # Mejorar validación de valor
                            if (val and 
                                val.upper() != "NAN" and 
                                val != "None" and 
                                len(val) > 2 and
                                val not in ["", " ", "N/A", "NA"]):
                                entidad_solicitante = val
                                print(f"      ✅ Entidad solicitante encontrada: {entidad_solicitante}")
                                break

        print(f"   📅 Año fiscal: {anio_fiscal}")
        print(f"   🏢 Entidad Solicitante: {entidad_solicitante if entidad_solicitante else '(no encontrada)'}")
        print(f"   🆔 NIF Solicitante: {nif_solicitante if nif_solicitante else '(no encontrado)'}")
        
    except Exception as e:
        print(f"   ⚠️ Error leyendo Datos solicitud: {e}")
        import traceback
        print(f"   {traceback.format_exc()}")

    # ==========================================
    # 2. PROCESAR PERSONAL (Ficha 2.1) - VERSIÓN ROBUSTA
    # ==========================================
    try:
        print("👤 Procesando Personal...")
        df_p = pd.read_excel(archivo_anexo, sheet_name="Personal", header=[12, 13])
        
        print(f"   Dimensiones originales: {df_p.shape[0]} filas x {df_p.shape[1]} columnas")
        print(f"   Año fiscal objetivo: {anio_fiscal}")
        
        # --- PASO 1: ENCONTRAR COLUMNAS ---
        col_nombre = None
        col_titulacion = None
        col_horas_it = None
        col_coste_it = None
        
        print(f"   Buscando columnas de interés...")
        
        for col in df_p.columns:
            try:
                # Extraer nivel 0 (año o nombre de campo) y nivel 1 (concepto)
                nivel_0 = str(col[0]).strip() if pd.notna(col[0]) else ""
                nivel_1 = str(col[1]).strip() if pd.notna(col[1]) else ""
                
                # Convertir a minúsculas para búsqueda insensible a mayúsculas
                nivel_0_lower = nivel_0.lower()
                nivel_1_lower = nivel_1.lower()
                
                # Buscar columna de Nombre (sin importar el nivel)
                if "nombre" in nivel_0_lower or "nombre" in nivel_1_lower:
                    col_nombre = col
                    print(f"      OK - Nombre encontrado: {col}")
                
                # Buscar columna de Titulación
                if "titulación" in nivel_0_lower or "titulacion" in nivel_0_lower:
                    col_titulacion = col
                    print(f"      OK - Titulación encontrada: {col}")
                
                # Buscar columnas del AÑO FISCAL ESPECÍFICO
                try:
                    anio_num = int(float(nivel_0))
                    if anio_num == anio_fiscal:
                        # Buscar Horas IT para este año
                        if "horas" in nivel_1_lower and "it" in nivel_1_lower:
                            col_horas_it = col
                            print(f"      OK - Horas IT ({anio_fiscal}) encontradas: {col}")
                        
                        # Buscar Coste IT para este año
                        if ("coste" in nivel_1_lower or "gasto" in nivel_1_lower) and "it" in nivel_1_lower:
                            col_coste_it = col
                            print(f"      OK - Coste IT ({anio_fiscal}) encontrado: {col}")
                except (ValueError, TypeError):
                    pass
            
            except Exception as e:
                print(f"      WARN - Error procesando columna {col}: {e}")
                continue
        
        # --- PASO 2: VALIDAR QUE TENEMOS LAS COLUMNAS NECESARIAS ---
        if not col_nombre:
            print(f"   WARN - No se encontró columna 'Nombre'")
        if not col_horas_it or not col_coste_it:
            print(f"   WARN - No se encontraron Horas/Coste IT para año {anio_fiscal}")
            print(f"      Anos disponibles: {[str(c[0]) for c in df_p.columns if str(c[0]).isdigit()]}")
        
        # --- PASO 3: EXTRAER Y PROCESAR DATOS ---
        if col_nombre and col_horas_it and col_coste_it:
            print(f"   Extrayendo datos...")
            
            # Crear DataFrame con columnas necesarias
            df_res = pd.DataFrame({
                "nombre_completo": df_p[col_nombre],
                "titulacion": df_p[col_titulacion] if col_titulacion else "",
                "horas_it": pd.to_numeric(df_p[col_horas_it], errors='coerce').fillna(0),
                "coste_it": pd.to_numeric(df_p[col_coste_it], errors='coerce').fillna(0)
            })
            
            print(f"   Registros antes de filtrar: {len(df_res)}")
            
            # Filtrar registros válidos
            # - Nombre no vacío
            # - Al menos horas o coste > 0
            df_res = df_res[df_res["nombre_completo"].notna()]
            df_res = df_res[df_res["nombre_completo"].astype(str).str.strip() != ""]
            df_res = df_res[(df_res["horas_it"] > 0) | (df_res["coste_it"] > 0)]
            
            print(f"   Registros después de filtrar: {len(df_res)}")
            
            if len(df_res) > 0:
                # Calcular coste horario (evitar división por cero)
                df_res["coste_horario"] = (df_res["coste_it"] / df_res["horas_it"]).replace([float('inf'), -float('inf')], 0).fillna(0).round(2)
                
                # Separar nombre y apellidos de forma simple
                nombres = []
                apellidos = []
                for nombre_completo in df_res["nombre_completo"]:
                    resultado = separar_nombre_completo(nombre_completo)
                    nombres.append(resultado.get("Nombre", ""))
                    apellidos.append(resultado.get("Apellidos", ""))
                
                # Crear DataFrame final con estructura esperada
                df_final_p = pd.DataFrame()
                df_final_p["Nombre"] = nombres
                df_final_p["Apellidos"] = apellidos
                df_final_p["Titulación 1"] = [str(t).replace("nan", "") if pd.notna(t) else "" for t in df_res["titulacion"]]
                df_final_p["Titulación 2"] = ""
                df_final_p["Coste horario (€/hora)"] = df_res["coste_horario"].values
                df_final_p["Horas totales"] = df_res["horas_it"].values
                df_final_p["Coste total (€)"] = df_res["coste_it"].values
                df_final_p["Coste IT (€)"] = df_res["coste_it"].values
                df_final_p["Horas IT"] = df_res["horas_it"].values
                
                # Agregar columnas opcionales vacías
                for col in ["Departamento", "Puesto actual", "Coste I+D (€)", "Horas I+D",
                            "EMPRESA 1", "PERIODO 1", "PUESTO 1",
                            "EMPRESA 2", "PERIODO 2", "PUESTO 2",
                            "EMPRESA 3", "PERIODO 3", "PUESTO 3"]:
                    df_final_p[col] = ""
                
                # Guardar JSON
                json_path_p = os.path.join(output_dir, "Excel_Personal_2.1.json")
                df_final_p.to_json(json_path_p, orient='records', force_ascii=False, date_format='iso')
                print(f"   OK - Personal generado: {len(df_final_p)} personas")
                print(f"   Archivo: {os.path.basename(json_path_p)}")
                print(f"   ✓ Ruta completa: {json_path_p}")
                print(f"   ✓ Existe: {os.path.exists(json_path_p)}")
                print(f"   ✓ Tamaño: {os.path.getsize(json_path_p)} bytes")
            else:
                print(f"   WARN - No hay registros validos con datos en el anio {anio_fiscal}")
                # Crear archivo vacío
                df_final_p = pd.DataFrame(columns=[
                    "Nombre", "Apellidos", "Titulación 1", "Titulación 2",
                    "Coste horario (€/hora)", "Horas totales", "Coste total (€)",
                    "Coste IT (€)", "Horas IT", "Departamento", "Puesto actual",
                    "Coste I+D (€)", "Horas I+D",
                    "EMPRESA 1", "PERIODO 1", "PUESTO 1",
                    "EMPRESA 2", "PERIODO 2", "PUESTO 2",
                    "EMPRESA 3", "PERIODO 3", "PUESTO 3"
                ])
                json_path_p = os.path.join(output_dir, "Excel_Personal_2.1.json")
                df_final_p.to_json(json_path_p, orient='records', force_ascii=False, date_format='iso')
                print(f"   Archivo vacio creado: {os.path.basename(json_path_p)}")
        else:
            print(f"   WARN - No se encontraron las columnas necesarias para procesar Personal")
            # Crear archivo vacío con estructura
            df_final_p = pd.DataFrame(columns=[
                "Nombre", "Apellidos", "Titulación 1", "Titulación 2",
                "Coste horario (€/hora)", "Horas totales", "Coste total (€)",
                "Coste IT (€)", "Horas IT", "Departamento", "Puesto actual",
                "Coste I+D (€)", "Horas I+D",
                "EMPRESA 1", "PERIODO 1", "PUESTO 1",
                "EMPRESA 2", "PERIODO 2", "PUESTO 2",
                "EMPRESA 3", "PERIODO 3", "PUESTO 3"
            ])
            json_path_p = os.path.join(output_dir, "Excel_Personal_2.1.json")
            df_final_p.to_json(json_path_p, orient='records', force_ascii=False, date_format='iso')
            print(f"   Archivo vacio creado: {os.path.basename(json_path_p)}")

    except Exception as e:
        print(f"   ERROR - Procesando Personal: {e}")
        import traceback
        print(f"   {traceback.format_exc()}")
        # Crear archivo vacío para evitar fallos posteriores
        try:
            df_final_p = pd.DataFrame(columns=[
                "Nombre", "Apellidos", "Titulación 1", "Titulación 2",
                "Coste horario (€/hora)", "Horas totales", "Coste total (€)",
                "Coste IT (€)", "Horas IT", "Departamento", "Puesto actual",
                "Coste I+D (€)", "Horas I+D",
                "EMPRESA 1", "PERIODO 1", "PUESTO 1",
                "EMPRESA 2", "PERIODO 2", "PUESTO 2",
                "EMPRESA 3", "PERIODO 3", "PUESTO 3"
            ])
            json_path_p = os.path.join(output_dir, "Excel_Personal_2.1.json")
            df_final_p.to_json(json_path_p, orient='records', force_ascii=False, date_format='iso')
        except:
            pass

    # ==========================================
    # 3. PROCESAR COLABORACIONES Y FACTURAS (Ficha 2.2)
    # ==========================================
    try:
        facturas_list = []
        colaboraciones_list = []
        
        # Leer todas las hojas disponibles
        try:
            excel_file = pd.ExcelFile(archivo_anexo)
            todas_las_hojas = excel_file.sheet_names
        except:
            todas_las_hojas = []
        
        # Buscar dinámicamente hojas que contengan "Externa" o "Colabora" en el nombre
        hojas_externas = [h for h in todas_las_hojas if "externa" in h.lower() or "colabora" in h.lower()]
        
        # Si no encuentra hojas, intentar con nombres conocidos
        if not hojas_externas:
            hojas_externas = [h for h in todas_las_hojas if "C." in h]  # Hojas que empiezan con "C."
        
        # Si aún no, intentar con nombres exactos antiguos (pero solo si existen)
        if not hojas_externas:
            nombres_conocidos = ["C.Externas (OPIS)", "C.Externas (Otros)"]
            hojas_externas = [h for h in nombres_conocidos if h in todas_las_hojas]
        
        # Si tampoco hay, es normal - generar JSONs vacíos
        if not hojas_externas:
            print(f"   ℹ️  No se encontraron hojas de colaboraciones (normal si el archivo no tiene secciones de colaboradores externos)")
        
        for hoja in hojas_externas:
            try:
                # Saltar si la hoja no existe
                if hoja not in excel_file.sheet_names:
                    continue
                    
                df_raw = pd.read_excel(archivo_anexo, sheet_name=hoja, header=None)
                
                # Buscar fila de cabecera - FLEXIBLE con múltiples variantes
                fila_head = -1
                for i, row in df_raw.head(30).iterrows():  # Buscar hasta 30 filas
                    row_str = " ".join([str(v).lower() for v in row.values if pd.notna(v)])
                    # Palabras clave para detectar encabezado
                    tiene_razon = "razón" in row_str or "razon" in row_str
                    tiene_social = "social" in row_str
                    tiene_entidad = "entidad" in row_str or "colaborador" in row_str
                    tiene_nif = "nif" in row_str or "cif" in row_str
                    
                    # Detectar si es encabezado (contiene múltiples palabras clave)
                    if (tiene_razon and tiene_social) or \
                       (tiene_entidad and tiene_nif) or \
                       ("razón social de entidad" in row_str):
                        fila_head = i
                        break
                
                # Si no encontró encabezado en esta hoja, saltar
                if fila_head == -1:
                    continue

                fila_anios = df_raw.iloc[fila_head]
                fila_conceptos = df_raw.iloc[fila_head + 1]
                
                idx_entidad = -1
                idx_nif = -1
                idx_total_anio = -1
                
                # Buscar índices de columnas de forma flexible
                for idx, val in enumerate(fila_anios):
                    val_str = str(val).lower()
                    # Buscar columna de razón social / entidad
                    if ("razón" in val_str or "razon" in val_str or "social" in val_str or "entidad" in val_str or "colaborador" in val_str):
                        if idx_entidad == -1:  # Usar la primera que encuentre
                            idx_entidad = idx
                    # Buscar columna de NIF/CIF
                    if ("nif" in val_str or "cif" in val_str):
                        if idx_nif == -1:  # Usar la primera que encuentre
                            idx_nif = idx
                
                # Buscar columna de total del año fiscal (flexible)
                for idx, val in enumerate(fila_anios):
                    val_str = str(val)
                    # Primero intentar con el año exacto
                    if str(anio_fiscal) in val_str:
                        for offset in range(4):
                            if idx + offset < len(fila_conceptos):
                                sub_val = str(fila_conceptos[idx + offset]).upper()
                                if "TOTAL" in sub_val:
                                    idx_total_anio = idx + offset
                                    break
                        break
                
                # Si no encontramos el año exacto, buscar cualquier TOTAL que sea número
                if idx_total_anio == -1:
                    for idx, val in enumerate(fila_anios):
                        val_str = str(val).lower()
                        if any(str(y) in val_str for y in range(2000, 2100)):  # Cualquier año válido
                            for offset in range(4):
                                if idx + offset < len(fila_conceptos):
                                    sub_val = str(fila_conceptos[idx + offset]).upper()
                                    if "TOTAL" in sub_val:
                                        idx_total_anio = idx + offset
                                        break
                            if idx_total_anio != -1:
                                break

                if idx_entidad != -1 and idx_total_anio != -1:
                    for i in range(fila_head + 2, len(df_raw)):
                        row = df_raw.iloc[i]
                        entidad = str(row[idx_entidad])
                        
                        # --- FILTROS ---
                        if pd.isna(entidad) or entidad.strip() == "" or "nan" in entidad.lower(): 
                            continue
                        if "TOTAL" in entidad.upper() or "SUMA" in entidad.upper():
                            continue

                        try:
                            importe = float(row[idx_total_anio])
                        except:
                            importe = 0
                            
                        if importe > 0:
                            nif_proveedor = str(row[idx_nif]) if idx_nif != -1 and pd.notna(row[idx_nif]) else ""
                            
                            # 1. Crear Colaboración
                            colaboraciones_list.append({
                                "Razón social": entidad.strip(),
                                "NIF": nif_proveedor,
                                "NIF 2": nif_solicitante, # NIF del cliente
                                "Entidad contratante": entidad_solicitante, # Nombre del cliente
                                "País de la entidad": "España", # Valor por defecto
                                "Localidad": "",
                                "Provincia": "",
                                "País de realización": ""
                            })
                            
                            # 2. Crear Factura Única
                            facturas_list.append({
                                "Entidad": entidad.strip(),
                                "Nombre factura": f"Personal {anio_fiscal}",
                                "Importe (€)": importe
                            })
                    
                    # Si encontramos datos en esta hoja, salir del loop de hojas
                    if colaboraciones_list:
                        break
            
            except Exception as e:
                # Silenciar errores - es normal si no hay hojas de colaboraciones
                pass

        # Generar JSONs (vacíos o con datos)
        df_colab = pd.DataFrame(colaboraciones_list).drop_duplicates(subset="Razón social") if colaboraciones_list else pd.DataFrame()
        json_path_colab = os.path.join(output_dir, "Excel_Colaboraciones_2.2.json")
        df_colab.to_json(json_path_colab, orient='records', force_ascii=False, date_format='iso')
        
        if len(df_colab) > 0:
            print(f"   ✅ Colaboraciones generado: {len(df_colab)} entidades")
        
        df_fact = pd.DataFrame(facturas_list) if facturas_list else pd.DataFrame()
        json_path_fact = os.path.join(output_dir, "Excel_Facturas_2.2.json")
        df_fact.to_json(json_path_fact, orient='records', force_ascii=False, date_format='iso')
        
        if len(df_fact) > 0:
            print(f"   ✅ Facturas generado: {len(df_fact)} registros")

    except Exception as e:
        print(f"   ❌ Error General en Colaboraciones: {e}")
        import traceback
        print(traceback.format_exc())
    
    print("\n--- 📋 RESUMEN FINAL ---")
    print(f"📁 Directorio de salida: {output_dir}")
    output_files = ['Excel_Personal_2.1.json', 'Excel_Colaboraciones_2.2.json', 'Excel_Facturas_2.2.json']
    for out_file in output_files:
        out_path = os.path.join(output_dir, out_file)
        if os.path.exists(out_path):
            file_size = os.path.getsize(out_path)
            with open(out_path, encoding='utf-8') as f:
                num_records = len(f.read().strip().split('},'))
            print(f"   ✅ {out_file} - {num_records} registros ({file_size} bytes)")
        else:
            print(f"   ❌ {out_file} NO ENCONTRADO")
    
    # Guardar metadatos en JSON
    metadata = {
        "entidad_solicitante": entidad_solicitante,
        "nif_cliente": nif_solicitante,
        "anio_fiscal": anio_fiscal
    }
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"   📝 Metadatos guardados: {os.path.basename(metadata_path)}")
    
    print("--- FIN PROCESAMIENTO ---\n")
    
    # Retornar los metadatos para que el backend pueda enviarlos al frontend
    return metadata

if __name__ == "__main__":
    procesar_anexo()