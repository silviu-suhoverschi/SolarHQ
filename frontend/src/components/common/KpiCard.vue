<template>
  <div class="bg-slate-900/50 border border-slate-800 p-5 rounded-2xl hover:border-slate-700 transition-all duration-300 group">
    <div class="flex items-start justify-between mb-3">
      <div class="p-2.5 rounded-xl" :class="colorClass">
        <component :is="icon" class="w-6 h-6" />
      </div>
      <div v-if="trend !== undefined" class="flex items-center gap-1 text-sm font-medium" :class="trend >= 0 ? 'text-emerald-500' : 'text-rose-500'">
        <TrendingUp v-if="trend >= 0" class="w-4 h-4" />
        <TrendingDown v-else class="w-4 h-4" />
        {{ Math.abs(trend) }}%
      </div>
    </div>
    <div class="space-y-1">
      <p class="text-sm font-medium text-slate-400">{{ label }}</p>
      <div class="flex items-baseline gap-2">
        <h3 class="text-2xl font-bold tracking-tight text-slate-100">{{ value }}</h3>
        <span v-if="unit" class="text-sm font-medium text-slate-500">{{ unit }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { TrendingUp, TrendingDown } from 'lucide-vue-next'

const props = defineProps({
  label: String,
  value: [String, Number],
  unit: String,
  icon: Object,
  colorClass: { type: String, default: 'bg-amber-500/10 text-amber-500' },
  trend: Number
})
</script>
