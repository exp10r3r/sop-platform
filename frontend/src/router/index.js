import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/assets/ip',
    name: 'IPAssets',
    component: () => import('@/views/assets/IPAssets.vue')
  },
  {
    path: '/assets/domain',
    name: 'DomainAssets',
    component: () => import('@/views/assets/DomainAssets.vue')
  },
  {
    path: '/assets/portserver',
    name: 'PortServer',
    component: () => import('@/views/assets/PortServer.vue')
  },
  {
    path: '/assets/webapp',
    name: 'WebApp',
    component: () => import('@/views/assets/WebApp.vue')
  },
  {
    path: '/assets/ssl',
    name: 'SSLCert',
    component: () => import('@/views/assets/SSLCert.vue')
  },
  {
    path: '/risks/poc',
    name: 'PocVulns',
    component: () => import('@/views/risks/PocVulns.vue')
  },
  {
    path: '/risks/version',
    name: 'VersionVulns',
    component: () => import('@/views/risks/VersionVulns.vue')
  },
  {
    path: '/risks/thirdvuln',
    name: 'ThirdVulns',
    component: () => import('@/views/risks/ThirdVulns.vue')
  },
  {
    path: '/risks/riskport',
    name: 'RiskPorts',
    component: () => import('@/views/risks/RiskPorts.vue')
  },
  {
    path: '/intel/vulinfo',
    name: 'VulInfo',
    component: () => import('@/views/intelligence/VulInfo.vue')
  },
  {
    path: '/intel/darkweb',
    name: 'DarkWeb',
    component: () => import('@/views/intelligence/DarkWeb.vue')
  },
  {
    path: '/intel/git',
    name: 'GitMonitor',
    component: () => import('@/views/intelligence/GitMonitor.vue')
  },
  {
    path: '/intel/shadow',
    name: 'ShadowAssets',
    component: () => import('@/views/intelligence/ShadowAssets.vue')
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/Reports.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router