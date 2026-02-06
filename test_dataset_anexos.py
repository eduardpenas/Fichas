#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de evaluación del procesamiento de Anexos II
Prueba todos los archivos en Dataset de Anexos y evalúa:
- Extracción de Personal
- Extracción de Colaboraciones
- Extracción de Facturas
"""

import sys
import os
import json
import shutil
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from procesar_anexo import procesar_anexo

# Colores para output
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

def print_color(text, color='RESET'):
    """Imprime con color"""
    print(f"{COLORS[color]}{text}{COLORS['RESET']}")

def print_header(text):
    """Imprime header con separador"""
    print_color("\n" + "="*80, 'BLUE')
    print_color(text, 'BOLD')
    print_color("="*80 + "\n", 'BLUE')

def print_result(label, value, ok=True):
    """Imprime resultado de una prueba"""
    color = 'GREEN' if ok else 'RED'
    icon = '✅' if ok else '❌'
    print(f"  {icon} {label}: {value}")

def evaluar_archivo(archivo_path, output_dir):
    """Evalúa un single archivo Excel"""
    
    archivo_nombre = os.path.basename(archivo_path)
    print_color(f"\n📄 Procesando: {archivo_nombre}", 'BOLD')
    print("-" * 60)
    
    resultados = {
        'archivo': archivo_nombre,
        'estado': 'OK',
        'personal': {'cantidad': 0, 'ok': False, 'detalles': []},
        'colaboraciones': {'cantidad': 0, 'ok': False, 'detalles': []},
        'facturas': {'cantidad': 0, 'ok': False, 'detalles': []},
        'errores': []
    }
    
    try:
        # Copiar archivo a inputs para processarlo
        temp_input_dir = os.path.join(os.path.dirname(__file__), 'inputs_temp')
        os.makedirs(temp_input_dir, exist_ok=True)
        
        archivo_copia = os.path.join(temp_input_dir, archivo_nombre)
        shutil.copy2(archivo_path, archivo_copia)
        
        # Crear directorio output temporal
        temp_output_dir = os.path.join(temp_input_dir)
        os.makedirs(temp_output_dir, exist_ok=True)
        
        # Procesar el archivo
        from procesar_anexo import procesar_anexo as procesar
        print("   🔄 Procesando...")
        
        # Leer el archivo directamente
        import pandas as pd
        try:
            # Intentar leer Datos solicitud
            df_datos = pd.read_excel(archivo_copia, sheet_name="Datos solicitud", header=11)
            print("   ✓ Hoja 'Datos solicitud' encontrada")
        except:
            resultados['errores'].append("No se encontró hoja 'Datos solicitud'")
        
        try:
            # Intentar leer Personal
            df_personal = pd.read_excel(archivo_copia, sheet_name="Personal", header=[12, 13])
            print(f"   ✓ Hoja 'Personal' encontrada ({df_personal.shape[0]} filas)")
        except Exception as e:
            resultados['errores'].append(f"Error leyendo Personal: {str(e)}")
        
        try:
            # Intentar leer Colaboraciones
            df_colabs = pd.read_excel(archivo_copia, sheet_name="C.Externas", header=[12, 13])
            print(f"   ✓ Hoja 'C.Externas' encontrada ({df_colabs.shape[0]} filas)")
        except Exception as e:
            resultados['errores'].append(f"Error leyendo C.Externas: {str(e)}")
        
        # Procesar con procesar_anexo
        try:
            # Modificar para que procese desde el archivo específico
            from procesar_anexo import procesar_anexo as procesar_func
            
            # Leer y procesar manualmente
            import pandas as pd
            import numpy as np
            
            print("   📝 Extractando datos...")
            archivo_completo = archivo_copia
            
            # Datos solicitud
            df_d = pd.read_excel(archivo_completo, sheet_name="Datos solicitud", header=11)
            
            # Personal
            try:
                df_p = pd.read_excel(archivo_completo, sheet_name="Personal", header=[12, 13])
                # Contar personas con datos
                personas_validas = df_p.shape[0]
                resultados['personal']['cantidad'] = personas_validas
                resultados['personal']['ok'] = personas_validas > 0
                print(f"   ✓ Personal: {personas_validas} registros")
                
                # Verificar columnas
                cols_encontradas = []
                for col in df_p.columns:
                    cols_encontradas.append(str(col))
                resultados['personal']['detalles'] = cols_encontradas[:5]  # Primeras 5 columnas
                
            except Exception as e:
                resultados['personal']['detalles'] = [f"Error: {str(e)}"]
            
            # Colaboraciones Externas
            try:
                df_c = pd.read_excel(archivo_completo, sheet_name="C.Externas", header=[12, 13])
                colabs_validas = df_c.shape[0]
                resultados['colaboraciones']['cantidad'] = colabs_validas
                resultados['colaboraciones']['ok'] = colabs_validas > 0
                print(f"   ✓ Colaboraciones: {colabs_validas} registros")
                
                # Verificar columnas
                cols_encontradas = []
                for col in df_c.columns:
                    cols_encontradas.append(str(col))
                resultados['colaboraciones']['detalles'] = cols_encontradas[:5]
                
            except Exception as e:
                resultados['colaboraciones']['detalles'] = [f"Error: {str(e)}"]
            
            # Facturas (si existe la hoja)
            try:
                df_f = pd.read_excel(archivo_completo, sheet_name="Facturas", header=[12, 13])
                facturas_validas = df_f.shape[0]
                resultados['facturas']['cantidad'] = facturas_validas
                resultados['facturas']['ok'] = facturas_validas > 0
                print(f"   ✓ Facturas: {facturas_validas} registros")
            except:
                # Facturas es opcional
                print(f"   ⚠️  Facturas: no encontrada (opcional)")
        
        except Exception as e:
            resultados['estado'] = 'ERROR'
            resultados['errores'].append(f"Error procesando: {str(e)}")
            print_color(f"   ❌ Error: {str(e)}", 'RED')
        
        # Limpiar
        try:
            shutil.rmtree(temp_input_dir)
        except:
            pass
    
    except Exception as e:
        resultados['estado'] = 'ERROR'
        resultados['errores'].append(str(e))
        print_color(f"   ❌ Error fundamental: {str(e)}", 'RED')
    
    return resultados

def main():
    """Función principal"""
    
    print_header("🧪 EVALUACIÓN DE PROCESAMIENTO DE ANEXOS II")
    
    dataset_dir = os.path.join(os.path.dirname(__file__), 'Dataset de Anexos')
    
    if not os.path.exists(dataset_dir):
        print_color(f"❌ Directorio no encontrado: {dataset_dir}", 'RED')
        return
    
    # Listar archivos (excluir archivos temporales de Excel como ~$...)
    archivos = [f for f in os.listdir(dataset_dir) if f.endswith('.xlsx') and not f.startswith('~$')]
    print(f"📂 Encontrados {len(archivos)} archivos Excel\n")
    
    estado_general = {
        'total': len(archivos),
        'procesados_ok': 0,
        'personal_ok': 0,
        'colaboraciones_ok': 0,
        'personal_total': 0,
        'colaboraciones_total': 0,
        'resultados': []
    }
    
    # Procesar cada archivo
    for archivo in sorted(archivos):
        archivo_path = os.path.join(dataset_dir, archivo)
        resultado = evaluar_archivo(archivo_path, dataset_dir)
        estado_general['resultados'].append(resultado)
        
        # Actualizar contadores
        if resultado['estado'] == 'OK':
            estado_general['procesados_ok'] += 1
            if resultado['personal']['ok']:
                estado_general['personal_ok'] += 1
                estado_general['personal_total'] += resultado['personal']['cantidad']
            if resultado['colaboraciones']['ok']:
                estado_general['colaboraciones_ok'] += 1
                estado_general['colaboraciones_total'] += resultado['colaboraciones']['cantidad']
    
    # Mostrar resumen
    print_header("📊 RESUMEN GENERAL")
    
    print_color("Archivos Evaluados:", 'BOLD')
    print_result("Total archivos", estado_general['total'])
    print_result("Procesados correctamente", estado_general['procesados_ok'], 
                 estado_general['procesados_ok'] == estado_general['total'])
    
    print_color("\n👥 Personal:", 'BOLD')
    print_result("Archivos con Personal", estado_general['personal_ok'])
    print_result("Total personas extraídas", estado_general['personal_total'])
    
    print_color("\n🤝 Colaboraciones:", 'BOLD')
    print_result("Archivos con Colaboraciones", estado_general['colaboraciones_ok'])
    print_result("Total colaboraciones extraídas", estado_general['colaboraciones_total'])
    
    # Tabla detallada
    print_header("📋 RESULTADOS DETALLADOS")
    
    print(f"{'Archivo':<50} {'Personal':<12} {'Colaboraciones':<18} {'Estado':<10}")
    print("-" * 90)
    
    for resultado in estado_general['resultados']:
        archivo_short = resultado['archivo'][:47]
        personal_str = f"✅ {resultado['personal']['cantidad']}" if resultado['personal']['ok'] else "❌"
        colabs_str = f"✅ {resultado['colaboraciones']['cantidad']}" if resultado['colaboraciones']['ok'] else "❌"
        estado_icon = "✅" if resultado['estado'] == 'OK' else "❌"
        
        print(f"{archivo_short:<50} {personal_str:<12} {colabs_str:<18} {estado_icon:<10}")
    
    # Estadísticas de éxito
    print_header("✨ CONCLUSIONES")
    
    porcentaje_ok = (estado_general['procesados_ok'] / estado_general['total'] * 100) if estado_general['total'] > 0 else 0
    
    if porcentaje_ok == 100:
        print_color(f"🎉 ¡EXCELENTE! Todos los {estado_general['total']} archivos se procesaron correctamente", 'GREEN')
    elif porcentaje_ok >= 80:
        print_color(f"✅ {porcentaje_ok:.1f}% de archivos procesados correctamente", 'GREEN')
    else:
        print_color(f"⚠️  Solo {porcentaje_ok:.1f}% de archivos procesados correctamente", 'YELLOW')
    
    if estado_general['personal_total'] > 0:
        print_color(f"\n✅ Se extrajeron {estado_general['personal_total']} personas", 'GREEN')
    else:
        print_color(f"\n⚠️  No se extrajeron personas", 'YELLOW')
    
    if estado_general['colaboraciones_total'] > 0:
        print_color(f"✅ Se extrajeron {estado_general['colaboraciones_total']} colaboraciones", 'GREEN')
    else:
        print_color(f"⚠️  No se extrajeron colaboraciones", 'YELLOW')
    
    # Archivos con problemas
    archivos_problemas = [r for r in estado_general['resultados'] if r['estado'] != 'OK' or r['errores']]
    if archivos_problemas:
        print_header("⚠️  ARCHIVOS CON PROBLEMAS")
        for resultado in archivos_problemas:
            print_color(f"\n{resultado['archivo']}", 'YELLOW')
            for error in resultado['errores']:
                print(f"  • {error}")
    
    # Guardar reporte en JSON
    reporte_path = os.path.join(os.path.dirname(__file__), 'reporte_dataset_anexos.json')
    with open(reporte_path, 'w', encoding='utf-8') as f:
        json.dump(estado_general, f, ensure_ascii=False, indent=2)
    
    print_header("✅ REPORTE GUARDADO")
    print(f"Archivo: {reporte_path}")
    print(f"Puedes revisar los detalles en el JSON")

if __name__ == "__main__":
    main()
