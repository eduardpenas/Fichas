import { useState } from 'react';
import { TablaPersonal } from './components/TablaPersonal';
import { BarraDeAcciones } from './components/BarradeAcciones';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="h-screen bg-gray-50 font-sans text-gray-900 flex flex-col overflow-hidden">
      
      {/* Header Fijo */}
      <header className="bg-white border-b border-gray-200 px-6 py-3 shrink-0 z-20 shadow-sm">
        <div className="w-full flex justify-between items-center">
          <div className="flex items-center gap-3">
             <div className="bg-blue-600 text-white p-2 rounded-lg shadow-sm">🚀</div>
             <div>
                <h1 className="text-xl font-extrabold text-gray-900 leading-tight">Generador de Fichas</h1>
                <p className="text-xs text-gray-500 font-medium">Dashboard Profesional v3.0 (Full Screen)</p>
             </div>
          </div>
          <div className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-bold border border-green-200">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            Sistema Online
          </div>
        </div>
      </header>

      {/* Contenido Principal - Ocupa TODO el ancho y alto restante */}
      <main className="flex-1 p-4 w-full flex flex-col min-h-0">
        
        {/* Barra de Acciones */}
        <div className="mb-4 shrink-0">
           <BarraDeAcciones onRefresh={handleRefresh} />
        </div>

        {/* Contenedor Tabla - Crece para llenar el hueco */}
        <div className="flex-1 bg-white rounded-xl shadow-lg border border-gray-200 p-1 flex flex-col overflow-hidden">
           <TablaPersonal key={refreshKey} />
        </div>

      </main>
    </div>
  );
}

export default App;