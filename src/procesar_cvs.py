import pandas as pd
import pdfplumber
import os
import re
import unicodedata
from difflib import SequenceMatcher

def normalizar_texto(texto):
    if not isinstance(texto, str): return ""
    return unicodedata.normalize('NFKD', texto.lower()).encode('ASCII', 'ignore').decode('utf-8').strip()

def similitud(a, b):
    """Calcula similitud entre dos strings (0-1)"""
    return SequenceMatcher(None, a, b).ratio()

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

def procesar_cvs(cliente_nif=None, proyecto_acronimo=None):
    print("\n--- 🕵️‍♂️ PROCESANDO CVs (CON ACTUALIZACIÓN DE PUESTO ACTUAL) ---")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    
    # Determinar de dónde leer los datos Y los CVs
    if cliente_nif and proyecto_acronimo:
        # Modo proyecto: leer desde carpeta del proyecto
        cliente_nif = cliente_nif.strip()
        proyecto_acronimo = proyecto_acronimo.strip().upper()
        PROYECTOS_DIR = os.path.join(BASE_DIR, 'proyectos')
        client_dir = os.path.join(PROYECTOS_DIR, f'Cliente_{cliente_nif}')
        project_dir = os.path.join(client_dir, proyecto_acronimo)
        data_dir = os.path.join(project_dir, 'data')
        cvs_dir = os.path.join(project_dir, 'cvs')  # CVs del proyecto
        EXCEL_PERSONAL_JSON = os.path.join(data_dir, "Excel_Personal_2.1.json")
        EXCEL_PERSONAL_XLSX = os.path.join(data_dir, "Excel_Personal_2.1.xlsx")
        print(f"🔍 Modo PROYECTO: {cliente_nif} / {proyecto_acronimo}")
        print(f"📁 Leyendo datos desde: {data_dir}")
        print(f"📁 Leyendo CVs desde: {cvs_dir}")
    elif cliente_nif:
        # Modo cliente: leer desde carpeta del cliente (compatibilidad hacia atrás)
        cliente_nif = cliente_nif.strip()
        PROYECTOS_DIR = os.path.join(BASE_DIR, 'proyectos')
        client_dir = os.path.join(PROYECTOS_DIR, f'Cliente_{cliente_nif}')
        data_dir = os.path.join(client_dir, 'data')
        cvs_dir = os.path.join(client_dir, 'cvs')  # CVs del cliente
        EXCEL_PERSONAL_JSON = os.path.join(data_dir, "Excel_Personal_2.1.json")
        EXCEL_PERSONAL_XLSX = os.path.join(data_dir, "Excel_Personal_2.1.xlsx")
        print(f"🔍 Modo CLIENTE: {cliente_nif}")
        print(f"📁 Leyendo datos desde: {data_dir}")
        print(f"📁 Leyendo CVs desde: {cvs_dir}")
    else:
        # Modo INPUT_DIR (compatibilidad con comportamiento anterior)
        cvs_dir = os.path.join(INPUT_DIR, 'cvs')
        EXCEL_PERSONAL_JSON = os.path.join(INPUT_DIR, "Excel_Personal_2.1.json")
        EXCEL_PERSONAL_XLSX = os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx")
        print(f"🔍 Modo INPUT_DIR (compatibilidad)")
        print(f"📁 Leyendo datos desde: {INPUT_DIR}")
        print(f"📁 Leyendo CVs desde: {cvs_dir}")

    print(f"📁 BASE_DIR: {BASE_DIR}")
    print(f"📁 CVS_DIR: {cvs_dir}")
    print(f"📁 EXCEL_PERSONAL_JSON: {EXCEL_PERSONAL_JSON}")
    print(f"📁 EXCEL_PERSONAL_XLSX: {EXCEL_PERSONAL_XLSX}")

    # Verificar si existen CVs
    if not os.path.exists(cvs_dir):
        print(f"❌ CVS_DIR NO EXISTE: {cvs_dir}")
        return
    
    archivos_cv_encontrados = os.listdir(cvs_dir) if os.path.exists(cvs_dir) else []
    print(f"📄 Archivos en CVS_DIR: {len(archivos_cv_encontrados)}")
    for f in archivos_cv_encontrados:
        print(f"   - {f}")
    
    if not archivos_cv_encontrados:
        print(f"⚠️  No hay archivos en {cvs_dir}")
        return

    # Verificar si existe Excel Personal
    if not (os.path.exists(EXCEL_PERSONAL_XLSX) or os.path.exists(EXCEL_PERSONAL_JSON)):
        print(f"❌ NO EXISTE Excel Personal en:")
        print(f"   - {EXCEL_PERSONAL_XLSX}")
        print(f"   - {EXCEL_PERSONAL_JSON}")
        return

    # Leer JSON si existe, si no leer xlsx
    if os.path.exists(EXCEL_PERSONAL_JSON):
        print(f"✅ Leyendo JSON: {EXCEL_PERSONAL_JSON}")
        df = pd.read_json(EXCEL_PERSONAL_JSON)
        salida_json = True
    else:
        print(f"✅ Leyendo XLSX: {EXCEL_PERSONAL_XLSX}")
        df = pd.read_excel(EXCEL_PERSONAL_XLSX)
        salida_json = False
    
    print(f"📊 DataFrame cargado: {len(df)} filas")
    print(f"📋 Columnas disponibles: {list(df.columns)}")
    
    # Aseguramos columnas necesarias, incluyendo 'Puesto actual'
    cols_check = [
        'EMPRESA 1', 'PERIODO 1', 'PUESTO 1', 
        'EMPRESA 2', 'PERIODO 2', 'PUESTO 2', 
        'EMPRESA 3', 'PERIODO 3', 'PUESTO 3',
        'Puesto actual' 
    ]
    for c in cols_check:
        if c not in df.columns: 
            print(f"   ➕ Agregando columna: {c}")
            df[c] = ""
        df[c] = df[c].astype('object')

    archivos_cv = [f for f in archivos_cv_encontrados if f.lower().endswith('.pdf')]
    encontrados = 0

    print(f"👤 Analizando {len(df)} perfiles...")
    print(f"\n{'NOMBRE EXCEL':<40} | {'CV ENCONTRADO':<40} | {'COINCIDENCIAS':<15}")
    print(f"{'-'*40}-+-{'-'*40}-+-{'-'*15}")
    
    for idx, row in df.iterrows():
        nombre_completo = f"{row.get('Nombre', '')} {row.get('Apellidos', '')}"
        nombre_norm = normalizar_texto(nombre_completo)
        nombre_parts = nombre_norm.split()
        pdf_match = None
        max_score = 0
        candidatos = []
        
        for pdf in archivos_cv:
            pdf_norm = normalizar_texto(pdf)
            pdf_parts = pdf_norm.split()
            
            # Estrategia 1: Coincidencias exactas de partes
            coincidencias = sum(1 for p in nombre_parts if p in pdf_norm and len(p)>2)
            
            # Estrategia 2: Similitud general (80%+)
            similitud_total = similitud(nombre_norm, pdf_norm)
            
            # Estrategia 3: Al menos un apellido coincide
            apellido1 = nombre_parts[-1] if len(nombre_parts) > 0 else ""
            apellido2 = nombre_parts[-2] if len(nombre_parts) > 1 else ""
            apellido_coincide = (apellido1 in pdf_norm and len(apellido1) > 2) or \
                                 (apellido2 in pdf_norm and len(apellido2) > 2)
            
            # Score final
            score = coincidencias
            if similitud_total >= 0.8:
                score += 10  # Bonus por similitud alta
            if apellido_coincide:
                score += 5   # Bonus por apellido coincidente
            
            # Registrar candidatos
            candidatos.append({
                'archivo': pdf,
                'coincidencias': coincidencias,
                'similitud': similitud_total,
                'score': score,
                'partes_pdf': pdf_parts
            })
            
            # Si el score es suficientemente alto, es match
            if score >= 2 and score > max_score:
                pdf_match = pdf
                max_score = score
        
        # Mostrar resultado
        resultado = f"{pdf_match if pdf_match else '❌ NO ENCONTRADO':<40}"
        score_str = f"{int(max_score)} ✅" if pdf_match else "0 ❌"
        print(f"{nombre_completo:<40} | {resultado} | {score_str:<15}")
        
        # Si no encontró, mostrar candidatos cercanos
        if not pdf_match:
            # Ordenar candidatos por score
            candidatos_ordenados = sorted(candidatos, key=lambda x: x['score'], reverse=True)
            if candidatos_ordenados and candidatos_ordenados[0]['score'] > 0:
                print(f"   💡 Candidatos cercanos (score):")
                for c in candidatos_ordenados[:3]:
                    if c['score'] > 0:
                        print(f"      - {c['archivo']}: {int(c['score'])} (coincidencias: {c['coincidencias']}, similitud: {c['similitud']:.0%})")
            continue
        
        if pdf_match:
            print(f"      📖 Extrayendo experiencia de: {pdf_match}")
            datos = extraer_experiencia_pdf(os.path.join(cvs_dir, pdf_match))
            print(f"      📊 Datos extraídos: {len(datos)} experiencias")
            
            for n, exp in enumerate(datos):
                if n >= 3: break
                num = n + 1
                df.at[idx, f'EMPRESA {num}'] = str(exp['Empresa'])
                df.at[idx, f'PUESTO {num}'] = str(exp['Puesto'])
                df.at[idx, f'PERIODO {num}'] = str(exp['Periodo'])
                print(f"         {num}. {exp['Empresa']} - {exp['Puesto']} ({exp['Periodo']})")
                
                # --- NUEVA LÓGICA: Si es la Experiencia 1, actualizamos 'Puesto actual' ---
                if num == 1:
                    df.at[idx, 'Puesto actual'] = str(exp['Puesto'])
                    print(f"            → Puesto actual: {exp['Puesto']}")
                # -------------------------------------------------------------------------
            
            if datos: 
                encontrados += 1

    # Guardar en el mismo formato de entrada (JSON o XLSX)
    if salida_json:
        print(f"💾 Guardando JSON: {EXCEL_PERSONAL_JSON}")
        df.to_json(EXCEL_PERSONAL_JSON, orient='records', force_ascii=False, date_format='iso')
        print(f"✅ JSON actualizado: {encontrados} perfiles procesados.")
    else:
        print(f"💾 Guardando XLSX: {EXCEL_PERSONAL_XLSX}")
        df.to_excel(EXCEL_PERSONAL_XLSX, index=False)
        print(f"✅ Excel actualizado: {encontrados} perfiles procesados.")
    
    print("--- FIN PROCESAMIENTO CVs ---\n")

if __name__ == "__main__":
    procesar_cvs()