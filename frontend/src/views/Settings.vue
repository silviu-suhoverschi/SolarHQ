<template>
  <div class="max-w-4xl space-y-8 animate-in fade-in duration-500">
    <div class="space-y-1">
      <h2 class="text-2xl font-bold tracking-tight">Configuration & Sensors</h2>
      <p class="text-slate-400">Manage Home Assistant sensor mapping and synchronization settings.</p>
    </div>

    <!-- Sync Section -->
    <section class="bg-slate-900/50 border border-slate-800 rounded-3xl p-8 space-y-6">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
           <div class="p-3 bg-blue-500/10 rounded-2xl">
             <RefreshCw class="w-6 h-6 text-blue-500" :class="{ 'animate-spin': isSyncing }" />
           </div>
           <div>
             <h3 class="text-lg font-semibold">Cloud Synchronization</h3>
             <p class="text-sm text-slate-500">Last synchronized with Home Assistant: {{ config?.last_sync || 'Never' }}</p>
           </div>
        </div>
        <button @click="manualSync" :disabled="isSyncing" class="px-6 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-100 font-semibold rounded-xl transition-all disabled:opacity-50">
          Sync Now
        </button>
      </div>
    </section>

    <!-- Sensor Mapping -->
    <section class="bg-slate-900/50 border border-slate-800 rounded-3xl overflow-hidden">
      <div class="p-8 border-b border-slate-800 flex items-center justify-between">
         <h3 class="text-lg font-semibold">Sensor Entity IDs</h3>
         <button @click="saveConfig" class="px-6 py-2 bg-amber-500 text-slate-950 font-bold rounded-xl hover:bg-amber-400 transition-all">
           Save Configuration
         </button>
      </div>
      <div class="p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div v-for="field in sensorFields" :key="field.key" class="space-y-2">
           <label class="text-sm font-semibold text-slate-400 ml-1">{{ field.label }}</label>
           <input 
             v-model="config[field.key]" 
             type="text" 
             placeholder="sensor.xxxx"
             class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-all"
           />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { RefreshCw } from 'lucide-vue-next'

const config = ref({})
const isSyncing = ref(false)

const sensorFields = [
  { label: 'Solar Production Entity', key: 'sensor_solar' },
  { label: 'House Load Entity', key: 'sensor_load' },
  { label: 'Grid Import (Buy) Entity', key: 'sensor_grid_import' },
  { label: 'Grid Export (Sell) Entity', key: 'sensor_grid_export' },
  { label: 'Battery Charge Entity', key: 'sensor_battery_charge' },
  { label: 'Battery Discharge Entity', key: 'sensor_battery_discharge' },
]

const fetchConfig = async () => {
  try {
    const response = await axios.get('/api/sensors/config')
    config.value = response.data
  } catch (err) {
    console.error('Failed to fetch config', err)
  }
}

const saveConfig = async () => {
  try {
    await axios.post('/api/sensors/config', config.value)
    alert('Configuration saved successfully')
  } catch (err) {
    alert('Failed to save configuration')
  }
}

const manualSync = async () => {
  isSyncing.value = true
  try {
    await axios.post('/api/sensors/sync')
    alert('Background sync triggered')
  } catch (err) {
    alert('Sync failed')
  } finally {
    isSyncing.value = false
  }
}

onMounted(fetchConfig)
</script>
