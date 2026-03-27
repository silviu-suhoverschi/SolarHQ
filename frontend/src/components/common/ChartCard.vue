<template>
  <div class="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl flex flex-col h-full">
    <div class="flex items-center justify-between mb-6">
      <h3 class="font-semibold text-slate-200">{{ title }}</h3>
      <slot name="extra"></slot>
    </div>
    <div class="flex-1 min-h-[300px]">
      <apexchart
        v-if="series?.length"
        :type="type"
        :options="chartOptions"
        :series="series"
        height="100%"
        width="100%"
      />
      <div v-else class="h-full flex items-center justify-center text-slate-500 text-sm">
        No data available
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  type: { type: String, default: 'area' },
  series: Array,
  categories: Array,
  colors: { type: Array, default: () => ['#f59e0b', '#10b981', '#3b82f6'] }
})

const chartOptions = computed(() => ({
  chart: {
    toolbar: { show: false },
    fontFamily: 'inherit',
    background: 'transparent',
    foreColor: '#94a3b8',
    animations: { duration: 800 }
  },
  theme: { mode: 'dark' },
  colors: props.colors,
  xaxis: {
    categories: props.categories,
    axisBorder: { show: false },
    axisTicks: { show: false },
  },
  grid: {
    borderColor: '#334155',
    strokeDashArray: 4,
    xaxis: { lines: { show: true } },
    padding: { top: 0, right: 0, bottom: 0, left: 10 }
  },
  stroke: { curve: 'smooth', width: 3 },
  dataLabels: { enabled: false },
  tooltip: { theme: 'dark', x: { show: true } },
  legend: { position: 'top', horizontalAlign: 'right' }
}))
</script>
