import { defineStore } from 'pinia'
import axios from 'axios'

export const useSolarHQStore = defineStore('solarhq', {
  state: () => ({
    dashboard: null,
    config: null,
    loading: false,
    error: null
  }),
  actions: {
    async fetchDashboard() {
      this.loading = true
      try {
        const response = await axios.get('/api/dashboard/')
        this.dashboard = response.data
      } catch (err) {
        this.error = 'Failed to fetch dashboard data'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async fetchConfig() {
      try {
        const response = await axios.get('/api/sensors/config')
        this.config = response.data
      } catch (err) {
        console.error(err)
      }
    }
  }
})
