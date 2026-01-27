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
# from main import ejecutar_generacion_word # Importaremos esto luego

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
    Lee el Excel 'Excel_Personal_2.1.xlsx' y lo devuelve como JSON
    para que la Tabla del Frontend lo pueda mostrar.
    """
    excel_path = os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx")
    if not os.path.exists(excel_path):
        raise HTTPException(status_code=404, detail="No existe el Excel. Sube el Anexo primero.")
    
    # Leemos el Excel, rellenamos los NaN (vacíos) con cadenas vacías ""
    df = pd.read_excel(excel_path).fillna("")
    
    # Convertimos a lista de diccionarios (JSON)
    datos = df.to_dict(orient="records")
    return datos

@app.post("/update-personal")
async def update_personal_data(data: List[Dict[str, Any]]):
    """
    Recibe los datos MODIFICADOS desde el Frontend y sobrescribe el Excel.
    ¡Esto es lo que permite editar como si fuera Google Sheets!
    """
    try:
        df = pd.DataFrame(data)
        excel_path = os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx")
        df.to_excel(excel_path, index=False)
        return {"status": "success", "message": "Excel actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))