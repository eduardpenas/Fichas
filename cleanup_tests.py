#!/usr/bin/env python3
"""
Script para limpiar datos de prueba del sistema Fichas
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
PROYECTOS_DIR = BASE_DIR / "proyectos"

def cleanup():
    """Elimina todas las carpetas de prueba"""
    
    test_clients = ["A12345678", "B87654321"]
    
    print("\n" + "="*70)
    print("  🧹 LIMPIEZA DE DATOS DE PRUEBA")
    print("="*70 + "\n")
    
    deleted_count = 0
    
    for nif in test_clients:
        client_dir = PROYECTOS_DIR / f"Cliente_{nif}"
        
        if client_dir.exists():
            try:
                shutil.rmtree(client_dir)
                print(f"✅ Eliminada carpeta: {client_dir}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Error eliminando {client_dir}: {e}")
        else:
            print(f"⏭️  No existe: {client_dir}")
    
    print(f"\n📊 Resultado: {deleted_count} carpeta(s) eliminada(s)")
    print("=" * 70 + "\n")
    
    if deleted_count > 0:
        print("✅ Limpieza completada. Ahora puedes ejecutar las pruebas nuevamente.\n")
    else:
        print("ℹ️  No había datos de prueba para limpiar.\n")

if __name__ == "__main__":
    try:
        cleanup()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        exit(1)
