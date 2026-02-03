#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test rápido del sistema"""

import requests
import json
from pathlib import Path

API_BASE = "http://localhost:8000"
BASE_DIR = Path(__file__).parent
PROYECTOS_DIR = BASE_DIR / "proyectos"
INPUTS_DIR = BASE_DIR / "inputs"

cliente = "A12345678"
proyecto = "PROJ01"

print("="*70)
print("TEST RAPIDO - VERIFICACION DEL FIX")
print("="*70 + "\n")

# 1. Listar clientes
print("[1/7] Limpiando datos...")
import shutil
client_dir = PROYECTOS_DIR / f"Cliente_{cliente}"
if client_dir.exists():
    shutil.rmtree(client_dir)
    print("    OK - Datos limpios")

# 2. Crear cliente y proyecto
print("\n[2/7] Creando cliente y proyecto...")
r = requests.post(f"{API_BASE}/clientes/{cliente}/proyectos", 
                  params={"proyecto_acronimo": proyecto})
print(f"    Status: {r.status_code} - {'OK' if r.status_code == 200 else 'ERROR'}")

# 3. Upload del Excel (Anexo)
print("\n[3/7] Upload del Excel...")
excel_file = INPUTS_DIR / "Anexo_II_tipo_a_.xlsx"
try:
    with open(excel_file, "rb") as f:
        r = requests.post(f"{API_BASE}/upload-anexo",
                         files={"file": f},
                         params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    print(f"    Status: {r.status_code} - {'OK' if r.status_code == 200 else 'ERROR'}")
    if r.status_code != 200:
        print(f"    Respuesta: {r.text[:200]}")
except Exception as e:
    print(f"    ERROR: {e}")

# 4. Verificar carpeta de proyecto
print("\n[4/7] Verificando carpeta de proyecto...")
project_dir = PROYECTOS_DIR / f"Cliente_{cliente}" / proyecto
data_dir = project_dir / "data"
print(f"    Carpeta proyecto: {project_dir.exists()} ({project_dir})")
print(f"    Carpeta data: {data_dir.exists()} ({data_dir})")

if data_dir.exists():
    files = list(data_dir.glob("*.json"))
    print(f"    Archivos JSON: {len(files)}")
    for f in files:
        print(f"      - {f.name}")

# 5. GET /personal
print("\n[5/7] Lectura de datos (GET /personal)...")
try:
    r = requests.get(f"{API_BASE}/personal",
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    data = r.json()
    count = len(data) if isinstance(data, list) else 0
    print(f"    Status: {r.status_code}, Registros: {count}")
    if count == 0:
        print(f"    PROBLEMA: No se cargaron datos del JSON")
    else:
        print(f"    OK - Se cargaron {count} registros")
except Exception as e:
    print(f"    ERROR: {e}")

# 6. Validación
print("\n[6/7] Validacion...")
try:
    r = requests.post(f"{API_BASE}/validate",
                     params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    if r.status_code == 200:
        data = r.json()
        print(f"    Status: {r.status_code}")
        print(f"    Valido: {data.get('exitosa', False)}")
    else:
        print(f"    Status: {r.status_code} - ERROR")
except Exception as e:
    print(f"    ERROR: {e}")

# 7. Generación de fichas
print("\n[7/7] Generacion de fichas...")
try:
    payload = {
        "cliente_nombre": "Test Cliente",
        "cliente_nif": cliente,
        "anio_fiscal": 2024
    }
    r = requests.post(f"{API_BASE}/generate-fichas",
                     json=payload,
                     params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    if r.status_code == 200:
        data = r.json()
        files = data.get("files", [])
        print(f"    Status: {r.status_code}")
        print(f"    Archivos generados: {len(files)}")
        for f in files:
            print(f"      - {f}")
    else:
        print(f"    Status: {r.status_code} - ERROR")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n" + "="*70)
print("FIN DEL TEST RAPIDO")
print("="*70 + "\n")
