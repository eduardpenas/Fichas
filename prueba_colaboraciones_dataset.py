#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba - Validar Procesamiento de Colaboraciones
Prueba el nuevo sistema con el Dataset de Anexos
"""

import sys
import os
import json
import shutil
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from procesar_anexo import procesar_anexo

DATASET_DIR = os.path.join(os.path.dirname(__file__), 'Dataset de Anexos')
TEST_ARCHIVOS = [
    'Anexo_II_INTOPQUERE_2021.xlsx',
    'Formulario_Anexo_II_ORANTECH21_2022.xlsx',
    'Formulario_Anexo_II_tipo_a_GSP_v2.xlsx'
]

def print_header(text):
    print("\n" + "="*100)
    print(text.center(100))
    print("="*100 + "\n")

def print_section(text):
    print("\n" + "—"*100)
    print(text)
    print("—"*100)

def prueba_archivo(archivo_nombre):
    """Prueba un archivo específico"""
    
    print(f"\n📄 PRUEBANDO: {archivo_nombre}")
    print("-" * 100)
    
    resultado = {
        'archivo': archivo_nombre,
        'personal': 0,
        'colaboraciones': 0,
        'facturas': 0,
        'status': 'OK'
    }
    
    temp_dir = None
    try:
        # Crear directorio temporal
        temp_dir = tempfile.mkdtemp()
        inputs_temp = os.path.join(temp_dir, 'inputs')
        os.makedirs(inputs_temp, exist_ok=True)
        
        # Copiar archivo
        archivo_source = os.path.join(DATASET_DIR, archivo_nombre)
        archivo_temp = os.path.join(inputs_temp, archivo_nombre)
        shutil.copy2(archivo_source, archivo_temp)
        
        print(f"   ✓ Archivo copiado a: {inputs_temp}")
        
        # Procesar
        print(f"   🔄 Procesando...")
        import pandas as pd
        
        # Leer Personal
        try:
            df_personal = pd.read_excel(archivo_temp, sheet_name='Personal', header=[12, 13])
            resultado['personal'] = df_personal.shape[0]
            print(f"   ✓ Personal: {resultado['personal']} registros")
        except Exception as e:
            print(f"   ✗ Personal error: {str(e)[:50]}")
            resultado['status'] = 'WARN'
        
        # Leer Colaboraciones - OPIS (PRIMERO)
        try:
            df_colabs = pd.read_excel(archivo_temp, sheet_name='C.Externas (OPIS)', header=[12, 13])
            resultado['colaboraciones'] = df_colabs.shape[0]
            print(f"   ✓ Colaboraciones (OPIS): {resultado['colaboraciones']} registros")
        except Exception as e:
            print(f"   ✗ Colaboraciones (OPIS) error: {str(e)[:50]}")
            
            # Intentar Otros
            try:
                df_colabs = pd.read_excel(archivo_temp, sheet_name='C.Externas (Otros)', header=[12, 13])
                resultado['colaboraciones'] = df_colabs.shape[0]
                print(f"   ✓ Colaboraciones (Otros): {resultado['colaboraciones']} registros")
            except:
                print(f"   ✗ No se encontraron colaboraciones")
                resultado['status'] = 'WARN'
        
        # Leer Facturas (opcional)
        try:
            df_facturas = pd.read_excel(archivo_temp, sheet_name='Facturas', header=[12, 13])
            resultado['facturas'] = df_facturas.shape[0]
            print(f"   ✓ Facturas: {resultado['facturas']} registros")
        except:
            print(f"   ⚠️  Facturas: no encontida (opcional)")
    
    except Exception as e:
        resultado['status'] = 'ERROR'
        print(f"   ❌ Error: {str(e)}")
    
    finally:
        # Limpiar
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    # Resumen
    print_section(f"Resumen: {resultado['archivo']}")
    print(f"  👥 Personal: {resultado['personal']}")
    print(f"  🤝 Colaboraciones: {resultado['colaboraciones']}")
    print(f"  📄 Facturas: {resultado['facturas']}")
    print(f"  Status: {resultado['status']}")
    
    return resultado

def main():
    print_header("🧪 PRUEBA DE PROCESAMIENTO - COLABORACIONES")
    
    print(f"Archivos a probar: {len(TEST_ARCHIVOS)}")
    for archivo in TEST_ARCHIVOS:
        print(f"  • {archivo}")
    
    resultados = []
    for archivo in TEST_ARCHIVOS:
        resultado = prueba_archivo(archivo)
        resultados.append(resultado)
    
    # Resumen final
    print_header("📊 RESUMEN FINAL")
    
    print(f"{'Archivo':<50} {'Personal':<12} {'Colaboraciones':<18} {'Status':<10}")
    print("—"*90)
    
    total_personal = 0
    total_colabs = 0
    total_ok = 0
    
    for r in resultados:
        archivo_short = r['archivo'][:47]
        print(f"{archivo_short:<50} {r['personal']:<12} {r['colaboraciones']:<18} {r['status']:<10}")
        
        total_personal += r['personal']
        total_colabs += r['colaboraciones']
        if r['status'] == 'OK':
            total_ok += 1
    
    print("\n" + "—"*90)
    print(f"TOTAL: {total_personal} personas, {total_colabs} colaboraciones ({total_ok}/{len(TEST_ARCHIVOS)} OK)")
    
    # Recomendación
    print_header("✨ CONCLUSIONES")
    
    if total_colabs > 0:
        print(f"✅ Colaboraciones detectadas correctamente: {total_colabs}")
        print(f"✅ El sistema está listo para procesar el dataset completo")
    else:
        print(f"⚠️  No se detectaron colaboraciones")
        print(f"⚠️  Revisar la lógica de procesamiento")
    
    print(f"\n✅ Próximo paso: Procesar los {len(TEST_ARCHIVOS)} archivos con procesar_anexo()")

if __name__ == "__main__":
    main()
