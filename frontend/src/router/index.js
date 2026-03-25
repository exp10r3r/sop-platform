import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/assets/ip',
    name: 'IPAssets',
    component: () => import('@/views/assets/IPAssets.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/assets/domain',
    name: 'DomainAssets',
    component: () => import('@/views/assets/DomainAssets.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/assets/portserver',
    name: 'PortServer',
    component: () => import('@/views/assets/PortServer.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/assets/webapp',
    name: 'WebApp',
    component: () => import('@/views/assets/WebApp.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/assets/ssl',
    name: 'SSLCert',
    component: () => import('@/views/assets/SSLCert.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/risks/poc',
    name: 'PocVulns',
    component: () => import('@/views/risks/PocVulns.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/risks/version',
    name: 'VersionVulns',
    component: () => import('@/views/risks/VersionVulns.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/risks/thirdvuln',
    name: 'ThirdVulns',
    component: () => import('@/views/risks/ThirdVulns.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/risks/riskport',
    name: 'RiskPorts',
    component: () => import('@/views/risks/RiskPorts.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/intel/vulinfo',
    name: 'VulInfo',
    component: () => import('@/views/intelligence/VulInfo.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/intel/darkweb',
    name: 'DarkWeb',
    component: () => import('@/views/intelligence/DarkWeb.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/intel/git',
    name: 'GitMonitor',
    component: () => import('@/views/intelligence/GitMonitor.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/intel/shadow',
    name: 'ShadowAssets',
    component: () => import('@/views/intelligence/ShadowAssets.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/Reports.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // 需要认证但未登录
  if (to.meta.requiresAuth !== false && !token) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  }
  // 已登录但访问登录页
  else if (to.path === '/login' && token) {
    next({ path: '/' })
  }
  else {
    next()
  }
})

export default router