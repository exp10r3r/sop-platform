<template>
  <div class="poc-vulns">
    <!-- 搜索栏 -->
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="漏洞名称">
          <el-input v-model="searchForm.vul_title" placeholder="请输入漏洞名称" clearable />
        </el-form-item>
        <el-form-item label="漏洞等级">
          <el-select v-model="searchForm.risklevel" placeholder="请选择" clearable>
            <el-option label="低危" value="0" />
            <el-option label="中危" value="1" />
            <el-option label="高危" value="2" />
            <el-option label="严重" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="处置状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="未处理" value="0" />
            <el-option label="已确认" value="1" />
            <el-option label="已修复" value="2" />
            <el-option label="误报" value="3" />
            <el-option label="待修复" value="4" />
            <el-option label="修复失败" value="5" />
            <el-option label="已验证" value="6" />
            <el-option label="忽略" value="7" />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址">
          <el-input v-model="searchForm.ip" placeholder="请输入IP地址" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card shadow="never">
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="vul_title" label="漏洞名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="risklevel" label="风险等级" width="100">
          <template #default="{ row }">
            <el-tag :type="riskLevelType(row.risklevel)" size="small">
              {{ riskLevelText(row.risklevel) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="vul_type" label="漏洞类型" min-width="120" />
        <el-table-column prop="target" label="目标地址" min-width="150" show-overflow-tooltip />
        <el-table-column prop="port" label="端口" width="80" />
        <el-table-column prop="status" label="处置状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">
              {{ statusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cve" label="CVE" min-width="140" show-overflow-tooltip />
        <el-table-column prop="createtime" label="发现时间" width="170" />
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadData"
        @current-change="loadData"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { risksApi } from '@/api'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  vul_title: '',
  risklevel: '',
  status: '',
  ip: ''
})

const riskLevelMap = {
  '0': { text: '低危', type: 'info' },
  '1': { text: '中危', type: 'warning' },
  '2': { text: '高危', type: 'danger' },
  '3': { text: '严重', type: 'danger' }
}

const statusMap = {
  '0': { text: '未处理', type: 'info' },
  '1': { text: '已确认', type: 'warning' },
  '2': { text: '已修复', type: 'success' },
  '3': { text: '误报', type: '' },
  '4': { text: '待修复', type: 'warning' },
  '5': { text: '修复失败', type: 'danger' },
  '6': { text: '已验证', type: 'success' },
  '7': { text: '忽略', type: 'info' }
}

const riskLevelText = (level) => riskLevelMap[level]?.text || '未知'
const riskLevelType = (level) => riskLevelMap[level]?.type || 'info'
const statusText = (status) => statusMap[status]?.text || '未知'
const statusType = (status) => statusMap[status]?.type || 'info'

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      limit: pageSize.value,
      offset: (currentPage.value - 1) * pageSize.value
    }
    if (searchForm.value.vul_title) params.vul_title = searchForm.value.vul_title
    if (searchForm.value.risklevel) params.risklevel = searchForm.value.risklevel
    if (searchForm.value.status) params.status = searchForm.value.status
    if (searchForm.value.ip) params.ip = searchForm.value.ip

    const res = await risksApi.getPocVulns(params)
    if (res.status) {
      tableData.value = res.info || []
      total.value = res.count || 0
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

const handleReset = () => {
  searchForm.value = { vul_title: '', risklevel: '', status: '', ip: '' }
  handleSearch()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.search-card {
  margin-bottom: 15px;
}

.pagination {
  margin-top: 15px;
  justify-content: flex-end;
}
</style>