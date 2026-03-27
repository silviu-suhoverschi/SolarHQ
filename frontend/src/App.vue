<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col md:flex-row">
    <!-- Navigation Sidebar -->
    <nav class="md:w-64 bg-slate-900/50 border-r border-slate-800 p-4 shrink-0">
      <div class="flex items-center gap-3 mb-8 px-2">
        <div class="p-2 bg-amber-500/10 rounded-lg">
          <Sun class="w-6 h-6 text-amber-500" />
        </div>
        <h1 class="text-xl font-bold tracking-tight">SolarHQ</h1>
      </div>
      
      <div class="space-y-1">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group"
          :class="$route.path === item.path ? 'bg-amber-500/10 text-amber-500' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-100'"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="font-medium">{{ item.name }}</span>
        </router-link>
      </div>

      <div class="mt-auto pt-8 border-t border-slate-800/50">
        <router-link 
          to="/settings"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-slate-400 hover:bg-slate-800 hover:text-slate-100 transition-all"
          :class="{ 'bg-slate-800 text-slate-100': $route.path === '/settings' }"
        >
          <Settings class="w-5 h-5" />
          <span class="font-medium">Settings</span>
        </router-link>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="flex-1 overflow-y-auto">
      <header class="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-slate-950/50 sticky top-0 z-10 backdrop-blur-md">
        <h2 class="text-lg font-semibold">{{ currentRouteName }}</h2>
        <div class="flex items-center gap-4">
          <div class="text-sm text-slate-400 hidden sm:block">Last Sync: {{ store.dashboard?.last_sync || 'Never' }}</div>
          <button @click="store.fetchDashboard()" class="p-2 hover:bg-slate-800 rounded-lg transition-colors">
            <RefreshCw class="w-5 h-5 text-slate-400" :class="{ 'animate-spin': store.loading }" />
          </button>
        </div>
      </header>
      
      <div class="p-6">
        <router-view v-slot="{ Component }">
          <transition 
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="transform translate-y-2 opacity-0"
            enter-to-class="transform translate-y-0 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="transform translate-y-0 opacity-100"
            leave-to-class="transform translate-y-2 opacity-0"
            mode="out-in"
          >
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSolarHQStore } from './stores/solarhq'
import { 
  LayoutDashboard, 
  Zap, 
  Wallet, 
  CircleDollarSign, 
  TrendingUp, 
  Settings, 
  RefreshCw,
  Sun
} from 'lucide-vue-next'

const route = useRoute()
const store = useSolarHQStore()

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Energy Records', path: '/energy', icon: Zap },
  { name: 'Installation Costs', path: '/costs', icon: Wallet },
  { name: 'Grid Pricing', path: '/pricing', icon: CircleDollarSign },
  { name: 'Trends & Analysis', path: '/trends', icon: TrendingUp },
]

const currentRouteName = computed(() => route.name)

onMounted(() => {
  store.fetchDashboard()
  store.fetchConfig()
})
</script>

<style>
/* Smooth transition between views */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
