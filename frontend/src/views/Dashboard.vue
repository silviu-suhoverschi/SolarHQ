<template>
  <div class="space-y-8 animate-in fade-in duration-500">
    <!-- KPI Grit -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <KpiCard 
        label="Total Savings" 
        :value="formatCurrency(store.dashboard?.summary.total_savings)" 
        unit="RON"
        :icon="Wallet"
        color-class="bg-emerald-500/10 text-emerald-500"
      />
      <KpiCard 
        label="ROI" 
        :value="store.dashboard?.summary.roi_percent" 
        unit="%"
        :icon="TrendingUp"
        color-class="bg-amber-500/10 text-amber-500"
      />
      <KpiCard 
        label="Payback Period" 
        :value="store.dashboard?.summary.payback_months" 
        unit="months"
        :icon="Calendar"
        color-class="bg-blue-500/10 text-blue-500"
      />
      <KpiCard 
        label="Self-Consumption" 
        :value="store.dashboard?.energy.self_consumption_percent" 
        unit="%"
        :icon="Zap"
        color-class="bg-violet-500/10 text-violet-500"
      />
    </div>

    <!-- Main Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <ChartCard 
        title="Monthly Savings Trend" 
        :series="savingsSeries" 
        :categories="monthlyCategories"
        :colors="['#10b981']" 
      />
      <ChartCard 
        title="Self-Consumption vs Grid" 
        type="bar"
        :series="energySeries" 
        :categories="monthlyCategories"
        :colors="['#f59e0b', '#3b82f6', '#ef4444']" 
      />
    </div>

    <!-- Secondary Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
       <KpiCard 
        label="Total Investment" 
        :value="formatCurrency(store.dashboard?.summary.total_investment)" 
        unit="RON"
        :icon="CreditCard"
        color-class="bg-slate-500/10 text-slate-400"
      />
      <KpiCard 
        label="Solar Production Cost" 
        :value="store.dashboard?.financial.cost_per_kwh" 
        unit="RON/kWh"
        :icon="Activity"
        color-class="bg-sky-500/10 text-sky-500"
      />
      <KpiCard 
        label="Export Income" 
        :value="formatCurrency(store.dashboard?.financial.export_income)" 
        unit="RON"
        :icon="Coins"
        color-class="bg-yellow-500/10 text-yellow-500"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSolarHQStore } from '../stores/solarhq'
import KpiCard from '../components/common/KpiCard.vue'
import ChartCard from '../components/common/ChartCard.vue'
import { 
  Wallet, 
  TrendingUp, 
  Calendar, 
  Zap, 
  CreditCard, 
  Activity, 
  Coins 
} from 'lucide-vue-next'

const store = useSolarHQStore()

const formatCurrency = (val) => {
  if (!val) return '0.00'
  return val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const monthlyCategories = computed(() => {
  return store.dashboard?.financial.monthly_savings.map(m => `${m.year}-${m.month.toString().padStart(2, '0')}`) || []
})

const savingsSeries = computed(() => ([{
  name: 'Savings',
  data: store.dashboard?.financial.monthly_savings.map(m => m.value) || []
}]))

const energySeries = computed(() => ([
  { name: 'Self Consumed', data: [/* map from metrics if available */] },
  { name: 'Imported', data: [/* ... */] },
  { name: 'Exported', data: [/* ... */] }
]))
</script>
