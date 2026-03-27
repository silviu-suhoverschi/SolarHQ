<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    <div class="flex items-center justify-between">
      <div class="space-y-1">
        <h2 class="text-2xl font-bold tracking-tight">Installation & Operational Costs</h2>
        <p class="text-slate-400">Track your platform investment to calculate ROI and payback period.</p>
      </div>
      <button @click="showAddModal = true" class="flex items-center gap-2 px-4 py-2 bg-amber-500 text-slate-950 font-semibold rounded-xl hover:bg-amber-400 transition-colors">
        <Plus class="w-5 h-5" />
        Add Cost Item
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="item in costs" :key="item.id" class="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:border-slate-700 transition-all group">
         <div class="flex justify-between items-start mb-4">
            <div class="text-xs font-bold text-slate-500 uppercase tracking-widest">{{ item.date }}</div>
            <button @click="deleteCost(item.id)" class="text-slate-600 hover:text-rose-500 opacity-0 group-hover:opacity-100 transition-all">
              <Trash2 class="w-4 h-4" />
            </button>
         </div>
         <h3 class="text-lg font-semibold text-slate-100 mb-2 truncate">{{ item.description }}</h3>
         <div class="flex items-baseline gap-2">
            <span class="text-2xl font-bold text-amber-500">{{ item.value.toLocaleString() }}</span>
            <span class="text-sm font-medium text-slate-500">{{ item.currency }}</span>
         </div>
      </div>
      <div v-if="costs.length === 0" class="md:col-span-3 border-2 border-dashed border-slate-800 rounded-2xl h-32 flex items-center justify-center text-slate-600 font-medium">
        No costs added yet. Click "Add Cost Item" to start tracking.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Plus, Trash2 } from 'lucide-vue-next'

const costs = ref([])
const showAddModal = ref(false)

const fetchCosts = async () => {
  try {
    const response = await axios.get('/api/costs/')
    costs.value = response.data
  } catch (err) {
    console.error('Failed to fetch costs', err)
  }
}

const deleteCost = async (id) => {
  if (!confirm('Are you sure?')) return
  try {
    await axios.delete(`/api/costs/${id}`)
    await fetchCosts()
  } catch (err) {
    alert('Error deleting cost')
  }
}

onMounted(fetchCosts)
</script>
