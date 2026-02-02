import React, { useState } from 'react';
import { apiService } from '../api/client';

interface ActionsPanelProps {
  onSuccess: (message: string) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
  onValidationResult?: (result: any) => void;
}

export const ActionsPanel: React.FC<ActionsPanelProps> = ({
  onSuccess,
  onError,
  onLoading,
  onValidationResult,
}) => {
  const [validationResult, setValidationResult] = useState<any>(null);

  const handleProcessCVs = async () => {
    try {
      onLoading(true);
      const response = await apiService.processCVs();
      onSuccess(`✅ CVs procesados: ${response.data.message}`);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleValidate = async () => {
    try {
      onLoading(true);
      const response = await apiService.validate();
      setValidationResult(response.data);
      onValidationResult?.(response.data);

      const resumen = response.data.resumen;
      if (response.data.exitosa) {
        onSuccess('✅ Validación exitosa - Todos los datos son correctos');
      } else {
        const errores = resumen.personal?.errores_count || 0;
        const advertencias = resumen.personal?.advertencias_count || 0;
        onError(
          `⚠️ Validación completada: ${errores} error(es), ${advertencias} advertencia(s)`
        );
      }
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleGenerateFichas = async () => {
    try {
      onLoading(true);
      const response = await apiService.generateFichas();
      onSuccess(`✅ Fichas generadas: ${response.data.message}`);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="card mb-6">
      <h2 className="text-2xl font-bold mb-4">⚙️ Acciones</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <button
          onClick={handleProcessCVs}
          className="btn-secondary text-lg py-3"
        >
          🔍 Procesar CVs
        </button>
        <button
          onClick={handleValidate}
          className="btn-primary text-lg py-3"
        >
          ✅ Validar Datos
        </button>
        <button
          onClick={handleGenerateFichas}
          className="btn-primary text-lg py-3"
        >
          📄 Generar Fichas
        </button>
      </div>

      {validationResult && (
        <div className="bg-gray-100 p-4 rounded-lg">
          <h3 className="font-bold mb-2">📊 Resultado de Validación</h3>

          {/* Resumen general */}
          <div className={`p-3 rounded mb-3 ${
            validationResult.exitosa
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          }`}>
            {validationResult.resumen?.mensaje_general || 'Validación completada'}
          </div>

          {/* Personal */}
          {validationResult.resumen?.personal && (
            <div className="mb-3">
              <h4 className="font-semibold">Personal:</h4>
              <p className="text-sm">
                Errores: {validationResult.resumen.personal.errores_count} | 
                Advertencias: {validationResult.resumen.personal.advertencias_count}
              </p>
              {validationResult.resumen.personal.errores?.length > 0 && (
                <ul className="text-sm text-red-600 ml-4">
                  {validationResult.resumen.personal.errores.slice(0, 3).map((err: string, idx: number) => (
                    <li key={idx}>• {err}</li>
                  ))}
                </ul>
              )}
            </div>
          )}

          {/* Colaboraciones */}
          {validationResult.resumen?.colaboraciones && (
            <div>
              <h4 className="font-semibold">Colaboraciones:</h4>
              <p className="text-sm">
                Errores: {validationResult.resumen.colaboraciones.errores_count} | 
                Advertencias: {validationResult.resumen.colaboraciones.advertencias_count}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ActionsPanel;
