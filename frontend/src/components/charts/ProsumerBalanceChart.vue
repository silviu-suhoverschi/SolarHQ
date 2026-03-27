<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Energy Balance</h3>
    <apexchart type="donut" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** @type {number} */
  selfConsumed: { type: Number, default: 0 },
  /** @type {number} */
  exported: { type: Number, default: 0 },
  /** @type {number} */
  imported: { type: Number, default: 0 },
})

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  labels: ['Self Consumed', 'Grid Export', 'Grid Import'],
  colors: ['#10b981', '#3b82f6', '#ef4444'],
  legend: { position: 'bottom' },
  tooltip: { y: { formatter: (v) => `${v.toFixed(1)} kWh` } },
  dataLabels: { formatter: (v) => `${v.toFixed(1)}%` },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  props.selfConsumed,
  props.exported,
  props.imported,
])
</script>
