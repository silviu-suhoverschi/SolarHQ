<template>
  <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
    <div class="flex items-center gap-2 mb-3">
      <div class="p-2 rounded-lg bg-yellow-50 dark:bg-yellow-900/20">
        <svg class="w-4 h-4 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">Solar Price</span>
    </div>
    <div class="text-3xl font-bold text-gray-900 dark:text-white">
      {{ price_per_kwh != null ? price_per_kwh.toFixed(3) : '—' }} {{ currency }}/kWh
    </div>
    <div v-if="vs_grid_price != null && price_per_kwh != null" class="mt-1">
      <span
        class="text-sm font-medium"
        :class="price_per_kwh <= vs_grid_price ? 'text-emerald-600' : 'text-amber-600'"
      >
        {{ price_per_kwh <= vs_grid_price ? '▼ cheaper' : '▲ more expensive' }} than grid ({{ vs_grid_price.toFixed(3) }} {{ currency }})
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  price_per_kwh: { type: Number, default: null },
  currency: { type: String, default: 'RON' },
  vs_grid_price: { type: Number, default: null },
})
</script>
