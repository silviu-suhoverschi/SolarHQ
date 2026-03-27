<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Year over Year</h3>
    <apexchart type="line" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /**
   * @type {{ year: number, solar: number, savings: number }[]}
   */
  yoyData: { type: Array, required: true },
  currency: { type: String, default: 'RON' },
})

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  xaxis: { categories: props.yoyData.map(d => d.year) },
  yaxis: [
    { labels: { formatter: (v) => `${v} kWh` }, title: { text: 'Solar (kWh)' } },
    { opposite: true, labels: { formatter: (v) => `${v} ${props.currency}` }, title: { text: `Savings (${props.currency})` } },
  ],
  colors: ['#f59e0b', '#10b981'],
  stroke: { width: 2, curve: 'smooth' },
  markers: { size: 4 },
  tooltip: { shared: true },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  { name: 'Solar Produced', data: props.yoyData.map(d => d.solar ?? 0) },
  { name: 'Savings', data: props.yoyData.map(d => d.savings ?? 0) },
])
</script>
