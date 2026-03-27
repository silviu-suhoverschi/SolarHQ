<template>
  <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
    <div class="flex items-center gap-2 mb-3">
      <div class="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/20">
        <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">Export Income</span>
    </div>
    <div class="text-3xl font-bold text-gray-900 dark:text-white">
      {{ total_income != null ? total_income.toLocaleString() : '—' }} {{ currency }}
    </div>
    <div v-if="last_month_income != null" class="mt-1">
      <span class="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300 text-xs">
        last month: {{ last_month_income.toFixed(2) }} {{ currency }}
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  total_income: { type: Number, default: null },
  currency: { type: String, default: 'RON' },
  last_month_income: { type: Number, default: null },
})
</script>
