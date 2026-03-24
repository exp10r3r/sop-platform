<template>
  <div class="ip-assets">
    <!-- 搜索栏 -->
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="IP地址">
          <el-input v-model="searchForm.ip" placeholder="请输入IP地址" clearable />
        </el-form-item>
        <el-form-item label="地理位置">
          <el-input v-model="searchForm.location" placeholder="请输入地理位置" clearable />
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
        <el-table-column prop="ip" label="IP地址" min-width="140" />
        <el-table-column prop="port" label="端口" min-width="120">
          <template #default="{ row }">
            <el-tag v-for="p in (row.port || []).slice(0, 5)" :key="p" size="small" class="port-tag">
              {{ p }}
            </el-tag>
            <span v-if="(row.port || []).length > 5">...</span>
          </template>
        </el-table-column>
        <el-table-column prop="service" label="服务" min-width="180">
          <template #default="{ row }">
            <span v-for="s in (row.service || []).slice(0, 2)" :key="s.port">
              {{ s.service }}:{{ s.port }}
              <span v-if="s.product">({{ s.product }})</span>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="os" label="操作系统" min-width="180" show-overflow-tooltip />
        <el-table-column prop="secstate" label="安全状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.secstate === 1 ? 'success' : 'danger'" size="small">
              {{ row.secstate === 1 ? '安全' : '存在风险' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createtime" label="创建时间" width="170" />
        <el-table-column prop="uptime" label="更新时间" width="170" />
        <el-table-column prop="location" label="地理位置" min-width="120" />
        <el-table-column prop="isp" label="运营商" min-width="100" />
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
import { assetsApi } from '@/api'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchForm = ref({
  ip: '',
  location: ''
})

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      limit: pageSize.value,
      offset: (currentPage.value - 1) * pageSize.value
    }
    if (searchForm.value.ip) params.ip = searchForm.value.ip
    if (searchForm.value.location) params.location = searchForm.value.location

    const res = await assetsApi.getIPAssets(params)
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
  searchForm.value = { ip: '', location: '' }
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

.port-tag {
  margin-right: 5px;
  margin-bottom: 3px;
}

.pagination {
  margin-top: 15px;
  justify-content: flex-end;
}
</style>