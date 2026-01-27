import { useEffect, useState, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react'; 
import axios from 'axios';
import type { ColDef, ColGroupDef } from 'ag-grid-community';

import { ModuleRegistry } from 'ag-grid-community';
import { ClientSideRowModelModule } from 'ag-grid-community';
ModuleRegistry.registerModules([ ClientSideRowModelModule ]);

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css"; 

export const TablaPersonal = () => {
  const [rowData, setRowData] = useState([]);

  // Definición de Columnas
  const [colDefs] = useState<(ColDef | ColGroupDef)[]>([
    { field: "Nombre", pinned: 'left', width: 150, filter: true },
    { field: "Apellidos", pinned: 'left', width: 200, filter: true },
    { 
      field: "Puesto actual", 
      headerName: "Puesto Actual", 
      width: 250, 
      editable: true, 
      cellStyle: {'backgroundColor': '#f0f9ff'} 
    },
    { 
      headerName: "Experiencia 1 (Reciente)",
      children: [
        { field: "EMPRESA 1", width: 180, editable: true },
        { field: "PUESTO 1", width: 180, editable: true },
        { field: "PERIODO 1", width: 150, editable: true },
      ]
    },
    { 
      headerName: "Experiencia 2",
      children: [
        { field: "EMPRESA 2", width: 180, editable: true },
        { field: "PUESTO 2", width: 180, editable: true },
        { field: "PERIODO 2", width: 150, editable: true },
      ]
    },
    { 
      headerName: "Experiencia 3",
      children: [
        { field: "EMPRESA 3", width: 180, editable: true },
        { field: "PUESTO 3", width: 180, editable: true },
        { field: "PERIODO 3", width: 150, editable: true },
      ]
    },
  ]);

  const defaultColDef = useMemo<ColDef>(() => {
    return {
      flex: 1, // Esto hace que las columnas se ensanchen para llenar el ancho
      minWidth: 100,
      filter: true,
      floatingFilter: true,
      resizable: true,
    };
  }, []);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/personal');
      setRowData(response.data);
    } catch (error) {
      console.error("Error cargando datos:", error);
    }
  };

  const guardarCambios = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/update-personal', rowData);
      alert("✅ ¡Excel actualizado correctamente!");
    } catch (error) {
      console.error("Error guardando:", error);
      alert("❌ Error al guardar.");
    }
  };

  return (
    <div className="w-full h-full flex flex-col">
      
      {/* Barra Interna (Aprox 60px de alto) */}
      <div className="flex justify-between items-center bg-white p-3 border-b border-gray-100 shrink-0 rounded-t-xl">
        <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
          📊 Base de Datos <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">({rowData.length} registros)</span>
        </h2>
        <div className="flex gap-2">
            <button onClick={fetchData} className="px-3 py-1.5 text-gray-600 bg-gray-50 hover:bg-gray-100 rounded border border-gray-200 text-sm font-medium transition-colors">
                🔄 Refrescar
            </button>
            <button onClick={guardarCambios} className="px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded shadow-sm text-sm font-bold flex items-center gap-2 transition-colors">
                💾 Guardar Todo
            </button>
        </div>
      </div>

      {/* LA TABLA (AG GRID) 
         Aquí está la clave: height calculado matemáticamente.
         100vh (toda la pantalla) - 190px (espacio del header y barra de acciones)
         width: 100% (todo el ancho)
      */}
      <div 
        className="ag-theme-quartz shadow-inner w-full"
        style={{ height: 'calc(100vh - 190px)', width: '100%' }}
      >
        <AgGridReact
            rowData={rowData}
            columnDefs={colDefs}
            defaultColDef={defaultColDef}
            pagination={true}
            paginationPageSize={100}
        />
      </div>
    </div>
  );
};