import { defineStore } from 'pinia'
import { pricingApi } from '@/api'

export const usePricingStore = defineStore('pricing', {
  state: () => ({
    gridPrices: [],
    prosumerPrices: [],
    savingsOffset: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchAll() {
      this.loading = true
      this.error = null
      try {
        const [grid, prosumer, offset] = await Promise.all([
          pricingApi.listGrid(),
          pricingApi.listProsumer(),
          pricingApi.getSavingsOffset(),
        ])
        this.gridPrices = grid
        this.prosumerPrices = prosumer
        this.savingsOffset = offset
      } catch (err) {
        this.error = 'Failed to fetch pricing data'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async createGrid(data) {
      const record = await pricingApi.createGrid(data)
      this.gridPrices.unshift(record)
      return record
    },
    async createProsumer(data) {
      const record = await pricingApi.createProsumer(data)
      this.prosumerPrices.unshift(record)
      return record
    },
    async updateSavingsOffset(data) {
      this.savingsOffset = await pricingApi.updateSavingsOffset(data)
    },
  },
})
