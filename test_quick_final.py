#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test final rápido sin CVs"""

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
    print(f"[{status}] {name}")
    if details:
        print(f"     {details}")
    if condition:
        tests_passed += 1
    else:
        tests_failed += 1

print("\n" + "="*70)
print("TEST FINAL - SISTEMA FICHAS")
print("="*70 + "\n")

cliente = "A12345678"
proyecto = "PROJ01"

# Cleanup
client_dir = PROYECTOS_DIR / f"Cliente_{cliente}"
if client_dir.exists():
    shutil.rmtree(client_dir)

# 1. API
try:
    r = requests.get(f"{API_BASE}/", timeout=5)
    test("API Disponible", r.status_code == 200)
except:
    test("API Disponible", False)

# 2. Client + Proyecto
try:
    r = requests.post(f"{API_BASE}/clientes/{cliente}/proyectos", 
                     params={"proyecto_acronimo": proyecto}, timeout=10)
    test("Cliente + Proyecto", r.status_code == 200)
except:
    test("Cliente + Proyecto", False)

# 3. Upload Excel
try:
    with open(INPUTS_DIR / "Anexo_II_tipo_a_.xlsx", "rb") as f:
        r = requests.post(f"{API_BASE}/upload-anexo",
                         files={"file": f},
                         params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                         timeout=15)
    test("Upload + Procesar Excel", r.status_code == 200)
except:
    test("Upload + Procesar Excel", False)

# 4. Carpetas
project_dir = PROYECTOS_DIR / f"Cliente_{cliente}" / proyecto
data_dir = project_dir / "data"
test("Carpeta proyecto", project_dir.exists())
test("Carpeta data", data_dir.exists())

if data_dir.exists():
    json_count = len(list(data_dir.glob("*.json")))
    test("JSONs generados", json_count >= 3, f"Count: {json_count}")

# 5. Lectura
try:
    r = requests.get(f"{API_BASE}/personal",
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    data = r.json()
    count = len(data) if isinstance(data, list) else 0
    test("GET /personal", count > 0, f"Registros: {count}")
except:
    test("GET /personal", False)

try:
    r = requests.get(f"{API_BASE}/colaboraciones",
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    data = r.json()
    count = len(data) if isinstance(data, list) else 0
    test("GET /colaboraciones", count > 0, f"Registros: {count}")
except:
    test("GET /colaboraciones", False)

try:
    r = requests.get(f"{API_BASE}/facturas",
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    data = r.json()
    count = len(data) if isinstance(data, list) else 0
    test("GET /facturas", count > 0, f"Registros: {count}")
except:
    test("GET /facturas", False)

# 6. Validacion
try:
    r = requests.post(f"{API_BASE}/validate",
                     params={"cliente_nif": cliente, "proyecto_acronimo": proyecto})
    if r.status_code == 200:
        valido = r.json().get("exitosa", False)
        test("Validacion", valido)
    else:
        test("Validacion", False, f"Status: {r.status_code}")
except:
    test("Validacion", False)

# 7. Generar fichas
try:
    payload = {"cliente_nombre": "Test", "cliente_nif": cliente, "anio_fiscal": 2024}
    r = requests.post(f"{API_BASE}/generate-fichas",
                     json=payload,
                     params={"cliente_nif": cliente, "proyecto_acronimo": proyecto},
                     timeout=30)
    if r.status_code == 200:
        files = r.json().get("files", [])
        test("Generar fichas 2.1+2.2", len(files) >= 2, f"Generados: {len(files)}")
    else:
        test("Generar fichas", False, f"Status: {r.status_code}")
except:
    test("Generar fichas", False)

# Resumen
print("\n" + "="*70)
print(f"TOTAL: {tests_passed}/{tests_passed + tests_failed}")
print(f"Exitosos: {tests_passed} | Fallidos: {tests_failed}")
if tests_passed + tests_failed > 0:
    pct = (tests_passed / (tests_passed + tests_failed)) * 100
    print(f"Tasa: {pct:.1f}%")
print("="*70 + "\n")
