import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health Check
  healthCheck: () => api.get('/'),

  // Upload Files
  uploadAnexo: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return (onProgress?: (pct: number) => void) => api.post('/upload-anexo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent: any) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      }
    });
  },

  uploadCVs: (files: File[]) => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    return (onProgress?: (pct: number) => void) => api.post('/upload-cvs', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent: any) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      }
    });
  },

  // Processing
  processAnexo: () => api.post('/upload-anexo'),
  processCVs: () => api.post('/process-cvs'),
  
  // Client Management
  listClients: () => api.get('/clientes'),
  
  // Data Management
  getPersonal: (clienteNif?: string) => api.get('/personal', { params: { cliente_nif: clienteNif } }),
  updatePersonal: (data: any[], clienteNif?: string) => api.post('/update-personal', { data, cliente_nif: clienteNif }),
  getColaboraciones: (clienteNif?: string) => api.get('/colaboraciones', { params: { cliente_nif: clienteNif } }),
  updateColaboraciones: (data: any[], clienteNif?: string) => api.post('/update-colaboraciones', { data, cliente_nif: clienteNif }),
  getFacturas: (clienteNif?: string) => api.get('/facturas', { params: { cliente_nif: clienteNif } }),
  updateFacturas: (data: any[], clienteNif?: string) => api.post('/update-facturas', { data, cliente_nif: clienteNif }),
  
  // Validation
  validate: () => api.post('/validate'),
  
  // Generation
  generateFichas: (payload?: any) => api.post('/generate-fichas', payload || {}),
  
  // Download
  downloadFichas: (onProgress?: (pct: number) => void) => api.get('/download-fichas', { responseType: 'blob', onDownloadProgress: (ev:any) => { if(onProgress && ev.total) onProgress(Math.round((ev.loaded*100)/ev.total)); } }),
  downloadFicha: (name: string, onProgress?: (pct: number) => void) => api.get('/download-ficha', { params: { name }, responseType: 'blob', onDownloadProgress: (ev:any) => { if(onProgress && ev.total) onProgress(Math.round((ev.loaded*100)/ev.total)); } }),
  
  // Preview
  previewFicha: (name: string) => api.get('/preview-ficha', { params: { name } }),
  previewFichaDocx: (name: string) => api.get('/download-ficha', { params: { name }, responseType: 'arraybuffer' }),
};

export default api;
