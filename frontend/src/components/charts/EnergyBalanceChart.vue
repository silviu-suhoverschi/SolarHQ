<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Energy Balance (12 Months)</h3>
    <apexchart type="area" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** @type {{ month: string, solar: number, load: number, grid_import: number }[]} */
  records: { type: Array, required: true },
})

const chartOptions = computed(() => ({
  chart: {
    toolbar: { show: false },
    animations: { enabled: true },
    stacked: false,
  },
  xaxis: { categories: props.records.map(r => r.month) },
  yaxis: { labels: { formatter: (v) => `${v} kWh` } },
  colors: ['#f59e0b', '#10b981', '#ef4444'],
  fill: { type: 'gradient', gradient: { opacityFrom: 0.4, opacityTo: 0.1 } },
  stroke: { width: 2, curve: 'smooth' },
  tooltip: { y: { formatter: (v) => `${v} kWh` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  { name: 'Solar Produced', data: props.records.map(r => r.solar ?? 0) },
  { name: 'Self Consumed', data: props.records.map(r => Math.max(0, (r.load ?? 0) - (r.grid_import ?? 0))) },
  { name: 'Grid Import', data: props.records.map(r => r.grid_import ?? 0) },
])
</script>
