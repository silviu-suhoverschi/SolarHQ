<template>
  <div class="rounded-2xl bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-100 dark:border-gray-700">
    <div class="flex items-center gap-2 mb-3">
      <div class="p-2 rounded-lg bg-blue-50 dark:bg-blue-900/20">
        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <span class="text-sm font-medium text-gray-600 dark:text-gray-400">Payback Period</span>
    </div>

    <div v-if="is_paid_back" class="flex items-center gap-2">
      <span class="text-2xl font-bold text-emerald-600">Paid back!</span>
      <span class="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 text-xs font-medium">✓</span>
    </div>
    <div v-else>
      <div class="text-3xl font-bold text-gray-900 dark:text-white">
        {{ years_to_payback != null ? years_to_payback.toFixed(1) : '—' }} yr
      </div>
      <div v-if="totalMonths > 0" class="mt-2">
        <div class="flex justify-between text-xs text-gray-500 mb-1">
          <span>{{ months_elapsed }} mo elapsed</span>
          <span>{{ totalMonths }} mo total</span>
        </div>
        <div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
          <div
            class="bg-blue-500 h-2 rounded-full transition-all"
            :style="{ width: `${Math.min(100, progressPct)}%` }"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  years_to_payback: { type: Number, default: null },
  is_paid_back: { type: Boolean, default: false },
  months_elapsed: { type: Number, default: 0 },
})

const totalMonths = computed(() => props.years_to_payback != null ? Math.round(props.years_to_payback * 12) : 0)
const progressPct = computed(() => totalMonths.value > 0 ? (props.months_elapsed / totalMonths.value) * 100 : 0)
</script>
