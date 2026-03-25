import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器 - 自动携带Token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 401 未登录或Token过期
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      // 跳转到登录页
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    ElMessage.error(error.response?.data?.detail || error.message || '请求失败')
    return Promise.reject(error)
  }
)

// 认证相关API
export const authApi = {
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
  changePassword: (data) => api.put('/auth/password', data),
  getUsers: () => api.get('/auth/users'),
  register: (data) => api.post('/auth/register', data),
  deleteUser: (id) => api.delete(`/auth/users/${id}`),
  getAuditLogs: (params) => api.get('/auth/audit-logs', { params })
}

// 资产相关API
export const assetsApi = {
  getIPAssets: (params) => api.get('/assets/ip', { params }),
  getDomains: (params) => api.get('/assets/domain', { params }),
  getPortServers: (params) => api.get('/assets/portserver', { params }),
  getWebApps: (params) => api.get('/assets/webapp', { params }),
  getURLs: (params) => api.get('/assets/url', { params }),
  getSSLCerts: (params) => api.get('/assets/ssl', { params })
}

// 风险相关API
export const risksApi = {
  getPocVulns: (params) => api.get('/risks/poc', { params }),
  getVersionVulns: (params) => api.get('/risks/version', { params }),
  getThirdVulns: (params) => api.get('/risks/thirdvuln', { params }),
  getRiskPorts: (params) => api.get('/risks/riskport', { params }),
  getAbnormalPorts: (params) => api.get('/risks/abnormal-port', { params })
}

// 情报相关API
export const intelApi = {
  getVulInfo: (params) => api.get('/intel/vulinfo', { params }),
  getDarkWeb: (params) => api.get('/intel/darkweb', { params }),
  getGitMonitor: (params) => api.get('/intel/git', { params }),
  getShadowAssets: (params) => api.get('/intel/shadow', { params }),
  getIMMonitor: (params) => api.get('/intel/im', { params }),
  getMailMonitor: (params) => api.get('/intel/mails', { params })
}

// 报表相关API
export const reportsApi = {
  getSummary: () => api.get('/reports/summary'),
  getAssetsReport: () => api.get('/reports/assets'),
  getRisksReport: () => api.get('/reports/risks'),
  getIntelligenceReport: () => api.get('/reports/intelligence'),
  getTrend: (days = 7) => api.get('/reports/trend', { params: { days } }),
  syncData: () => api.post('/reports/sync')
}

export default api