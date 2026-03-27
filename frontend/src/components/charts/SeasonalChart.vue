<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Seasonal Solar Production</h3>
    <apexchart type="radar" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const props = defineProps({
  /**
   * Average solar production per month.
   * @type {Record<number, number>} Keys 1–12
   */
  seasonalAverages: { type: Object, required: true },
})

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  xaxis: { categories: MONTHS },
  yaxis: { labels: { formatter: (v) => `${v} kWh` } },
  colors: ['#f59e0b'],
  fill: { opacity: 0.4 },
  stroke: { width: 2 },
  tooltip: { y: { formatter: (v) => `${v} kWh` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  {
    name: 'Avg Solar',
    data: Array.from({ length: 12 }, (_, i) => props.seasonalAverages[i + 1] ?? 0),
  },
])
</script>
