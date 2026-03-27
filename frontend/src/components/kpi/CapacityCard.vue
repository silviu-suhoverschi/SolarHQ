<template>
  <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
    <div class="flex items-center gap-2 mb-3">
      <div class="p-2 rounded-lg bg-orange-50 dark:bg-orange-900/20">
        <svg class="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">Capacity Factor</span>
    </div>
    <div class="text-3xl font-bold text-gray-900 dark:text-white">
      {{ capacity_factor_pct != null ? capacity_factor_pct.toFixed(1) : '—' }}%
    </div>
    <div v-if="avg_peak_sun_hours != null" class="text-sm text-gray-500 mt-1">
      avg {{ avg_peak_sun_hours.toFixed(1) }} peak sun hours/day
    </div>
  </div>
</template>

<script setup>
defineProps({
  capacity_factor_pct: { type: Number, default: null },
  avg_peak_sun_hours: { type: Number, default: null },
})
</script>
