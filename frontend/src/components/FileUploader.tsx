import React, { useState } from 'react';
import { apiService } from '../api/client';

interface FileUploaderProps {
  clienteNif?: string | null;
  proyectoAcronimo?: string | null;
  onSuccess: (message: string) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
  onUploadComplete?: () => void;  // ← Callback para refrescar después del upload de Anexo
  onCVsUploadComplete?: () => void;  // ← Callback para procesar después del upload de CVs
}

export const FileUploader: React.FC<FileUploaderProps> = ({ clienteNif, proyectoAcronimo, onSuccess, onError, onLoading, onUploadComplete, onCVsUploadComplete }) => {
  const [anexoFile, setAnexoFile] = useState<File | null>(null);
  const [cvFiles, setCvFiles] = useState<File[]>([]);
  const [anexoProgress, setAnexoProgress] = useState<number>(0);
  const [cvsProgress, setCvsProgress] = useState<number>(0);

  const handleAnexoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.name.endsWith('.xlsx')) {
      setAnexoFile(file);
    } else {
      onError('⚠️ Por favor selecciona un archivo Excel (.xlsx)');
    }
  };

  const handleCVsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const pdfFiles = files.filter(f => f.name.endsWith('.pdf'));
    if (pdfFiles.length !== files.length) {
      onError('⚠️ Solo se aceptan archivos PDF');
    }
    setCvFiles(pdfFiles);
  };

  const uploadAnexo = async () => {
    if (!anexoFile) {
      onError('❌ Selecciona un archivo Anexo');
      return;
    }

    try {
      onLoading(true);
      setAnexoProgress(0);
      console.log(`[FileUploader] Subiendo anexo para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}`);
      const uploadFn = apiService.uploadAnexo(anexoFile, clienteNif || undefined, proyectoAcronimo || undefined);
      const response = await uploadFn((pct:number) => setAnexoProgress(pct));
      onSuccess(`✅ Anexo procesado: ${response.data.message}`);
      setAnexoFile(null);
      setAnexoProgress(0);
      
      // 🔄 Refrescar datos automáticamente después del upload
      console.log('[FileUploader] Anexo cargado exitosamente, refrescando datos...');
      if (onUploadComplete) {
        onUploadComplete();
      }
    } catch (error: any) {
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  const uploadCVs = async () => {
    if (cvFiles.length === 0) {
      onError('❌ Selecciona al menos un CV');
      return;
    }

    try {
      onLoading(true);
      setCvsProgress(0);
      console.log(`[FileUploader] Subiendo ${cvFiles.length} CV(s) para cliente: ${clienteNif} / proyecto: ${proyectoAcronimo || 'NONE'}...`);
      cvFiles.forEach((f, i) => console.log(`   [${i+1}] ${f.name} (${f.size} bytes)`));
      
      const uploadFn = apiService.uploadCVs(cvFiles, clienteNif || undefined, proyectoAcronimo || undefined);
      const response = await uploadFn((pct:number) => {
        console.log(`[FileUploader] Upload Progress: ${pct}%`);
        setCvsProgress(pct);
      });
      
      console.log('[FileUploader] Upload response:', response.data);
      onSuccess(`✅ ${cvFiles.length} CV(s) cargados. Procesando automáticamente...`);
      setCvFiles([]);
      setCvsProgress(0);
      
      // 🔄 Procesar CVs automáticamente después de subir
      console.log('[FileUploader] CVs cargados, llamando callback para procesar...');
      if (onCVsUploadComplete) {
        onCVsUploadComplete();
      }
    } catch (error: any) {
      console.error('[FileUploader] Error:', error);
      onError(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="card mb-6">
      <h2 className="text-2xl font-bold mb-4">📁 Cargar Archivos</h2>

      {/* Anexo II */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Anexo II (Excel)</h3>
        <div className="flex gap-2">
          <input
            type="file"
            accept=".xlsx"
            onChange={handleAnexoChange}
            className="flex-1 input"
          />
          <button
            onClick={uploadAnexo}
            className="btn-primary"
          >
            Cargar Anexo
          </button>
        </div>
        {anexoFile && <p className="text-sm text-green-600 mt-2">✓ {anexoFile.name}</p>}
        {anexoProgress > 0 && (
          <div className="w-full bg-gray-200 rounded mt-2 h-3">
            <div className="bg-blue-500 h-3 rounded" style={{ width: `${anexoProgress}%` }} />
          </div>
        )}
      </div>

      {/* CVs */}
      <div>
        <h3 className="text-lg font-semibold mb-2">CVs (PDF)</h3>
        <div className="flex gap-2">
          <input
            type="file"
            multiple
            accept=".pdf"
            onChange={handleCVsChange}
            className="flex-1 input"
          />
          <button
            onClick={uploadCVs}
            className="btn-secondary"
          >
            Cargar CVs ({cvFiles.length})
          </button>
        </div>
        {cvFiles.length > 0 && (
          <div className="text-sm text-green-600 mt-2">
            ✓ {cvFiles.map(f => f.name).join(', ')}
          </div>
        )}
        {cvsProgress > 0 && (
          <div className="w-full bg-gray-200 rounded mt-2 h-3">
            <div className="bg-blue-500 h-3 rounded" style={{ width: `${cvsProgress}%` }} />
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUploader;
