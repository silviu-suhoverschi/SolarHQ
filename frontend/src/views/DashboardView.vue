<template>
  <div class="p-4 space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-semibold">Solar Dashboard</h1>
      <span class="text-xs text-gray-400">
        Last sync: {{ lastSync ? formatDate(lastSync) : 'Never' }}
      </span>
    </div>

    <!-- Loading -->
    <div v-if="dashboardStore.loading" class="flex justify-center py-12">
      <div class="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <!-- Error -->
    <div v-else-if="dashboardStore.error" class="rounded-xl bg-red-50 border border-red-200 p-4 text-red-700 text-sm">
      {{ dashboardStore.error }}
    </div>

    <template v-else-if="dashboardStore.data">
      <!-- KPI Cards Grid -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <ROICard
          :roi_percentage="dashboardStore.data.roi?.roi_percent"
          :total_invested="dashboardStore.data.roi?.total_investment"
          :currency="dashboardStore.data.savings?.currency"
        />
        <SavingsCard
          :total_savings="dashboardStore.data.savings?.total"
          :currency="dashboardStore.data.savings?.currency"
          :monthly_avg="monthlyAvg"
        />
        <PaybackCard
          :years_to_payback="dashboardStore.data.payback?.months_to_payback != null ? dashboardStore.data.payback.months_to_payback / 12 : null"
          :is_paid_back="dashboardStore.data.payback?.status === 'paid_back'"
          :months_elapsed="0"
        />
        <SelfConsumptionCard
          :rate_pct="dashboardStore.data.self_consumption?.self_consumption_percent"
          :self_consumed_kwh="dashboardStore.data.self_consumption?.self_consumed_kwh"
          :total_solar_kwh="dashboardStore.data.capacity?.estimated_kwp"
        />
        <SolarPriceCard
          :price_per_kwh="dashboardStore.data.solar_price?.cost_per_kwh_produced"
          :currency="dashboardStore.data.savings?.currency"
        />
        <ExportIncomeCard
          :total_income="dashboardStore.data.export_income?.total_export_income"
          :currency="dashboardStore.data.export_income?.currency"
          :last_month_income="lastMonthExportIncome"
        />
        <CapacityCard
          :capacity_factor_pct="dashboardStore.data.capacity?.avg_capacity_factor != null ? dashboardStore.data.capacity.avg_capacity_factor * 100 : null"
          :avg_peak_sun_hours="dashboardStore.data.capacity?.avg_peak_sun_hours"
        />
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <MonthlySavingsChart
          :savings="monthlySavingsForChart"
          :currency="dashboardStore.data.savings?.currency"
        />
        <SolarVsConsumptionChart :records="energyStore.records" />
        <GridImportExportChart :records="energyStore.records" />
        <CumulativeSavingsChart
          :monthly-savings="monthlySavingsAmounts"
          :investment="dashboardStore.data.roi?.total_investment ?? 0"
          :currency="dashboardStore.data.savings?.currency"
        />
      </div>
    </template>

    <!-- Empty state -->
    <div v-else class="text-center py-12 text-gray-400 text-sm">
      No data available. Configure sensors and trigger a sync in Settings.
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { useEnergyStore } from '@/stores/energy'

import ROICard from '@/components/kpi/ROICard.vue'
import SavingsCard from '@/components/kpi/SavingsCard.vue'
import PaybackCard from '@/components/kpi/PaybackCard.vue'
import SelfConsumptionCard from '@/components/kpi/SelfConsumptionCard.vue'
import SolarPriceCard from '@/components/kpi/SolarPriceCard.vue'
import ExportIncomeCard from '@/components/kpi/ExportIncomeCard.vue'
import CapacityCard from '@/components/kpi/CapacityCard.vue'

import MonthlySavingsChart from '@/components/charts/MonthlySavingsChart.vue'
import SolarVsConsumptionChart from '@/components/charts/SolarVsConsumptionChart.vue'
import GridImportExportChart from '@/components/charts/GridImportExportChart.vue'
import CumulativeSavingsChart from '@/components/charts/CumulativeSavingsChart.vue'

const dashboardStore = useDashboardStore()
const energyStore = useEnergyStore()

onMounted(async () => {
  await Promise.all([dashboardStore.fetch(), energyStore.fetch()])
})

const lastSync = computed(() => {
  const records = energyStore.records
  if (!records.length) return null
  return records.reduce((latest, r) => {
    if (!r.last_sync) return latest
    return !latest || r.last_sync > latest ? r.last_sync : latest
  }, null)
})

const monthlyAvg = computed(() => {
  const monthly = dashboardStore.data?.savings?.monthly ?? []
  if (!monthly.length) return null
  return dashboardStore.data.savings.total / monthly.length
})

const monthlySavingsForChart = computed(() => {
  return (dashboardStore.data?.savings?.monthly ?? []).map(m => ({
    month: `${m.year}-${String(m.month).padStart(2, '0')}`,
    value: m.value,
  }))
})

const monthlySavingsAmounts = computed(() =>
  (dashboardStore.data?.savings?.monthly ?? []).map(m => m.value)
)

const lastMonthExportIncome = computed(() => {
  const monthly = dashboardStore.data?.export_income?.monthly_export_income ?? []
  return monthly.length ? monthly[monthly.length - 1].value : null
})

function formatDate(dt) {
  return new Date(dt).toLocaleString()
}
</script>
