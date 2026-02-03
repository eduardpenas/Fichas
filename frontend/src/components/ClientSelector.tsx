import React, { useState, useEffect } from 'react';
import { apiService } from '../api/client';

interface Client {
  nif: string;
  nombre: string;
  folder: string;
}

interface ClientSelectorProps {
  onSelectClient: (clientNif: string) => void;
  onSuccess: (message: string) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const ClientSelector: React.FC<ClientSelectorProps> = ({
  onSelectClient,
  onSuccess,
  onError,
  onLoading,
}) => {
  const [clientes, setClientes] = useState<Client[]>([]);
  const [newClientNif, setNewClientNif] = useState<string>('');
  const [newClientName, setNewClientName] = useState<string>('');
  const [showNewForm, setShowNewForm] = useState(false);
  const [clientToDelete, setClientToDelete] = useState<string | null>(null);

  useEffect(() => {
    loadClientes();
  }, []);

  const loadClientes = async () => {
    try {
      onLoading(true);
      const response = await apiService.listClients();
      setClientes(response.data?.clientes || []);
    } catch (error: any) {
      onError(`❌ Error al cargar clientes: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleCreateClient = async () => {
    if (!newClientNif.trim()) {
      onError('❌ El NIF es obligatorio');
      return;
    }

    if (clientes.some(c => c.nif === newClientNif)) {
      onError('❌ Ya existe un cliente con ese NIF');
      return;
    }

    try {
      onLoading(true);
      // Crear carpeta del cliente (se crea automáticamente al guardar datos)
      // Por ahora, simplemente seleccionamos el cliente
      setClientes([...clientes, {
        nif: newClientNif,
        nombre: newClientName || newClientNif,
        folder: `Cliente_${newClientNif}`
      }]);
      onSuccess(`✅ Cliente ${newClientNif} creado`);
      setNewClientNif('');
      setNewClientName('');
      setShowNewForm(false);
      onSelectClient(newClientNif);
    } catch (error: any) {
      onError(`❌ Error: ${error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleDeleteClient = async (nif: string) => {
    try {
      onLoading(true);
      await apiService.deleteClient(nif);
      setClientes(clientes.filter(c => c.nif !== nif));
      onSuccess(`✅ Cliente ${nif} eliminado correctamente`);
      setClientToDelete(null);
    } catch (error: any) {
      onError(`❌ Error al eliminar cliente: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">📋 Generador de Fichas</h1>
          <p className="text-gray-600">Selecciona un cliente o crea uno nuevo</p>
        </div>

        {/* Clientes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {clientes.map((cliente) => (
            <div
              key={cliente.nif}
              className="bg-white rounded-lg shadow-md p-6 border-2 border-transparent hover:border-blue-500 transition-all duration-200"
            >
              <div className="text-2xl mb-2">👤</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-1">{cliente.nombre}</h3>
              <p className="text-sm text-gray-600 mb-4">NIF: {cliente.nif}</p>
              <div className="flex gap-2">
                <button
                  onClick={() => onSelectClient(cliente.nif)}
                  className="btn-primary text-sm py-2 flex-1"
                >
                  ✏️ Abrir Portal
                </button>
                <button
                  onClick={() => setClientToDelete(cliente.nif)}
                  className="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-3 rounded text-sm transition-colors"
                  title="Eliminar cliente"
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}

          {/* Botón crear nuevo cliente */}
          <div
            onClick={() => setShowNewForm(!showNewForm)}
            className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200 border-2 border-dashed border-green-500 flex items-center justify-center"
          >
            <div className="text-center">
              <div className="text-4xl mb-2">➕</div>
              <h3 className="text-lg font-semibold text-gray-800">Nuevo Cliente</h3>
              <p className="text-sm text-gray-600">Crear nuevo portal</p>
            </div>
          </div>
        </div>

        {/* Formulario Nuevo Cliente */}
        {showNewForm && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-2xl font-bold">➕ Crear Nuevo Cliente</h3>
                <button
                  onClick={() => setShowNewForm(false)}
                  className="text-lg hover:text-red-500"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    NIF del Cliente
                  </label>
                  <input
                    type="text"
                    value={newClientNif}
                    onChange={(e) => setNewClientNif(e.target.value.toUpperCase())}
                    placeholder="12345678A"
                    className="input w-full"
                    autoFocus
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre del Cliente (opcional)
                  </label>
                  <input
                    type="text"
                    value={newClientName}
                    onChange={(e) => setNewClientName(e.target.value)}
                    placeholder="Nombre empresa o persona"
                    className="input w-full"
                  />
                </div>

                <div className="flex gap-2 pt-4">
                  <button
                    onClick={() => setShowNewForm(false)}
                    className="btn-secondary flex-1 py-2"
                  >
                    ❌ Cancelar
                  </button>
                  <button
                    onClick={handleCreateClient}
                    className="btn-primary flex-1 py-2"
                  >
                    ✅ Crear Cliente
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Info Footer */}
        <div className="bg-blue-50 border-l-4 border-blue-500 rounded p-4 mt-8">
          <p className="text-sm text-gray-700">
            💡 <strong>Cada cliente tiene su propio portal</strong> donde se guardan automáticamente todos los cambios realizados. 
            Los datos históricos se mantienen en el servidor para referencia futura.
          </p>
        </div>

        {/* Modal de Confirmación de Eliminación */}
        {clientToDelete && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
              <div className="mb-4">
                <h3 className="text-2xl font-bold text-red-600 mb-2">⚠️ Eliminar Cliente</h3>
                <p className="text-gray-700 mb-2">
                  ¿Está seguro de que desea eliminar el cliente <strong>{clientes.find(c => c.nif === clientToDelete)?.nombre}</strong> ({clientToDelete})?
                </p>
                <p className="text-sm text-red-600 font-medium">
                  ⚠️ Esta acción es irreversible. Se eliminarán todos los datos asociados a este cliente.
                </p>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => setClientToDelete(null)}
                  className="btn-secondary flex-1 py-2"
                >
                  ❌ Cancelar
                </button>
                <button
                  onClick={() => {
                    if (clientToDelete) {
                      handleDeleteClient(clientToDelete);
                    }
                  }}
                  className="bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded flex-1 transition-colors"
                >
                  🗑️ Eliminar
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientSelector;
