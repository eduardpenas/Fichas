#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Prueba Automática Simplificado - Sin Emojis para Windows
"""

import requests
import json
import os
import shutil
import time
from pathlib import Path
from datetime import datetime

# Configuración
API_BASE = "http://localhost:8000"
BASE_DIR = Path(__file__).parent
PROYECTOS_DIR = BASE_DIR / "proyectos"
INPUTS_DIR = BASE_DIR / "inputs"

class TestRunner:
    def __init__(self):
        self.results = []
        self.test_count = 0
        self.passed = 0
        self.failed = 0
        self.test_data = {
            "cliente1": "A12345678",
            "cliente2": "B87654321",
            "proyecto1": "PROJ01",
            "proyecto2": "PROJ02",
            "proyecto3": "TESTPROJ"
        }
    
    def log(self, message):
        """Log con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def test(self, name, condition, details=""):
        """Registra un test"""
        self.test_count += 1
        status = "[PASS]" if condition else "[FAIL]"
        
        self.log(f"{status} Test {self.test_count}: {name}")
        if details:
            self.log(f"   --> {details}")
        
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        
        self.results.append({"name": name, "passed": condition, "details": details})
    
    def section(self, title):
        """Imprime una sección"""
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    
    def cleanup(self):
        """Limpia datos de prueba"""
        self.log("Limpiando datos de prueba...")
        
        for cliente in [self.test_data["cliente1"], self.test_data["cliente2"]]:
            client_dir = PROYECTOS_DIR / f"Cliente_{cliente}"
            if client_dir.exists():
                shutil.rmtree(client_dir)
                self.log(f"   Eliminada carpeta: {client_dir}")
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("\n" + "="*70)
        print("  PRUEBA AUTOMATICA DEL SISTEMA FICHAS")
        print("="*70 + "\n")
        
        # Grupo 1: Conexión API
        self.test_api_connection()
        
        # Grupo 2: Clientes
        self.test_client_management()
        
        # Grupo 3: Proyectos
        self.test_project_management()
        
        # Grupo 4: Upload Anexo
        self.test_upload_anexo()
        
        # Grupo 5: Lectura de datos
        self.test_read_data()
        
        # Grupo 6: Upload CVs
        self.test_upload_cvs()
        
        # Grupo 7: Procesar CVs
        self.test_process_cvs()
        
        # Grupo 8: Validación
        self.test_validation()
        
        # Grupo 9: Generación de fichas
        self.test_generate_fichas()
        
        # Grupo 10: Estructura de carpetas
        self.test_folder_structure()
        
        # Resumen
        self.print_summary()
    
    def test_api_connection(self):
        """Test 1: Verificar conexión a API"""
        self.section("1. PRUEBA: CONEXION A API")
        
        try:
            response = requests.get(f"{API_BASE}/")
            self.test(
                "Conexion a API",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Conexion a API", False, str(e))
    
    def test_client_management(self):
        """Test 2: Gestión de clientes"""
        self.section("2. PRUEBA: GESTION DE CLIENTES")
        
        # Limpiar primero
        self.cleanup()
        
        cliente = self.test_data["cliente1"]
        
        # Listar clientes
        try:
            response = requests.get(f"{API_BASE}/clientes")
            clientes_iniciales = response.json().get("clientes", [])
            self.test(
                "Listar clientes (lista vacia)",
                len(clientes_iniciales) == 0,
                f"Encontrados {len(clientes_iniciales)} clientes"
            )
        except Exception as e:
            self.test("Listar clientes", False, str(e))
        
        # Crear cliente
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": "TEMP"}
            )
            success = response.status_code == 200
            self.test(
                f"Crear cliente {cliente}",
                success,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear cliente", False, str(e))
    
    def test_project_management(self):
        """Test 3: Gestión de proyectos"""
        self.section("3. PRUEBA: GESTION DE PROYECTOS")
        
        cliente = self.test_data["cliente1"]
        
        # Crear proyecto 1
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": self.test_data["proyecto1"]}
            )
            self.test(
                f"Crear proyecto {self.test_data['proyecto1']}",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear proyecto 1", False, str(e))
        
        # Crear proyecto 2
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": self.test_data["proyecto2"]}
            )
            self.test(
                f"Crear proyecto {self.test_data['proyecto2']}",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear proyecto 2", False, str(e))
    
    def test_upload_anexo(self):
        """Test 4: Upload de Anexo"""
        self.section("4. PRUEBA: UPLOAD DE ANEXO")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        # Buscar Excel - usar el Anexo disponible
        excel_path = INPUTS_DIR / "Anexo_II_tipo_a_.xlsx"
        
        if not excel_path.exists():
            self.test("Upload Anexo", False, f"No existe {excel_path}")
            return
        
        if not excel_path:
            self.test("Upload Anexo", False, "No existe archivo Excel")
            return
        
        try:
            with open(excel_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    f"{API_BASE}/upload-anexo",
                    files=files,
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
                )
            
            self.test(
                f"Upload Anexo a {proyecto}",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Upload Anexo", False, str(e))
    
    def test_read_data(self):
        """Test 5: Leer datos"""
        self.section("5. PRUEBA: LEER DATOS")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        # GET /personal
        try:
            response = requests.get(
                f"{API_BASE}/personal",
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            data = response.json()
            count = len(data) if isinstance(data, list) else 0
            self.test(
                "GET /personal",
                response.status_code == 200 and count > 0,
                f"Status: {response.status_code}, Registros: {count}"
            )
        except Exception as e:
            self.test("GET /personal", False, str(e))
    
    def test_upload_cvs(self):
        """Test 6: Upload de CVs"""
        self.section("6. PRUEBA: UPLOAD DE CVs")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        # Buscar PDFs
        cvs_dir = INPUTS_DIR / "cvs"
        pdfs = list(cvs_dir.glob("*.pdf"))[:3]
        
        if not pdfs:
            self.test("Upload CVs", False, f"No existen PDFs en {cvs_dir}")
            return
        
        try:
            files = [("files", open(pdf, "rb")) for pdf in pdfs]
            response = requests.post(
                f"{API_BASE}/upload-cvs",
                files=files,
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            
            for _, f in files:
                f.close()
            
            uploaded = len(response.json().get("files", []))
            self.test(
                f"Upload {len(pdfs)} CVs",
                response.status_code == 200 and uploaded == len(pdfs),
                f"Status: {response.status_code}, Cargados: {uploaded}"
            )
        except Exception as e:
            self.test("Upload CVs", False, str(e))
    
    def test_process_cvs(self):
        """Test 7: Procesar CVs"""
        self.section("7. PRUEBA: PROCESAR CVs")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        try:
            response = requests.post(
                f"{API_BASE}/process-cvs",
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            
            self.test(
                f"Procesar CVs de {proyecto}",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Procesar CVs", False, str(e))
    
    def test_validation(self):
        """Test 8: Validación"""
        self.section("8. PRUEBA: VALIDACION")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        try:
            response = requests.post(
                f"{API_BASE}/validate",
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            
            data = response.json()
            valid = data.get("exitosa", False)
            self.test(
                f"Validar datos de {proyecto}",
                response.status_code == 200,
                f"Status: {response.status_code}, Valido: {valid}"
            )
        except Exception as e:
            self.test("Validacion", False, str(e))
    
    def test_generate_fichas(self):
        """Test 9: Generación de fichas"""
        self.section("9. PRUEBA: GENERACION DE FICHAS")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        payload = {
            "cliente_nombre": "Test Cliente",
            "cliente_nif": cliente,
            "anio_fiscal": 2024
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/generate-fichas",
                json=payload,
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            
            data = response.json()
            files = data.get("files", [])
            self.test(
                f"Generar fichas de {proyecto}",
                response.status_code == 200 and len(files) >= 1,
                f"Status: {response.status_code}, Archivos: {files}"
            )
        except Exception as e:
            self.test("Generar fichas", False, str(e))
    
    def test_folder_structure(self):
        """Test 10: Estructura de carpetas"""
        self.section("10. PRUEBA: ESTRUCTURA DE CARPETAS")
        
        cliente1 = self.test_data["cliente1"]
        proyecto1 = self.test_data["proyecto1"]
        
        client_dir = PROYECTOS_DIR / f"Cliente_{cliente1}"
        project_dir = client_dir / proyecto1
        data_dir = project_dir / "data"
        
        self.test(
            f"Carpeta cliente existe",
            client_dir.exists(),
            f"Path: {client_dir}"
        )
        
        self.test(
            f"Carpeta proyecto existe",
            project_dir.exists(),
            f"Path: {project_dir}"
        )
        
        self.test(
            f"Carpeta data existe",
            data_dir.exists(),
            f"Path: {data_dir}"
        )
        
        # Verificar archivos JSON
        json_files = {
            "Excel_Personal_2.1.json": data_dir / "Excel_Personal_2.1.json",
            "Excel_Colaboraciones_2.2.json": data_dir / "Excel_Colaboraciones_2.2.json",
            "Excel_Facturas_2.2.json": data_dir / "Excel_Facturas_2.2.json"
        }
        
        for name, path in json_files.items():
            self.test(
                f"Archivo {name} existe",
                path.exists(),
                f"Path: {path}"
            )
    
    def print_summary(self):
        """Imprime resumen de pruebas"""
        self.section("RESUMEN DE PRUEBAS")
        
        print(f"Total de tests: {self.test_count}")
        print(f"[PASS] Pasados: {self.passed}")
        print(f"[FAIL] Fallidos: {self.failed}\n")
        
        percentage = (self.passed / self.test_count * 100) if self.test_count > 0 else 0
        
        print(f"Tasa de exito: {percentage:.1f}%\n")
        
        if self.failed > 0:
            print("Detalles de fallos:")
            for result in self.results:
                if not result["passed"]:
                    print(f"  [FAIL] {result['name']}")
                    if result['details']:
                        print(f"         {result['details']}")

def main():
    runner = TestRunner()
    
    try:
        runner.run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrumpido por usuario\n")
        runner.print_summary()
    except Exception as e:
        print(f"\nError fatal: {e}\n")
        runner.print_summary()

if __name__ == "__main__":
    main()
