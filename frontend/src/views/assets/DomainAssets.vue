<template>
  <div class="domain-assets">
    <el-card shadow="never">
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="domain" label="域名" min-width="200" />
        <el-table-column prop="ip" label="关联IP" min-width="150" />
        <el-table-column prop="title" label="标题" min-width="150" />
        <el-table-column prop="createtime" label="创建时间" width="170" />
      </el-table>
      <el-pagination
        v-model:current-page="currentPage"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="loadData"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { assetsApi } from '@/api'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)

const loadData = async () => {
  loading.value = true
  try {
    const res = await assetsApi.getDomains({ limit: 10, offset: (currentPage.value - 1) * 10 })
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