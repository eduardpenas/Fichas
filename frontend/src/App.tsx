import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import EditableTable from './components/EditableTable';
import ActionsPanel from './components/ActionsPanel';
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-gray-900">📋 Gestor de Fichas</h1>
          <p className="text-gray-600 text-sm">Sistema de gestión de datos y generación automática de fichas</p>
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
              onSuccess={(msg) => addAlert('success', msg)}
              onError={(msg) => addAlert('error', msg)}
              onLoading={setIsLoading}
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
    </div>
  );
}
