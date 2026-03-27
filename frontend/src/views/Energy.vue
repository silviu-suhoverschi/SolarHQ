<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    <div class="flex items-center justify-between">
      <div class="space-y-1">
        <h2 class="text-2xl font-bold tracking-tight">Monthly Energy Records</h2>
        <p class="text-slate-400">View and manage your solar production and consumption data.</p>
      </div>
      <div class="flex gap-3">
        <button @click="showAddModal = true" class="flex items-center gap-2 px-4 py-2 bg-amber-500 text-slate-950 font-semibold rounded-xl hover:bg-amber-400 transition-colors">
          <Plus class="w-5 h-5" />
          Add Record
        </button>
        <a href="/api/export/csv" class="flex items-center gap-2 px-4 py-2 bg-slate-800 text-slate-100 font-semibold rounded-xl hover:bg-slate-700 transition-colors border border-slate-700">
          <Download class="w-5 h-5" />
          Export CSV
        </a>
      </div>
    </div>

    <!-- Energy Table -->
    <div class="bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead class="bg-slate-800/50 text-slate-400 text-xs uppercase tracking-wider">
          <tr>
            <th class="px-6 py-4 font-semibold">Period</th>
            <th class="px-6 py-4 font-semibold text-amber-500">Solar (kWh)</th>
            <th class="px-6 py-4 font-semibold text-emerald-500">Load (kWh)</th>
            <th class="px-6 py-4 font-semibold text-blue-500">Import (kWh)</th>
            <th class="px-6 py-4 font-semibold text-rose-500">Export (kWh)</th>
            <th class="px-6 py-4 font-semibold">Source</th>
            <th class="px-6 py-4 font-semibold text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr v-for="record in records" :key="record.id" class="hover:bg-slate-800/30 transition-colors group">
            <td class="px-6 py-4 font-medium text-slate-200">
              {{ record.year }}-{{ record.month.toString().padStart(2, '0') }}
            </td>
            <td class="px-6 py-4 font-mono text-amber-500/90 font-semibold">{{ record.solar.toFixed(2) }}</td>
            <td class="px-6 py-4 font-mono text-emerald-500/90 font-semibold">{{ record.load.toFixed(2) }}</td>
            <td class="px-6 py-4 font-mono text-blue-500/90 font-semibold">{{ record.grid_import.toFixed(2) }}</td>
            <td class="px-6 py-4 font-mono text-rose-500/90 font-semibold">{{ record.grid_export.toFixed(2) }}</td>
            <td class="px-6 py-4">
              <span class="px-2 py-1 rounded-md text-[10px] font-bold uppercase tracking-tight" 
                :class="record.source === 'ha_sync' ? 'bg-blue-500/10 text-blue-400' : 'bg-slate-700 text-slate-400'">
                {{ record.source }}
              </span>
            </td>
            <td class="px-6 py-4 text-right">
              <button @click="deleteRecord(record.id)" class="p-2 text-slate-600 hover:text-rose-500 transition-colors">
                <Trash2 class="w-5 h-5" />
              </button>
            </td>
          </tr>
          <tr v-if="records.length === 0">
            <td colspan="7" class="px-6 py-12 text-center text-slate-500">No records found. Configure sensors or add manual data.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Plus, Download, Trash2 } from 'lucide-vue-next'

const records = ref([])
const showAddModal = ref(false)

const fetchRecords = async () => {
  try {
    const response = await axios.get('/api/energy/')
    records.value = response.data
  } catch (err) {
    console.error('Failed to fetch energy records', err)
  }
}

const deleteRecord = async (id) => {
  if (!confirm('Are you sure you want to delete this record?')) return
  try {
    await axios.delete(`/api/energy/${id}`)
    await fetchRecords()
  } catch (err) {
    alert('Failed to delete record')
  }
}

onMounted(fetchRecords)
</script>
