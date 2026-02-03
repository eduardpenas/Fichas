import React, { useState, useRef } from 'react';
import FileUploader from './components/FileUploader';
import EditableTable from './components/EditableTable';
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
  const [editedData, setEditedData] = useState<any[]>([]);
  const [selectedClient, setSelectedClient] = useState<string | null>(null);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const editableTableRef = useRef<any>(null);  // ← Ref para refrescar la tabla

  const addAlert = (type: Alert['type'], message: string) => {
    const id = Date.now().toString();
    const alert: Alert = { id, type, message };
    setAlerts(prev => [alert, ...prev]);

    setTimeout(() => {
      setAlerts(prev => prev.filter(a => a.id !== id));
    }, 5000);
  };

  const removeAlert = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  const handleUploadComplete = () => {
    // Refrescar la tabla después de cargar el anexo
    console.log('[App] Upload completado, refrescando tabla...');
    if (editableTableRef.current?.loadData) {
      editableTableRef.current.loadData();
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
      
      // Refrescar la tabla para ver los datos actualizados
      if (editableTableRef.current?.loadData) {
        editableTableRef.current.loadData();
      }
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
          onSelectClient={setSelectedClient}
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
                <p className="text-sm text-gray-500">Cliente: <span className="font-semibold">{selectedClient}</span> | Proyecto: <span className="font-semibold">{selectedProject}</span></p>
              </div>
              <button
                onClick={() => {
                  setSelectedProject(null);
                  setSelectedClient(null);
                }}
                className="btn-secondary"
              >
                ← Volver
              </button>
            </div>
          </header>

      {/* Alerts */}
      <div className="max-w-7xl mx-auto px-6 py-4">
        {alerts.map(alert => (
          <div
            key={alert.id}
            className={`alert alert-${alert.type} flex justify-between items-center`}
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
            />
          </div>
        </section>

        {/* Step 2: Edit Data */}
        <section className="mb-8">
          <div className="bg-white rounded-lg shadow-sm p-1">
            <div className="flex items-center gap-3 mb-6 p-5 bg-green-50 rounded">
              <span className="text-3xl">2️⃣</span>
              <div>
                <h2 className="text-lg font-bold">Revisar y Editar Datos</h2>
                <p className="text-sm text-gray-600">Visualiza y modifica la información antes de generar fichas</p>
              </div>
            </div>

            <EditableTable
              ref={editableTableRef}
              clienteNif={selectedClient}
              proyectoAcronimo={selectedProject}
              title="📊 Tabla de Personal (Ficha 2.1)"
              subtitle="Edita los datos haciendo clic en cada celda. Los cambios se guardan localmente."
              onDataChange={setEditedData}
              onError={(msg) => addAlert('error', msg)}
              onLoading={setIsLoading}
            />
          </div>
        </section>

        {/* Step 3: Actions */}
        <section className="mb-8">
          <div className="bg-white rounded-lg shadow-sm p-1">
            <div className="flex items-center gap-3 mb-6 p-5 bg-purple-50 rounded">
              <span className="text-3xl">3️⃣</span>
              <div>
                <h2 className="text-lg font-bold">Procesar y Generar</h2>
                <p className="text-sm text-gray-600">Procesa CVs, valida datos y genera las fichas finales</p>
              </div>
            </div>

            <ActionsPanel
              clienteNif={selectedClient}
              proyectoAcronimo={selectedProject}
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
