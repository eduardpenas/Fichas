import React, { useState, useRef } from 'react';
import FileUploader from './components/FileUploader';
import ActionsPanel from './components/ActionsPanel';
import ClientSelector from './components/ClientSelector';
import ProjectSelector from './components/ProjectSelector';
import { apiService } from './api/client';
import './index.css';

interface Alert {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  message: string;
}

export default function App() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedClient, setSelectedClient] = useState<string | null>(null);
  const [selectedClientName, setSelectedClientName] = useState<string | null>(null);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [uploadRefreshTrigger, setUploadRefreshTrigger] = useState<number>(0);
  const [anexoMetadata, setAnexoMetadata] = useState<any>(null);  // ← Para almacenar metadatos extraídos
  const alertIdCounterRef = useRef<number>(0);  // ← Contador para IDs únicos de alertas

  const addAlert = (type: Alert['type'], message: string) => {
    alertIdCounterRef.current++;
    const id = `${Date.now()}-${alertIdCounterRef.current}`;  // Combinación: timestamp + contador
    const alert: Alert = { id, type, message };
    console.log(`[App] 📢 addAlert - type: ${type}, message: "${message}", id: ${id}`);
    setAlerts(prev => {
      console.log(`[App] 📊 alerts state actualizado:`, [alert, ...prev]);
      return [alert, ...prev];
    });

    setTimeout(() => {
      setAlerts(prev => prev.filter(a => a.id !== id));
    }, 5000);
  };

  const removeAlert = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  const handleUploadComplete = () => {
    // Refrescar completamente después de cargar el anexo
    console.log('\n' + '='.repeat(60));
    console.log('[App] 📤 UPLOAD COMPLETADO');
    console.log(`    Cliente: ${selectedClient}`);
    console.log(`    Proyecto: ${selectedProject}`);
    console.log('='.repeat(60));
    
    console.log('[App] ♻️ Re-verificando fichas disponibles...');
    setUploadRefreshTrigger(prev => {
      const newValue = prev + 1;
      console.log(`[App] 📍 uploadRefreshTrigger: ${prev} → ${newValue}`);
      return newValue;
    });
  };

  const handleAnexoMetadata = (metadata: any) => {
    // Callback para recibir metadatos del anexo
    console.log('[App] 📊 Metadatos del Anexo recibidos:', metadata);
    setAnexoMetadata(metadata);
    
    // Mostrar alerta con información del año fiscal
    if (metadata?.anio_fiscal) {
      addAlert('success', `✓ Año fiscal extraído del Anexo: ${metadata.anio_fiscal}`);
    }
  };

  const handleCVsUploadComplete = async () => {
    // Auto-procesar CVs después de subir
    console.log(`[App] CVs subidos, iniciando procesamiento automático para cliente: ${selectedClient} / proyecto: ${selectedProject}...`);
    try {
      setIsLoading(true);
      const response = await apiService.processCVs(selectedClient || undefined, selectedProject || undefined);
      console.log('[App] CVs procesados:', response.data);
      addAlert('success', `✅ CVs procesados automáticamente: ${response.data.message}`);
    } catch (error: any) {
      console.error('[App] Error procesando CVs:', error);
      addAlert('error', `❌ Error procesando CVs: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Si no hay cliente o proyecto seleccionado, mostrar selector
  const showProjectSelector = selectedClient && !selectedProject;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {!selectedClient ? (
        <ClientSelector
          onSelectClient={(nif, name) => {
            setSelectedClient(nif);
            setSelectedClientName(name || nif);
          }}
          onSuccess={(msg) => addAlert('success', msg)}
          onError={(msg) => addAlert('error', msg)}
          onLoading={setIsLoading}
        />
      ) : showProjectSelector ? (
        <ProjectSelector
          clienteNif={selectedClient}
          onSelectProject={setSelectedProject}
          onBack={() => setSelectedClient(null)}
          onSuccess={(msg) => addAlert('success', msg)}
          onError={(msg) => addAlert('error', msg)}
          onLoading={setIsLoading}
        />
      ) : selectedClient && selectedProject ? (
        <>
          {/* Header con botón de volver */}
          <header className="bg-white shadow-sm sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
              <div>
                <h1 className="text-2xl font-bold">📊 Fichas de Investigación</h1>
                <p className="text-sm text-gray-500">Cliente: <span className="font-semibold">{selectedClientName || selectedClient}</span> | Proyecto: <span className="font-semibold">{selectedProject}</span></p>
              </div>
              <button
                onClick={() => {
                  setSelectedProject(null);
                  setSelectedClient(null);
                  setSelectedClientName(null);
                }}
                className="btn-secondary"
              >
                ← Volver
              </button>
            </div>
          </header>

      {/* Alerts - Fixed Position */}
      <div className="fixed top-0 left-0 right-0 z-50 max-w-7xl mx-auto px-6 py-4">
        {alerts.map(alert => (
          <div
            key={alert.id}
            className={`alert alert-${alert.type} flex justify-between items-center mb-2`}
          >
            <span>{alert.message}</span>
            <button
              onClick={() => removeAlert(alert.id)}
              className="text-lg cursor-pointer"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      {/* Loading Overlay */}
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Procesando...</p>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 pb-12">
        {/* Step 1: File Upload */}
        <section className="mb-8">
          <div className="bg-white rounded-lg shadow-sm p-1">
            <div className="flex items-center gap-3 mb-6 p-5 bg-blue-50 rounded">
              <span className="text-3xl">1️⃣</span>
              <div>
                <h2 className="text-lg font-bold">Cargar Archivos</h2>
                <p className="text-sm text-gray-600">Sube el Anexo II y los CVs en PDF</p>
              </div>
            </div>

            <FileUploader
              clienteNif={selectedClient}
              proyectoAcronimo={selectedProject}
              onSuccess={(msg) => addAlert('success', msg)}
              onError={(msg) => addAlert('error', msg)}
              onLoading={setIsLoading}
              onUploadComplete={handleUploadComplete}
              onCVsUploadComplete={handleCVsUploadComplete}
              onAnexoMetadata={handleAnexoMetadata}
            />
          </div>
        </section>

        {/* Step 2: Actions */}
        <section className="mb-8">
          <div className="bg-white rounded-lg shadow-sm p-1">
            <div className="flex items-center gap-3 mb-6 p-5 bg-purple-50 rounded">
              <span className="text-3xl">2️⃣</span>
              <div>
                <h2 className="text-lg font-bold">Generar Fichas</h2>
                <p className="text-sm text-gray-600">Valida datos y genera las fichas finales en Word</p>
              </div>
            </div>

            <ActionsPanel
              clienteNif={selectedClient}
              clienteNombre={selectedClientName}
              proyectoAcronimo={selectedProject}
              refreshTrigger={uploadRefreshTrigger}
              extractedMetadata={anexoMetadata}
              onSuccess={(msg) => addAlert('success', msg)}
              onError={(msg) => addAlert('warning', msg)}
              onLoading={setIsLoading}
              onValidationResult={(result) => {
                if (!result.exitosa) {
                  addAlert('warning', '⚠️ Revisa los errores de validación arriba');
                }
              }}
            />
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-12 pt-6 border-t border-gray-200 text-center text-gray-600 text-sm">
          <p>🚀 Gestor de Fichas v1.0 - Sistema de procesamiento automático</p>
          <p className="mt-2">API: http://localhost:8000 | Frontend: http://localhost:5173</p>
        </footer>
      </main>
        </>
      ) : null}
    </div>
  );
}
