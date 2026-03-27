import axios from 'axios'

const api = axios.create({
  baseURL: '/api',  // relative — works with any Ingress sub-path
  timeout: 30000,
})

api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API error:', error.response?.status, error.config?.url)
    return Promise.reject(error)
  }
)

export const energyApi = {
  list: (year) => api.get('/energy/', { params: year ? { year } : {} }),
  create: (data) => api.post('/energy/', data),
  update: (id, data) => api.put(`/energy/${id}`, data),
  delete: (id) => api.delete(`/energy/${id}`),
}

export const costsApi = {
  list: () => api.get('/costs/'),
  create: (data) => api.post('/costs/', data),
  update: (id, data) => api.put(`/costs/${id}`, data),
  delete: (id) => api.delete(`/costs/${id}`),
}

export const pricingApi = {
  list: () => api.get('/pricing/'),
  create: (data) => api.post('/pricing/', data),
  update: (id, data) => api.put(`/pricing/${id}`, data),
  delete: (id) => api.delete(`/pricing/${id}`),
}

export const dashboardApi = {
  get: () => api.get('/dashboard/'),
}

export const sensorsApi = {
  discover: () => api.get('/sensors/discover'),
  getConfig: () => api.get('/sensors/config'),
  saveConfig: (data) => api.post('/sensors/config', data),
  triggerSync: () => api.post('/sensors/sync'),
}

export const exportApi = {
  downloadCsv: () => api.get('/export/csv', { responseType: 'blob' }),
}

export default api
