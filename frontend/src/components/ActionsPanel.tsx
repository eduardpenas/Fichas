import React, { useState, useRef } from 'react';
import { apiService } from '../api/client';
import * as docx from 'docx-preview';
import DataEditor from './DataEditor';

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
  const [clienteNombre, setClienteNombre] = useState<string>('');
  const [clienteNIF, setClienteNIF] = useState<string>('');
  const [anioFiscal, setAnioFiscal] = useState<string>(new Date().getFullYear().toString());
  const [generatedFiles, setGeneratedFiles] = useState<string[]>([]);
  const [previewHtml, setPreviewHtml] = useState<string | null>(null);
  const [previewDocx, setPreviewDocx] = useState<boolean>(false);
  const [generationProgress, setGenerationProgress] = useState<number>(0);
  const [downloadProgress, setDownloadProgress] = useState<number>(0);
  const [showDataEditor, setShowDataEditor] = useState<'personal' | 'colaboraciones' | 'facturas' | null>(null);
  const previewContainerRef = useRef<HTMLDivElement>(null);
  
  const validateNIF = (nif: string) => {
    if (!nif) return true;
    const s = nif.trim().toUpperCase();
    // DNI/NIE basic patterns and CIF-like pattern (approximate)
    const dniRe = /^[0-9]{8}[A-Z]$/;
    const nieRe = /^[XYZ][0-9]{7}[A-Z]$/;
    const cifRe = /^[A-HJ-NP-SUVW][0-9]{7}[0-9A-Z]$/;
    return dniRe.test(s) || nieRe.test(s) || cifRe.test(s);
  };

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
      if (clienteNIF && !validateNIF(clienteNIF)) {
        onError('❌ NIF inválido');
        return;
      }

      onLoading(true);
      setGenerationProgress(2);
      // animate progress up to 85%
      const interval = setInterval(() => {
        setGenerationProgress((p) => {
          if (p >= 85) return p;
          return p + Math.floor(Math.random() * 6) + 1;
        });
      }, 700);

      const payload = {
        cliente_nombre: clienteNombre || undefined,
        cliente_nif: clienteNIF || undefined,
        anio_fiscal: anioFiscal ? parseInt(anioFiscal) : undefined,
      };
      const response = await apiService.generateFichas(payload);
      clearInterval(interval);
      setGenerationProgress(95);
      onSuccess(`✅ Fichas generadas: ${response.data.message}`);
      if (response.data.files && Array.isArray(response.data.files)) {
        setGeneratedFiles(response.data.files);
      }
      setGenerationProgress(100);
      setTimeout(() => setGenerationProgress(0), 800);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
      setGenerationProgress(0);
    } finally {
      onLoading(false);
    }
  };

  const handleDownloadFicha = async (name: string) => {
    try {
      onLoading(true);
      const response = await apiService.downloadFicha(name);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', name);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);
      onSuccess(`✅ ${name} descargado`);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handlePreviewFicha = async (name: string) => {
    try {
      onLoading(true);
      const response = await apiService.previewFichaDocx(name);
      setPreviewHtml(null);
      setPreviewDocx(true);
      
      // Renderizar el documento después de que el modal esté visible
      setTimeout(() => {
        if (previewContainerRef.current) {
          docx.renderAsync(response.data, previewContainerRef.current)
            .then(() => {
              console.log('✅ Documento renderizado correctamente');
            })
            .catch((err: any) => {
              console.error('Error renderizando docx:', err);
              onError(`❌ Error al renderizar: ${err.message}`);
            });
        }
      }, 100);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleDownloadFichas = async () => {
    try {
      onLoading(true);
      setDownloadProgress(0);
      const response = await apiService.downloadFichas((pct:number) => setDownloadProgress(pct));
      
      // Crear un blob y descargarlo
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'fichas.zip');
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      onSuccess('✅ Fichas descargadas correctamente');
      setTimeout(() => setDownloadProgress(0), 600);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
      setDownloadProgress(0);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="card mb-6">
      <h2 className="text-2xl font-bold mb-4">⚙️ Acciones</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Entidad solicitante (Razón social)</label>
          <input
            value={clienteNombre}
            onChange={(e) => setClienteNombre(e.target.value)}
            placeholder="Nombre del cliente"
            className="input mt-1 w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">NIF Cliente</label>
          <input
            value={clienteNIF}
            onChange={(e) => setClienteNIF(e.target.value)}
            placeholder="NIF"
            className="input mt-1 w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Año Fiscal</label>
          <input
            type="number"
            value={anioFiscal}
            onChange={(e) => setAnioFiscal(e.target.value)}
            placeholder="2024"
            min="2000"
            max="2099"
            className="input mt-1 w-full"
          />
        </div>
      </div>

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
          className={`btn-primary text-lg py-3 ${clienteNIF && !validateNIF(clienteNIF) ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={!!(clienteNIF && !validateNIF(clienteNIF))}
        >
          📄 Generar Fichas
        </button>
      </div>

      <div className="mb-6">
        <button
          onClick={handleDownloadFichas}
          className="btn-success text-lg py-3 w-full"
        >
          ⬇️ Descargar Fichas (ZIP)
        </button>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3">📋 Editar Datos Antes de Generar</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={() => setShowDataEditor('personal')}
            className="btn-secondary text-sm py-2"
          >
            ✏️ Personal (Ficha 2.1)
          </button>
          <button
            onClick={() => setShowDataEditor('colaboraciones')}
            className="btn-secondary text-sm py-2"
          >
            ✏️ Colaboraciones (Ficha 2.2)
          </button>
          <button
            onClick={() => setShowDataEditor('facturas')}
            className="btn-secondary text-sm py-2"
          >
            ✏️ Facturas (Ficha 2.2)
          </button>
        </div>
      </div>

      {(generationProgress > 0) && (
        <div className="w-full bg-gray-200 rounded mt-2 h-3">
          <div className="bg-green-500 h-3 rounded" style={{ width: `${generationProgress}%` }} />
        </div>
      )}

      {(downloadProgress > 0) && (
        <div className="w-full bg-gray-200 rounded mt-2 h-3">
          <div className="bg-blue-500 h-3 rounded" style={{ width: `${downloadProgress}%` }} />
        </div>
      )}

      {generatedFiles.length > 0 && (
        <div className="mb-6 bg-white p-4 rounded shadow-sm">
          <h3 className="font-semibold mb-2">Descargas individuales</h3>
          <ul className="space-y-2">
            {generatedFiles.map((f) => (
              <li key={f} className="flex gap-2 items-center">
                <span className="flex-1">{f}</span>
                <button onClick={() => handlePreviewFicha(f)} className="btn-secondary btn-sm mr-2">🔎 Previsualizar</button>
                <button onClick={() => handleDownloadFicha(f)} className="btn-primary btn-sm">⬇️ Descargar</button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {previewHtml && (
        <div className="fixed inset-0 z-50 flex items-start justify-center p-8 bg-black/50">
          <div className="bg-white rounded-lg shadow-lg max-w-3xl w-full max-h-[80vh] overflow-auto">
            <div className="p-4 border-b flex justify-between items-center bg-gray-50">
              <h4 className="font-bold">Previsualización (HTML)</h4>
              <button onClick={() => { setPreviewHtml(null); setPreviewDocx(false); }} className="text-lg hover:text-red-500">✕</button>
            </div>
            <div className="p-4" dangerouslySetInnerHTML={{ __html: previewHtml }} />
          </div>
        </div>
      )}

      {previewDocx && (
        <div className="fixed inset-0 z-50 flex items-start justify-center p-8 bg-black/50">
          <div className="bg-white rounded-lg shadow-lg max-w-4xl w-full max-h-[80vh] overflow-auto">
            <div className="p-4 border-b flex justify-between items-center bg-gray-50">
              <h4 className="font-bold">Previsualización Documento</h4>
              <button onClick={() => { setPreviewDocx(false); setPreviewHtml(null); }} className="text-lg hover:text-red-500">✕</button>
            </div>
            <div ref={previewContainerRef} className="p-4" />
          </div>
        </div>
      )}

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

      {showDataEditor && (
        <DataEditor
          dataType={showDataEditor}
          onSuccess={onSuccess}
          onError={onError}
          onLoading={onLoading}
          onClose={() => setShowDataEditor(null)}
          clienteNif={clienteNIF}
        />
      )}
    </div>
  );
};

export default ActionsPanel;
