<template>
  <div class="p-4 space-y-6">
    <h1 class="text-xl font-semibold">Settings</h1>

    <!-- Sensor Configuration -->
    <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-medium">HA Energy Sensors</h2>
        <button @click="discoverSensors" :disabled="discovering" class="px-3 py-1.5 border border-gray-300 text-sm rounded-lg hover:bg-gray-50 disabled:opacity-50">
          {{ discovering ? 'Discovering…' : 'Discover Sensors' }}
        </button>
      </div>

      <div v-if="settingsStore.loading" class="flex justify-center py-6">
        <div class="w-6 h-6 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
      </div>

      <div v-else class="space-y-3">
        <SensorSelect
          v-model="config.sensor_solar"
          label="Solar Production Sensor"
          :options="discovered.solar ?? []"
        />
        <SensorSelect
          v-model="config.sensor_grid_import"
          label="Grid Import Sensor"
          :options="discovered.grid_import ?? []"
        />
        <SensorSelect
          v-model="config.sensor_grid_export"
          label="Grid Export Sensor"
          :options="discovered.grid_export ?? []"
        />
        <SensorSelect
          v-model="config.sensor_load"
          label="Load / Consumption Sensor"
          :options="discovered.load ?? []"
        />
        <SensorSelect
          v-model="config.sensor_battery_charge"
          label="Battery Charge Sensor (optional)"
          :options="discovered.battery_charge ?? []"
        />
        <SensorSelect
          v-model="config.sensor_battery_discharge"
          label="Battery Discharge Sensor (optional)"
          :options="discovered.battery_discharge ?? []"
        />
      </div>

      <div v-if="configError" class="mt-3 text-xs text-red-600">{{ configError }}</div>
      <div v-if="configSuccess" class="mt-3 text-xs text-emerald-600">Configuration saved.</div>

      <button @click="saveConfig" :disabled="configSaving" class="mt-4 w-full px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 disabled:opacity-50">
        {{ configSaving ? 'Saving…' : 'Save Sensor Config' }}
      </button>
    </div>

    <!-- Manual Sync -->
    <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <h2 class="font-medium mb-3">Data Synchronization</h2>
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-600">Last sync from HA</p>
          <p class="text-sm font-medium">{{ settingsStore.config?.last_sync ? new Date(settingsStore.config.last_sync).toLocaleString() : 'Never' }}</p>
        </div>
        <button @click="triggerSync" :disabled="settingsStore.syncing" class="px-4 py-2 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700 disabled:opacity-50">
          {{ settingsStore.syncing ? 'Syncing…' : 'Sync Now' }}
        </button>
      </div>
      <div v-if="syncMessage" class="mt-2 text-xs" :class="syncSuccess ? 'text-emerald-600' : 'text-red-600'">
        {{ syncMessage }}
      </div>
    </div>

    <!-- Investment Settings -->
    <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <h2 class="font-medium mb-3">Solar System</h2>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-xs text-gray-500">Initial Investment ({{ pricingStore.savingsOffset?.currency ?? 'RON' }})</label>
          <input v-model.number="offsetForm.value" type="number" step="0.01" class="input w-full" />
        </div>
        <div>
          <label class="text-xs text-gray-500">Currency</label>
          <select v-model="offsetForm.currency" class="input w-full">
            <option>RON</option><option>EUR</option><option>USD</option>
          </select>
        </div>
      </div>
      <div v-if="offsetError" class="mt-2 text-xs text-red-600">{{ offsetError }}</div>
      <div v-if="offsetSuccess" class="mt-2 text-xs text-emerald-600">Saved.</div>
      <button @click="saveOffset" :disabled="offsetSaving" class="mt-4 w-full px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 disabled:opacity-50">
        {{ offsetSaving ? 'Saving…' : 'Save' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useSettingsStore } from '@/stores/settings'
import { usePricingStore } from '@/stores/pricing'
import SensorSelect from '@/components/SensorSelect.vue'

const settingsStore = useSettingsStore()
const pricingStore = usePricingStore()

const config = reactive({
  sensor_solar: '',
  sensor_grid_import: '',
  sensor_grid_export: '',
  sensor_load: '',
  sensor_battery_charge: '',
  sensor_battery_discharge: '',
})

const discovered = ref({})
const discovering = ref(false)

onMounted(async () => {
  await Promise.all([settingsStore.fetchConfig(), pricingStore.fetchAll()])
  if (settingsStore.config) {
    Object.assign(config, settingsStore.config)
  }
  offsetForm.value = pricingStore.savingsOffset?.value ?? 0
  offsetForm.currency = pricingStore.savingsOffset?.currency ?? 'RON'
})

async function discoverSensors() {
  discovering.value = true
  try {
    await settingsStore.discover()
    discovered.value = settingsStore.discovered ?? {}
  } finally {
    discovering.value = false
  }
}

// Sensor config save
const configSaving = ref(false)
const configError = ref('')
const configSuccess = ref(false)

async function saveConfig() {
  configSaving.value = true
  configError.value = ''
  configSuccess.value = false
  try {
    await settingsStore.saveConfig({ ...config })
    configSuccess.value = true
    setTimeout(() => { configSuccess.value = false }, 3000)
  } catch (err) {
    configError.value = err?.response?.data?.detail ?? 'Save failed'
  } finally {
    configSaving.value = false
  }
}

// Sync
const syncMessage = ref('')
const syncSuccess = ref(false)

async function triggerSync() {
  syncMessage.value = ''
  try {
    await settingsStore.triggerSync()
    syncSuccess.value = true
    syncMessage.value = 'Sync started in background.'
    setTimeout(() => { syncMessage.value = '' }, 4000)
  } catch {
    syncSuccess.value = false
    syncMessage.value = 'Sync failed. Check HA connection.'
  }
}

// Investment offset
const offsetForm = reactive({ value: 0, currency: 'RON' })
const offsetSaving = ref(false)
const offsetError = ref('')
const offsetSuccess = ref(false)

async function saveOffset() {
  offsetSaving.value = true
  offsetError.value = ''
  offsetSuccess.value = false
  try {
    await pricingStore.updateSavingsOffset({ ...offsetForm })
    offsetSuccess.value = true
    setTimeout(() => { offsetSuccess.value = false }, 3000)
  } catch (err) {
    offsetError.value = err?.response?.data?.detail ?? 'Save failed'
  } finally {
    offsetSaving.value = false
  }
}
</script>

<style scoped>
@reference "tailwindcss";
.input {
  @apply mt-0.5 border border-gray-200 rounded-lg px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400;
}
</style>
