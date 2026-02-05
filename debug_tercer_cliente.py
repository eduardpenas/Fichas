#!/usr/bin/env python3
"""
Script para debuggear el problema de crear tercer cliente
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("🔍 DEBUG: ¿POR QUÉ NO SE CREA EL TERCERO?")
print("=" * 70)

# Listar clientes actuales
print("\n1. Clientes actuales:")
resp = requests.get(f"{BASE_URL}/clientes")
clientes = resp.json().get("clientes", [])
print(f"   Total: {len(clientes)}")
for c in clientes:
    print(f"   - {c['nif']}: {c['nombre']}")

# Intentar crear NUEVO001
print("\n2. Crear NUEVO001:")
resp = requests.post(
    f"{BASE_URL}/clientes",
    params={"nif": "NUEVO001", "nombre": "Nuevo Cliente 001"}
)
print(f"   Status: {resp.status_code}")
print(f"   Response: {json.dumps(resp.json(), indent=4)}")

# Intentar crear NUEVO002
print("\n3. Crear NUEVO002:")
resp = requests.post(
    f"{BASE_URL}/clientes",
    params={"nif": "NUEVO002", "nombre": "Nuevo Cliente 002"}
)
print(f"   Status: {resp.status_code}")
print(f"   Response: {json.dumps(resp.json(), indent=4)}")

# Intentar crear NUEVO003
print("\n4. Crear NUEVO003:")
resp = requests.post(
    f"{BASE_URL}/clientes",
    params={"nif": "NUEVO003", "nombre": "Nuevo Cliente 003"}
)
print(f"   Status: {resp.status_code}")
print(f"   Response: {json.dumps(resp.json(), indent=4)}")

# Listar todos después
print("\n5. Clientes DESPUÉS de crear:")
resp = requests.get(f"{BASE_URL}/clientes")
clientes = resp.json().get("clientes", [])
print(f"   Total: {len(clientes)}")
for c in clientes:
    print(f"   - {c['nif']}: {c['nombre']}")

print("\n" + "=" * 70)
