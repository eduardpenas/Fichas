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
    return api.post('/upload-anexo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  uploadCVs: (files: File[]) => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    return api.post('/upload-cvs', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  // Processing
  processAnexo: () => api.post('/upload-anexo'),
  processCVs: () => api.post('/process-cvs'),
  
  // Data Management
  getPersonal: () => api.get('/personal'),
  updatePersonal: (data: any[]) => api.post('/update-personal', data),
  
  // Validation
  validate: () => api.post('/validate'),
  
  // Generation
  generateFichas: () => api.post('/generate-fichas'),
};

export default api;
