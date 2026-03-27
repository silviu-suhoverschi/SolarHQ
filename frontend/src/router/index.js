import { createRouter, createWebHashHistory } from 'vue-router'

// CRITICAL: Hash mode required for HA Ingress
// History mode breaks because HA Ingress doesn't support HTML5 pushState
const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/',         component: () => import('../views/DashboardView.vue') },
    { path: '/energy',   component: () => import('../views/EnergyView.vue') },
    { path: '/costs',    component: () => import('../views/CostsView.vue') },
    { path: '/pricing',  component: () => import('../views/PricingView.vue') },
    { path: '/trends',   component: () => import('../views/TrendsView.vue') },
    { path: '/settings', component: () => import('../views/SettingsView.vue') },
  ],
})

export default router
