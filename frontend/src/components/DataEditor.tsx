import React, { useState, useEffect } from 'react';
import { apiService } from '../api/client';

interface DataEditorProps {
  dataType: 'personal' | 'colaboraciones' | 'facturas';
  onSuccess: (message: string) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
  onClose: () => void;
  clienteNif?: string;
  proyectoAcronimo?: string;
  onDataSaved?: () => void;
}

// Define the column structure for each data type
const COLUMN_DEFINITIONS: Record<string, string[]> = {
  personal: [
    'Nombre',
    'Apellidos',
    'Titulación 1',
    'Titulación 2',
    'Coste horario (€/hora)',
    'Horas totales',
    'Coste total (€)',
    'Coste IT (€)',
    'Horas IT',
    'Departamento',
    'Puesto actual',
    'Coste I+D (€)',
    'Horas I+D',
    'EMPRESA 1',
    'PERIODO 1',
    'PUESTO 1',
    'EMPRESA 2',
    'PERIODO 2',
    'PUESTO 2',
    'EMPRESA 3',
    'PERIODO 3',
    'PUESTO 3',
  ],
  colaboraciones: [
    'Razón social',
    'NIF',
    'NIF 2',
    'Entidad contratante',
    'País de la entidad',
    'Localidad',
    'Provincia',
    'País de realización',
  ],
  facturas: [
    'Entidad',
    'Nombre factura',
    'Importe (€)',
  ],
};

// Create empty row template based on data type
const createEmptyRow = (dataType: 'personal' | 'colaboraciones' | 'facturas') => {
  const columns = COLUMN_DEFINITIONS[dataType];
  const emptyRow: any = {};
  columns.forEach(col => {
    emptyRow[col] = '';
  });
  return emptyRow;
};

export const DataEditor: React.FC<DataEditorProps> = ({
  dataType,
  onSuccess,
  onError,
  onLoading,
  onClose,
  clienteNif,
  proyectoAcronimo,
}) => {
  const [data, setData] = useState<any[]>([]);
  const [displayData, setDisplayData] = useState<any[]>([]);
  const [editingCell, setEditingCell] = useState<{ row: number; col: string } | null>(null);
  const [showEditor, setShowEditor] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  const typeLabels = {
    personal: 'Personal (Ficha 2.1)',
    colaboraciones: 'Colaboraciones (Ficha 2.2)',
    facturas: 'Facturas (Ficha 2.2)',
  };

  const loadData = async () => {
    try {
      onLoading(true);
      let response;
      switch (dataType) {
        case 'personal':
          response = await apiService.getPersonal(clienteNif, proyectoAcronimo);
          break;
        case 'colaboraciones':
          response = await apiService.getColaboraciones(clienteNif, proyectoAcronimo);
          break;
        case 'facturas':
          response = await apiService.getFacturas(clienteNif, proyectoAcronimo);
          break;
      }
      
      // Si no hay datos, inicializa con columnas vacías pero con la estructura correcta
      const loadedData = response.data || [];
      setData(loadedData);
      setDisplayData(loadedData);
      setHasChanges(false);
    } catch (error: any) {
      // En caso de error (archivo no existe), inicializa con estructura vacía
      console.log(`ℹ️ No hay datos, inicializando estructura vacía para ${dataType}`);
      const emptyData: any[] = [];
      setData(emptyData);
      setDisplayData(emptyData);
      setHasChanges(false);
    } finally {
      onLoading(false);
    }
  };

  useEffect(() => {
    if (showEditor) {
      loadData();
    }
  }, [showEditor, dataType]);

  const handleCellChange = (rowIndex: number, column: string, value: string) => {
    const newData = [...displayData];
    newData[rowIndex] = { ...newData[rowIndex], [column]: value };
    setDisplayData(newData);
    setHasChanges(true);
  };

  const handleAddRow = () => {
    const newRow = createEmptyRow(dataType);
    const newData = [...displayData, newRow];
    setDisplayData(newData);
    setHasChanges(true);
  };

  const handleDeleteRow = (rowIndex: number) => {
    const newData = displayData.filter((_, idx) => idx !== rowIndex);
    setDisplayData(newData);
    setHasChanges(true);
  };

  const handleSave = async () => {
    try {
      onLoading(true);
      let response;
      switch (dataType) {
        case 'personal':
          response = await apiService.updatePersonal(displayData, clienteNif, proyectoAcronimo);
          break;
        case 'colaboraciones':
          response = await apiService.updateColaboraciones(displayData, clienteNif, proyectoAcronimo);
          break;
        case 'facturas':
          response = await apiService.updateFacturas(displayData, clienteNif, proyectoAcronimo);
          break;
      }
      setData(displayData);
      setHasChanges(false);
      onSuccess(`✅ Datos de ${typeLabels[dataType]} guardados (${displayData.length} registros)`);
      
      // Notify parent to refresh available fichas
      if (onDataSaved) {
        setTimeout(() => onDataSaved(), 500);
      }
    } catch (error: any) {
      onError(`❌ Error al guardar: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleCancel = () => {
    setDisplayData(data);
    setHasChanges(false);
    setEditingCell(null);
    onClose();
  };

  if (!showEditor) {
    return (
      <div className="card mb-6">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold">📊 {typeLabels[dataType]}</h3>
          <button
            onClick={() => setShowEditor(true)}
            className="btn-secondary text-sm"
          >
            ✏️ Editar Datos
          </button>
        </div>
      </div>
    );
  }

  const columns = displayData.length > 0 ? Object.keys(displayData[0]) : COLUMN_DEFINITIONS[dataType];

  return (
    <div className="fixed inset-0 z-40 flex items-start justify-center p-4 bg-black/50 overflow-y-auto">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-6xl my-8">
        <div className="p-4 border-b flex justify-between items-center bg-gray-50 sticky top-0 z-10">
          <h3 className="font-bold text-lg">📊 {typeLabels[dataType]}</h3>
          <button
            onClick={onClose}
            className="text-lg hover:text-red-500"
          >
            ✕
          </button>
        </div>

        {displayData.length === 0 ? (
          <div className="p-6 text-center">
            <p className="text-gray-500 mb-4">No hay datos. Haz clic en "➕ Agregar fila" para crear nuevos registros.</p>
            <button
              onClick={handleAddRow}
              className="btn-primary text-sm"
            >
              ➕ Agregar fila
            </button>
          </div>
        ) : (
          <>
            <div className="p-4 overflow-x-auto">
              <table className="w-full border-collapse text-sm">
                <thead>
                  <tr className="bg-gray-100 border-b">
                    <th className="border px-2 py-2 w-8 text-center font-semibold text-gray-700">
                      #
                    </th>
                    {columns.map((col) => (
                      <th
                        key={col}
                        className="border px-2 py-2 text-left font-semibold text-gray-700"
                      >
                        {col}
                      </th>
                    ))}
                    <th className="border px-2 py-2 w-12 text-center font-semibold text-gray-700">
                      ✕
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {displayData.map((row, rowIdx) => (
                    <tr key={rowIdx} className="hover:bg-blue-50 border-b">
                      <td className="border px-2 py-2 text-center text-gray-500 text-xs bg-gray-50">
                        {rowIdx + 1}
                      </td>
                      {columns.map((col) => (
                        <td
                          key={`${rowIdx}-${col}`}
                          className="border px-2 py-2"
                          onClick={() => setEditingCell({ row: rowIdx, col })}
                        >
                          {editingCell?.row === rowIdx && editingCell?.col === col ? (
                            <input
                              type="text"
                              value={displayData[rowIdx][col] || ''}
                              onChange={(e) =>
                                handleCellChange(rowIdx, col, e.target.value)
                              }
                              onBlur={() => setEditingCell(null)}
                              onKeyDown={(e) => {
                                if (e.key === 'Enter') setEditingCell(null);
                                if (e.key === 'Escape') {
                                  handleCancel();
                                }
                              }}
                              autoFocus
                              className="w-full px-1 py-0 border rounded"
                            />
                          ) : (
                            <span className="cursor-pointer hover:bg-yellow-100 px-1 rounded block">
                              {displayData[rowIdx][col] || ''}
                            </span>
                          )}
                        </td>
                      ))}
                      <td className="border px-2 py-2 text-center bg-gray-50">
                        <button
                          onClick={() => handleDeleteRow(rowIdx)}
                          className="text-red-500 hover:text-red-700 text-lg font-bold"
                          title="Eliminar fila"
                        >
                          ✕
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="p-4 border-t bg-gray-50">
              <div className="flex justify-between items-center mb-3">
                <div className="text-sm text-gray-600">
                  {displayData.length} registro(s) {hasChanges && '• Hay cambios sin guardar'}
                </div>
                <button
                  onClick={handleAddRow}
                  className="btn-secondary text-sm"
                >
                  ➕ Agregar fila
                </button>
              </div>

              <div className="flex justify-between gap-2">
                <div></div>
                <div className="flex gap-2">
                  <button
                    onClick={handleCancel}
                    className="btn-secondary text-sm"
                  >
                    ❌ Cancelar
                  </button>
                  <button
                    onClick={handleSave}
                    disabled={!hasChanges}
                    className={`btn-primary text-sm ${!hasChanges ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    💾 Guardar Cambios
                  </button>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default DataEditor;
