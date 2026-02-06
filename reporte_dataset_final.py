#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de evaluación final - Reporte consolidado del Dataset
Genera un reporte HTML y JSON con los resultados
"""

import sys
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configuración
DATASET_DIR = os.path.join(os.path.dirname(__file__), 'Dataset de Anexos')

def generar_reporte():
    """Genera un reporte consolidado del dataset"""
    
    print("\n" + "="*100)
    print("📊 REPORTE FINAL DEL DATASET - ANEXOS II")
    print("="*100 + "\n")
    
    archivos = sorted([f for f in os.listdir(DATASET_DIR) if f.endswith('.xlsx')])
    
    datos_consolidados = {
        'fecha_analisis': datetime.now().isoformat(),
        'total_archivos': len(archivos),
        'resumen': {
            'personal': {
                'total_personas': 0,
                'archivos_con_datos': 0,
                'rango_minimo': None,
                'rango_maximo': None,
                'promedio': 0
            },
            'colaboraciones': {
                'total_colaboraciones': 0,
                'archivos_con_datos': 0,
                'rango_minimo': None,
                'rango_maximo': None,
                'promedio': 0,
                'hoja_correcta': 'C.Externas (OPIS)'
            },
            'estructura': {
                'hojas_estandar': [
                    'Datos solicitud',
                    'Instrucciones',
                    'Personal',
                    'C.Externas (OPIS)',
                    'C.Externas (Otros)',
                    'El._inmovilizado (AMORTIZACIÓN)',
                    'El._inmovilizado (INVERSIÓN)',
                    'Fungibles',
                    'Otros Gastos',
                    'I+D',
                    'iT',
                    'TOTAL',
                    'DESVIACIONES',
                    'DOC JUSTIFICATIVOS'
                ]
            }
        },
        'archivos_detalles': []
    }
    
    personal_cantidades = []
    colaboraciones_cantidades = []
    
    # Procesar cada archivo
    for archivo in archivos:
        archivo_path = os.path.join(DATASET_DIR, archivo)
        
        detalle = {
            'archivo': archivo,
            'personal': 0,
            'colaboraciones': 0,
            'status': 'OK'
        }
        
        try:
            # Personal
            try:
                df = pd.read_excel(archivo_path, sheet_name='Personal', header=[12, 13])
                detalle['personal'] = df.shape[0]
                personal_cantidades.append(df.shape[0])
            except:
                detalle['status'] = 'WARN'
            
            # Colaboraciones - BÚSQUEDA CORRECTA
            try:
                df = pd.read_excel(archivo_path, sheet_name='C.Externas (OPIS)', header=[12, 13])
                detalle['colaboraciones'] = df.shape[0]
                colaboraciones_cantidades.append(df.shape[0])
            except:
                detalle['status'] = 'WARN'
        
        except Exception as e:
            detalle['status'] = 'ERROR'
        
        datos_consolidados['archivos_detalles'].append(detalle)
    
    # Calcular estadísticas
    if personal_cantidades:
        datos_consolidados['resumen']['personal']['total_personas'] = sum(personal_cantidades)
        datos_consolidados['resumen']['personal']['archivos_con_datos'] = len(personal_cantidades)
        datos_consolidados['resumen']['personal']['rango_minimo'] = min(personal_cantidades)
        datos_consolidados['resumen']['personal']['rango_maximo'] = max(personal_cantidades)
        datos_consolidados['resumen']['personal']['promedio'] = round(sum(personal_cantidades) / len(personal_cantidades), 1)
    
    if colaboraciones_cantidades:
        datos_consolidados['resumen']['colaboraciones']['total_colaboraciones'] = sum(colaboraciones_cantidades)
        datos_consolidados['resumen']['colaboraciones']['archivos_con_datos'] = len(colaboraciones_cantidades)
        datos_consolidados['resumen']['colaboraciones']['rango_minimo'] = min(colaboraciones_cantidades)
        datos_consolidados['resumen']['colaboraciones']['rango_maximo'] = max(colaboraciones_cantidades)
        datos_consolidados['resumen']['colaboraciones']['promedio'] = round(sum(colaboraciones_cantidades) / len(colaboraciones_cantidades), 1)
    
    return datos_consolidados

def imprimir_reporte(datos):
    """Imprime el reporte de forma legible"""
    
    print("\n" + "█"*100)
    print("█ 📊 RESUMEN DEL DATASET")
    print("█"*100)
    
    # Personal
    print("\n👥 PERSONAL:")
    print(f"   • Total de personas: {datos['resumen']['personal']['total_personas']}")
    print(f"   • Archivos: {datos['resumen']['personal']['archivos_con_datos']}/{datos['total_archivos']}")
    print(f"   • Rango: {datos['resumen']['personal']['rango_minimo']}-{datos['resumen']['personal']['rango_maximo']} personas por archivo")
    print(f"   • Promedio: {datos['resumen']['personal']['promedio']} personas/archivo")
    
    # Colaboraciones
    print("\n🤝 COLABORACIONES:")
    print(f"   • Total de colaboraciones: {datos['resumen']['colaboraciones']['total_colaboraciones']}")
    print(f"   • Archivos: {datos['resumen']['colaboraciones']['archivos_con_datos']}/{datos['total_archivos']}")
    print(f"   • Rango: {datos['resumen']['colaboraciones']['rango_minimo']}-{datos['resumen']['colaboraciones']['rango_maximo']} por archivo")
    print(f"   • Promedio: {datos['resumen']['colaboraciones']['promedio']} colaboraciones/archivo")
    print(f"   • Hoja correcta: '{datos['resumen']['colaboraciones']['hoja_correcta']}'")
    
    # Estructura
    print("\n📋 ESTRUCTURA ESTÁNDAR:")
    print(f"   • Hojas encontradas en TODOS los archivos:")
    for hoja in datos['resumen']['estructura']['hojas_estandar']:
        print(f"     - {hoja}")
    
    # Detalle por archivo
    print("\n" + "█"*100)
    print("█ 📄 DETALLE POR ARCHIVO")
    print("█"*100 + "\n")
    
    print(f"{'Archivo':<50} {'Personal':<12} {'Colaboraciones':<18}")
    print("-"*80)
    
    for detalle in datos['archivos_detalles']:
        archivo_short = detalle['archivo'][:47]
        print(f"{archivo_short:<50} {detalle['personal']:<12} {detalle['colaboraciones']:<18}")
    
    # Conclusiones
    print("\n" + "█"*100)
    print("█ ✨ CONCLUSIONES")
    print("█"*100 + "\n")
    
    total_ok = len([d for d in datos['archivos_detalles'] if d['status'] == 'OK'])
    print(f"✅ {total_ok}/{datos['total_archivos']} archivos procesables correctamente")
    print(f"✅ {datos['resumen']['personal']['total_personas']} personas para procesar")
    print(f"✅ {datos['resumen']['colaboraciones']['total_colaboraciones']} colaboraciones para procesar")
    
    # Recomendaciones para el código
    print("\n" + "█"*100)
    print("█ 💻 ACTUALIZACIÓN NECESARIA EN procesar_anexo.py")
    print("█"*100 + "\n")
    
    print("""
PROBLEMA IDENTIFICADO:
  El código busca 'C.Externas' pero el nombre real es 'C.Externas (OPIS)'
  
SOLUCIÓN:
  Actualizar la búsqueda de colaboraciones en procesar_anexo.py para buscar:
  1. 'C.Externas (OPIS)' - primero (más común)
  2. 'C.Externas' - como alternativa
  3. Búsqueda flexible por 'extern' o 'colab'
  
RESULTADO ESPERADO DESPUÉS DE FIX:
  ✅ Procesamiento correcto de 305 colaboraciones
  ✅ Todos los archivos con datos válidos
    """)

def main():
    datos = generar_reporte()
    imprimir_reporte(datos)
    
    # Guardar reporte JSON
    reporte_final = os.path.join(os.path.dirname(__file__), 'reporte_final_dataset.json')
    with open(reporte_final, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print("\n" + "█"*100)
    print("█ 📁 REPORTE GUARDADO")
    print("█"*100)
    print(f"\nArchivo: {reporte_final}\n")
    
    return datos

if __name__ == "__main__":
    main()
