import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

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