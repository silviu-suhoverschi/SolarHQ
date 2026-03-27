import { defineStore } from 'pinia'
import { sensorsApi } from '@/api'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    config: null,
    discovered: null,
    loading: false,
    syncing: false,
    error: null,
  }),
  actions: {
    async fetchConfig() {
      this.loading = true
      this.error = null
      try {
        this.config = await sensorsApi.getConfig()
      } catch (err) {
        this.error = 'Failed to fetch config'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async saveConfig(data) {
      this.config = await sensorsApi.saveConfig(data)
    },
    async discover() {
      this.loading = true
      try {
        this.discovered = await sensorsApi.discover()
      } catch (err) {
        this.error = 'Failed to discover sensors'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async triggerSync() {
      this.syncing = true
      try {
        await sensorsApi.triggerSync()
      } finally {
        this.syncing = false
      }
    },
  },
})
