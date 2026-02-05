#!/usr/bin/env python3
"""
Script de depuración para probar creación de múltiples clientes
"""
import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"
PROYECTOS_DIR = r"c:\Fichas\proyectos"

print("=" * 70)
print("🧪 TEST: CREAR MÚLTIPLES CLIENTES")
print("=" * 70)

# Test 1: Listar clientes actuales
print("\n1️⃣  LISTAR CLIENTES ACTUALES")
print("-" * 70)
try:
    resp = requests.get(f"{BASE_URL}/clientes")
    print(f"Status: {resp.status_code}")
    clientes = resp.json().get("clientes", [])
    print(f"Clientes actuales: {len(clientes)}")
    for c in clientes:
        print(f"   - {c['nif']}: {c['nombre']}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Crear primer cliente
print("\n2️⃣  CREAR PRIMER CLIENTE (TEST001)")
print("-" * 70)
try:
    resp = requests.post(
        f"{BASE_URL}/clientes",
        params={"nif": "TEST001", "nombre": "Test Cliente 001"}
    )
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    # Verificar carpeta
    client_dir = os.path.join(PROYECTOS_DIR, "Cliente_TEST001")
    exists = os.path.exists(client_dir)
    print(f"Carpeta creada: {exists} ({client_dir})")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Crear segundo cliente
print("\n3️⃣  CREAR SEGUNDO CLIENTE (TEST002)")
print("-" * 70)
try:
    resp = requests.post(
        f"{BASE_URL}/clientes",
        params={"nif": "TEST002", "nombre": "Test Cliente 002"}
    )
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    # Verificar carpeta
    client_dir = os.path.join(PROYECTOS_DIR, "Cliente_TEST002")
    exists = os.path.exists(client_dir)
    print(f"Carpeta creada: {exists} ({client_dir})")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Crear tercer cliente
print("\n4️⃣  CREAR TERCER CLIENTE (TEST003)")
print("-" * 70)
try:
    resp = requests.post(
        f"{BASE_URL}/clientes",
        params={"nif": "TEST003", "nombre": "Test Cliente 003"}
    )
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    # Verificar carpeta
    client_dir = os.path.join(PROYECTOS_DIR, "Cliente_TEST003")
    exists = os.path.exists(client_dir)
    print(f"Carpeta creada: {exists} ({client_dir})")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Listar todos los clientes
print("\n5️⃣  LISTAR TODOS LOS CLIENTES DESPUÉS DE CREAR")
print("-" * 70)
try:
    resp = requests.get(f"{BASE_URL}/clientes")
    print(f"Status: {resp.status_code}")
    clientes = resp.json().get("clientes", [])
    print(f"Total de clientes: {len(clientes)}")
    for c in clientes:
        nif = c['nif']
        nombre = c['nombre']
        client_dir = os.path.join(PROYECTOS_DIR, f"Cliente_{nif}")
        exists = "✅" if os.path.exists(client_dir) else "❌"
        print(f"   {exists} {nif}: {nombre}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 6: Verificar carpetas en disco
print("\n6️⃣  VERIFICAR CARPETAS EN DISCO")
print("-" * 70)
if os.path.exists(PROYECTOS_DIR):
    carpetas = os.listdir(PROYECTOS_DIR)
    print(f"Carpetas en {PROYECTOS_DIR}: {len(carpetas)}")
    for carpeta in sorted(carpetas):
        ruta = os.path.join(PROYECTOS_DIR, carpeta)
        if os.path.isdir(ruta) and carpeta.startswith("Cliente_"):
            nif = carpeta.replace("Cliente_", "")
            config_file = os.path.join(ruta, "config.json")
            has_config = "✅" if os.path.exists(config_file) else "❌"
            print(f"   {carpeta} {has_config}")
else:
    print(f"❌ No existe: {PROYECTOS_DIR}")

# Test 7: Intentar crear cliente duplicado
print("\n7️⃣  INTENTAR CREAR CLIENTE DUPLICADO (TEST001)")
print("-" * 70)
try:
    resp = requests.post(
        f"{BASE_URL}/clientes",
        params={"nif": "TEST001", "nombre": "Intento Duplicado"}
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"✅ Error esperado: {resp.json().get('detail', 'Sin detalle')}")
    else:
        print(f"❌ Se permitió crear duplicado: {resp.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO")
print("=" * 70)
