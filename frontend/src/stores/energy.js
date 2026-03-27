import { defineStore } from 'pinia'
import { energyApi } from '@/api'

export const useEnergyStore = defineStore('energy', {
  state: () => ({
    records: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetch(year = null) {
      this.loading = true
      this.error = null
      try {
        this.records = await energyApi.list(year)
      } catch (err) {
        this.error = 'Failed to fetch energy records'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async create(data) {
      const record = await energyApi.create(data)
      this.records.push(record)
      return record
    },
    async update(id, data) {
      const updated = await energyApi.update(id, data)
      const idx = this.records.findIndex(r => r.id === id)
      if (idx !== -1) this.records[idx] = updated
      return updated
    },
    async remove(id) {
      await energyApi.delete(id)
      this.records = this.records.filter(r => r.id !== id)
    },
  },
})
