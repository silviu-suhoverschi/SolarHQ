import { defineStore } from 'pinia'
import { dashboardApi } from '@/api'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    data: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetch() {
      this.loading = true
      this.error = null
      try {
        this.data = await dashboardApi.get()
      } catch (err) {
        this.error = 'Failed to fetch dashboard data'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
  },
})
