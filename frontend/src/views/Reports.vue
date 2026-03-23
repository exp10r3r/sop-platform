<template>
  <div class="reports">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span>资产统计</span></template>
          <div ref="assetChartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span>风险统计</span></template>
          <div ref="riskChartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header><span>情报统计</span></template>
          <div ref="intelChartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { reportsApi } from '@/api'

const assetChartRef = ref(null)
const riskChartRef = ref(null)
const intelChartRef = ref(null)

const loadReports = async () => {
  try {
    const [assetsRes, risksRes, intelRes] = await Promise.all([
      reportsApi.getAssetsReport(),
      reportsApi.getRisksReport(),
      reportsApi.getIntelligenceReport()
    ])

    renderAssetChart(assetsRes.data)
    renderRiskChart(risksRes.data)
    renderIntelChart(intelRes.data)
  } catch (error) {
    console.error('加载报表失败:', error)
  }
}

const renderAssetChart = (data) => {
  const chart = echarts.init(assetChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'category', data: ['IP资产', '域名', '端口服务', '站点', 'URL', 'SSL证书'] },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [data.ip, data.domain, data.portserver, data.webapp, data.url, data.ssl_cert],
      itemStyle: { color: '#409EFF' }
    }]
  })
}

const renderRiskChart = (data) => {
  const chart = echarts.init(riskChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: '60%',
      data: [
        { value: data.total.poc, name: 'PoC漏洞' },
        { value: data.total.version, name: '版本漏洞' },
        { value: data.total.thirdvuln, name: '第三方漏洞' },
        { value: data.total.riskport, name: '高危端口' }
      ]
    }]
  })
}

const renderIntelChart = (data) => {
  const chart = echarts.init(intelChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: {
      type: 'category',
      data: ['漏洞情报', '暗网监控', '开源社区', '影子资产', 'IM监控', '邮箱监控', '文档监控', '网盘监控']
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: [data.vulinfo, data.darkweb, data.git, data.shadow, data.im, data.mail, data.doc, data.pan],
      itemStyle: { color: '#67C23A' }
    }]
  })
}

onMounted(() => {
  loadReports()
})
</script>

<style scoped>
.reports {
  padding: 0;
}
</style>