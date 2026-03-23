<template>
  <div class="dashboard">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { reportsApi } from '@/api'

const summary = ref({})
const riskChartRef = ref(null)
const statusChartRef = ref(null)

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

onMounted(() => {
  loadSummary()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
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