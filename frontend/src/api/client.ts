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
  uploadAnexo: (file: File, clienteNif?: string, proyectoAcronimo?: string) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const params: any = {};
    if (clienteNif) params.cliente_nif = clienteNif;
    if (proyectoAcronimo) params.proyecto_acronimo = proyectoAcronimo;
    
    console.log(`[API] POST /upload-anexo - cliente: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    
    return (onProgress?: (pct: number) => void) => api.post('/upload-anexo', formData, {
      params,
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent: any) => {
        if (onProgress && progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percentCompleted);
        }
      }
    });
  },

  uploadCVs: (files: File[], clienteNif?: string, proyectoAcronimo?: string) => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    
    // Construir parámetros
    const params = new URLSearchParams();
    if (clienteNif) params.append('cliente_nif', clienteNif);
    if (proyectoAcronimo) params.append('proyecto_acronimo', proyectoAcronimo);
    
    console.log(`[API] POST /upload-cvs - cliente_nif: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    
    return (onProgress?: (pct: number) => void) => api.post('/upload-cvs', formData, {
      params: Object.fromEntries(params),
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
  processCVs: (clienteNif?: string, proyectoAcronimo?: string) => {
    console.log(`[API] POST /process-cvs - cliente_nif: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    return api.post('/process-cvs', null, { params: { cliente_nif: clienteNif, proyecto_acronimo: proyectoAcronimo } });
  },
  
  // Client Management
  listClients: () => api.get('/clientes'),
  deleteClient: (clienteNif: string) => {
    console.log(`[API] DELETE /clientes/${clienteNif}`);
    return api.delete(`/clientes/${encodeURIComponent(clienteNif)}`);
  },

  // Project Management
  listProyectos: (clienteNif: string) => {
    console.log(`[API] GET /clientes/${clienteNif}/proyectos`);
    return api.get(`/clientes/${encodeURIComponent(clienteNif)}/proyectos`);
  },
  createProyecto: (clienteNif: string, proyectoAcronimo: string) => {
    console.log(`[API] POST /clientes/${clienteNif}/proyectos - acronimo: ${proyectoAcronimo}`);
    return api.post(`/clientes/${encodeURIComponent(clienteNif)}/proyectos`, null, { 
      params: { proyecto_acronimo: proyectoAcronimo } 
    });
  },
  
  // Data Management
  getPersonal: (clienteNif?: string, proyectoAcronimo?: string) => {
    console.log(`[API] GET /personal - cliente_nif: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    return api.get('/personal', { params: { cliente_nif: clienteNif, proyecto_acronimo: proyectoAcronimo } });
  },
  updatePersonal: (data: any[], clienteNif?: string) => {
    console.log(`[API] POST /update-personal - cliente_nif: ${clienteNif || 'NONE'} - registros: ${data.length}`);
    return api.post('/update-personal', { data, cliente_nif: clienteNif });
  },
  getColaboraciones: (clienteNif?: string, proyectoAcronimo?: string) => {
    console.log(`[API] GET /colaboraciones - cliente_nif: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    return api.get('/colaboraciones', { params: { cliente_nif: clienteNif, proyecto_acronimo: proyectoAcronimo } });
  },
  updateColaboraciones: (data: any[], clienteNif?: string) => {
    console.log(`[API] POST /update-colaboraciones - cliente_nif: ${clienteNif || 'NONE'} - registros: ${data.length}`);
    return api.post('/update-colaboraciones', { data, cliente_nif: clienteNif });
  },
  getFacturas: (clienteNif?: string, proyectoAcronimo?: string) => {
    console.log(`[API] GET /facturas - cliente_nif: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    return api.get('/facturas', { params: { cliente_nif: clienteNif, proyecto_acronimo: proyectoAcronimo } });
  },
  updateFacturas: (data: any[], clienteNif?: string) => {
    console.log(`[API] POST /update-facturas - cliente_nif: ${clienteNif || 'NONE'} - registros: ${data.length}`);
    return api.post('/update-facturas', { data, cliente_nif: clienteNif });
  },

  // Metadata
  getMetadata: (clienteNif: string) => {
    console.log(`[API] GET /metadata - cliente_nif: ${clienteNif}`);
    return api.get('/metadata', { params: { cliente_nif: clienteNif } });
  },
  
  saveMetadata: (data: any) => {
    console.log(`[API] POST /metadata - cliente_nif: ${data.cliente_nif}`);
    return api.post('/metadata', null, { params: data });
  },
  
  // Validation
  validate: (clienteNif?: string, proyectoAcronimo?: string) => {
    console.log(`[API] POST /validate - cliente_nif: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    return api.post('/validate', null, { params: { cliente_nif: clienteNif, proyecto_acronimo: proyectoAcronimo } });
  },
  
  // Generation
  generateFichas: (clienteNif?: string, proyectoAcronimo?: string, payload?: any) => {
    console.log(`[API] POST /generate-fichas - cliente_nif: ${clienteNif || 'NONE'} - proyecto: ${proyectoAcronimo || 'NONE'}`);
    return api.post('/generate-fichas', payload || {}, { params: { cliente_nif: clienteNif, proyecto_acronimo: proyectoAcronimo } });
  },
  
  // Download
  downloadFichas: (clienteNif?: string, onProgress?: (pct: number) => void) => {
    console.log(`[API] GET /download-fichas - cliente_nif: ${clienteNif || 'NONE (INPUT_DIR)'}`);
    return api.get('/download-fichas', { params: { cliente_nif: clienteNif }, responseType: 'blob', onDownloadProgress: (ev:any) => { if(onProgress && ev.total) onProgress(Math.round((ev.loaded*100)/ev.total)); } });
  },
  downloadFicha: (name: string, clienteNif?: string, onProgress?: (pct: number) => void) => {
    console.log(`[API] GET /download-ficha - cliente_nif: ${clienteNif || 'NONE (INPUT_DIR)'} - archivo: ${name}`);
    return api.get('/download-ficha', { params: { name, cliente_nif: clienteNif }, responseType: 'blob', onDownloadProgress: (ev:any) => { if(onProgress && ev.total) onProgress(Math.round((ev.loaded*100)/ev.total)); } });
  },
  
  // Preview
  previewFicha: (name: string, clienteNif?: string) => {
    console.log(`[API] GET /preview-ficha - cliente_nif: ${clienteNif || 'NONE (INPUT_DIR)'} - archivo: ${name}`);
    return api.get('/preview-ficha', { params: { name, cliente_nif: clienteNif } });
  },
  previewFichaDocx: (name: string, clienteNif?: string) => {
    console.log(`[API] GET /download-ficha (arraybuffer) - cliente_nif: ${clienteNif || 'NONE (INPUT_DIR)'} - archivo: ${name}`);
    return api.get('/download-ficha', { params: { name, cliente_nif: clienteNif }, responseType: 'arraybuffer' });
  },
};

export default api;
