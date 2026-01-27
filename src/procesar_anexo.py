import pandas as pd
import os
import re
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

def procesar_anexo():
    print("--- 🔄 PROCESANDO ANEXO II (VERSIÓN FINAL) ---")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    
    archivo_anexo = buscar_archivo_anexo(INPUT_DIR)
    if not archivo_anexo:
        print(f"❌ ERROR: No se encontró ningún archivo 'Anexo...xlsx' en {INPUT_DIR}")
        return

    print(f"📖 Leyendo: {os.path.basename(archivo_anexo)}")

    # 1. DETECTAR DATOS GENERALES (AÑO, NIF, RAZÓN SOCIAL)
    anio_fiscal = 2024
    nif_solicitante = ""
    entidad_solicitante = "CLIENTE" # Valor por defecto si falla la lectura
    
    try:
        df_datos = pd.read_excel(archivo_anexo, sheet_name="Datos solicitud", header=None)
        
        # Búsqueda robusta en toda la hoja
        for i, row in df_datos.iterrows():
            row_str = row.astype(str).str.upper().tolist()
            
            # A) Buscar Año
            for cell in row_str:
                if "FECHA FIN" in cell or "EJERCICIO FISCAL" in cell:
                    match = re.search(r'(20\d{2})', str(row_str))
                    if match:
                        anio_fiscal = int(match.group(1))
            
            # B) Buscar NIF Solicitante y Razón Social
            for idx, cell in enumerate(row_str):
                # NIF
                if "NIF" in cell and ("ENTIDAD" in cell or "SOLICITANTE" in cell):
                    for offset in range(1, 5):
                        if idx + offset < len(row):
                            val = str(row[idx + offset]).strip()
                            if val and val.upper() != "NAN" and len(val) > 4:
                                nif_solicitante = val
                                break
                
                # Razón Social (Entidad Contratante)
                if "RAZÓN SOCIAL" in cell or "RAZON SOCIAL" in cell:
                    for offset in range(1, 5):
                        if idx + offset < len(row):
                            val = str(row[idx + offset]).strip()
                            if val and val.upper() != "NAN" and len(val) > 3:
                                entidad_solicitante = val
                                break

        print(f"   📅 Año fiscal: {anio_fiscal}")
        print(f"   🏢 Entidad Solicitante: {entidad_solicitante}")
        print(f"   🆔 NIF Solicitante: {nif_solicitante}")
        
    except Exception as e:
        print(f"   ⚠️ Error leyendo Datos solicitud: {e}")

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
                      "EMPRESA 1", "PERIODO 1", "PUESTO 1", "Actividad 1", "Actividad 2", "Actividad 3", "Actividad 4"]:
                df_final_p[c] = ""

            df_final_p.to_excel(os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx"), index=False)
            print(f"   ✅ Personal generado: {len(df_final_p)} personas")
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
            df_colab.to_excel(os.path.join(INPUT_DIR, "Excel_Colaboraciones_2.2.xlsx"), index=False)
            print(f"   ✅ Colaboraciones generado: {len(df_colab)} entidades")
            
            df_fact = pd.DataFrame(facturas_list)
            df_fact.to_excel(os.path.join(INPUT_DIR, "Excel_Facturas_2.2.xlsx"), index=False)
            print(f"   ✅ Facturas generado: {len(df_fact)} registros")
        else:
            print("   ⚠️ No se encontraron datos de colaboraciones con importe > 0")

    except Exception as e:
        print(f"   ❌ Error General en Colaboraciones: {e}")

if __name__ == "__main__":
    procesar_anexo()