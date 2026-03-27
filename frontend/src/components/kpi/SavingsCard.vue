<template>
  <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
    <div class="flex items-center gap-2 mb-3">
      <div class="p-2 rounded-lg bg-green-50 dark:bg-green-900/20">
        <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Savings</span>
    </div>
    <div class="text-3xl font-bold text-gray-900 dark:text-white">
      {{ total_savings != null ? total_savings.toLocaleString() : '—' }} {{ currency }}
    </div>
    <div v-if="monthly_avg != null" class="text-sm text-gray-500 mt-1">
      avg {{ monthly_avg.toFixed(0) }} {{ currency }}/month
    </div>
  </div>
</template>

<script setup>
defineProps({
  total_savings: { type: Number, default: null },
  currency: { type: String, default: 'RON' },
  monthly_avg: { type: Number, default: null },
})
</script>
