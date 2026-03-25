<template>
  <div class="dashboard">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="welcome">
        <h2>安全运营总览</h2>
        <p class="update-time" v-if="summary.updated_at">
          上次更新: {{ summary.updated_at }}
        </p>
      </div>
      <el-button type="primary" @click="handleSync" :loading="syncing" class="sync-btn">
        <el-icon><Refresh /></el-icon>
        数据同步
      </el-button>
    </div>

    <!-- 统计卡片 -->
    <div class="stat-cards">
      <div class="stat-card">
        <div class="stat-icon ip">
          <el-icon><Monitor /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ summary.assets?.ip_count || 0 }}</div>
          <div class="stat-label">IP资产</div>
        </div>
        <div class="stat-trend up" v-if="trendData.length > 1">
          <el-icon><Top /></el-icon>
          {{ getTrend('ip_count') }}
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon domain">
          <el-icon><Link /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ summary.assets?.domain_count || 0 }}</div>
          <div class="stat-label">域名资产</div>
        </div>
        <div class="stat-trend up" v-if="trendData.length > 1">
          <el-icon><Top /></el-icon>
          {{ getTrend('domain_count') }}
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon vuln">
          <el-icon><Warning /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ summary.risks?.poc_count || 0 }}</div>
          <div class="stat-label">PoC漏洞</div>
        </div>
        <div class="stat-trend down" v-if="trendData.length > 1">
          <el-icon><Bottom /></el-icon>
          {{ getTrend('poc_count') }}
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon intel">
          <el-icon><Document /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ summary.intelligence?.vulinfo_count || 0 }}</div>
          <div class="stat-label">漏洞情报</div>
        </div>
        <div class="stat-trend up" v-if="trendData.length > 1">
          <el-icon><Top /></el-icon>
          {{ getTrend('vulinfo_count') }}
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- 风险等级分布 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>漏洞风险等级分布</h3>
        </div>
        <div class="chart-body">
          <div ref="riskChartRef" class="chart"></div>
        </div>
      </div>

      <!-- 处置状态 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>漏洞处置状态</h3>
        </div>
        <div class="chart-body">
          <div ref="statusChartRef" class="chart"></div>
        </div>
      </div>

      <!-- 资产趋势 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>资产趋势</h3>
        </div>
        <div class="chart-body">
          <div ref="assetTrendRef" class="chart"></div>
        </div>
      </div>

      <!-- 漏洞趋势 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>漏洞趋势</h3>
        </div>
        <div class="chart-body">
          <div ref="vulnTrendRef" class="chart"></div>
        </div>
      </div>

      <!-- 风险等级趋势 -->
      <div class="chart-card full-width">
        <div class="chart-header">
          <h3>风险等级趋势</h3>
        </div>
        <div class="chart-body">
          <div ref="riskLevelTrendRef" class="chart"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { reportsApi } from '@/api'
import { ElMessage } from 'element-plus'
import { Top, Bottom } from '@element-plus/icons-vue'

const summary = ref({})
const trendData = ref([])
const riskChartRef = ref(null)
const statusChartRef = ref(null)
const assetTrendRef = ref(null)
const vulnTrendRef = ref(null)
const riskLevelTrendRef = ref(null)
const syncing = ref(false)

const getTrend = (field) => {
  if (trendData.value.length < 2) return '0%'
  const last = trendData.value[trendData.value.length - 1][field] || 0
  const prev = trendData.value[trendData.value.length - 2][field] || 0
  if (prev === 0) return '新增'
  const change = ((last - prev) / prev * 100).toFixed(1)
  return `${Math.abs(change)}%`
}

const loadSummary = async () => {
  try {
    const res = await reportsApi.getSummary()
    if (res.status) {
      summary.value = res.data
      renderCharts()
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const loadTrendData = async () => {
  try {
    const res = await reportsApi.getTrend(7)
    if (res.status) {
      trendData.value = res.data
      renderTrendCharts()
    }
  } catch (error) {
    console.error('加载趋势数据失败:', error)
  }
}

const handleSync = async () => {
  syncing.value = true
  try {
    const res = await reportsApi.syncData()
    if (res.status) {
      ElMessage.success('数据同步成功')
      await loadSummary()
      await loadTrendData()
    }
  } catch (error) {
    ElMessage.error('数据同步失败')
  } finally {
    syncing.value = false
  }
}

const chartColors = {
  critical: '#ef4444',
  high: '#f97316',
  medium: '#eab308',
  low: '#22c55e',
  primary: '#6366f1',
  secondary: '#8b5cf6'
}

const renderCharts = () => {
  // 风险等级饼图
  const riskChart = echarts.init(riskChartRef.value)
  riskChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#e5e7eb', borderWidth: 1 },
    legend: { bottom: 0, itemWidth: 10, itemHeight: 10, textStyle: { color: '#6b7280' } },
    series: [{
      type: 'pie',
      radius: ['50%', '75%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
      labelLine: { show: false },
      data: [
        { value: summary.value.risks?.by_level?.critical || 0, name: '严重', itemStyle: { color: chartColors.critical } },
        { value: summary.value.risks?.by_level?.high || 0, name: '高危', itemStyle: { color: chartColors.high } },
        { value: summary.value.risks?.by_level?.medium || 0, name: '中危', itemStyle: { color: chartColors.medium } },
        { value: summary.value.risks?.by_level?.low || 0, name: '低危', itemStyle: { color: chartColors.low } }
      ]
    }]
  })

  // 处置状态饼图
  const statusChart = echarts.init(statusChartRef.value)
  statusChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#e5e7eb', borderWidth: 1 },
    legend: { bottom: 0, itemWidth: 10, itemHeight: 10, textStyle: { color: '#6b7280' } },
    series: [{
      type: 'pie',
      radius: ['50%', '75%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
      labelLine: { show: false },
      data: [
        { value: summary.value.risks?.by_status?.unhandled || 0, name: '未处理', itemStyle: { color: '#9ca3af' } },
        { value: summary.value.risks?.by_status?.fixed || 0, name: '已修复', itemStyle: { color: chartColors.low } }
      ]
    }]
  })
}

const renderTrendCharts = () => {
  const dates = trendData.value.map(item => item.date.slice(5)) // 只显示月-日
  const ipCounts = trendData.value.map(item => item.ip_count)
  const domainCounts = trendData.value.map(item => item.domain_count)
  const pocCounts = trendData.value.map(item => item.poc_count)
  const versionCounts = trendData.value.map(item => item.version_count)
  const criticalCounts = trendData.value.map(item => item.critical_count)
  const highCounts = trendData.value.map(item => item.high_count)
  const mediumCounts = trendData.value.map(item => item.medium_count)
  const lowCounts = trendData.value.map(item => item.low_count)

  const commonOption = {
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#e5e7eb', borderWidth: 1 },
    legend: { bottom: 0, itemWidth: 12, itemHeight: 4, textStyle: { color: '#6b7280', fontSize: 11 } },
    grid: { left: '3%', right: '3%', bottom: '18%', top: '8%', containLabel: true },
    xAxis: { type: 'category', data: dates, axisLine: { lineStyle: { color: '#e5e7eb' } }, axisLabel: { color: '#6b7280', fontSize: 11 } },
    yAxis: { type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: '#f3f4f6' } }, axisLabel: { color: '#6b7280', fontSize: 11 } }
  }

  // 资产趋势折线图
  const assetTrendChart = echarts.init(assetTrendRef.value)
  assetTrendChart.setOption({
    ...commonOption,
    series: [
      { name: 'IP资产', type: 'line', data: ipCounts, smooth: true, symbol: 'circle', symbolSize: 6, lineStyle: { width: 2, color: chartColors.primary }, itemStyle: { color: chartColors.primary } },
      { name: '域名资产', type: 'line', data: domainCounts, smooth: true, symbol: 'circle', symbolSize: 6, lineStyle: { width: 2, color: chartColors.secondary }, itemStyle: { color: chartColors.secondary } }
    ]
  })

  // 漏洞趋势折线图
  const vulnTrendChart = echarts.init(vulnTrendRef.value)
  vulnTrendChart.setOption({
    ...commonOption,
    series: [
      { name: 'PoC漏洞', type: 'line', data: pocCounts, smooth: true, symbol: 'circle', symbolSize: 6, lineStyle: { width: 2, color: chartColors.high }, itemStyle: { color: chartColors.high } },
      { name: '版本漏洞', type: 'line', data: versionCounts, smooth: true, symbol: 'circle', symbolSize: 6, lineStyle: { width: 2, color: chartColors.critical }, itemStyle: { color: chartColors.critical } }
    ]
  })

  // 风险等级堆叠面积图
  const riskLevelTrendChart = echarts.init(riskLevelTrendRef.value)
  riskLevelTrendChart.setOption({
    ...commonOption,
    xAxis: { ...commonOption.xAxis, boundaryGap: false },
    series: [
      { name: '严重', type: 'line', stack: 'Total', areaStyle: { opacity: 0.6 }, data: criticalCounts, lineStyle: { width: 0 }, itemStyle: { color: chartColors.critical } },
      { name: '高危', type: 'line', stack: 'Total', areaStyle: { opacity: 0.6 }, data: highCounts, lineStyle: { width: 0 }, itemStyle: { color: chartColors.high } },
      { name: '中危', type: 'line', stack: 'Total', areaStyle: { opacity: 0.6 }, data: mediumCounts, lineStyle: { width: 0 }, itemStyle: { color: chartColors.medium } },
      { name: '低危', type: 'line', stack: 'Total', areaStyle: { opacity: 0.6 }, data: lowCounts, lineStyle: { width: 0 }, itemStyle: { color: chartColors.low } }
    ]
  })
}

onMounted(() => {
  loadSummary()
  loadTrendData()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.welcome h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.update-time {
  font-size: 13px;
  color: #9ca3af;
}

.sync-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 500;
}

.sync-btn:hover {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
}

/* 统计卡片 */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon .el-icon {
  font-size: 24px;
  color: #fff;
}

.stat-icon.ip {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
}

.stat-icon.domain {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}

.stat-icon.vuln {
  background: linear-gradient(135deg, #f97316, #ea580c);
}

.stat-icon.intel {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 12px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 20px;
}

.stat-trend.up {
  color: #16a34a;
  background: #dcfce7;
}

.stat-trend.down {
  color: #dc2626;
  background: #fee2e2;
}

/* 图表网格 */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.chart-card.full-width {
  grid-column: span 2;
}

.chart-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
}

.chart-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
}

.chart-body {
  padding: 16px;
}

.chart {
  height: 280px;
}

/* 响应式 */
@media (max-width: 1200px) {
  .stat-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .chart-card.full-width {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .stat-cards {
    grid-template-columns: 1fr;
  }

  .action-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>