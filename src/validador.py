"""
Módulo de validación automática para fichas.
Detecta inconsistencias, datos faltantes y formatos inválidos.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple


class ValidadorFichas:
    """Valida datos de personal y colaboraciones antes de generar fichas."""
    
    def __init__(self):
        self.errores = []
        self.advertencias = []
        self.info = []
    
    def limpiar(self):
        """Reinicia los contadores de validación."""
        self.errores = []
        self.advertencias = []
        self.info = []
    
    def validar_personal(self, df_personal: pd.DataFrame) -> bool:
        """
        Valida el DataFrame de Personal (Ficha 2.1).
        Retorna True si está OK, False si hay errores críticos.
        """
        self.limpiar()
        
        if df_personal.empty:
            self.errores.append("❌ [CRÍTICO] El DataFrame de Personal está vacío")
            return False
        
        print(f"\n🔍 Validando {len(df_personal)} registros de Personal...\n")
        
        # Validaciones generales
        self._validar_campos_obligatorios(df_personal, "personal")
        self._validar_formatos_personal(df_personal)
        self._validar_consistencia_costes(df_personal)
        self._validar_duplicados(df_personal, "Nombre", "Apellidos")
        self._validar_experiencia_laboral(df_personal)
        
        # Mostrar resultados
        self._mostrar_reporte()
        
        # Retorna False solo si hay errores críticos
        return len(self.errores) == 0
    
    def validar_colaboraciones(self, df_colab: pd.DataFrame, df_facturas: pd.DataFrame) -> bool:
        """
        Valida DataFrames de Colaboraciones y Facturas (Ficha 2.2).
        Retorna True si está OK, False si hay errores críticos.
        """
        self.limpiar()
        
        if df_colab.empty:
            self.errores.append("❌ [CRÍTICO] El DataFrame de Colaboraciones está vacío")
            return False
        
        if df_facturas.empty:
            self.errores.append("❌ [CRÍTICO] El DataFrame de Facturas está vacío")
            return False
        
        print(f"\n🔍 Validando {len(df_colab)} colaboraciones y {len(df_facturas)} facturas...\n")
        
        # Validaciones generales
        self._validar_campos_obligatorios(df_colab, "colaboraciones")
        self._validar_campos_obligatorios(df_facturas, "facturas")
        self._validar_nif(df_colab)
        self._validar_duplicados(df_colab, "Razón social")
        self._validar_consistencia_facturas(df_colab, df_facturas)
        
        # Mostrar resultados
        self._mostrar_reporte()
        
        return len(self.errores) == 0
    
    # ==========================================
    # VALIDACIONES ESPECÍFICAS
    # ==========================================
    
    def _validar_campos_obligatorios(self, df: pd.DataFrame, tipo: str):
        """Verifica que los campos requeridos no estén vacíos."""
        
        campos_obligatorios = {
            "personal": ["Nombre", "Apellidos", "Titulación 1", "Coste horario (€/hora)", "Horas totales"],
            "colaboraciones": ["Razón social", "NIF", "País de la entidad"],
            "facturas": ["Entidad", "Nombre factura", "Importe (€)"]
        }
        
        requeridos = campos_obligatorios.get(tipo, [])
        
        for idx, row in df.iterrows():
            fila_num = idx + 1
            for campo in requeridos:
                if campo not in df.columns:
                    continue
                
                val = row[campo]
                # Consideramos vacío: NaN, cadena vacía, None
                if pd.isna(val) or (isinstance(val, str) and val.strip() == ""):
                    self.errores.append(
                        f"❌ Fila {fila_num}: Campo '{campo}' está vacío (obligatorio)"
                    )
    
    def _validar_formatos_personal(self, df: pd.DataFrame):
        """Valida formatos en datos de Personal."""
        
        for idx, row in df.iterrows():
            fila_num = idx + 1
            
            # Validar nombre y apellidos (no números)
            nombre = str(row.get("Nombre", ""))
            apellidos = str(row.get("Apellidos", ""))
            
            if nombre and re.search(r'\d', nombre):
                self.advertencias.append(
                    f"⚠️ Fila {fila_num}: Nombre contiene números: '{nombre}'"
                )
            
            if apellidos and re.search(r'\d', apellidos):
                self.advertencias.append(
                    f"⚠️ Fila {fila_num}: Apellidos contienen números: '{apellidos}'"
                )
            
            # Validar coste horario > 0
            try:
                coste_horario = float(row.get("Coste horario (€/hora)", 0))
                if coste_horario <= 0:
                    self.errores.append(
                        f"❌ Fila {fila_num}: Coste horario debe ser > 0, se encontró: {coste_horario}"
                    )
            except (ValueError, TypeError):
                self.errores.append(
                    f"❌ Fila {fila_num}: Coste horario no es un número válido"
                )
            
            # Validar horas totales > 0
            try:
                horas = float(row.get("Horas totales", 0))
                if horas <= 0:
                    self.errores.append(
                        f"❌ Fila {fila_num}: Horas totales debe ser > 0, se encontró: {horas}"
                    )
            except (ValueError, TypeError):
                self.errores.append(
                    f"❌ Fila {fila_num}: Horas totales no es un número válido"
                )
    
    def _validar_consistencia_costes(self, df: pd.DataFrame):
        """Verifica que Coste total ≈ Coste horario × Horas totales."""
        
        for idx, row in df.iterrows():
            fila_num = idx + 1
            
            try:
                coste_horario = float(row.get("Coste horario (€/hora)", 0))
                horas = float(row.get("Horas totales", 0))
                coste_total = float(row.get("Coste total (€)", 0))
                
                if horas > 0 and coste_horario > 0:
                    coste_calculado = coste_horario * horas
                    diferencia_pct = abs(coste_total - coste_calculado) / coste_calculado * 100
                    
                    if diferencia_pct > 1:  # Tolerancia del 1%
                        self.advertencias.append(
                            f"⚠️ Fila {fila_num}: Inconsistencia en costes. "
                            f"Coste total ({coste_total}€) ≠ {coste_horario}€/h × {horas}h = {coste_calculado}€ "
                            f"(diferencia: {diferencia_pct:.1f}%)"
                        )
            except (ValueError, TypeError):
                pass
    
    def _validar_duplicados(self, df: pd.DataFrame, *columnas):
        """Detecta duplicados en las columnas especificadas."""
        
        if len(columnas) == 1:
            duplicados = df[df.duplicated(subset=columnas, keep=False)]
            if not duplicados.empty:
                for idx, row in duplicados.iterrows():
                    val = row[columnas[0]]
                    self.advertencias.append(
                        f"⚠️ Fila {idx + 1}: '{val}' está duplicado en el listado"
                    )
        else:
            duplicados = df[df.duplicated(subset=list(columnas), keep=False)]
            if not duplicados.empty:
                self.advertencias.append(
                    f"⚠️ Se encontraron {len(duplicados)} registros duplicados "
                    f"por {', '.join(columnas)}"
                )
    
    def _validar_experiencia_laboral(self, df: pd.DataFrame):
        """Valida que al menos haya experiencia laboral documentada."""
        
        personas_sin_experiencia = 0
        
        for idx, row in df.iterrows():
            empresa1 = str(row.get("EMPRESA 1", "")).strip()
            
            if not empresa1:
                personas_sin_experiencia += 1
        
        if personas_sin_experiencia > 0:
            self.advertencias.append(
                f"⚠️ {personas_sin_experiencia} persona(s) sin experiencia laboral documentada "
                f"(EMPRESA 1 vacío). Considera procesar sus CVs."
            )
    
    def _validar_nif(self, df: pd.DataFrame):
        """Valida formato de NIF."""
        
        patron_nif = r'^[A-Z0-9]{8,9}$'
        
        for idx, row in df.iterrows():
            nif = str(row.get("NIF", "")).strip().upper()
            
            if nif and not re.match(patron_nif, nif):
                self.advertencias.append(
                    f"⚠️ Fila {idx + 1}: NIF con formato sospechoso: '{nif}' "
                    f"(esperado: 8-9 caracteres alfanuméricos)"
                )
    
    def _validar_consistencia_facturas(self, df_colab: pd.DataFrame, df_facturas: pd.DataFrame):
        """Verifica que todas las facturas tengan una colaboración asociada."""
        
        entidades_colab = set(df_colab["Razón social"].unique())
        entidades_fact = set(df_facturas["Entidad"].unique())
        
        facturas_sin_colab = entidades_fact - entidades_colab
        
        if facturas_sin_colab:
            self.advertencias.append(
                f"⚠️ Hay {len(facturas_sin_colab)} factura(s) sin colaboración asociada: "
                f"{', '.join(list(facturas_sin_colab)[:3])}{'...' if len(facturas_sin_colab) > 3 else ''}"
            )
        
        # Validar importes > 0
        for idx, row in df_facturas.iterrows():
            try:
                importe = float(row.get("Importe (€)", 0))
                if importe <= 0:
                    self.errores.append(
                        f"❌ Fila {idx + 1} (Facturas): Importe debe ser > 0, se encontró: {importe}"
                    )
            except (ValueError, TypeError):
                self.errores.append(
                    f"❌ Fila {idx + 1} (Facturas): Importe no es un número válido"
                )
    
    # ==========================================
    # REPORTE Y PRESENTACIÓN
    # ==========================================
    
    def _mostrar_reporte(self):
        """Muestra un reporte visual de validaciones."""
        
        print("\n" + "="*70)
        print("📋 REPORTE DE VALIDACIÓN")
        print("="*70)
        
        # Errores críticos
        if self.errores:
            print(f"\n❌ ERRORES CRÍTICOS ({len(self.errores)}):")
            print("-" * 70)
            for i, error in enumerate(self.errores[:10], 1):  # Mostrar primeros 10
                print(f"  {i}. {error}")
            if len(self.errores) > 10:
                print(f"  ... y {len(self.errores) - 10} error(es) más")
        
        # Advertencias
        if self.advertencias:
            print(f"\n⚠️ ADVERTENCIAS ({len(self.advertencias)}):")
            print("-" * 70)
            for i, advertencia in enumerate(self.advertencias[:10], 1):
                print(f"  {i}. {advertencia}")
            if len(self.advertencias) > 10:
                print(f"  ... y {len(self.advertencias) - 10} advertencia(s) más")
        
        # Resumen
        print("\n" + "-" * 70)
        if not self.errores and not self.advertencias:
            print("✅ VALIDACIÓN EXITOSA: Todos los datos están correctos")
        elif not self.errores:
            print(f"✅ OK PARA PROCESAR (con {len(self.advertencias)} advertencia(s) menor(es))")
        else:
            print(f"❌ NO SE PUEDE PROCESAR: Hay {len(self.errores)} error(es) crítico(s)")
        
        print("=" * 70 + "\n")
    
    def obtener_resumen(self) -> Dict:
        """Retorna un resumen de validación en formato diccionario."""
        return {
            "exitosa": len(self.errores) == 0,
            "errores_count": len(self.errores),
            "advertencias_count": len(self.advertencias),
            "errores": self.errores[:20],  # Primeros 20
            "advertencias": self.advertencias[:20],  # Primeros 20
            "mensaje": self._generar_mensaje_resumido()
        }
    
    def _generar_mensaje_resumido(self) -> str:
        """Genera un mensaje resumido de validación."""
        if not self.errores and not self.advertencias:
            return "✅ Todos los datos son válidos"
        
        msg_parts = []
        if self.errores:
            msg_parts.append(f"❌ {len(self.errores)} error(es)")
        if self.advertencias:
            msg_parts.append(f"⚠️ {len(self.advertencias)} advertencia(s)")
        
        return " | ".join(msg_parts)


# ==========================================
# FUNCIONES AUXILIARES GLOBALES
# ==========================================

def validar_antes_generar(ruta_personal, ruta_colaboraciones, ruta_facturas) -> Tuple[bool, Dict]:
    """
    Valida todos los archivos antes de generar fichas.
    Retorna (es_valido, resumen_validacion).
    """
    import os
    validador = ValidadorFichas()
    
    try:
        # Detectar formato
        _, ext_p = os.path.splitext(ruta_personal)
        df_personal = pd.read_json(ruta_personal) if ext_p.lower() == '.json' else pd.read_excel(ruta_personal)
        
        _, ext_c = os.path.splitext(ruta_colaboraciones)
        df_colab = pd.read_json(ruta_colaboraciones) if ext_c.lower() == '.json' else pd.read_excel(ruta_colaboraciones)
        
        _, ext_f = os.path.splitext(ruta_facturas)
        df_facturas = pd.read_json(ruta_facturas) if ext_f.lower() == '.json' else pd.read_excel(ruta_facturas)
        
    except Exception as e:
        return False, {
            "exitosa": False,
            "errores_count": 1,
            "advertencias_count": 0,
            "errores": [f"Error al cargar archivos: {str(e)}"],
            "advertencias": [],
            "mensaje": f"❌ Error: {str(e)}"
        }
    
    # Validar personal
    valido_personal = validador.validar_personal(df_personal)
    resumen_personal = validador.obtener_resumen()
    
    # Validar colaboraciones
    valido_colab = validador.validar_colaboraciones(df_colab, df_facturas)
    resumen_colab = validador.obtener_resumen()
    
    # Resumen combinado
    resumen_final = {
        "exitosa": valido_personal and valido_colab,
        "personal": resumen_personal,
        "colaboraciones": resumen_colab,
        "mensaje_general": "✅ LISTO PARA GENERAR FICHAS" if (valido_personal and valido_colab) else "❌ Corrija los errores antes de continuar"
    }
    
    return valido_personal and valido_colab, resumen_final
