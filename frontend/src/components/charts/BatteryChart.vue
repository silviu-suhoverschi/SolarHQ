<template>
  <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
    <h3 class="text-sm font-medium text-gray-500 mb-3">Battery Activity</h3>
    <div v-if="hasBatteryData">
      <apexchart type="area" :options="chartOptions" :series="series" height="250" />
    </div>
    <div v-else class="flex items-center justify-center h-40 text-gray-400 text-sm">
      No battery data available
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** @type {{ month: string, battery_charge: number|null, battery_discharge: number|null }[]} */
  records: { type: Array, required: true },
})

const hasBatteryData = computed(() =>
  props.records.some(r => (r.battery_charge ?? 0) > 0 || (r.battery_discharge ?? 0) > 0)
)

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  xaxis: { categories: props.records.map(r => r.month) },
  yaxis: { labels: { formatter: (v) => `${v} kWh` } },
  colors: ['#8b5cf6', '#ec4899'],
  fill: { opacity: 0.4 },
  stroke: { width: 2 },
  tooltip: { y: { formatter: (v) => `${v} kWh` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 200 } } }],
}))

const series = computed(() => [
  { name: 'Battery Charge', data: props.records.map(r => r.battery_charge ?? 0) },
  { name: 'Battery Discharge', data: props.records.map(r => r.battery_discharge ?? 0) },
])
</script>
