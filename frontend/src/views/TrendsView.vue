<template>
  <div class="p-4 space-y-6">
    <h1 class="text-xl font-semibold">Trends &amp; Forecasts</h1>

    <div v-if="dashboardStore.loading" class="flex justify-center py-12">
      <div class="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else-if="dashboardStore.error" class="rounded-xl bg-red-50 border border-red-200 p-4 text-red-700 text-sm">
      {{ dashboardStore.error }}
    </div>

    <template v-else-if="trends">
      <!-- Seasonal Analysis -->
      <section>
        <h2 class="text-sm font-medium text-gray-500 mb-3">Seasonal Production Pattern</h2>
        <SeasonalChart :seasonal-averages="seasonalAveragesMap" />
      </section>

      <!-- Year over Year -->
      <section>
        <h2 class="text-sm font-medium text-gray-500 mb-3">Year over Year Comparison</h2>
        <YearOverYearChart :yoy-data="yoyData" :currency="currency" />
      </section>

      <!-- ROI Forecast -->
      <section>
        <h2 class="text-sm font-medium text-gray-500 mb-3">ROI Forecast</h2>
        <div class="rounded-xl bg-white dark:bg-gray-800 p-4 shadow-sm">
          <apexchart type="line" :options="forecastOptions" :series="forecastSeries" height="300" />
        </div>
      </section>

      <!-- Quick stats -->
      <section class="grid grid-cols-2 gap-4">
        <div class="rounded-2xl bg-white dark:bg-gray-800 p-4 shadow-sm border border-gray-100">
          <div class="text-xs text-gray-500">YoY Solar Change</div>
          <div class="text-2xl font-bold mt-1"
            :class="trends.yoy_solar_percent >= 0 ? 'text-emerald-600' : 'text-red-500'">
            {{ trends.yoy_solar_percent >= 0 ? '+' : '' }}{{ trends.yoy_solar_percent.toFixed(1) }}%
          </div>
        </div>
        <div class="rounded-2xl bg-white dark:bg-gray-800 p-4 shadow-sm border border-gray-100">
          <div class="text-xs text-gray-500">MoM Solar Change</div>
          <div class="text-2xl font-bold mt-1"
            :class="trends.mom_solar_percent >= 0 ? 'text-emerald-600' : 'text-red-500'">
            {{ trends.mom_solar_percent >= 0 ? '+' : '' }}{{ trends.mom_solar_percent.toFixed(1) }}%
          </div>
        </div>
      </section>
    </template>

    <div v-else class="text-center py-12 text-gray-400 text-sm">
      Not enough data for trend analysis. Add more energy records.
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import SeasonalChart from '@/components/charts/SeasonalChart.vue'
import YearOverYearChart from '@/components/charts/YearOverYearChart.vue'

const dashboardStore = useDashboardStore()

onMounted(() => {
  if (!dashboardStore.data) dashboardStore.fetch()
})

const trends = computed(() => dashboardStore.data?.trends ?? null)
const currency = computed(() => dashboardStore.data?.savings?.currency ?? 'RON')

// SeasonalChart expects Record<number, number> (month -> avg)
const seasonalAveragesMap = computed(() => {
  const result = {}
  for (const s of trends.value?.seasonal_averages ?? []) {
    result[s.month] = s.avg_solar
  }
  return result
})

// YearOverYearChart expects { year, solar, savings }[]
const yoyData = computed(() =>
  (trends.value?.year_over_year ?? []).map(d => ({
    year: d.year,
    solar: d.total_solar,
    savings: d.total_savings,
  }))
)

// Forecast chart — 3 scenarios
const forecastYears = computed(() => (trends.value?.roi_forecast?.scenarios ?? []).map(s => s.year))

const forecastOptions = computed(() => ({
  chart: { toolbar: { show: false }, animations: { enabled: true } },
  xaxis: { categories: forecastYears.value },
  yaxis: { labels: { formatter: (v) => `${v} ${currency.value}` } },
  colors: ['#10b981', '#3b82f6', '#f59e0b'],
  stroke: { width: 2, dashArray: [0, 4, 4] },
  legend: { position: 'top' },
  tooltip: { y: { formatter: (v) => `${v} ${currency.value}` } },
  theme: { mode: 'light' },
  responsive: [{ breakpoint: 480, options: { chart: { height: 220 } } }],
}))

const forecastSeries = computed(() => {
  const scenarios = trends.value?.roi_forecast?.scenarios ?? []
  return [
    { name: 'Base', data: scenarios.map(s => s.base) },
    { name: 'Optimistic', data: scenarios.map(s => s.optimistic) },
    { name: 'Pessimistic', data: scenarios.map(s => s.pessimistic) },
  ]
})
</script>
