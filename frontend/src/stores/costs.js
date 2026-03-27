import { defineStore } from 'pinia'
import { costsApi } from '@/api'

export const useCostsStore = defineStore('costs', {
  state: () => ({
    records: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetch() {
      this.loading = true
      this.error = null
      try {
        this.records = await costsApi.list()
      } catch (err) {
        this.error = 'Failed to fetch costs'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async create(data) {
      const record = await costsApi.create(data)
      this.records.unshift(record)
      return record
    },
    async update(id, data) {
      const updated = await costsApi.update(id, data)
      const idx = this.records.findIndex(r => r.id === id)
      if (idx !== -1) this.records[idx] = updated
      return updated
    },
    async remove(id) {
      await costsApi.delete(id)
      this.records = this.records.filter(r => r.id !== id)
    },
  },
})
