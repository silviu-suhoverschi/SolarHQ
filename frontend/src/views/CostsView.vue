<template>
  <div class="p-4 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-semibold">Costs</h1>
      <button @click="openModal(null)" class="px-3 py-1.5 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700">
        + Add Cost
      </button>
    </div>

    <div v-if="store.loading" class="flex justify-center py-12">
      <div class="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else-if="store.error" class="rounded-xl bg-red-50 border border-red-200 p-4 text-red-700 text-sm">
      {{ store.error }}
    </div>

    <div v-else-if="store.records.length" class="overflow-x-auto rounded-xl border border-gray-100 shadow-sm">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
          <tr>
            <th class="px-3 py-2 text-left">Date</th>
            <th class="px-3 py-2 text-left">Description</th>
            <th class="px-3 py-2 text-right">Value</th>
            <th class="px-3 py-2 text-right">Total Cost</th>
            <th class="px-3 py-2 text-left">Currency</th>
            <th class="px-3 py-2 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="r in store.records" :key="r.id" class="hover:bg-gray-50">
            <td class="px-3 py-2">{{ r.date }}</td>
            <td class="px-3 py-2">{{ r.description || '—' }}</td>
            <td class="px-3 py-2 text-right">{{ r.value?.toFixed(2) }}</td>
            <td class="px-3 py-2 text-right font-medium">{{ r.total_cost?.toFixed(2) ?? r.value?.toFixed(2) }}</td>
            <td class="px-3 py-2">{{ r.currency }}</td>
            <td class="px-3 py-2 text-right space-x-1">
              <button @click="openModal(r)" class="text-xs text-blue-600 hover:underline">Edit</button>
              <button @click="confirmDelete(r)" class="text-xs text-red-600 hover:underline">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-center py-12 text-gray-400 text-sm">
      No cost records yet. Add installation, subscription, or other costs.
    </div>

    <!-- Add/Edit Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-md mx-4 shadow-xl">
          <h2 class="font-semibold mb-4">{{ editRecord ? 'Edit' : 'Add' }} Cost</h2>
          <form @submit.prevent="saveRecord" class="space-y-3">
            <div>
              <label class="text-xs text-gray-500">Date</label>
              <input v-model="form.date" type="date" required class="input w-full" />
            </div>
            <div>
              <label class="text-xs text-gray-500">Description</label>
              <input v-model="form.description" type="text" class="input w-full" />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-xs text-gray-500">Value</label>
                <input v-model.number="form.value" type="number" step="0.01" required class="input w-full" />
              </div>
              <div>
                <label class="text-xs text-gray-500">Currency</label>
                <select v-model="form.currency" class="input w-full">
                  <option>RON</option>
                  <option>EUR</option>
                  <option>USD</option>
                </select>
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
          <h2 class="font-semibold mb-2">Delete Cost</h2>
          <p class="text-sm text-gray-600 mb-4">Delete this cost entry? This cannot be undone.</p>
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
import { ref, onMounted } from 'vue'
import { useCostsStore } from '@/stores/costs'

const store = useCostsStore()
onMounted(() => store.fetch())

const showModal = ref(false)
const editRecord = ref(null)
const saving = ref(false)
const modalError = ref('')
const form = ref({})

function openModal(record) {
  editRecord.value = record
  form.value = record ? { ...record } : { date: new Date().toISOString().slice(0, 10), value: 0, currency: 'RON', description: '' }
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

const deleteTarget = ref(null)
const deleting = ref(false)

function confirmDelete(record) { deleteTarget.value = record }

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
