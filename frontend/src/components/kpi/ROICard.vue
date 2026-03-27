<template>
  <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
    <div class="flex items-center gap-2 mb-3">
      <div class="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-900/20">
        <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">ROI</span>
    </div>
    <div class="text-3xl font-bold text-gray-900 dark:text-white">
      {{ roi_percentage != null ? roi_percentage.toFixed(1) : '—' }}%
    </div>
    <div class="text-sm text-gray-500 mt-1">
      on {{ total_invested != null ? total_invested.toLocaleString() : '—' }} {{ currency }} invested
    </div>
    <div v-if="total_returned != null" class="text-xs text-emerald-600 mt-1">
      {{ total_returned.toLocaleString() }} {{ currency }} returned
    </div>
  </div>
</template>

<script setup>
defineProps({
  roi_percentage: { type: Number, default: null },
  total_invested: { type: Number, default: null },
  total_returned: { type: Number, default: null },
  currency: { type: String, default: 'RON' },
})
</script>
