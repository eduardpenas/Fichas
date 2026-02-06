import React, { useState, useRef, useEffect } from 'react';
import { apiService } from '../api/client';
import * as docx from 'docx-preview';
import DataEditor from './DataEditor';

interface ActionsPanelProps {
  clienteNif?: string | null;
  clienteNombre?: string | null;
  proyectoAcronimo?: string | null;
  refreshTrigger?: number; // Se usa para forzar refresh desde el padre
  extractedMetadata?: any; // Metadatos extraídos del Anexo (año fiscal, NIF, entidad)
  onSuccess: (message: string) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
  onValidationResult?: (result: any) => void;
}

export const ActionsPanel: React.FC<ActionsPanelProps> = ({
  clienteNif,
  clienteNombre: clienteNombreProps,
  proyectoAcronimo,
  refreshTrigger,
  extractedMetadata,
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
  const [isLoadingMetadata, setIsLoadingMetadata] = useState<boolean>(false);
  const [generationAvisos, setGenerationAvisos] = useState<string[]>([]);
  const [puede_generar_2_1, setPuedeGenerar2_1] = useState<boolean>(false);
  const [puede_generar_2_2, setPuedeGenerar2_2] = useState<boolean>(false);
  const previewContainerRef = useRef<HTMLDivElement>(null);
  
  // Verificar fichas disponibles cuando cambian los datos
  const checkAvailableFichas = async () => {
    try {
      console.log(`\n✅ CHECK-AVAILABLE-FICHAS INICIADO`);
      console.log(`   Cliente: ${clienteNif} / Proyecto: ${proyectoAcronimo || 'NONE'}`);
      
      const response = await apiService.checkAvailableFichas(clienteNif || undefined, proyectoAcronimo || undefined);
      
      if (response.data.status === 'success') {
        console.log(`   📊 Respuesta del servidor:`);
        console.log(`      - Puede generar 2.1: ${response.data.puede_generar_2_1}`);
        console.log(`      - Puede generar 2.2: ${response.data.puede_generar_2_2}`);
        console.log(`      - Personal: ${response.data.datos.personal} registros`);
        console.log(`      - Colaboraciones: ${response.data.datos.colaboraciones} registros`);
        console.log(`      - Facturas: ${response.data.datos.facturas} registros`);
        
        setPuedeGenerar2_1(response.data.puede_generar_2_1);
        setPuedeGenerar2_2(response.data.puede_generar_2_2);
        
        console.log(`   ✅ Estados actualizados`);
      }
    } catch (error) {
      console.error('❌ Error verificando fichas disponibles:', error);
      setPuedeGenerar2_1(false);
      setPuedeGenerar2_2(false);
    }
  };
  
  // Cargar metadatos y verificar fichas cuando cambia el cliente
  useEffect(() => {
    if (clienteNif) {
      loadMetadata();
      checkAvailableFichas();
      // Autocompletar nombre del cliente si viene del selector
      if (clienteNombreProps) {
        setClienteNombre(clienteNombreProps);
      }
    }
  }, [clienteNif, clienteNombreProps, proyectoAcronimo]);

  // Verificar fichas disponibles cada 2 segundos mientras no haya datos
  // Esto ayuda a detectar cuando se procesa el Anexo
  useEffect(() => {
    if (!puede_generar_2_1 && !puede_generar_2_2 && clienteNif && proyectoAcronimo) {
      const interval = setInterval(() => {
        console.log('🔄 Re-verificando fichas disponibles...');
        checkAvailableFichas();
      }, 1000);  // Cambié a 1 segundo para ser más rápido
      
      return () => clearInterval(interval);
    }
  }, [clienteNif, proyectoAcronimo, puede_generar_2_1, puede_generar_2_2]);

  // Forzar recarga cuando se dispara refreshTrigger (p.ej., después de cargar Anexo)
  useEffect(() => {
    if (refreshTrigger !== undefined && refreshTrigger !== null && refreshTrigger > 0) {
      console.log(`\n${'='.repeat(60)}`);
      console.log(`🔄 REFRESH TRIGGER DETECTADO: ${refreshTrigger}`);
      console.log(`   Cliente: ${clienteNif}`);
      console.log(`   Proyecto: ${proyectoAcronimo}`);
      console.log(`${'='.repeat(60)}`);
      
      console.log('🔄 Iniciando verificaciones múltiples...');
      // Hacer múltiples verificaciones en rápida sucesión
      checkAvailableFichas();
      
      const timeout1 = setTimeout(() => {
        console.log('   🔄 Verificación #2...');
        checkAvailableFichas();
      }, 300);
      
      const timeout2 = setTimeout(() => {
        console.log('   🔄 Verificación #3...');
        checkAvailableFichas();
      }, 600);
      
      const timeout3 = setTimeout(() => {
        console.log('   🔄 Verificación #4...');
        checkAvailableFichas();
      }, 1000);
      
      return () => {
        clearTimeout(timeout1);
        clearTimeout(timeout2);
        clearTimeout(timeout3);
      };
    }
  }, [refreshTrigger]);

  // Autocompletar campos cuando se reciben metadatos extraídos del Anexo
  useEffect(() => {
    if (extractedMetadata) {
      console.log('[ActionsPanel] 📊 Autocompletando campos con metadatos extraídos:', extractedMetadata);
      
      // Autocompletar año fiscal
      if (extractedMetadata.anio_fiscal) {
        const anio = extractedMetadata.anio_fiscal.toString();
        console.log(`   📅 Año fiscal: ${anio}`);
        setAnioFiscal(anio);
      }
      
      // Autocompletar NIF cliente
      if (extractedMetadata.nif_cliente) {
        console.log(`   🆔 NIF cliente: ${extractedMetadata.nif_cliente}`);
        setClienteNIF(extractedMetadata.nif_cliente);
      }
      
      // Autocompletar entidad solicitante (razón social)
      if (extractedMetadata.entidad_solicitante) {
        console.log(`   🏢 Entidad: ${extractedMetadata.entidad_solicitante}`);
        setClienteNombre(extractedMetadata.entidad_solicitante);
      }
      
      console.log('[ActionsPanel] ✅ Campos autocompletados');
    }
  }, [extractedMetadata]);

  const loadMetadata = async () => {
    if (!clienteNif) return;
    
    try {
      setIsLoadingMetadata(true);
      console.log(`🔄 Cargando metadata para cliente: ${clienteNif}`);
      const response = await apiService.getMetadata(clienteNif);
      const metadata = response.data;
      
      console.log('✅ Metadata cargada:', metadata);
      
      // Autocompleta los campos con los datos del Anexo
      if (metadata.entidad_solicitante) {
        setClienteNombre(metadata.entidad_solicitante);
      }
      if (metadata.nif_cliente) {
        setClienteNIF(metadata.nif_cliente);
      }
      if (metadata.anio_fiscal) {
        setAnioFiscal(metadata.anio_fiscal.toString());
      } else {
        // Si no hay año fiscal en metadata, usar el año actual
        setAnioFiscal(new Date().getFullYear().toString());
      }
    } catch (error: any) {
      // No es crítico si no existe metadata (cliente nuevo)
      console.log('ℹ️ No se encontró metadata (cliente nuevo o sin Anexo procesado)');
      // Asegurar que el año fiscal por defecto sea el año actual
      setAnioFiscal(new Date().getFullYear().toString());
    } finally {
      setIsLoadingMetadata(false);
    }
  };

  const saveMetadata = async () => {
    if (!clienteNif) return;
    
    try {
      onLoading(true);
      console.log(`📝 Guardando metadatos para cliente: ${clienteNif}`);
      
      const response = await apiService.saveMetadata({
        cliente_nif: clienteNif,
        entidad_solicitante: clienteNombre,
        nif_cliente: clienteNIF,
        anio_fiscal: parseInt(anioFiscal) || new Date().getFullYear()
      });
      
      console.log('✅ Metadatos guardados:', response.data);
      onSuccess(`✅ Datos de cliente guardados`);
    } catch (error: any) {
      console.error('❌ Error guardando metadatos:', error);
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };
  
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
      console.log(`[ActionsPanel] Iniciando procesamiento de CVs para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}`);
      const response = await apiService.processCVs(clienteNif || undefined, proyectoAcronimo || undefined);
      console.log('[ActionsPanel] Respuesta del procesamiento:', response.data);
      onSuccess(`✅ CVs procesados: ${response.data.message}`);
    } catch (error: any) {
      console.error('[ActionsPanel] Error procesando CVs:', error);
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleValidate = async () => {
    try {
      onLoading(true);
      console.log(`[ActionsPanel] Iniciando validación para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}`);
      const response = await apiService.validate(clienteNif || undefined, proyectoAcronimo || undefined);
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
      console.log(`[ActionsPanel] Generando fichas para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}`);
      const response = await apiService.generateFichas(clienteNif || undefined, proyectoAcronimo || undefined, payload);
      clearInterval(interval);
      setGenerationProgress(95);
      
      // Capturar avisos y disponibilidad de fichas
      const avisos = response.data.avisos || [];
      const puede2_1 = response.data.puede_generar_2_1 || false;
      const puede2_2 = response.data.puede_generar_2_2 || false;
      
      setGenerationAvisos(avisos);
      setPuedeGenerar2_1(puede2_1);
      setPuedeGenerar2_2(puede2_2);
      
      onSuccess(`✅ Fichas generadas: ${response.data.message}`);
      if (response.data.files && Array.isArray(response.data.files)) {
        setGeneratedFiles(response.data.files);
      }
      setGenerationProgress(100);
      setTimeout(() => setGenerationProgress(0), 800);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
      setGenerationProgress(0);
      setGenerationAvisos([]);
      setPuedeGenerar2_1(false);
      setPuedeGenerar2_2(false);
    } finally {
      onLoading(false);
    }
  };

  const handleGenerarFicha2_1Solo = async () => {
    // Si no hay datos, mostrar aviso
    if (!puede_generar_2_1) {
      onError('⚠️ No hay datos de personal. Cargue un Anexo o edite los datos.');
      setGenerationAvisos(['No hay datos de personal']);
      return;
    }

    try {
      if (clienteNIF && !validateNIF(clienteNIF)) {
        onError('❌ NIF inválido');
        return;
      }

      onLoading(true);
      const payload = {
        cliente_nombre: clienteNombre || undefined,
        cliente_nif: clienteNIF || undefined,
        anio_fiscal: anioFiscal ? parseInt(anioFiscal) : undefined,
      };
      console.log(`[ActionsPanel] Generando solo Ficha 2.1 para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}`);
      const response = await apiService.generateFicha2_1Only(clienteNif || undefined, proyectoAcronimo || undefined, payload);
      
      if (!response.data.success) {
        // No se pudo generar - mostrar aviso amigable
        onError(`⚠️ ${response.data.aviso}`);
        setGenerationAvisos([response.data.aviso]);
      } else {
        // Se generó correctamente
        onSuccess(`✅ Ficha 2.1 generada`);
        if (response.data.file) {
          setGeneratedFiles([response.data.file]);
        }
        setGenerationAvisos([]);
      }
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
      setGenerationAvisos([]);
    } finally {
      onLoading(false);
    }
  };

  const handleGenerarFicha2_2Solo = async () => {
    // Si no hay datos, mostrar aviso
    if (!puede_generar_2_2) {
      onError('⚠️ No hay datos de colaboraciones o facturas. Cargue un Anexo o edite los datos.');
      setGenerationAvisos(['No hay datos de colaboraciones o facturas']);
      return;
    }

    try {
      if (clienteNIF && !validateNIF(clienteNIF)) {
        onError('❌ NIF inválido');
        return;
      }

      onLoading(true);
      const payload = {
        cliente_nombre: clienteNombre || undefined,
        cliente_nif: clienteNIF || undefined,
        anio_fiscal: anioFiscal ? parseInt(anioFiscal) : undefined,
      };
      console.log(`[ActionsPanel] Generando solo Ficha 2.2 para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}`);
      const response = await apiService.generateFicha2_2Only(clienteNif || undefined, proyectoAcronimo || undefined, payload);
      
      if (!response.data.success) {
        // No se pudo generar - mostrar aviso amigable
        onError(`⚠️ ${response.data.aviso}`);
        setGenerationAvisos([response.data.aviso]);
      } else {
        // Se generó correctamente
        onSuccess(`✅ Ficha 2.2 generada`);
        if (response.data.file) {
          setGeneratedFiles([response.data.file]);
        }
        setGenerationAvisos([]);
      }
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
      setGenerationAvisos([]);
    } finally {
      onLoading(false);
    }
  };

  // Función helper para generar nombre personalizado de descarga
  const getCustomFileName = (ficheroBase: string, cliente: string | null, proyecto?: string | null): string => {
    if (!cliente) return ficheroBase;
    
    // Extraer tipo de ficha (2_1 o 2_2)
    const partes = ficheroBase.replace('Ficha_', '').replace('.docx', '');
    // Sanitizar y convertir a mayúsculas: solo alfanuméricos
    const clienteSanitizado = cliente.replace(/[^a-zA-Z0-9]/g, '').toUpperCase().substring(0, 30);
    const proyectoSanitizado = proyecto?.replace(/[^a-zA-Z0-9]/g, '').toUpperCase().substring(0, 30) || '';
    
    // Formato: Ficha_Ampliacion_Aptdo_2_1_CLIENTE_PROYECTO.docx
    if (proyectoSanitizado) {
      return `Ficha_Ampliacion_Aptdo_${partes}_${clienteSanitizado}_${proyectoSanitizado}.docx`;
    } else {
      return `Ficha_Ampliacion_Aptdo_${partes}_${clienteSanitizado}.docx`;
    }
  };

  const handleDownloadFicha = async (name: string) => {
    try {
      onLoading(true);
      console.log(`[ActionsPanel] Descargando ficha para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'} - archivo: ${name}`);
      const response = await apiService.downloadFicha(name, clienteNif || undefined, proyectoAcronimo || undefined);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      // Usar nombre personalizado con cliente y proyecto
      const customName = getCustomFileName(name, clienteNombre, proyectoAcronimo);
      link.setAttribute('download', customName);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(url);
      onSuccess(`✅ ${customName} descargado`);
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handlePreviewFicha = async (name: string) => {
    try {
      onLoading(true);
      console.log(`[ActionsPanel] Previsualizando ficha para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'} - archivo: ${name}`);
      const response = await apiService.previewFichaDocx(name, clienteNif || undefined, proyectoAcronimo || undefined);
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
      console.log(`[ActionsPanel] Descargando ZIP de fichas para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}`);
      const response = await apiService.downloadFichas(clienteNif || undefined, proyectoAcronimo || undefined, (pct:number) => setDownloadProgress(pct));
      
      // Crear un blob y descargarlo
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      // Usar nombre personalizado para el ZIP
      // Formato: Fichas_ampliacion_CLIENTE_PROYECTO.ZIP
      const customZipName = clienteNombre && proyectoAcronimo 
        ? `Fichas_ampliacion_${clienteNombre.replace(/[^a-zA-Z0-9]/g, '').toUpperCase()}_${proyectoAcronimo.replace(/[^a-zA-Z0-9]/g, '').toUpperCase()}.ZIP`
        : clienteNombre
        ? `Fichas_ampliacion_${clienteNombre.replace(/[^a-zA-Z0-9]/g, '').toUpperCase()}.ZIP`
        : 'Fichas_ampliacion.ZIP';
      link.setAttribute('download', customZipName);
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

      {/* Display destacado del año fiscal cuando se carga desde el Anexo */}
      {anioFiscal && (
        <div className={`mb-6 p-4 rounded-lg border-2 ${
          parseInt(anioFiscal) > 2000
            ? 'bg-blue-50 border-blue-300'
            : 'bg-gray-50 border-gray-300'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Año Fiscal Detectado</p>
              <p className="text-3xl font-bold text-blue-600">{anioFiscal}</p>
            </div>
            <div className="text-4xl">📅</div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Entidad solicitante (Razón social)
            {isLoadingMetadata && <span className="ml-2 text-xs text-blue-500">📥 Cargando...</span>}
          </label>
          <input
            value={clienteNombre}
            onChange={(e) => setClienteNombre(e.target.value)}
            placeholder="Se autocompleta desde el Anexo"
            disabled={isLoadingMetadata}
            className="input mt-1 w-full disabled:opacity-50"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            NIF Cliente
            {isLoadingMetadata && <span className="ml-2 text-xs text-blue-500">📥 Cargando...</span>}
          </label>
          <input
            value={clienteNIF}
            onChange={(e) => setClienteNIF(e.target.value)}
            placeholder="Se autocompleta desde el Anexo"
            disabled={isLoadingMetadata}
            className="input mt-1 w-full disabled:opacity-50"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Año Fiscal
            {isLoadingMetadata && <span className="ml-2 text-xs text-blue-500">📥 Cargando...</span>}
          </label>
          <input
            type="number"
            value={anioFiscal}
            onChange={(e) => setAnioFiscal(e.target.value)}
            placeholder="Se autocompleta desde el Anexo"
            disabled={isLoadingMetadata}
            min="2000"
            max="2099"
            className="input mt-1 w-full disabled:opacity-50"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <button
          onClick={saveMetadata}
          className="btn-secondary text-lg py-3"
        >
          💾 Guardar Datos
        </button>
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
      </div>

      {/* Avisos de generación */}
      {generationAvisos.length > 0 && (
        <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-400 rounded">
          <div className="flex items-start gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <h3 className="font-semibold text-red-800 mb-2">Falta de datos para generar fichas</h3>
              <ul className="space-y-2">
                {generationAvisos.map((aviso, idx) => (
                  <li key={idx} className="text-red-700 text-sm flex items-start gap-2">
                    <span className="text-red-500 mt-0.5">•</span>
                    <span>{aviso}</span>
                  </li>
                ))}
              </ul>
              <p className="text-red-600 text-xs mt-3 italic">💡 Cargue un Anexo o edite los datos existentes para poder generar todas las fichas</p>
            </div>
          </div>
        </div>
      )}

      {/* Opciones de generación selectiva - siempre visible */}
      <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="text-sm font-semibold mb-3 text-blue-800">📄 Generar Fichas Individuales:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button
            onClick={handleGenerarFicha2_1Solo}
            className={`text-sm py-2 font-medium rounded transition-colors ${
              puede_generar_2_1 
                ? 'btn-secondary hover:bg-blue-600' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
            disabled={!puede_generar_2_1}
          >
            📄 Generar Ficha 2.1 (Personal)
          </button>
          <button
            onClick={handleGenerarFicha2_2Solo}
            className={`text-sm py-2 font-medium rounded transition-colors ${
              puede_generar_2_2 
                ? 'btn-secondary hover:bg-blue-600' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
            disabled={!puede_generar_2_2}
          >
            📄 Generar Ficha 2.2 (Colaboraciones/Facturas)
          </button>
        </div>
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
          proyectoAcronimo={proyectoAcronimo ? proyectoAcronimo : undefined}
          onDataSaved={checkAvailableFichas}
        />
      )}
    </div>
  );
};

export default ActionsPanel;
