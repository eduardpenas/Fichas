import os
import sys
import pandas as pd

# Añadimos el directorio actual al path para importar los módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logica_fichas import generar_ficha_2_1, generar_ficha_2_2

def main():
    # 1. Configuración de Directorios (Rutas relativas para que funcione en cualquier PC)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

    # Crear carpeta de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("--- GENERADOR DE FICHAS AUTOMÁTICAS ---")
    print(f"Leyendo archivos desde: {INPUT_DIR}")
    print(f"Guardando resultados en: {OUTPUT_DIR}")

    # 2. Simulación de inputs (En el futuro, esto vendrá del Frontend)
    # Nota: Asegúrate de que estos archivos existan en la carpeta 'inputs'
    archivo_personal = os.path.join(INPUT_DIR, "Excel_Personal_2.1.xlsx")
    archivo_colaboraciones = os.path.join(INPUT_DIR, "Excel_Colaboraciones_2.2.xlsx")
    archivo_facturas = os.path.join(INPUT_DIR, "Excel_Facturas_2.2.xlsx")
    
    plantilla_2_1 = os.path.join(INPUT_DIR, "2.1.docx")
    plantilla_2_2 = os.path.join(INPUT_DIR, "2.2.docx")

    # Datos variables
    anio = "2024"
    cliente = "Empresa Cliente S.L"
    acronimo = "PROYECTO_TEST"

    # 3. Ejecución de Ficha 2.1
    if os.path.exists(archivo_personal) and os.path.exists(plantilla_2_1):
        print("\n🚀 Generando Ficha 2.1...")
        try:
            ruta_salida_21 = os.path.join(OUTPUT_DIR, f"Ficha_2_1_{acronimo}_{anio}.docx")
            generar_ficha_2_1(archivo_personal, plantilla_2_1, ruta_salida_21, anio, cliente)
            print(f"✅ Ficha 2.1 generada correctamente: {ruta_salida_21}")
        except Exception as e:
            print(f"❌ Error generando Ficha 2.1: {e}")
    else:
        print(f"⚠️ No se encontró {archivo_personal} o {plantilla_2_1}. Saltando Ficha 2.1.")

    # 4. Ejecución de Ficha 2.2
    if os.path.exists(archivo_colaboraciones) and os.path.exists(archivo_facturas) and os.path.exists(plantilla_2_2):
        print("\n🚀 Generando Ficha 2.2...")
        try:
            ruta_salida_22 = os.path.join(OUTPUT_DIR, f"Ficha_2_2_{acronimo}_{anio}.docx")
            generar_ficha_2_2(archivo_colaboraciones, archivo_facturas, plantilla_2_2, ruta_salida_22)
            print(f"✅ Ficha 2.2 generada correctamente: {ruta_salida_22}")
        except Exception as e:
            print(f"❌ Error generando Ficha 2.2: {e}")
    else:
        print(f"⚠️ Faltan archivos para la Ficha 2.2. Saltando.")

if __name__ == "__main__":
    main()