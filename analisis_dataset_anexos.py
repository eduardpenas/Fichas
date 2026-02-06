#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de evaluación avanzada del procesamiento de Anexos II
Detecta qué hojas existen en cada Excel y evalúa extracción de datos
"""

import sys
import os
import json
import pandas as pd
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Colores para output
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

def print_color(text, color='RESET'):
    print(f"{COLORS[color]}{text}{COLORS['RESET']}")

def print_header(text):
    print_color("\n" + "="*100, 'BLUE')
    print_color(text, 'BOLD')
    print_color("="*100 + "\n", 'BLUE')

def analizar_archivo(archivo_path):
    """Analiza un archivo Excel y extrae información sobre su estructura"""
    
    archivo_nombre = os.path.basename(archivo_path)
    resultado = {
        'archivo': archivo_nombre,
        'hojas': {},
        'datos_solicitud': {'ok': False, 'entidad': None, 'nif': None},
        'personal': {'ok': False, 'cantidad': 0, 'columnas': []},
        'colaboraciones': {'ok': False, 'cantidad': 0, 'hoja': None},
        'facturas': {'ok': False, 'cantidad': 0},
    }
    
    try:
        # Leer todas las hojas
        excel_file = pd.ExcelFile(archivo_path)
        hojas_disponibles = excel_file.sheet_names
        
        print_color(f"\n📄 {archivo_nombre}", 'CYAN')
        print(f"   Hojas encontradas: {', '.join(hojas_disponibles)}")
        
        # Guardar hojas
        resultado['hojas'] = hojas_disponibles
        
        # ========== DATOS SOLICITUD ==========
        for hoja in hojas_disponibles:
            if 'Datos' in hoja or 'datos' in hoja:
                try:
                    df = pd.read_excel(archivo_path, sheet_name=hoja)
                    resultado['datos_solicitud']['ok'] = True
                    print(f"   ✓ Datos solicitud (hoja: '{hoja}', {df.shape[0]} filas)")
                    
                    # Intentar extraer Entidad y NIF
                    for col in df.columns:
                        if 'entidad' in col.lower() or 'empresa' in col.lower():
                            if df[col].notna().any():
                                resultado['datos_solicitud']['entidad'] = str(df[col].iloc[0])
                                break
                except Exception as e:
                    pass
                break
        
        # ========== PERSONAL ==========
        for hoja in hojas_disponibles:
            if 'personal' in hoja.lower():
                try:
                    df = pd.read_excel(archivo_path, sheet_name=hoja, header=[12, 13] if 'header' not in hoja.lower() else None)
                    resultado['personal']['ok'] = True
                    resultado['personal']['cantidad'] = df.shape[0]
                    resultado['personal']['columnas'] = list(df.columns)[:5]  # Primeras 5
                    print(f"   ✓ Personal (hoja: '{hoja}', {df.shape[0]} filas, {df.shape[1]} columnas)")
                except Exception as e:
                    print(f"   ⚠️  Personal (hoja: '{hoja}') - Error: {str(e)[:40]}")
                break
        
        # ========== COLABORACIONES - BÚSQUEDA FLEXIBLE ==========
        nombres_alternos = ['C.Externas', 'C. Externas', 'Colaboraciones', 'colaboradores', 
                           'Externos', 'externos', 'Externas', 'externas', 'External']
        
        for hoja in hojas_disponibles:
            # Busca por nombre directo
            if hoja in nombres_alternos or hoja.lower() in [n.lower() for n in nombres_alternos]:
                try:
                    df = pd.read_excel(archivo_path, sheet_name=hoja, header=[12, 13])
                    resultado['colaboraciones']['ok'] = True
                    resultado['colaboraciones']['cantidad'] = df.shape[0]
                    resultado['colaboraciones']['hoja'] = hoja
                    print(f"   ✓ Colaboraciones (hoja: '{hoja}', {df.shape[0]} filas, {df.shape[1]} columnas)")
                except Exception as e:
                    print(f"   ⚠️  Colaboraciones (hoja: '{hoja}') - {str(e)[:40]}")
                break
            
            # Búsqueda parcial en el nombre
            if 'extern' in hoja.lower() or 'colab' in hoja.lower():
                try:
                    df = pd.read_excel(archivo_path, sheet_name=hoja, header=[12, 13])
                    resultado['colaboraciones']['ok'] = True
                    resultado['colaboraciones']['cantidad'] = df.shape[0]
                    resultado['colaboraciones']['hoja'] = hoja
                    print(f"   ✓ Colaboraciones (hoja: '{hoja}', {df.shape[0]} filas, {df.shape[1]} columnas)")
                except Exception as e:
                    print(f"   ⚠️  Colaboraciones (hoja: '{hoja}') - {str(e)[:40]}")
                break
        
        # ========== FACTURAS ==========
        for hoja in hojas_disponibles:
            if 'factura' in hoja.lower():
                try:
                    df = pd.read_excel(archivo_path, sheet_name=hoja)
                    resultado['facturas']['ok'] = True
                    resultado['facturas']['cantidad'] = df.shape[0]
                    print(f"   ✓ Facturas (hoja: '{hoja}', {df.shape[0]} filas)")
                except Exception as e:
                    print(f"   ⚠️  Facturas (hoja: '{hoja}') - Error")
                break
    
    except Exception as e:
        print_color(f"   ❌ Error leyendo archivo: {str(e)}", 'RED')
    
    return resultado

def main():
    print_header("🔬 ANÁLISIS AVANZADO - DATASET DE ANEXOS")
    
    dataset_dir = os.path.join(os.path.dirname(__file__), 'Dataset de Anexos')
    
    if not os.path.exists(dataset_dir):
        print_color(f"❌ Directorio no encontrado: {dataset_dir}", 'RED')
        return
    
    archivos = sorted([f for f in os.listdir(dataset_dir) if f.endswith('.xlsx')])
    print(f"📂 Analizando {len(archivos)} archivos...\n")
    
    # Analizar cada archivo
    resultados = []
    estadisticas = {
        'total': len(archivos),
        'personal_ok': 0,
        'colaboraciones_ok': 0,
        'personal_total': 0,
        'colaboraciones_total': 0,
        'hojas_encontradas': set()
    }
    
    for archivo in archivos:
        archivo_path = os.path.join(dataset_dir, archivo)
        resultado = analizar_archivo(archivo_path)
        resultados.append(resultado)
        
        # Actualizar estadísticas
        if resultado['personal']['ok']:
            estadisticas['personal_ok'] += 1
            estadisticas['personal_total'] += resultado['personal']['cantidad']
        
        if resultado['colaboraciones']['ok']:
            estadisticas['colaboraciones_ok'] += 1
            estadisticas['colaboraciones_total'] += resultado['colaboraciones']['cantidad']
        
        # Registrar hojas encontradas
        for hoja in resultado['hojas']:
            estadisticas['hojas_encontradas'].add(hoja)
    
    # Resumen
    print_header("📊 ANÁLISIS DE RESULTADOS")
    
    print_color("👥 PERSONAL:", 'BOLD')
    print(f"  ✅ Archivos con Personal: {estadisticas['personal_ok']}/{estadisticas['total']}")
    print(f"  ✅ Total de personas: {estadisticas['personal_total']}")
    print(f"  📊 Promedio por archivo: {estadisticas['personal_total']/estadisticas['personal_ok']:.1f}" if estadisticas['personal_ok'] > 0 else "")
    
    print_color("\n🤝 COLABORACIONES:", 'BOLD')
    print(f"  ✅ Archivos con Colaboraciones: {estadisticas['colaboraciones_ok']}/{estadisticas['total']}")
    print(f"  ✅ Total de colaboraciones: {estadisticas['colaboraciones_total']}")
    
    print_color("\n📋 HOJAS ENCONTRADAS EN EL DATASET:", 'BOLD')
    hojas_sorted = sorted(estadisticas['hojas_encontradas'])
    for hoja in hojas_sorted:
        apariciones = sum(1 for r in resultados if hoja in r['hojas'])
        print(f"  • {hoja:<40} ({apariciones} archivos)")
    
    # Detectar patrón de nombres de hojas
    print_header("🔍 ANÁLISIS DE ESTRUCTURA")
    
    # Hojas de Colaboraciones detectadas
    hojas_colabs = set()
    for r in resultados:
        if r['colaboraciones']['ok']:
            hojas_colabs.add(r['colaboraciones']['hoja'])
    
    if hojas_colabs:
        print_color("Hojas de Colaboraciones Detectadas:", 'BOLD')
        for hoja in sorted(hojas_colabs):
            print(f"  • {hoja}")
    else:
        print_color("⚠️  No se detectaron hojas de Colaboraciones", 'YELLOW')
    
    # Análisis de variabilidad
    print_color("\n📈 VARIABILIDAD DE DATOS:", 'BOLD')
    personas_por_archivo = [r['personal']['cantidad'] for r in resultados if r['personal']['ok']]
    if personas_por_archivo:
        print(f"  Mínimo de personas: {min(personas_por_archivo)}")
        print(f"  Máximo de personas: {max(personas_por_archivo)}")
        print(f"  Promedio: {sum(personas_por_archivo)/len(personas_por_archivo):.1f}")
    
    # Recomendaciones
    print_header("💡 RECOMENDACIONES")
    
    if estadisticas['colaboraciones_ok'] == 0:
        print_color("⚠️  ENCONTRADO: Ningún archivo tiene datos de Colaboraciones", 'YELLOW')
        print("   Posibles razones:")
        print("   1. La hoja no existe en estos formularios")
        print("   2. El nombre de la hoja es diferente")
        print("   3. Los datos están vacíos")
        print("\n   Acción recomendada:")
        print("   • Revisar manualmente uno de los Excel")
        print("   • Buscar si existe alguna hoja con colaboradores/externos")
    
    if estadisticas['personal_ok'] == estadisticas['total']:
        print_color("✅ EXCELENTE: Todos los archivos tienen Personal", 'GREEN')
    
    # Guardar análisis completo
    export_data = {
        'estadisticas': {
            'total_archivos': estadisticas['total'],
            'archivos_personal': estadisticas['personal_ok'],
            'archivos_colaboraciones': estadisticas['colaboraciones_ok'],
            'total_personas': estadisticas['personal_total'],
            'total_colaboraciones': estadisticas['colaboraciones_total'],
        },
        'hojas_detectadas': list(estadisticas['hojas_encontradas']),
        'resultados_detallados': resultados
    }
    
    reporte_path = os.path.join(os.path.dirname(__file__), 'analisis_dataset_anexos.json')
    with open(reporte_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print_header("✅ ANÁLISIS COMPLETADO")
    print(f"Reporte guardado: {reporte_path}")

if __name__ == "__main__":
    main()
