"""
Script de prueba para demostrar la validación automática con casos de error.
"""

import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.validador import ValidadorFichas


def test_validacion_con_errores():
    """Prueba la validación con datos que contienen errores."""
    
    # Crear DataFrame de prueba con errores
    datos_con_errores = {
        'Nombre': ['Juan', 'María', ''],  # Tercera fila sin nombre
        'Apellidos': ['García', 'López', 'Martínez'],
        'Titulación 1': ['Ingeniero', 'Abogada', 'Médico'],
        'Coste horario (€/hora)': [50.0, 60.0, 0],  # Tercera con coste 0
        'Horas totales': [100, 80, 50],
        'Coste total (€)': [5000, 4800, 0],  # Inconsistencia
        'EMPRESA 1': ['Empresa A', '', ''],  # Muchas sin experiencia
        'EMPRESA 2': ['', '', ''],
        'EMPRESA 3': ['', '', ''],
    }
    
    df_prueba = pd.DataFrame(datos_con_errores)
    
    print("\n" + "="*70)
    print("🧪 TEST DE VALIDACIÓN CON ERRORES")
    print("="*70)
    
    validador = ValidadorFichas()
    es_valido = validador.validar_personal(df_prueba)
    
    print(f"\n✅ Validación completada. ¿Es válido? {es_valido}")
    print(f"\n📊 Resumen:")
    resumen = validador.obtener_resumen()
    print(f"   - Errores: {resumen['errores_count']}")
    print(f"   - Advertencias: {resumen['advertencias_count']}")
    print(f"   - Mensaje: {resumen['mensaje']}")


def test_validacion_correcta():
    """Prueba la validación con datos correctos."""
    
    # Crear DataFrame de prueba válido
    datos_correctos = {
        'Nombre': ['Juan', 'María'],
        'Apellidos': ['García', 'López'],
        'Titulación 1': ['Ingeniero', 'Abogada'],
        'Coste horario (€/hora)': [50.0, 60.0],
        'Horas totales': [100, 80],
        'Coste total (€)': [5000, 4800],
        'EMPRESA 1': ['Empresa A', 'Empresa B'],
        'EMPRESA 2': ['', ''],
        'EMPRESA 3': ['', ''],
    }
    
    df_prueba = pd.DataFrame(datos_correctos)
    
    print("\n" + "="*70)
    print("🧪 TEST DE VALIDACIÓN CORRECTA")
    print("="*70)
    
    validador = ValidadorFichas()
    es_valido = validador.validar_personal(df_prueba)
    
    print(f"\n✅ Validación completada. ¿Es válido? {es_valido}")
    print(f"\n📊 Resumen:")
    resumen = validador.obtener_resumen()
    print(f"   - Errores: {resumen['errores_count']}")
    print(f"   - Advertencias: {resumen['advertencias_count']}")
    print(f"   - Mensaje: {resumen['mensaje']}")


if __name__ == "__main__":
    test_validacion_correcta()
    test_validacion_con_errores()
