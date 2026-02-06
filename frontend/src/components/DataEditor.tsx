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

// Mapeo de nombres display para mostrar en la UI
// Las claves internas permanecen igual, solo cambia lo que se muestra
const COLUMN_DISPLAY_NAMES: Record<string, string> = {
  'NIF 2': 'NIF cliente',
};

// Función para obtener el nombre display de una columna
const getDisplayName = (colName: string): string => {
  return COLUMN_DISPLAY_NAMES[colName] || colName;
};

// Crear empty row template based on data type
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
  onDataSaved,
}) => {
  const [data, setData] = useState<any[]>([]);
  const [displayData, setDisplayData] = useState<any[]>([]);
  const [editingCell, setEditingCell] = useState<{ row: number; col: string } | null>(null);
  const [showEditor, setShowEditor] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const [selectedCells, setSelectedCells] = useState<Set<string>>(new Set()); // Celdas seleccionadas: "row-col"

  const typeLabels = {
    personal: 'Personal (Ficha 2.1)',
    colaboraciones: 'Colaboraciones (Ficha 2.2)',
    facturas: 'Facturas (Ficha 2.2)',
  };

  // Obtener todas las celdas disponibles en orden
  const getAllCells = (): Array<{ row: number; col: string }> => {
    const cells: Array<{ row: number; col: string }> = [];
    const columns = displayData.length > 0 ? Object.keys(displayData[0]) : COLUMN_DEFINITIONS[dataType];
    displayData.forEach((_, rowIdx) => {
      columns.forEach(col => {
        cells.push({ row: rowIdx, col });
      });
    });
    return cells;
  };

  // Obtener el índice de una celda
  const getCellIndex = (row: number, col: string): number => {
    return getAllCells().findIndex(c => c.row === row && c.col === col);
  };

  // Navegar a la siguiente celda
  const navigateToNextCell = (currentRow: number, currentCol: string, direction: 'next' | 'prev') => {
    const cells = getAllCells();
    const currentIndex = getCellIndex(currentRow, currentCol);
    const nextIndex = direction === 'next' ? currentIndex + 1 : currentIndex - 1;
    
    if (nextIndex >= 0 && nextIndex < cells.length) {
      const nextCell = cells[nextIndex];
      setEditingCell({ row: nextCell.row, col: nextCell.col });
    }
  };

  // Manejar selección múltiple de celdas
  const handleCellClick = (rowIdx: number, col: string, event: React.MouseEvent) => {
    const cellKey = `${rowIdx}-${col}`;
    const newSelected = new Set(selectedCells);
    
    if (event.ctrlKey || event.metaKey) {
      // Ctrl/Cmd + Click: toggle individual cell
      if (newSelected.has(cellKey)) {
        newSelected.delete(cellKey);
      } else {
        newSelected.add(cellKey);
      }
    } else if (event.shiftKey && editingCell) {
      // Shift + Click: select range (solo en la misma fila o columna)
      newSelected.clear();
      const cells = getAllCells();
      const currentIndex = getCellIndex(editingCell.row, editingCell.col);
      const targetIndex = getCellIndex(rowIdx, col);
      const minIdx = Math.min(currentIndex, targetIndex);
      const maxIdx = Math.max(currentIndex, targetIndex);
      
      for (let i = minIdx; i <= maxIdx; i++) {
        newSelected.add(`${cells[i].row}-${cells[i].col}`);
      }
    } else {
      // Click normal: solo esta celda
      newSelected.clear();
      newSelected.add(cellKey);
    }
    
    setSelectedCells(newSelected);
    setEditingCell({ row: rowIdx, col });
  };

  // Aplicar cambio a una celda o múltiples celdas
  const applyChangeToCell = (rowIndex: number, column: string, value: string) => {
    const newData = [...displayData];
    
    if (selectedCells.size > 1 && selectedCells.has(`${rowIndex}-${column}`)) {
      // Aplicar a todas las celdas seleccionadas
      selectedCells.forEach(cellKey => {
        const [row, col] = cellKey.split('-');
        const rowIdx = parseInt(row);
        newData[rowIdx] = { ...newData[rowIdx], [col]: value };
      });
    } else {
      // Aplicar solo a esta celda
      newData[rowIndex] = { ...newData[rowIndex], [column]: value };
    }
    
    setDisplayData(newData);
    setHasChanges(true);
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
    applyChangeToCell(rowIndex, column, value);
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
      setSelectedCells(new Set());
      onSuccess(`✅ Datos de ${typeLabels[dataType]} guardados (${displayData.length} registros)`);
      
      // Notify parent to refresh available fichas
      setTimeout(() => onDataSaved?.(), 500);
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
    setSelectedCells(new Set());
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
                        {getDisplayName(col)}
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
                      {columns.map((col) => {
                        const cellKey = `${rowIdx}-${col}`;
                        const isSelected = selectedCells.has(cellKey);
                        const isEditing = editingCell?.row === rowIdx && editingCell?.col === col;
                        
                        return (
                          <td
                            key={cellKey}
                            className={`border px-2 py-2 cursor-pointer transition ${
                              isSelected ? 'bg-blue-200' : isEditing ? 'bg-yellow-100' : 'hover:bg-yellow-50'
                            }`}
                            onClick={(e) => handleCellClick(rowIdx, col, e)}
                          >
                            {isEditing ? (
                              <input
                                type="text"
                                value={displayData[rowIdx][col] || ''}
                                onChange={(e) =>
                                  handleCellChange(rowIdx, col, e.target.value)
                                }
                                onBlur={() => setEditingCell(null)}
                                onKeyDown={(e) => {
                                  if (e.key === 'Tab') {
                                    e.preventDefault();
                                    navigateToNextCell(rowIdx, col, e.shiftKey ? 'prev' : 'next');
                                  } else if (e.key === 'Enter') {
                                    setEditingCell(null);
                                  } else if (e.key === 'Escape') {
                                    handleCancel();
                                  }
                                }}
                                autoFocus
                                className="w-full px-1 py-0 border rounded"
                              />
                            ) : (
                              <span className="px-1 rounded block">
                                {displayData[rowIdx][col] || ''}
                              </span>
                            )}
                          </td>
                        );
                      })}
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
