#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Prueba Automática del Sistema Fichas
Prueba todas las casuísticas del sistema
"""

import requests
import json
import os
import shutil
import time
from pathlib import Path
from datetime import datetime
import sys
import io

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuración
API_BASE = "http://localhost:8000"
BASE_DIR = Path(__file__).parent
PROYECTOS_DIR = BASE_DIR / "proyectos"
INPUTS_DIR = BASE_DIR / "inputs"

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

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
    
    def log(self, message, level="INFO"):
        """Log con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}]"
        print(f"{prefix} {message}")
    
    def test(self, name, condition, details=""):
        """Registra un test"""
        self.test_count += 1
        status = "✅ PASS" if condition else "❌ FAIL"
        color = Colors.GREEN if condition else Colors.RED
        
        self.log(f"{color}{status}{Colors.RESET} Test {self.test_count}: {name}")
        if details:
            self.log(f"   └─ {details}")
        
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        
        self.results.append({"name": name, "passed": condition, "details": details})
    
    def section(self, title):
        """Imprime una sección"""
        print(f"\n{Colors.BLUE}{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}{Colors.RESET}\n")
    
    def cleanup(self):
        """Limpia datos de prueba"""
        self.log("Limpiando datos de prueba...", level="CLEANUP")
        
        for cliente in [self.test_data["cliente1"], self.test_data["cliente2"]]:
            client_dir = PROYECTOS_DIR / f"Cliente_{cliente}"
            if client_dir.exists():
                shutil.rmtree(client_dir)
                self.log(f"   Eliminada carpeta: {client_dir}")
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"  🧪 PRUEBA AUTOMÁTICA DEL SISTEMA FICHAS")
        print(f"{'='*70}{Colors.RESET}\n")
        
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
        
        # Grupo 10: Multi-proyecto
        self.test_multiproject()
        
        # Grupo 11: Casos edge
        self.test_edge_cases()
        
        # Grupo 12: Estructura de carpetas
        self.test_folder_structure()
        
        # Resumen
        self.print_summary()
    
    def test_api_connection(self):
        """Test 1: Verificar conexión a API"""
        self.section("1️⃣  PRUEBA: CONEXIÓN A API")
        
        try:
            response = requests.get(f"{API_BASE}/")
            self.test(
                "Conexión a API",
                response.status_code == 200,
                f"Status: {response.status_code}, Mensaje: {response.json().get('mensaje', '')}"
            )
        except Exception as e:
            self.test("Conexión a API", False, str(e))
    
    def test_client_management(self):
        """Test 2: Gestión de clientes"""
        self.section("2️⃣  PRUEBA: GESTIÓN DE CLIENTES")
        
        # Limpiar primero
        self.cleanup()
        
        # Listar clientes (debe estar vacío)
        try:
            response = requests.get(f"{API_BASE}/clientes")
            clientes_iniciales = response.json().get("clientes", [])
            self.test(
                "Listar clientes (lista vacía)",
                len(clientes_iniciales) == 0,
                f"Encontrados {len(clientes_iniciales)} clientes"
            )
        except Exception as e:
            self.test("Listar clientes", False, str(e))
        
        # Crear cliente 1
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{self.test_data['cliente1']}/proyectos",
                params={"proyecto_acronimo": "TEMP"}
            )
            success = response.status_code == 200
            self.test(
                f"Crear cliente {self.test_data['cliente1']}",
                success,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear cliente 1", False, str(e))
        
        # Listar clientes nuevamente
        try:
            response = requests.get(f"{API_BASE}/clientes")
            clientes = response.json().get("clientes", [])
            self.test(
                "Listar clientes (1 cliente)",
                len(clientes) >= 1,
                f"Encontrados {len(clientes)} clientes"
            )
        except Exception as e:
            self.test("Listar clientes", False, str(e))
    
    def test_project_management(self):
        """Test 3: Gestión de proyectos"""
        self.section("3️⃣  PRUEBA: GESTIÓN DE PROYECTOS")
        
        cliente = self.test_data["cliente1"]
        
        # Crear proyecto 1
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": self.test_data["proyecto1"]}
            )
            success = response.status_code == 200
            self.test(
                f"Crear proyecto {self.test_data['proyecto1']}",
                success,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear proyecto 1", False, str(e))
        
        # Listar proyectos
        try:
            response = requests.get(f"{API_BASE}/clientes/{cliente}/proyectos")
            proyectos = response.json().get("proyectos", [])
            self.test(
                f"Listar proyectos de {cliente}",
                len(proyectos) >= 1,
                f"Encontrados {len(proyectos)} proyectos"
            )
        except Exception as e:
            self.test("Listar proyectos", False, str(e))
        
        # Crear proyecto 2
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": self.test_data["proyecto2"]}
            )
            success = response.status_code == 200
            self.test(
                f"Crear proyecto {self.test_data['proyecto2']}",
                success,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear proyecto 2", False, str(e))
    
    def test_upload_anexo(self):
        """Test 4: Upload de Anexo"""
        self.section("4️⃣  PRUEBA: UPLOAD DE ANEXO")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        # Verificar que existe un Excel de prueba
        excel_path = INPUTS_DIR / "Anexo_Test.xlsx"
        if not excel_path.exists():
            # Usar el primero disponible
            excels = list(INPUTS_DIR.glob("Excel_*.xlsx"))
            if excels:
                excel_path = excels[0]
        
        if not excel_path.exists():
            self.test("Upload Anexo", False, f"No existe archivo: {excel_path}")
            return
        
        try:
            with open(excel_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    f"{API_BASE}/upload-anexo",
                    files=files,
                    params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
                )
            
            success = response.status_code == 200
            self.test(
                f"Upload Anexo a {proyecto}",
                success,
                f"Status: {response.status_code}, {response.json().get('message', '')}"
            )
        except Exception as e:
            self.test("Upload Anexo", False, str(e))
    
    def test_read_data(self):
        """Test 5: Leer datos"""
        self.section("5️⃣  PRUEBA: LEER DATOS")
        
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
        
        # GET /colaboraciones
        try:
            response = requests.get(
                f"{API_BASE}/colaboraciones",
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            data = response.json()
            count = len(data) if isinstance(data, list) else 0
            self.test(
                "GET /colaboraciones",
                response.status_code == 200,
                f"Status: {response.status_code}, Registros: {count}"
            )
        except Exception as e:
            self.test("GET /colaboraciones", False, str(e))
        
        # GET /facturas
        try:
            response = requests.get(
                f"{API_BASE}/facturas",
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            data = response.json()
            count = len(data) if isinstance(data, list) else 0
            self.test(
                "GET /facturas",
                response.status_code == 200,
                f"Status: {response.status_code}, Registros: {count}"
            )
        except Exception as e:
            self.test("GET /facturas", False, str(e))
    
    def test_upload_cvs(self):
        """Test 6: Upload de CVs"""
        self.section("6️⃣  PRUEBA: UPLOAD DE CVs")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        # Buscar PDFs de prueba
        cvs_dir = INPUTS_DIR / "cvs"
        pdfs = list(cvs_dir.glob("*.pdf"))[:3]  # Tomar primeros 3
        
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
            
            # Cerrar archivos
            for _, f in files:
                f.close()
            
            success = response.status_code == 200
            uploaded = len(response.json().get("files", []))
            self.test(
                f"Upload {len(pdfs)} CVs",
                success and uploaded == len(pdfs),
                f"Status: {response.status_code}, Cargados: {uploaded}"
            )
        except Exception as e:
            self.test("Upload CVs", False, str(e))
    
    def test_process_cvs(self):
        """Test 7: Procesar CVs"""
        self.section("7️⃣  PRUEBA: PROCESAR CVs")
        
        cliente = self.test_data["cliente1"]
        proyecto = self.test_data["proyecto1"]
        
        try:
            response = requests.post(
                f"{API_BASE}/process-cvs",
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto}
            )
            
            success = response.status_code == 200
            self.test(
                f"Procesar CVs de {proyecto}",
                success,
                f"Status: {response.status_code}, {response.json().get('message', '')}"
            )
        except Exception as e:
            self.test("Procesar CVs", False, str(e))
    
    def test_validation(self):
        """Test 8: Validación"""
        self.section("8️⃣  PRUEBA: VALIDACIÓN")
        
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
                f"Status: {response.status_code}, Válido: {valid}"
            )
        except Exception as e:
            self.test("Validación", False, str(e))
    
    def test_generate_fichas(self):
        """Test 9: Generación de fichas"""
        self.section("9️⃣  PRUEBA: GENERACIÓN DE FICHAS")
        
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
    
    def test_multiproject(self):
        """Test 10: Multi-proyecto"""
        self.section("🔟 PRUEBA: MULTI-PROYECTO")
        
        cliente = self.test_data["cliente1"]
        proyecto2 = self.test_data["proyecto2"]
        
        # Crear proyecto 3
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": self.test_data["proyecto3"]}
            )
            self.test(
                f"Crear proyecto {self.test_data['proyecto3']}",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear proyecto 3", False, str(e))
        
        # Verificar que existen 3 proyectos
        try:
            response = requests.get(f"{API_BASE}/clientes/{cliente}/proyectos")
            proyectos = response.json().get("proyectos", [])
            self.test(
                f"Verificar 3 proyectos en {cliente}",
                len(proyectos) >= 3,
                f"Encontrados {len(proyectos)} proyectos"
            )
        except Exception as e:
            self.test("Verificar proyectos", False, str(e))
    
    def test_edge_cases(self):
        """Test 11: Casos edge"""
        self.section("1️⃣1️⃣  PRUEBA: CASOS EDGE")
        
        cliente = self.test_data["cliente1"]
        
        # Intentar crear proyecto duplicado
        try:
            response = requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": self.test_data["proyecto1"]}
            )
            # No debería error, solo crear carpeta vacía
            self.test(
                "Crear proyecto duplicado",
                response.status_code in [200, 400],
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.test("Crear proyecto duplicado", False, str(e))
        
        # Leer datos de proyecto sin Anexo
        proyecto_sin_anexo = "EMPTY_PROJ"
        try:
            requests.post(
                f"{API_BASE}/clientes/{cliente}/proyectos",
                params={"proyecto_acronimo": proyecto_sin_anexo}
            )
            
            response = requests.get(
                f"{API_BASE}/personal",
                params={"cliente_nif": cliente, "proyecto_acronimo": proyecto_sin_anexo}
            )
            
            data = response.json()
            empty = len(data) == 0
            self.test(
                "Leer datos proyecto sin Anexo",
                response.status_code == 200 and empty,
                f"Status: {response.status_code}, Registros: {len(data)}"
            )
        except Exception as e:
            self.test("Leer datos sin Anexo", False, str(e))
    
    def test_folder_structure(self):
        """Test 12: Estructura de carpetas"""
        self.section("1️⃣2️⃣  PRUEBA: ESTRUCTURA DE CARPETAS")
        
        cliente1 = self.test_data["cliente1"]
        proyecto1 = self.test_data["proyecto1"]
        
        # Verificar estructura
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
        self.section("📊 RESUMEN DE PRUEBAS")
        
        print(f"Total de tests: {self.test_count}")
        print(f"{Colors.GREEN}✅ Pasados: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}❌ Fallidos: {self.failed}{Colors.RESET}\n")
        
        percentage = (self.passed / self.test_count * 100) if self.test_count > 0 else 0
        
        if percentage == 100:
            status = f"{Colors.GREEN}✅ EXITO TOTAL{Colors.RESET}"
        elif percentage >= 80:
            status = f"{Colors.YELLOW}⚠️  MAYORÍA PASÓ{Colors.RESET}"
        else:
            status = f"{Colors.RED}❌ FALLOS CRÍTICOS{Colors.RESET}"
        
        print(f"Tasa de éxito: {percentage:.1f}% {status}\n")
        
        print(f"{Colors.CYAN}Detalles de fallos:{Colors.RESET}")
        for result in self.results:
            if not result["passed"]:
                print(f"  ❌ {result['name']}")
                if result['details']:
                    print(f"     └─ {result['details']}")

def main():
    runner = TestRunner()
    
    try:
        runner.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrumpido por usuario{Colors.RESET}\n")
        runner.print_summary()
    except Exception as e:
        print(f"\n{Colors.RED}Error fatal: {e}{Colors.RESET}\n")
        runner.print_summary()

if __name__ == "__main__":
    main()
