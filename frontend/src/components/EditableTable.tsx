import React, { useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import { apiService } from '../api/client';

interface EditableTableProps {
  clienteNif: string | null;
  proyectoAcronimo?: string | null;
  title: string;
  subtitle?: string;
  onDataChange: (data: any[]) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const EditableTable = forwardRef<any, EditableTableProps>(({
  clienteNif,
  proyectoAcronimo,
  title,
  subtitle,
  onDataChange,
  onError,
  onLoading,
}, ref) => {
  const [data, setData] = useState<any[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [editingCell, setEditingCell] = useState<{ row: number; col: string } | null>(null);

  useEffect(() => {
    loadData();
  }, [clienteNif, proyectoAcronimo]);

  const loadData = async () => {
    try {
      onLoading(true);
      console.log(`\n============================================================`);
      console.log(`📊 EDITABLETABLE - LOADDATA INICIADO`);
      console.log(`   cliente_nif: ${clienteNif}`);
      console.log(`   proyecto: ${proyectoAcronimo}`);
      console.log(`============================================================`);
      
      const response = await apiService.getPersonal(clienteNif || undefined, proyectoAcronimo || undefined);
      const personal = response.data;
      
      console.log(`✅ Datos obtenidos del backend: ${personal.length} registros`);
      if (personal.length > 0) {
        console.log(`   Primer registro:`, personal[0]);
      }
      
      setData(personal);
      
      if (personal.length > 0) {
        const cols = Object.keys(personal[0]).filter(key => key !== 'id');
        console.log(`   Columnas: ${cols.length} - ${cols.join(', ').substring(0, 50)}...`);
        setColumns(cols);
      } else {
        console.log(`   ⚠️ Sin datos, limpiando columnas`);
        setColumns([]);
      }
      
      console.log(`============================================================\n`);
    } catch (error: any) {
      console.error(`❌ Error cargando datos:`, error);
      onError(`❌ Error cargando datos: ${error.message}`);
    } finally {
      onLoading(false);
    }
  };

  // Exponer loadData mediante ref
  useImperativeHandle(ref, () => ({
    loadData
  }));

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
      await apiService.updatePersonal(data, clienteNif || undefined, proyectoAcronimo || undefined);
      // Recargar datos sin salir del cliente
      await loadData();
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
                          className="input p-2 text-sm"
                        />
                      ) : (
                        <span className="text-sm block truncate max-w-xs" title={String(row[col] ?? '')}>
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
});

EditableTable.displayName = 'EditableTable';

export default EditableTable;
