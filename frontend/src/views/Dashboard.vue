<template>
  <div class="dashboard">
    <!-- 操作栏 -->
    <div class="action-bar">
      <el-button type="primary" @click="handleSync" :loading="syncing">
        <el-icon><Refresh /></el-icon>数据同步
      </el-button>
      <span class="update-time" v-if="summary.updated_at">
        上次更新: {{ summary.updated_at }}
      </span>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #409EFF;">
            <el-icon><Monitor /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ summary.assets?.ip_count || 0 }}</div>
            <div class="stat-label">IP资产</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #67C23A;">
            <el-icon><Link /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ summary.assets?.domain_count || 0 }}</div>
            <div class="stat-label">域名资产</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #E6A23C;">
            <el-icon><Warning /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ summary.risks?.poc_count || 0 }}</div>
            <div class="stat-label">PoC漏洞</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #F56C6C;">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ summary.intelligence?.vulinfo_count || 0 }}</div>
            <div class="stat-label">漏洞情报</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 风险等级分布 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span>漏洞风险等级分布</span>
          </template>
          <div ref="riskChartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span>漏洞处置状态</span>
          </template>
          <div ref="statusChartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 趋势图表 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span>资产趋势</span>
          </template>
          <div ref="assetTrendRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span>漏洞趋势</span>
          </template>
          <div ref="vulnTrendRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span>风险等级趋势</span>
          </template>
          <div ref="riskLevelTrendRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { reportsApi } from '@/api'
import { ElMessage } from 'element-plus'

const summary = ref({})
const trendData = ref([])
const riskChartRef = ref(null)
const statusChartRef = ref(null)
const assetTrendRef = ref(null)
const vulnTrendRef = ref(null)
const riskLevelTrendRef = ref(null)
const syncing = ref(false)

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

const renderCharts = () => {
  // 风险等级饼图
  const riskChart = echarts.init(riskChartRef.value)
  riskChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
      labelLine: { show: false },
      data: [
        { value: summary.value.risks?.by_level?.critical || 0, name: '严重', itemStyle: { color: '#F56C6C' } },
        { value: summary.value.risks?.by_level?.high || 0, name: '高危', itemStyle: { color: '#E6A23C' } },
        { value: summary.value.risks?.by_level?.medium || 0, name: '中危', itemStyle: { color: '#409EFF' } },
        { value: summary.value.risks?.by_level?.low || 0, name: '低危', itemStyle: { color: '#67C23A' } }
      ]
    }]
  })

  // 处置状态饼图
  const statusChart = echarts.init(statusChartRef.value)
  statusChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
      labelLine: { show: false },
      data: [
        { value: summary.value.risks?.by_status?.unhandled || 0, name: '未处理', itemStyle: { color: '#909399' } },
        { value: summary.value.risks?.by_status?.fixed || 0, name: '已修复', itemStyle: { color: '#67C23A' } }
      ]
    }]
  })
}

const renderTrendCharts = () => {
  const dates = trendData.value.map(item => item.date)
  const ipCounts = trendData.value.map(item => item.ip_count)
  const domainCounts = trendData.value.map(item => item.domain_count)
  const pocCounts = trendData.value.map(item => item.poc_count)
  const versionCounts = trendData.value.map(item => item.version_count)
  const criticalCounts = trendData.value.map(item => item.critical_count)
  const highCounts = trendData.value.map(item => item.high_count)
  const mediumCounts = trendData.value.map(item => item.medium_count)
  const lowCounts = trendData.value.map(item => item.low_count)

  // 资产趋势折线图
  const assetTrendChart = echarts.init(assetTrendRef.value)
  assetTrendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '3%', containLabel: true },
    xAxis: { type: 'category', data: dates, axisLabel: { rotate: 45, fontSize: 10 } },
    yAxis: { type: 'value' },
    series: [
      { name: 'IP资产', type: 'line', data: ipCounts, smooth: true, itemStyle: { color: '#409EFF' } },
      { name: '域名资产', type: 'line', data: domainCounts, smooth: true, itemStyle: { color: '#67C23A' } }
    ]
  })

  // 漏洞趋势折线图
  const vulnTrendChart = echarts.init(vulnTrendRef.value)
  vulnTrendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '3%', containLabel: true },
    xAxis: { type: 'category', data: dates, axisLabel: { rotate: 45, fontSize: 10 } },
    yAxis: { type: 'value' },
    series: [
      { name: 'PoC漏洞', type: 'line', data: pocCounts, smooth: true, itemStyle: { color: '#E6A23C' } },
      { name: '版本漏洞', type: 'line', data: versionCounts, smooth: true, itemStyle: { color: '#F56C6C' } }
    ]
  })

  // 风险等级堆叠面积图
  const riskLevelTrendChart = echarts.init(riskLevelTrendRef.value)
  riskLevelTrendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '3%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: dates, axisLabel: { rotate: 45, fontSize: 10 } },
    yAxis: { type: 'value' },
    series: [
      { name: '严重', type: 'line', stack: 'Total', areaStyle: {}, data: criticalCounts, itemStyle: { color: '#F56C6C' } },
      { name: '高危', type: 'line', stack: 'Total', areaStyle: {}, data: highCounts, itemStyle: { color: '#E6A23C' } },
      { name: '中危', type: 'line', stack: 'Total', areaStyle: {}, data: mediumCounts, itemStyle: { color: '#409EFF' } },
      { name: '低危', type: 'line', stack: 'Total', areaStyle: {}, data: lowCounts, itemStyle: { color: '#67C23A' } }
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
  align-items: center;
  margin-bottom: 15px;
}

.update-time {
  margin-left: 15px;
  color: #909399;
  font-size: 13px;
}

.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 10px;
}

.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  width: 100%;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-icon .el-icon {
  font-size: 28px;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
</style>