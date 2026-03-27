<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Monthly Savings</h3>
    <apexchart type="bar" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** @type {{ month: string, value: number }[]} */
  savings: { type: Array, required: true },
  currency: { type: String, default: 'RON' },
})

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  xaxis: { categories: props.savings.map(s => s.month) },
  yaxis: { labels: { formatter: (v) => `${v} ${props.currency}` } },
  colors: props.savings.map(s => s.value >= 0 ? '#10b981' : '#ef4444'),
  plotOptions: { bar: { distributed: true } },
  legend: { show: false },
  tooltip: { y: { formatter: (v) => `${v} ${props.currency}` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  { name: 'Savings', data: props.savings.map(s => s.value) },
])
</script>
