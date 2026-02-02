import os
import sys

# Añadimos el directorio actual al path para importar los módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from procesar_anexo import procesar_anexo
from procesar_cvs import procesar_cvs
from logica_fichas import generar_ficha_2_1, generar_ficha_2_2

def main():
    # 1. Configuración de Directorios
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

    # Crear carpeta de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n" + "="*70)
    print("🚀 PIPELINE PRINCIPAL: GENERACIÓN DE FICHAS")
    print("="*70)
    print(f"\n📁 Directorio de entrada: {INPUT_DIR}")
    print(f"📁 Directorio de salida: {OUTPUT_DIR}\n")

    # ========================================
    # PASO 1: Procesar Anexo II
    # ========================================
    print("[1/3] Procesando Anexo II...")
    procesar_anexo()

    # ========================================
    # PASO 2: Procesar CVs (actualiza JSON Personal)
    # ========================================
    print("\n[2/3] Procesando CVs...")
    procesar_cvs()

    # ========================================
    # PASO 3: Generar Fichas con Plantillas
    # ========================================
    print("\n[3/3] Generando fichas con plantillas...\n")

    # Rutas de JSONs generados
    archivo_personal = os.path.join(INPUT_DIR, "Excel_Personal_2.1.json")
    archivo_colaboraciones = os.path.join(INPUT_DIR, "Excel_Colaboraciones_2.2.json")
    archivo_facturas = os.path.join(INPUT_DIR, "Excel_Facturas_2.2.json")
    
    # Plantillas
    plantilla_2_1 = os.path.join(INPUT_DIR, "2.1.docx")
    plantilla_2_2 = os.path.join(INPUT_DIR, "2.2.docx")

    # Rutas de salida
    ruta_salida_21 = os.path.join(OUTPUT_DIR, "Ficha_2_1.docx")
    ruta_salida_22 = os.path.join(OUTPUT_DIR, "Ficha_2_2.docx")

    # Datos variables
    anio = 2024
    acronimo = "ACR"

    # Ficha 2.1 (Personal)
    if os.path.exists(archivo_personal) and os.path.exists(plantilla_2_1):
        print(f"   📄 Generando Ficha 2.1 (Personal)...")
        print(f"      Datos: {archivo_personal}")
        print(f"      Plantilla: {plantilla_2_1}")
        print(f"      Salida: {ruta_salida_21}")
        try:
            generar_ficha_2_1(archivo_personal, plantilla_2_1, ruta_salida_21, anio, acronimo)
            print(f"   ✅ Ficha 2.1 generada exitosamente\n")
        except Exception as e:
            print(f"   ❌ Error generando Ficha 2.1: {e}\n")
    else:
        print(f"   ⚠️ No se encontraron {archivo_personal} o {plantilla_2_1}\n")

    # Ficha 2.2 (Colaboraciones)
    if os.path.exists(archivo_colaboraciones) and os.path.exists(archivo_facturas) and os.path.exists(plantilla_2_2):
        print(f"   📄 Generando Ficha 2.2 (Colaboraciones)...")
        print(f"      Datos Colab: {archivo_colaboraciones}")
        print(f"      Datos Fact: {archivo_facturas}")
        print(f"      Plantilla: {plantilla_2_2}")
        print(f"      Salida: {ruta_salida_22}")
        try:
            generar_ficha_2_2(archivo_colaboraciones, archivo_facturas, plantilla_2_2, ruta_salida_22)
            print(f"   ✅ Ficha 2.2 generada exitosamente\n")
        except Exception as e:
            print(f"   ❌ Error generando Ficha 2.2: {e}\n")
    else:
        print(f"   ⚠️ Faltan archivos para la Ficha 2.2. Saltando.\n")

    print("="*70)
    print("✅ Pipeline completado")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()