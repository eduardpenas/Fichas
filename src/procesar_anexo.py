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
    elif cliente_nif:
        # Guardar en carpeta del cliente (compatibilidad hacia atrás)
        PROYECTOS_DIR = os.path.join(BASE_DIR, 'proyectos')
        client_dir = os.path.join(PROYECTOS_DIR, f'Cliente_{cliente_nif}')
        output_dir = os.path.join(client_dir, 'data')
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Modo CLIENTE: Guardando en {output_dir}")
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
    anio_fiscal = 2024
    nif_solicitante = ""
    entidad_solicitante = ""  # Sin valor por defecto, se dejará vacío si no se encuentra
    
    try:
        df_datos = pd.read_excel(archivo_anexo, sheet_name="Datos solicitud", header=None)
        
        print(f"   📖 Leyendo hoja 'Datos solicitud' ({len(df_datos)} filas)")
        
        # Convertir a string y buscar patrones
        for i, row in df_datos.iterrows():
            row_str = row.astype(str).str.upper().tolist()
            row_original = row.astype(str).tolist()
            
            # A) Buscar Año Fiscal
            for cell in row_str:
                if "FECHA FIN" in cell or "EJERCICIO FISCAL" in cell or "EJERCICIO" in cell:
                    match = re.search(r'(20\d{2})', str(row_str))
                    if match:
                        anio_fiscal = int(match.group(1))
                        print(f"      ✅ Año fiscal encontrado: {anio_fiscal}")
            
            # B) Buscar NIF Solicitante
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
                
                # C) Buscar Razón Social / Entidad Solicitante (mejorado)
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
    # 2. PROCESAR PERSONAL (Ficha 2.1)
    # ==========================================
    try:
        print("👤 Procesando Personal...")
        df_p = pd.read_excel(archivo_anexo, sheet_name="Personal", header=[12, 13])
        
        col_nombre = None
        col_horas = None
        col_coste = None
        col_titulacion = None

        for col in df_p.columns:
            if "nombre" in str(col[0]).lower(): col_nombre = col
            if "titulación" in str(col[0]).lower(): col_titulacion = col
            
            if str(col[0]) == str(anio_fiscal):
                sub_col = str(col[1]).lower()
                if "horas" in sub_col and "it" in sub_col:
                    col_horas = col
                elif ("coste" in sub_col or "gasto" in sub_col) and "it" in sub_col:
                    col_coste = col

        if col_nombre and col_horas and col_coste:
            df_res = pd.DataFrame({
                "nombres_completos": df_p[col_nombre],
                "titulacion": df_p[col_titulacion] if col_titulacion else "",
                "horas": df_p[col_horas].fillna(0),
                "coste": df_p[col_coste].fillna(0)
            })
            
            df_res = df_res[df_res["nombres_completos"].notna()]
            df_res = df_res[df_res["coste"] > 0]
            
            df_res["coste_horario"] = (df_res["coste"] / df_res["horas"]).replace([float('inf')], 0).fillna(0).round(2)
            split_names = df_res["nombres_completos"].apply(separar_nombre_completo)
            
            df_final_p = pd.DataFrame()
            df_final_p["Nombre"] = split_names["Nombre"]
            df_final_p["Apellidos"] = split_names["Apellidos"]
            df_final_p["Titulación 1"] = df_res["titulacion"]
            df_final_p["Titulación 2"] = ""
            df_final_p["Coste horario (€/hora)"] = df_res["coste_horario"]
            df_final_p["Horas totales"] = df_res["horas"]
            df_final_p["Coste total (€)"] = df_res["coste"]
            df_final_p["Coste IT (€)"] = df_res["coste"]
            df_final_p["Horas IT"] = df_res["horas"]
            
            for c in ["Departamento", "Puesto actual", "Coste I+D (€)", "Horas I+D", 
                      "EMPRESA 1", "PERIODO 1", "PUESTO 1", 
                      "EMPRESA 2", "PERIODO 2", "PUESTO 2", 
                      "EMPRESA 3", "PERIODO 3", "PUESTO 3"]:
                df_final_p[c] = ""

            json_path_p = os.path.join(output_dir, "Excel_Personal_2.1.json")
            df_final_p.to_json(json_path_p, orient='records', force_ascii=False, date_format='iso')
            print(f"   ✅ Personal generado: {len(df_final_p)} personas (JSON: {os.path.basename(json_path_p)})")
        else:
            print("   ⚠️ No se encontraron columnas de Personal para el año detectado.")

    except Exception as e:
        print(f"   ❌ Error en Personal: {e}")

    # ==========================================
    # 3. PROCESAR COLABORACIONES Y FACTURAS (Ficha 2.2)
    # ==========================================
    try:
        print("🏢 Procesando Colaboraciones Externas...")
        
        facturas_list = []
        colaboraciones_list = []
        
        hojas_externas = ["C.Externas (Otros)", "C.Externas (OPIS)"]
        
        for hoja in hojas_externas:
            try:
                df_raw = pd.read_excel(archivo_anexo, sheet_name=hoja, header=None)
                
                # Buscar fila de cabecera
                fila_head = -1
                for i, row in df_raw.head(20).iterrows():
                    if "Entidad" in row.values:
                        fila_head = i
                        break
                
                if fila_head == -1: continue

                fila_anios = df_raw.iloc[fila_head]
                fila_conceptos = df_raw.iloc[fila_head + 1]
                
                idx_entidad = -1
                idx_nif = -1
                idx_total_anio = -1
                
                for idx, val in enumerate(fila_anios):
                    val_str = str(val).lower()
                    if "entidad" in val_str: idx_entidad = idx
                    if "nif" in val_str: idx_nif = idx
                
                for idx, val in enumerate(fila_anios):
                    if str(anio_fiscal) in str(val):
                        for offset in range(4):
                            sub_val = str(fila_conceptos[idx + offset]).upper()
                            if "TOTAL" in sub_val:
                                idx_total_anio = idx + offset
                                break
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
            except Exception as e:
                print(f"   ⚠️ Error leyendo hoja {hoja}: {e}")

        if colaboraciones_list:
            df_colab = pd.DataFrame(colaboraciones_list).drop_duplicates(subset="Razón social")
            json_path_colab = os.path.join(output_dir, "Excel_Colaboraciones_2.2.json")
            df_colab.to_json(json_path_colab, orient='records', force_ascii=False, date_format='iso')
            print(f"   ✅ Colaboraciones generado: {len(df_colab)} entidades (JSON: {os.path.basename(json_path_colab)})")
            
            df_fact = pd.DataFrame(facturas_list)
            json_path_fact = os.path.join(output_dir, "Excel_Facturas_2.2.json")
            df_fact.to_json(json_path_fact, orient='records', force_ascii=False, date_format='iso')
            print(f"   ✅ Facturas generado: {len(df_fact)} registros (JSON: {os.path.basename(json_path_fact)})")
        else:
            print("   ⚠️ No se encontraron datos de colaboraciones con importe > 0")

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

if __name__ == "__main__":
    procesar_anexo()