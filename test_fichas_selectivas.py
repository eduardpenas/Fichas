#!/usr/bin/env python
"""
Script de prueba para los nuevos endpoints de fichas selectivas
Prueba tanto /generate-fichas como /generate-ficha-2-1-only y /generate-ficha-2-2-only
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_generate_fichas_complete():
    """Test /generate-fichas para proyecto con datos completos (GRANDES)"""
    print("\n" + "="*70)
    print("TEST 1: /generate-fichas con datos completos (GRANDES)")
    print("="*70)
    
    payload = {
        "cliente_nombre": "Test Cliente",
        "cliente_nif": "A31768138",
        "anio_fiscal": 2024
    }
    
    params = {
        "cliente_nif": "A31768138",
        "proyecto_acronimo": "GRANDES"
    }
    
    response = requests.post(f"{BASE_URL}/generate-fichas", json=payload, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ VALIDACION:")
        print(f"  - puede_generar_2_1: {data.get('puede_generar_2_1', False)}")
        print(f"  - puede_generar_2_2: {data.get('puede_generar_2_2', False)}")
        print(f"  - avisos: {data.get('avisos', [])}")
        print(f"  - datos generados: {data.get('datos', {})}")
    
    return response.status_code == 200


def test_generate_fichas_partial():
    """Test /generate-fichas para proyecto con datos parciales (PLANEROPTI)"""
    print("\n" + "="*70)
    print("TEST 2: /generate-fichas con datos parciales (PLANEROPTI)")
    print("="*70)
    
    payload = {
        "cliente_nombre": "Test Cliente",
        "cliente_nif": "A31768138",
        "anio_fiscal": 2024
    }
    
    params = {
        "cliente_nif": "A31768138",
        "proyecto_acronimo": "PLANEROPTI"
    }
    
    response = requests.post(f"{BASE_URL}/generate-fichas", json=payload, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ VALIDACION:")
        print(f"  - puede_generar_2_1: {data.get('puede_generar_2_1', False)}")
        print(f"  - puede_generar_2_2: {data.get('puede_generar_2_2', False)}")
        print(f"  - avisos: {data.get('avisos', [])}")
        print(f"  - Esperado: puede_generar_2_1=true, puede_generar_2_2=false")
    
    return response.status_code == 200


def test_generate_ficha_2_1_only():
    """Test /generate-ficha-2-1-only"""
    print("\n" + "="*70)
    print("TEST 3: /generate-ficha-2-1-only")
    print("="*70)
    
    payload = {
        "cliente_nombre": "Test Cliente",
        "cliente_nif": "A31768138",
        "anio_fiscal": 2024
    }
    
    params = {
        "cliente_nif": "A31768138",
        "proyecto_acronimo": "PLANEROPTI"
    }
    
    response = requests.post(f"{BASE_URL}/generate-ficha-2-1-only", json=payload, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        print("\n✅ Ficha 2.1 generada correctamente")
    else:
        print("\n❌ Error al generar Ficha 2.1")
    
    return response.status_code == 200


def test_generate_ficha_2_2_only_partial():
    """Test /generate-ficha-2-2-only con datos parciales (debe fallar)"""
    print("\n" + "="*70)
    print("TEST 4: /generate-ficha-2-2-only con datos parciales (debe fallar)")
    print("="*70)
    
    payload = {
        "cliente_nombre": "Test Cliente",
        "cliente_nif": "A31768138",
        "anio_fiscal": 2024
    }
    
    params = {
        "cliente_nif": "A31768138",
        "proyecto_acronimo": "PLANEROPTI"
    }
    
    response = requests.post(f"{BASE_URL}/generate-ficha-2-2-only", json=payload, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 400:
        print("\n✅ Correctamente rechazado (sin datos de colaboraciones/facturas)")
    else:
        print("\n❌ Debería retornar 400 (sin datos)")
    
    return response.status_code == 400


def test_generate_ficha_2_2_only_complete():
    """Test /generate-ficha-2-2-only con datos completos (debe funcionar)"""
    print("\n" + "="*70)
    print("TEST 5: /generate-ficha-2-2-only con datos completos (GRANDES)")
    print("="*70)
    
    payload = {
        "cliente_nombre": "Test Cliente",
        "cliente_nif": "A31768138",
        "anio_fiscal": 2024
    }
    
    params = {
        "cliente_nif": "A31768138",
        "proyecto_acronimo": "GRANDES"
    }
    
    response = requests.post(f"{BASE_URL}/generate-ficha-2-2-only", json=payload, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        print("\n✅ Ficha 2.2 generada correctamente")
    else:
        print("\n❌ Error al generar Ficha 2.2")
    
    return response.status_code == 200


def main():
    print("\n" + "🧪 PRUEBAS DE FICHAS SELECTIVAS")
    print("=" * 70)
    print("Verificando que el backend esté disponible...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print("✅ Backend disponible")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Backend no disponible en", BASE_URL)
        print("   Asegúrate de que uvicorn esté ejecutándose:")
        print("   cd C:\\Fichas\\backend && C:\\Fichas\\venv\\Scripts\\python.exe -m uvicorn main:app --reload")
        return
    
    results = []
    
    results.append(("Test 1: Fichas completas (GRANDES)", test_generate_fichas_complete()))
    results.append(("Test 2: Fichas parciales (PLANEROPTI)", test_generate_fichas_partial()))
    results.append(("Test 3: Ficha 2.1 sola", test_generate_ficha_2_1_only()))
    results.append(("Test 4: Ficha 2.2 (debe fallar sin datos)", test_generate_ficha_2_2_only_partial()))
    results.append(("Test 5: Ficha 2.2 sola (GRANDES)", test_generate_ficha_2_2_only_complete()))
    
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    print(f"\n{passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")


if __name__ == "__main__":
    main()
