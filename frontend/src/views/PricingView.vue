<template>
  <div class="p-4 space-y-6">
    <h1 class="text-xl font-semibold">Pricing</h1>

    <div v-if="store.loading" class="flex justify-center py-12">
      <div class="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>
    <div v-else-if="store.error" class="rounded-xl bg-red-50 border border-red-200 p-4 text-red-700 text-sm">
      {{ store.error }}
    </div>

    <template v-else>
      <!-- Grid Pricing -->
      <section>
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-medium text-gray-700">Grid Pricing</h2>
          <button @click="openGridModal" class="px-3 py-1.5 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700">
            + Add
          </button>
        </div>
        <div v-if="store.gridPrices.length" class="overflow-x-auto rounded-xl border border-gray-100 shadow-sm">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
              <tr>
                <th class="px-3 py-2 text-left">Year</th>
                <th class="px-3 py-2 text-left">Month</th>
                <th class="px-3 py-2 text-right">Price/kWh</th>
                <th class="px-3 py-2 text-left">Type</th>
                <th class="px-3 py-2 text-left">Currency</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="r in store.gridPrices" :key="r.id" class="hover:bg-gray-50">
                <td class="px-3 py-2">{{ r.year }}</td>
                <td class="px-3 py-2">{{ r.month }}</td>
                <td class="px-3 py-2 text-right">{{ r.price_per_kwh?.toFixed(4) }}</td>
                <td class="px-3 py-2">
                  <span class="px-1.5 py-0.5 rounded text-xs"
                    :class="{
                      'bg-gray-100 text-gray-700': r.time_of_use === 'flat',
                      'bg-orange-50 text-orange-700': r.time_of_use === 'peak',
                      'bg-blue-50 text-blue-700': r.time_of_use === 'offpeak',
                    }">
                    {{ r.time_of_use }}
                  </span>
                </td>
                <td class="px-3 py-2">{{ r.currency }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-center py-6 text-gray-400 text-sm">No grid prices added yet.</div>
      </section>

      <!-- Prosumer Pricing -->
      <section>
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-medium text-gray-700">Prosumer Export Rate</h2>
          <button @click="openProsumerModal" class="px-3 py-1.5 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700">
            + Add
          </button>
        </div>
        <div v-if="store.prosumerPrices.length" class="overflow-x-auto rounded-xl border border-gray-100 shadow-sm">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
              <tr>
                <th class="px-3 py-2 text-left">Year</th>
                <th class="px-3 py-2 text-left">Month</th>
                <th class="px-3 py-2 text-right">Export Rate/kWh</th>
                <th class="px-3 py-2 text-left">Currency</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="r in store.prosumerPrices" :key="r.id" class="hover:bg-gray-50">
                <td class="px-3 py-2">{{ r.year }}</td>
                <td class="px-3 py-2">{{ r.month }}</td>
                <td class="px-3 py-2 text-right">{{ r.export_price_per_kwh?.toFixed(4) }}</td>
                <td class="px-3 py-2">{{ r.currency }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-center py-6 text-gray-400 text-sm">No prosumer rates added yet.</div>
      </section>

      <!-- Investment Settings link -->
      <section class="rounded-2xl border border-gray-100 p-4 shadow-sm bg-gray-50">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="font-medium text-gray-700">Investment Settings</h2>
            <p class="text-xs text-gray-500 mt-0.5">Initial investment, installation year, panel capacity</p>
          </div>
          <RouterLink to="/settings" class="px-3 py-1.5 border border-gray-300 text-sm rounded-lg hover:bg-white">
            Go to Settings →
          </RouterLink>
        </div>
      </section>
    </template>

    <!-- Grid Price Modal -->
    <Teleport to="body">
      <div v-if="showGridModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-md mx-4 shadow-xl">
          <h2 class="font-semibold mb-4">Add Grid Price</h2>
          <form @submit.prevent="saveGridPrice" class="space-y-3">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-xs text-gray-500">Year</label>
                <input v-model.number="gridForm.year" type="number" min="2000" max="2100" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Month</label>
                <input v-model.number="gridForm.month" type="number" min="1" max="12" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Price/kWh</label>
                <input v-model.number="gridForm.price_per_kwh" type="number" step="0.0001" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Type</label>
                <select v-model="gridForm.time_of_use" class="input w-full">
                  <option value="flat">Flat</option>
                  <option value="peak">Peak</option>
                  <option value="offpeak">Off-peak</option>
                </select>
              </div>
              <div>
                <label class="text-xs text-gray-500">Currency</label>
                <select v-model="gridForm.currency" class="input w-full">
                  <option>RON</option><option>EUR</option><option>USD</option>
                </select>
              </div>
            </div>
            <div v-if="gridError" class="text-xs text-red-600">{{ gridError }}</div>
            <div class="flex gap-2 mt-2">
              <button type="submit" :disabled="gridSaving" class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 disabled:opacity-50">
                {{ gridSaving ? 'Saving…' : 'Save' }}
              </button>
              <button type="button" @click="showGridModal = false" class="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Prosumer Modal -->
    <Teleport to="body">
      <div v-if="showProsumerModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-md mx-4 shadow-xl">
          <h2 class="font-semibold mb-4">Add Prosumer Rate</h2>
          <form @submit.prevent="saveProsumerPrice" class="space-y-3">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-xs text-gray-500">Year</label>
                <input v-model.number="prosumerForm.year" type="number" min="2000" max="2100" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Month</label>
                <input v-model.number="prosumerForm.month" type="number" min="1" max="12" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Export Rate/kWh</label>
                <input v-model.number="prosumerForm.export_price_per_kwh" type="number" step="0.0001" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Currency</label>
                <select v-model="prosumerForm.currency" class="input w-full">
                  <option>RON</option><option>EUR</option><option>USD</option>
                </select>
              </div>
            </div>
            <div v-if="prosumerError" class="text-xs text-red-600">{{ prosumerError }}</div>
            <div class="flex gap-2 mt-2">
              <button type="submit" :disabled="prosumerSaving" class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 disabled:opacity-50">
                {{ prosumerSaving ? 'Saving…' : 'Save' }}
              </button>
              <button type="button" @click="showProsumerModal = false" class="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { usePricingStore } from '@/stores/pricing'

const store = usePricingStore()
onMounted(() => store.fetchAll())

// Grid price modal
const showGridModal = ref(false)
const gridForm = ref({})
const gridSaving = ref(false)
const gridError = ref('')

function openGridModal() {
  gridForm.value = { year: new Date().getFullYear(), month: new Date().getMonth() + 1, price_per_kwh: 0, time_of_use: 'flat', currency: 'RON' }
  gridError.value = ''
  showGridModal.value = true
}

async function saveGridPrice() {
  gridSaving.value = true
  gridError.value = ''
  try {
    await store.createGrid(gridForm.value)
    showGridModal.value = false
  } catch (err) {
    gridError.value = err?.response?.data?.detail ?? 'Save failed'
  } finally {
    gridSaving.value = false
  }
}

// Prosumer modal
const showProsumerModal = ref(false)
const prosumerForm = ref({})
const prosumerSaving = ref(false)
const prosumerError = ref('')

function openProsumerModal() {
  prosumerForm.value = { year: new Date().getFullYear(), month: new Date().getMonth() + 1, export_price_per_kwh: 0, currency: 'RON' }
  prosumerError.value = ''
  showProsumerModal.value = true
}

async function saveProsumerPrice() {
  prosumerSaving.value = true
  prosumerError.value = ''
  try {
    await store.createProsumer(prosumerForm.value)
    showProsumerModal.value = false
  } catch (err) {
    prosumerError.value = err?.response?.data?.detail ?? 'Save failed'
  } finally {
    prosumerSaving.value = false
  }
}
</script>

<style scoped>
@reference "tailwindcss";
.input {
  @apply mt-0.5 border border-gray-200 rounded-lg px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400;
}
</style>
