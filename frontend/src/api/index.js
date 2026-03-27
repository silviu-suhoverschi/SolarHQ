import axios from 'axios'

// Derive API base from current page location so it works under any HA Ingress path prefix.
// e.g. https://ha.local/api/hassio_ingress/TOKEN/ → baseURL = .../TOKEN/api
const _basePath = window.location.pathname.replace(/\/$/, '')
const api = axios.create({
  baseURL: `${window.location.origin}${_basePath}/api`,
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
  listGrid: (year) => api.get('/pricing/grid', { params: year ? { year } : {} }),
  createGrid: (data) => api.post('/pricing/grid', data),
  listProsumer: (year) => api.get('/pricing/prosumer', { params: year ? { year } : {} }),
  createProsumer: (data) => api.post('/pricing/prosumer', data),
  getSavingsOffset: () => api.get('/pricing/savings-offset'),
  updateSavingsOffset: (data) => api.put('/pricing/savings-offset', data),
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
