<template>
  <div class="third-vulns">
    <el-card shadow="never">
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="vul_title" label="漏洞名称" min-width="200" />
        <el-table-column prop="risklevel" label="风险等级" width="100" />
        <el-table-column prop="target" label="目标地址" min-width="150" />
        <el-table-column prop="source" label="来源" width="120" />
      </el-table>
      <el-pagination v-model:current-page="currentPage" :total="total" layout="total, prev, pager, next" @current-change="loadData" class="pagination" />
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

const loadData = async () => {
  loading.value = true
  try {
    const res = await risksApi.getThirdVulns({ limit: 10, offset: (currentPage.value - 1) * 10 })
    if (res.status) {
      tableData.value = res.info || []
      total.value = res.count || 0
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => loadData())
</script>

<style scoped>
.pagination { margin-top: 15px; justify-content: flex-end; }
</style>