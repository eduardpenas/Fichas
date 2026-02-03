#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

API_BASE = "http://localhost:8000"
cliente = "A12345678"
proyecto = "PROJ01"

print("\n[Generacion de fichas]...")
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
    print(f"Status: {r.status_code}")
    data = r.json()
    files = data.get("files", [])
    print(f"Archivos generados: {len(files)}")
    for f in files:
        print(f"  - {f}")
except Exception as e:
    print(f"ERROR: {e}")
