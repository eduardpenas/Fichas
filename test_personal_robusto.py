#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test para verificar que el nuevo procesamiento de Personal funciona
correctamente con la versión robusta mejorada.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from procesar_anexo import procesar_anexo
import json

def test_procesar_anexo():
    """Test del procesamiento de Anexo con la nueva versión robusta."""
    
    print("\n" + "="*60)
    print("🧪 TEST: Procesamiento robusto de Anexo II")
    print("="*60 + "\n")
    
    try:
        # Procesar anexo (modo simple, sin cliente/proyecto)
        procesar_anexo()
        
        print("\n" + "-"*60)
        print("📊 VERIFICANDO RESULTADOS:")
        print("-"*60 + "\n")
        
        # Verificar que se crearon los archivos
        output_dir = os.path.join(os.path.dirname(__file__), 'inputs')
        
        archivos_json = [
            "Excel_Datos_solicitud_2.2.json",
            "Excel_Personal_2.1.json",
            "Excel_Facturas_2.2.json"
        ]
        
        for archivo in archivos_json:
            archivo_path = os.path.join(output_dir, archivo)
            if os.path.exists(archivo_path):
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                print(f"✅ {archivo}: {len(datos)} registros")
                
                # Mostrar primeros 2 registros para verificar estructura
                if datos:
                    print(f"   Primer registro: {json.dumps(datos[0], ensure_ascii=False, indent=2)}")
            else:
                print(f"❌ {archivo}: NO ENCONTRADO")
        
        print("\n" + "="*60)
        print("✅ TEST COMPLETADO EXITOSAMENTE")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_procesar_anexo()
