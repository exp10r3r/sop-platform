<template>
  <div class="ssl-cert">
    <el-card shadow="never">
      <el-table :data="tableData" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="domain" label="域名" min-width="200" />
        <el-table-column prop="issuer" label="颁发者" min-width="150" />
        <el-table-column prop="not_after" label="过期时间" width="170" />
        <el-table-column prop="is_valid" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_valid ? 'success' : 'danger'" size="small">
              {{ row.is_valid ? '有效' : '已过期' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-model:current-page="currentPage" :total="total" layout="total, prev, pager, next" @current-change="loadData" class="pagination" />
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
    const res = await assetsApi.getSSLCerts({ limit: 10, offset: (currentPage.value - 1) * 10 })
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