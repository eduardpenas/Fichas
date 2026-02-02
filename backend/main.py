import sys
import os
import shutil
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Ahora sí podemos importar tus scripts mágicos
from procesar_anexo import procesar_anexo
from procesar_cvs import procesar_cvs
from logica_fichas import generar_ficha_2_1, generar_ficha_2_2

# Inicializamos la APP (El restaurante)
app = FastAPI(title="Generador de Fichas API", version="1.0")

# --- SEGURIDAD (CORS) ---
# Esto permite que el Frontend (que vivirá en el puerto 5173) 
# pueda hablar con el Backend (que vivirá en el puerto 8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción esto se cambia, pero para desarrollo: ¡barra libre!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos rutas (Directorios)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'inputs')

# --- ENDPOINTS (LOS PLATOS DE LA CARTA) ---

@app.get("/")
def read_root():
    """Para probar si la API está viva."""
    return {"mensaje": "¡Hola! La API de Fichas está funcionando 🚀"}

@app.post("/upload-anexo")
async def upload_anexo(file: UploadFile = File(...)):
    """
    1. Recibe el archivo Anexo II.
    2. Lo guarda en la carpeta inputs.
    3. Ejecuta tu script 'procesar_anexo.py'.
    """
    try:
        # Guardar el archivo subido
        file_location = os.path.join(INPUT_DIR, "Anexo_Subido.xlsx")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Ejecutar tu lógica de extracción
        print("🍳 Cocinando: Procesando Anexo...")
        procesar_anexo() # Llamamos a tu función original
        
        return {"status": "success", "message": "Anexo procesado y Excels generados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-cvs")
async def upload_cvs(files: List[UploadFile] = File(...)):
    """
    Recibe múltiples PDFs de CVs y los guarda en inputs/cvs
    """
    cvs_dir = os.path.join(INPUT_DIR, 'cvs')
    if not os.path.exists(cvs_dir):
        os.makedirs(cvs_dir)
        
    saved_files = []
    for file in files:
        file_location = os.path.join(cvs_dir, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
    
    return {"status": "success", "files": saved_files}

@app.post("/process-cvs")
def trigger_process_cvs():
    """
    Dispara el script de lectura de CVs (el que acabamos de arreglar)
    """
    try:
        procesar_cvs()
        return {"status": "success", "message": "CVs leídos e integrados en el Excel"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personal")
def get_personal_data():
    """
    Lee el JSON 'Excel_Personal_2.1.json' o Excel y lo devuelve como JSON.
    Prioriza JSON si existe.
    """
    json_path = os.path.join(INPUT_DIR, "Excel_Personal_2.1.json")
    excel_path = os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx")
    
    if os.path.exists(json_path):
        df = pd.read_json(json_path)
    elif os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
    else:
        raise HTTPException(status_code=404, detail="No existe Excel ni JSON. Sube el Anexo primero.")
    
    # Rellenamos los NaN (vacíos) con cadenas vacías
    df = df.fillna("")
    
    # Convertimos a lista de diccionarios (JSON)
    datos = df.to_dict(orient="records")
    return datos

@app.post("/update-personal")
async def update_personal_data(data: List[Dict[str, Any]]):
    """
    Recibe los datos MODIFICADOS desde el Frontend y sobrescribe el archivo.
    Guarda en JSON si existe, en Excel si no.
    """
    try:
        df = pd.DataFrame(data)
        json_path = os.path.join(INPUT_DIR, "Excel_Personal_2.1.json")
        excel_path = os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx")
        
        if os.path.exists(json_path):
            df.to_json(json_path, orient='records', force_ascii=False, date_format='iso')
            formato = "JSON"
        else:
            df.to_excel(excel_path, index=False)
            formato = "Excel"
        
        return {"status": "success", "message": f"{formato} actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-fichas")
def generate_fichas():
    """
    Genera las fichas Word (2.1 y 2.2) usando las plantillas y JSONs.
    """
    try:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        # Rutas de JSONs
        json_personal = os.path.join(INPUT_DIR, "Excel_Personal_2.1.json")
        json_colaboraciones = os.path.join(INPUT_DIR, "Excel_Colaboraciones_2.2.json")
        json_facturas = os.path.join(INPUT_DIR, "Excel_Facturas_2.2.json")
        
        # Plantillas
        plantilla_2_1 = os.path.join(INPUT_DIR, "2.1.docx")
        plantilla_2_2 = os.path.join(INPUT_DIR, "2.2.docx")
        
        # Salidas
        salida_2_1 = os.path.join(output_dir, "Ficha_2_1.docx")
        salida_2_2 = os.path.join(output_dir, "Ficha_2_2.docx")
        
        generadas = []
        errores = []
        
        # Generar Ficha 2.1
        if os.path.exists(json_personal) and os.path.exists(plantilla_2_1):
            try:
                generar_ficha_2_1(json_personal, plantilla_2_1, salida_2_1, 2024, 'ACR')
                generadas.append("Ficha_2_1.docx")
            except Exception as e:
                errores.append(f"Error en Ficha 2.1: {str(e)}")
        
        # Generar Ficha 2.2
        if os.path.exists(json_colaboraciones) and os.path.exists(json_facturas) and os.path.exists(plantilla_2_2):
            try:
                generar_ficha_2_2(json_colaboraciones, json_facturas, plantilla_2_2, salida_2_2)
                generadas.append("Ficha_2_2.docx")
            except Exception as e:
                errores.append(f"Error en Ficha 2.2: {str(e)}")
        
        if errores:
            raise HTTPException(status_code=500, detail=" | ".join(errores))
        
        return {
            "status": "success",
            "message": f"Fichas generadas: {', '.join(generadas)}",
            "files": generadas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))