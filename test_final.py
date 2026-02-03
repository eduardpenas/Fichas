#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test final completo con todos los flujos"""

import requests
import json
import shutil
from pathlib import Path

API_BASE = "http://localhost:8000"
BASE_DIR = Path(__file__).parent
PROYECTOS_DIR = BASE_DIR / "proyectos"
INPUTS_DIR = BASE_DIR / "inputs"

results = []
tests_passed = 0
tests_failed = 0

def test(name, condition, details=""):
    global tests_passed, tests_failed
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    if details:
        print(f"       {details}")
    if condition:
        tests_passed += 1
    else:
        tests_failed += 1
    results.append({"name": name, "passed": condition, "details": details})

print("\n" + "="*70)
print("TEST FINAL DEL SISTEMA - PROYECTO FICHAS")
print("="*70 + "\n")

# === GROUP 1: Setup ===
print("1. SETUP")
cliente = "A12345678"
proyecto = "PROJ01"

client_dir = PROYECTOS_DIR / f"Cliente_{cliente}"
if client_dir.exists():
    shutil.rmtree(client_dir)
print(f"  [INFO] Datos limpios")

# === GROUP 2: API & Clients ===
print("\n2. API & CLIENTS")
try:
    r = requests.get(f"{API_BASE}/", timeout=5)
    test("API Disponible", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("API Disponible", False, str(e))

try:
    r = requests.post(f"{API_BASE}/clientes/{cliente}/proyectos", 
                     params={"proyecto_acronimo": proyecto}, timeout=10)
    test("Crear Cliente + Proyecto", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("Crear Cliente + Proyecto", False, str(e))

# === GROUP 3: Upload Anexo ===
print("\n3. UPLOAD ANEXO")
excel_file = INPUTS_DIR / "Anexo_II_tipo_a_.xlsx"
try:
    with open(excel_file, "rb") as f:
        r = requests.post(f"{API_BASE}/upload-anexo",
                         files={"file": f},
                         params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                         timeout=15)
    test("Upload Excel + Procesar", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("Upload Excel + Procesar", False, str(e))

# === GROUP 4: Verify Folder Structure ===
print("\n4. ESTRUCTURA DE CARPETAS")
project_dir = PROYECTOS_DIR / f"Cliente_{cliente}" / proyecto
data_dir = project_dir / "data"

test("Carpeta Proyecto Creada", project_dir.exists(), f"{project_dir}")
test("Carpeta data Creada", data_dir.exists(), f"{data_dir}")

if data_dir.exists():
    json_files = list(data_dir.glob("*.json"))
    test("JSONs Generados", len(json_files) >= 3, f"Encontrados: {len(json_files)}")
    
    for json_name in ["Excel_Personal_2.1.json", "Excel_Colaboraciones_2.2.json", "Excel_Facturas_2.2.json"]:
        json_path = data_dir / json_name
        test(f"Archivo {json_name}", json_path.exists(), f"{json_path}")

# === GROUP 5: Data Reading ===
print("\n5. LECTURA DE DATOS")
try:
    r = requests.get(f"{API_BASE}/personal",
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                    timeout=10)
    data = r.json()
    count = len(data) if isinstance(data, list) else 0
    test("GET /personal", count > 0, f"Status: {r.status_code}, Registros: {count}")
except Exception as e:
    test("GET /personal", False, str(e))

try:
    r = requests.get(f"{API_BASE}/colaboraciones",
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                    timeout=10)
    data = r.json()
    count = len(data) if isinstance(data, list) else 0
    test("GET /colaboraciones", count > 0, f"Status: {r.status_code}, Registros: {count}")
except Exception as e:
    test("GET /colaboraciones", False, str(e))

try:
    r = requests.get(f"{API_BASE}/facturas",
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                    timeout=10)
    data = r.json()
    count = len(data) if isinstance(data, list) else 0
    test("GET /facturas", count > 0, f"Status: {r.status_code}, Registros: {count}")
except Exception as e:
    test("GET /facturas", False, str(e))

# === GROUP 6: CVs Upload ===
print("\n6. UPLOAD CVs")
cvs_dir = INPUTS_DIR / "cvs"
pdfs = list(cvs_dir.glob("*.pdf"))[:2]

if pdfs:
    try:
        files = [("files", open(pdf, "rb")) for pdf in pdfs]
        r = requests.post(f"{API_BASE}/upload-cvs",
                         files=files,
                         params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                         timeout=15)
        for _, f in files:
            f.close()
        uploaded = len(r.json().get("files", []))
        test(f"Upload {len(pdfs)} CVs", r.status_code == 200 and uploaded == len(pdfs), 
             f"Status: {r.status_code}, Cargados: {uploaded}")
    except Exception as e:
        test("Upload CVs", False, str(e))

# === GROUP 7: Process CVs ===
print("\n7. PROCESAR CVs")
try:
    r = requests.post(f"{API_BASE}/process-cvs",
                     params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                     timeout=15)
    test("Procesar CVs", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("Procesar CVs", False, str(e))

# === GROUP 8: Validation ===
print("\n8. VALIDACION")
try:
    r = requests.post(f"{API_BASE}/validate",
                     params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                     timeout=10)
    if r.status_code == 200:
        data = r.json()
        valido = data.get("exitosa", False)
        test("Validar Datos", valido, f"Valido: {valido}")
    else:
        test("Validar Datos", False, f"Status: {r.status_code}")
except Exception as e:
    test("Validar Datos", False, str(e))

# === GROUP 9: Generate Fichas ===
print("\n9. GENERACION DE FICHAS")
try:
    payload = {
        "cliente_nombre": "Test Cliente",
        "cliente_nif": cliente,
        "anio_fiscal": 2024
    }
    r = requests.post(f"{API_BASE}/generate-fichas",
                     json=payload,
                     params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                     timeout=30)
    if r.status_code == 200:
        data = r.json()
        files = data.get("files", [])
        test("Generar Fichas 2.1 + 2.2", len(files) >= 2, f"Generados: {files}")
    else:
        test("Generar Fichas", False, f"Status: {r.status_code}")
except Exception as e:
    test("Generar Fichas", False, str(e))

# === SUMMARY ===
print("\n" + "="*70)
print("RESUMEN")
print("="*70)
print(f"Total de Tests: {tests_passed + tests_failed}")
print(f"Exitosos: {tests_passed} [PASS]")
print(f"Fallidos: {tests_failed} [FAIL]")
if tests_passed + tests_failed > 0:
    percentage = (tests_passed / (tests_passed + tests_failed)) * 100
    print(f"Tasa de exito: {percentage:.1f}%")
print("\n")

if tests_failed > 0:
    print("Tests que fallaron:")
    for r in results:
        if not r["passed"]:
            print(f"  - {r['name']}")
            if r['details']:
                print(f"    {r['details']}")
    print()
