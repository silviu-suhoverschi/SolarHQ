<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Grid Import / Export</h3>
    <apexchart type="bar" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** @type {{ month: string, grid_import: number, grid_export: number }[]} */
  records: { type: Array, required: true },
})

const chartOptions = computed(() => ({
  chart: {
    toolbar: { show: false },
    animations: { enabled: true },
    stacked: true,
  },
  xaxis: { categories: props.records.map(r => r.month) },
  yaxis: { labels: { formatter: (v) => `${v} kWh` } },
  colors: ['#ef4444', '#10b981'],
  plotOptions: { bar: { columnWidth: '60%' } },
  tooltip: { y: { formatter: (v) => `${Math.abs(v)} kWh` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  { name: 'Grid Import', data: props.records.map(r => r.grid_import ?? 0) },
  { name: 'Grid Export', data: props.records.map(r => -(r.grid_export ?? 0)) },
])
</script>
