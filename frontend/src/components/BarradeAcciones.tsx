import React, { useRef, useState } from 'react';
import axios from 'axios';
import { Upload, FileText, Cpu, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface Props {
  onRefresh: () => void; // Función para recargar la tabla tras procesar
}

export const BarraDeAcciones: React.FC<Props> = ({ onRefresh }) => {
  const [loading, setLoading] = useState(false);
  const [mensaje, setMensaje] = useState("");
  
  // Referencias ocultas a los inputs de archivos
  const inputExcelRef = useRef<HTMLInputElement>(null);
  const inputCVsRef = useRef<HTMLInputElement>(null);

  // 1. Subir Excel (Anexo)
  const handleUploadExcel = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    setLoading(true);
    setMensaje("Subiendo Excel...");

    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    try {
      await axios.post('http://127.0.0.1:8000/upload-anexo', formData);
      setMensaje("✅ Excel cargado correctamente");
      onRefresh(); // Recargar datos
    } catch (error) {
      console.error(error);
      setMensaje("❌ Error subiendo Excel");
    }
    setLoading(false);
  };

  // 2. Subir CVs (PDFs)
  const handleUploadCVs = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.length) return;
    setLoading(true);
    setMensaje(`Subiendo ${e.target.files.length} CVs...`);

    const formData = new FormData();
    // Añadimos todos los archivos seleccionados
    Array.from(e.target.files).forEach(file => {
      formData.append("files", file);
    });

    try {
      await axios.post('http://127.0.0.1:8000/upload-cvs', formData);
      setMensaje(`✅ ${e.target.files.length} CVs subidos.`);
    } catch (error) {
      console.error(error);
      setMensaje("❌ Error subiendo CVs");
    }
    setLoading(false);
  };

  // 3. Disparar el Procesamiento (Python)
  const handleProcesar = async () => {
    setLoading(true);
    setMensaje("🧠 Analizando CVs y extrayendo experiencia... (Esto puede tardar)");
    
    try {
      const res = await axios.post('http://127.0.0.1:8000/process-cvs');
      setMensaje("✨ ¡Proceso terminado! Datos actualizados.");
      onRefresh(); // ¡Magia! La tabla se actualiza sola
    } catch (error) {
      console.error(error);
      setMensaje("❌ Error en el procesamiento");
    }
    setLoading(false);
  };

  return (
    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
      
      {/* Inputs ocultos */}
      <input type="file" accept=".xlsx,.xls" hidden ref={inputExcelRef} onChange={handleUploadExcel} />
      <input type="file" multiple accept=".pdf" hidden ref={inputCVsRef} onChange={handleUploadCVs} />

      <div className="flex gap-3">
        {/* Botón Excel */}
        <button 
          onClick={() => inputExcelRef.current?.click()}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 hover:bg-green-100 rounded-lg border border-green-200 font-medium transition-colors"
        >
          <Upload size={18} /> Importar Excel
        </button>

        {/* Botón CVs */}
        <button 
          onClick={() => inputCVsRef.current?.click()}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-purple-50 text-purple-700 hover:bg-purple-100 rounded-lg border border-purple-200 font-medium transition-colors"
        >
          <FileText size={18} /> Subir CVs (PDF)
        </button>
      </div>

      {/* Estado Central */}
      {mensaje && (
        <div className={`text-sm font-medium animate-pulse flex items-center gap-2 ${mensaje.includes('❌') ? 'text-red-500' : 'text-blue-600'}`}>
           {loading && <Loader2 className="animate-spin" size={16}/>}
           {mensaje}
        </div>
      )}

      {/* Botón Mágico de Procesar */}
      <button 
        onClick={handleProcesar}
        disabled={loading}
        className={`flex items-center gap-2 px-6 py-2 rounded-lg font-bold text-white shadow-md transition-all 
          ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:scale-105 active:scale-95'}
        `}
      >
        <Cpu size={20} />
        {loading ? 'Procesando...' : 'Auto-Completar con IA'}
      </button>

    </div>
  );
};