<template>
  <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
    <div class="flex items-center gap-2 mb-3">
      <div class="p-2 rounded-lg bg-teal-50 dark:bg-teal-900/20">
        <svg class="w-4 h-4 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">Self-Consumption</span>
    </div>
    <div class="text-3xl font-bold text-gray-900 dark:text-white">
      {{ rate_pct != null ? rate_pct.toFixed(1) : '—' }}%
    </div>
    <div class="mt-2">
      <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
        <div
          class="bg-teal-500 h-2 rounded-full transition-all"
          :style="{ width: `${Math.min(100, rate_pct ?? 0)}%` }"
        />
      </div>
    </div>
    <div v-if="self_consumed_kwh != null && total_solar_kwh != null" class="text-xs text-gray-500 mt-1">
      {{ self_consumed_kwh.toFixed(0) }} kWh of {{ total_solar_kwh.toFixed(0) }} kWh
    </div>
  </div>
</template>

<script setup>
defineProps({
  rate_pct: { type: Number, default: null },
  self_consumed_kwh: { type: Number, default: null },
  total_solar_kwh: { type: Number, default: null },
})
</script>
