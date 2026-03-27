<template>
  <div class="p-4 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-semibold">Energy Records</h1>
      <button @click="openModal(null)" class="px-3 py-1.5 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700">
        + Add Record
      </button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="flex justify-center py-12">
      <div class="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <!-- Error -->
    <div v-else-if="store.error" class="rounded-xl bg-red-50 border border-red-200 p-4 text-red-700 text-sm">
      {{ store.error }}
    </div>

    <!-- Table -->
    <div v-else-if="store.records.length" class="overflow-x-auto rounded-xl border border-gray-100 shadow-sm">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
          <tr>
            <th class="px-3 py-2 text-left">Year</th>
            <th class="px-3 py-2 text-left">Month</th>
            <th class="px-3 py-2 text-right">Solar (kWh)</th>
            <th class="px-3 py-2 text-right">Load (kWh)</th>
            <th class="px-3 py-2 text-right">Import (kWh)</th>
            <th class="px-3 py-2 text-right">Export (kWh)</th>
            <th class="px-3 py-2 text-right">Battery</th>
            <th class="px-3 py-2 text-left">Source</th>
            <th class="px-3 py-2 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="r in sortedRecords" :key="r.id" class="hover:bg-gray-50">
            <td class="px-3 py-2">{{ r.year }}</td>
            <td class="px-3 py-2">{{ r.month }}</td>
            <td class="px-3 py-2 text-right">{{ r.solar?.toFixed(1) }}</td>
            <td class="px-3 py-2 text-right">{{ r.load?.toFixed(1) }}</td>
            <td class="px-3 py-2 text-right">{{ r.grid_import?.toFixed(1) }}</td>
            <td class="px-3 py-2 text-right">{{ r.grid_export?.toFixed(1) }}</td>
            <td class="px-3 py-2 text-right">{{ r.battery_charge != null ? r.battery_charge.toFixed(1) : '—' }}</td>
            <td class="px-3 py-2">
              <span v-if="r.source === 'ha_sync'" class="px-1.5 py-0.5 rounded bg-blue-50 text-blue-700 text-xs">HA Sync</span>
              <span v-else class="text-gray-400 text-xs">{{ r.source || 'manual' }}</span>
            </td>
            <td class="px-3 py-2 text-right space-x-1">
              <button @click="openModal(r)" class="text-xs text-blue-600 hover:underline">Edit</button>
              <button @click="confirmDelete(r)" class="text-xs text-red-600 hover:underline">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty state -->
    <div v-else class="text-center py-12 text-gray-400 text-sm">
      No energy records. Add one manually or sync from Home Assistant in Settings.
    </div>

    <!-- Add/Edit Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-md mx-4 shadow-xl">
          <h2 class="font-semibold mb-4">{{ editRecord ? 'Edit' : 'Add' }} Energy Record</h2>
          <form @submit.prevent="saveRecord" class="space-y-3">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-xs text-gray-500">Year</label>
                <input v-model.number="form.year" type="number" min="2000" max="2100" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Month (1-12)</label>
                <input v-model.number="form.month" type="number" min="1" max="12" required class="input w-full" />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-xs text-gray-500">Solar (kWh)</label>
                <input v-model.number="form.solar" type="number" step="0.01" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Load (kWh)</label>
                <input v-model.number="form.load" type="number" step="0.01" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Grid Import (kWh)</label>
                <input v-model.number="form.grid_import" type="number" step="0.01" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Grid Export (kWh)</label>
                <input v-model.number="form.grid_export" type="number" step="0.01" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Battery Charge (optional)</label>
                <input v-model.number="form.battery_charge" type="number" step="0.01" class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Battery Discharge (optional)</label>
                <input v-model.number="form.battery_discharge" type="number" step="0.01" class="input w-full" />
              </div>
            </div>
            <div v-if="modalError" class="text-xs text-red-600">{{ modalError }}</div>
            <div class="flex gap-2 mt-2">
              <button type="submit" :disabled="saving" class="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 disabled:opacity-50">
                {{ saving ? 'Saving…' : 'Save' }}
              </button>
              <button type="button" @click="showModal = false" class="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirmation -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-sm mx-4 shadow-xl">
          <h2 class="font-semibold mb-2">Delete Record</h2>
          <p class="text-sm text-gray-600 mb-4">
            Delete {{ deleteTarget.year }}/{{ deleteTarget.month }}? This cannot be undone.
          </p>
          <div class="flex gap-2">
            <button @click="doDelete" :disabled="deleting" class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 disabled:opacity-50">
              {{ deleting ? 'Deleting…' : 'Delete' }}
            </button>
            <button @click="deleteTarget = null" class="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEnergyStore } from '@/stores/energy'

const store = useEnergyStore()

onMounted(() => store.fetch())

const sortedRecords = computed(() =>
  [...store.records].sort((a, b) => a.year !== b.year ? a.year - b.year : a.month - b.month)
)

// Modal state
const showModal = ref(false)
const editRecord = ref(null)
const saving = ref(false)
const modalError = ref('')
const form = ref({})

function openModal(record) {
  editRecord.value = record
  form.value = record ? { ...record } : { year: new Date().getFullYear(), month: new Date().getMonth() + 1, solar: 0, load: 0, grid_import: 0, grid_export: 0 }
  modalError.value = ''
  showModal.value = true
}

async function saveRecord() {
  saving.value = true
  modalError.value = ''
  try {
    if (editRecord.value) {
      await store.update(editRecord.value.id, form.value)
    } else {
      await store.create(form.value)
    }
    showModal.value = false
  } catch (err) {
    modalError.value = err?.response?.data?.detail ?? 'Save failed'
  } finally {
    saving.value = false
  }
}

// Delete state
const deleteTarget = ref(null)
const deleting = ref(false)

function confirmDelete(record) {
  deleteTarget.value = record
}

async function doDelete() {
  deleting.value = true
  try {
    await store.remove(deleteTarget.value.id)
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
@reference "tailwindcss";
.input {
  @apply mt-0.5 border border-gray-200 rounded-lg px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400;
}
</style>
