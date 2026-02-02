import React, { useState, useEffect } from 'react';
import { apiService } from '../api/client';

interface EditableTableProps {
  title: string;
  subtitle?: string;
  onDataChange: (data: any[]) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const EditableTable: React.FC<EditableTableProps> = ({
  title,
  subtitle,
  onDataChange,
  onError,
  onLoading,
}) => {
  const [data, setData] = useState<any[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [editingCell, setEditingCell] = useState<{ row: number; col: string } | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      onLoading(true);
      const response = await apiService.getPersonal();
      const personal = response.data;
      setData(personal);
      
      if (personal.length > 0) {
        setColumns(Object.keys(personal[0]).filter(key => key !== 'id'));
      }
    } catch (error: any) {
      onError(`❌ Error cargando datos: ${error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleCellChange = (rowIndex: number, column: string, value: any) => {
    const newData = [...data];
    newData[rowIndex][column] = value;
    setData(newData);
    onDataChange(newData);
  };

  const handleAddRow = () => {
    const newRow: any = {};
    columns.forEach(col => {
      newRow[col] = '';
    });
    setData([...data, newRow]);
  };

  const handleDeleteRow = (rowIndex: number) => {
    const newData = data.filter((_, idx) => idx !== rowIndex);
    setData(newData);
    onDataChange(newData);
  };

  const handleSave = async () => {
    try {
      onLoading(true);
      await apiService.updatePersonal(data);
      window.location.reload();
      // onSuccess('✅ Datos guardados exitosamente');
    } catch (error: any) {
      onError(`❌ Error guardando datos: ${error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const handleRefresh = () => {
    loadData();
  };

  return (
    <div className="card mb-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-2xl font-bold">{title}</h2>
          {subtitle && <p className="text-gray-600 text-sm">{subtitle}</p>}
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleRefresh}
            className="btn-secondary btn-sm"
          >
            🔄 Actualizar
          </button>
          <button
            onClick={handleAddRow}
            className="btn-secondary btn-sm"
          >
            ➕ Agregar Fila
          </button>
          <button
            onClick={handleSave}
            className="btn-primary btn-sm"
          >
            💾 Guardar
          </button>
        </div>
      </div>

      {data.length === 0 ? (
        <p className="text-gray-500">No hay datos disponibles. Carga el Anexo primero.</p>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th className="w-12">Acciones</th>
                {columns.map(col => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIdx) => (
                <tr key={rowIdx}>
                  <td className="w-12">
                    <button
                      onClick={() => handleDeleteRow(rowIdx)}
                      className="btn-danger btn-sm text-xs"
                    >
                      🗑️
                    </button>
                  </td>
                  {columns.map(col => (
                    <td
                      key={`${rowIdx}-${col}`}
                      className="cursor-pointer hover:bg-blue-50"
                      onClick={() => setEditingCell({ row: rowIdx, col })}
                    >
                      {editingCell?.row === rowIdx && editingCell?.col === col ? (
                        <input
                          autoFocus
                          type="text"
                          value={row[col] ?? ''}
                          onChange={(e) =>
                            handleCellChange(rowIdx, col, e.target.value)
                          }
                          onBlur={() => setEditingCell(null)}
                          className="input p-1"
                        />
                      ) : (
                        <span className="text-sm">
                          {typeof row[col] === 'object'
                            ? JSON.stringify(row[col])
                            : String(row[col] ?? '')}
                        </span>
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <p className="text-xs text-gray-500 mt-4">
        Total: {data.length} registros | Columnas: {columns.length}
      </p>
    </div>
  );
};

export default EditableTable;
