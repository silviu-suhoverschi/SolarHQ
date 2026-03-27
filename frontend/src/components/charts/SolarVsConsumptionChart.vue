<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Solar vs Consumption</h3>
    <apexchart type="bar" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** @type {{ month: string, solar: number, load: number }[]} */
  records: { type: Array, required: true },
})

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  xaxis: { categories: props.records.map(r => r.month) },
  yaxis: { labels: { formatter: (v) => `${v} kWh` } },
  colors: ['#f59e0b', '#6366f1'],
  plotOptions: { bar: { columnWidth: '60%' } },
  tooltip: { y: { formatter: (v) => `${v} kWh` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  { name: 'Solar Produced', data: props.records.map(r => r.solar ?? 0) },
  { name: 'Total Consumed', data: props.records.map(r => r.load ?? 0) },
])
</script>
