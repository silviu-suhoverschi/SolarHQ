<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Cumulative Savings vs Investment</h3>
    <apexchart type="line" :options="chartOptions" :series="series" height="250" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** @type {number[]} */
  monthlySavings: { type: Array, required: true },
  /** @type {number} */
  investment: { type: Number, default: 0 },
  currency: { type: String, default: 'RON' },
})

const cumulativeData = computed(() => {
  let total = 0
  return props.monthlySavings.map(v => {
    total += v
    return parseFloat(total.toFixed(2))
  })
})

const paybackMonth = computed(() => {
  return cumulativeData.value.findIndex(v => v >= props.investment)
})

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  xaxis: {
    categories: props.monthlySavings.map((_, i) => `M${i + 1}`),
  },
  yaxis: { labels: { formatter: (v) => `${v} ${props.currency}` } },
  colors: ['#10b981', '#6366f1'],
  stroke: { width: [2, 2], dashArray: [0, 6] },
  fill: { type: ['gradient', 'solid'], gradient: { opacityFrom: 0.3, opacityTo: 0 } },
  annotations: paybackMonth.value >= 0 ? {
    xaxis: [{
      x: `M${paybackMonth.value + 1}`,
      borderColor: '#f59e0b',
      label: { text: 'Payback', style: { color: '#fff', background: '#f59e0b' } },
    }],
  } : {},
  tooltip: { y: { formatter: (v) => `${v} ${props.currency}` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  { name: 'Cumulative Savings', data: cumulativeData.value },
  { name: 'Investment', data: props.monthlySavings.map(() => props.investment) },
])
</script>
