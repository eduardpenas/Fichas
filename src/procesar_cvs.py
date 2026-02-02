import pandas as pd
import pdfplumber
import os
import re
import unicodedata

def normalizar_texto(texto):
    if not isinstance(texto, str): return ""
    return unicodedata.normalize('NFKD', texto.lower()).encode('ASCII', 'ignore').decode('utf-8').strip()

def traducir_periodo_a_espanol(texto):
    if not isinstance(texto, str): return texto
    
    # Eliminar " de " redundante
    texto = re.sub(r'\s+de\s+', ' ', texto, flags=re.IGNORECASE)

    mapa = {
        "january": "Enero", "jan": "Ene", "jan.": "Ene",
        "february": "Febrero", "feb": "Feb", "feb.": "Feb",
        "march": "Marzo", "mar": "Mar", "mar.": "Mar",
        "april": "Abril", "apr": "Abr", "apr.": "Abr",
        "may": "Mayo",
        "june": "Junio", "jun": "Jun", "jun.": "Jun",
        "july": "Julio", "jul": "Jul", "jul.": "Jul",
        "august": "Agosto", "aug": "Ago", "aug.": "Ago",
        "september": "Septiembre", "sep": "Sep", "sep.": "Sep", "sept": "Sep",
        "october": "Octubre", "oct": "Oct", "oct.": "Oct",
        "november": "Noviembre", "nov": "Nov", "nov.": "Nov",
        "december": "Diciembre", "dec": "Dic", "dec.": "Dic",
        "present": "Actualidad", "current": "Actualidad", "now": "Actualidad",
        "actualidad": "Actualidad"
    }

    def reemplazo(match):
        palabra = match.group(0)
        clave = palabra.lower().strip()
        if clave in mapa: return mapa[clave]
        return palabra

    texto_traducido = re.sub(r'[a-zA-Záéíóúñ\.]+', reemplazo, texto)
    return texto_traducido

def es_linea_duracion(texto):
    return bool(re.search(r'^\d+\s+(año|year|mes|mos|month)', texto, re.IGNORECASE))

def es_linea_fecha(texto):
    meses = r"(enero|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z\.]*"
    anio = r"\d{4}"
    conector = r"(-|–|to|a)"
    fin = r"(" + meses + r"|" + anio + r"|actualidad|present|presente)"
    patron = rf"{anio}.*?{conector}.*?{fin}"
    return bool(re.search(patron, texto, re.IGNORECASE)) and bool(re.search(r'\d{4}', texto))

def es_basura(texto):
    texto_lower = texto.lower()
    if len(texto) < 3: return True
    keywords = ["aptitudes", "skills", "languages", "idiomas", "certificaciones", "certifications", "educación", "education"]
    if texto_lower in keywords: return True
    if "native or bilingual" in texto_lower or "professional working" in texto_lower: return True
    return False

def es_ubicacion(texto):
    texto_lower = texto.lower()
    ciudades = ["barcelona", "madrid", "spain", "españa", "valencia", "sevilla", "bilbao", "alrededores", "area", "remote", "remoto"]
    for c in ciudades:
        if c in texto_lower: return True
    return False

def extraer_experiencia_pdf(ruta_pdf):
    experiencias = []
    
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            texto_completo = ""
            for page in pdf.pages:
                width = page.width
                height = page.height
                try:
                    left_crop = page.crop((width * 0.3, 0, width, height))
                    texto_pag = left_crop.extract_text()
                except:
                    texto_pag = page.extract_text()
                
                if texto_pag: texto_completo += texto_pag + "\n"
    except Exception as e:
        print(f"❌ Error PDF: {e}")
        return []

    match = re.search(r'\n(Experiencia|Experience)\n', texto_completo, re.IGNORECASE)
    if not match: match = re.search(r'(Experiencia|Experience)', texto_completo, re.IGNORECASE)
    if not match: return []
    
    texto = texto_completo[match.end():]
    match_fin = re.search(r'\n(Educación|Education|Licencias|Aptitudes)', texto, re.IGNORECASE)
    if match_fin: texto = texto[:match_fin.start()]

    lines = [l.strip() for l in texto.split('\n') if l.strip() and not es_basura(l.strip())]

    empresa_contexto = None 
    buffer_lineas = [] 

    for i, linea in enumerate(lines):
        
        if es_linea_duracion(linea):
            if buffer_lineas:
                empresa_contexto = buffer_lineas[-1] 
            continue 

        elif es_linea_fecha(linea):
            if not buffer_lineas: continue
            
            puesto = buffer_lineas[-1]
            periodo = linea
            
            match_fecha_clean = re.search(r'([A-Za-záéíóúñ]+\.?\s+(?:de\s+)?\d{4}.*)', periodo, re.IGNORECASE)
            if match_fecha_clean: periodo = match_fecha_clean.group(1)
            periodo = traducir_periodo_a_espanol(periodo)

            empresa_final = "Empresa desconocida"
            
            candidata = None
            if len(buffer_lineas) >= 2:
                posible = buffer_lineas[-2]
                if not es_ubicacion(posible) and len(posible) > 2:
                    candidata = posible
            
            if candidata:
                empresa_final = candidata
                empresa_contexto = candidata 
            elif empresa_contexto:
                empresa_final = empresa_contexto
            elif len(buffer_lineas) >= 2:
                 empresa_final = buffer_lineas[-2]

            if len(empresa_final) > 2 and len(puesto) > 2:
                experiencias.append({
                    "Empresa": empresa_final,
                    "Puesto": puesto,
                    "Periodo": periodo
                })

            if len(experiencias) >= 3: break
            
        else:
            buffer_lineas.append(linea)
            if len(buffer_lineas) > 5: buffer_lineas.pop(0)

    return experiencias

def procesar_cvs():
    print("\n--- 🕵️‍♂️ PROCESANDO CVs (CON ACTUALIZACIÓN DE PUESTO ACTUAL) ---")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    CVS_DIR = os.path.join(INPUT_DIR, 'cvs')
    EXCEL_PERSONAL_XLSX = os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx")
    EXCEL_PERSONAL_JSON = os.path.join(INPUT_DIR, "Excel_Personal_2.1.json")

    if not os.path.exists(CVS_DIR): return
    if not (os.path.exists(EXCEL_PERSONAL_XLSX) or os.path.exists(EXCEL_PERSONAL_JSON)): return

    # Leer JSON si existe, si no leer xlsx
    if os.path.exists(EXCEL_PERSONAL_JSON):
        df = pd.read_json(EXCEL_PERSONAL_JSON)
        salida_json = True
    else:
        df = pd.read_excel(EXCEL_PERSONAL_XLSX)
        salida_json = False
    
    # Aseguramos columnas necesarias, incluyendo 'Puesto actual'
    cols_check = [
        'EMPRESA 1', 'PERIODO 1', 'PUESTO 1', 
        'EMPRESA 2', 'PERIODO 2', 'PUESTO 2', 
        'EMPRESA 3', 'PERIODO 3', 'PUESTO 3',
        'Puesto actual' 
    ]
    for c in cols_check:
        if c not in df.columns: df[c] = ""
        df[c] = df[c].astype('object')

    archivos_cv = [f for f in os.listdir(CVS_DIR) if f.lower().endswith('.pdf')]
    encontrados = 0

    print(f"📖 Analizando {len(df)} perfiles...")
    
    for idx, row in df.iterrows():
        nombre_parts = normalizar_texto(f"{row['Nombre']} {row['Apellidos']}").split()
        pdf_match = None
        
        for pdf in archivos_cv:
            pdf_norm = normalizar_texto(pdf)
            coincidencias = sum(1 for p in nombre_parts if p in pdf_norm and len(p)>2)
            if coincidencias >= 2:
                pdf_match = pdf
                break
        
        if pdf_match:
            datos = extraer_experiencia_pdf(os.path.join(CVS_DIR, pdf_match))
            
            for n, exp in enumerate(datos):
                if n >= 3: break
                num = n + 1
                df.at[idx, f'EMPRESA {num}'] = str(exp['Empresa'])
                df.at[idx, f'PUESTO {num}'] = str(exp['Puesto'])
                df.at[idx, f'PERIODO {num}'] = str(exp['Periodo'])
                
                # --- NUEVA LÓGICA: Si es la Experiencia 1, actualizamos 'Puesto actual' ---
                if num == 1:
                    df.at[idx, 'Puesto actual'] = str(exp['Puesto'])
                # -------------------------------------------------------------------------
            
            if datos: encontrados += 1

    # Guardar en el mismo formato de entrada (JSON o XLSX)
    if salida_json:
        df.to_json(EXCEL_PERSONAL_JSON, orient='records', force_ascii=False, date_format='iso')
        print(f"\n💾 JSON actualizado: {encontrados} perfiles procesados.")
    else:
        df.to_excel(EXCEL_PERSONAL_XLSX, index=False)
        print(f"\n💾 Excel actualizado: {encontrados} perfiles procesados.")

if __name__ == "__main__":
    procesar_cvs()