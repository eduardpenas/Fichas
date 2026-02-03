import React, { useState, useEffect } from 'react';
import { apiService } from '../api/client';

interface Proyecto {
  acronimo: string;
  path: string;
}

interface ProjectSelectorProps {
  clienteNif: string;
  onSelectProject: (proyectoAcronimo: string) => void;
  onBack: () => void;
  onSuccess: (message: string) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const ProjectSelector: React.FC<ProjectSelectorProps> = ({
  clienteNif,
  onSelectProject,
  onBack,
  onSuccess,
  onError,
  onLoading,
}) => {
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [newProjectAcronimo, setNewProjectAcronimo] = useState<string>('');
  const [showNewForm, setShowNewForm] = useState(false);

  useEffect(() => {
    loadProyectos();
  }, [clienteNif]);

  const loadProyectos = async () => {
    try {
      onLoading(true);
      const response = await apiService.listProyectos(clienteNif);
      setProyectos(response.data?.proyectos || []);
    } catch (error: any) {
      // No es crítico si no hay proyectos
      console.log('ℹ️ No hay proyectos aún');
      setProyectos([]);
    } finally {
      onLoading(false);
    }
  };

  const handleCreateProject = async () => {
    if (!newProjectAcronimo.trim()) {
      onError('❌ El acrónimo del proyecto es obligatorio');
      return;
    }

    if (proyectos.some(p => p.acronimo.toUpperCase() === newProjectAcronimo.toUpperCase())) {
      onError('❌ Ya existe un proyecto con ese acrónimo');
      return;
    }

    try {
      onLoading(true);
      await apiService.createProyecto(clienteNif, newProjectAcronimo);
      onSuccess(`✅ Proyecto ${newProjectAcronimo.toUpperCase()} creado`);
      setNewProjectAcronimo('');
      setShowNewForm(false);
      onSelectProject(newProjectAcronimo.toUpperCase());
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
      <div className="bg-white rounded-lg shadow-2xl p-8 max-w-2xl w-full">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">🎯 Selecciona Proyecto</h1>
          <p className="text-gray-600">
            Cliente: <span className="font-semibold text-blue-600">{clienteNif}</span>
          </p>
        </div>

        {/* Lista de proyectos existentes */}
        {proyectos.length > 0 && (
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-3">📁 Proyectos Existentes</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {proyectos.map((proyecto) => (
                <button
                  key={proyecto.acronimo}
                  onClick={() => onSelectProject(proyecto.acronimo)}
                  className="p-4 border-2 border-blue-300 rounded-lg hover:bg-blue-50 hover:border-blue-600 transition-all text-left"
                >
                  <span className="font-semibold text-blue-600">{proyecto.acronimo}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Formulario para nuevo proyecto */}
        {!showNewForm ? (
          <button
            onClick={() => setShowNewForm(true)}
            className="btn-primary w-full mb-4"
          >
            ✨ Crear Nuevo Proyecto
          </button>
        ) : (
          <div className="bg-gray-50 p-4 rounded-lg mb-4">
            <h3 className="text-lg font-semibold mb-3">Crear Nuevo Proyecto</h3>
            <input
              type="text"
              placeholder="Acrónimo del proyecto (ej: ACR, PROJ2024)"
              value={newProjectAcronimo}
              onChange={(e) => setNewProjectAcronimo(e.target.value.toUpperCase())}
              className="input w-full mb-3"
              maxLength={20}
            />
            <div className="flex gap-2">
              <button
                onClick={handleCreateProject}
                className="btn-primary flex-1"
              >
                ✅ Crear
              </button>
              <button
                onClick={() => {
                  setShowNewForm(false);
                  setNewProjectAcronimo('');
                }}
                className="btn-secondary flex-1"
              >
                ✕ Cancelar
              </button>
            </div>
          </div>
        )}

        {/* Botón para volver */}
        <button
          onClick={onBack}
          className="btn-secondary w-full"
        >
          ← Volver a Seleccionar Cliente
        </button>
      </div>
    </div>
  );
};

export default ProjectSelector;
