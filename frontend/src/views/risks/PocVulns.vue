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
        <el-table-column prop="vul_title" label="漏洞名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="risklevel" label="风险等级" width="90">
          <template #default="{ row }">
            <el-tag :type="riskLevelType(row.risklevel)" size="small">
              {{ riskLevelText(row.risklevel) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target" label="目标地址" min-width="140" show-overflow-tooltip />
        <el-table-column prop="port" label="端口" width="70" />
        <el-table-column prop="status" label="处置状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">
              {{ statusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="change_state" label="变更状态" width="90">
          <template #default="{ row }">
            <el-tag :type="changeStateType(row.change_state)" size="small">
              {{ changeStateText(row.change_state) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="rce" label="RCE" width="70">
          <template #default="{ row }">
            <el-tag v-if="row.rce == 1" type="danger" size="small">是</el-tag>
            <el-tag v-else type="info" size="small">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cve" label="CVE" min-width="120" show-overflow-tooltip />
        <el-table-column label="资产组" min-width="100">
          <template #default="{ row }">
            <span v-if="row.assets_group?.net?.length">{{ row.assets_group.net[0].name }}</span>
            <span v-else-if="row.assets_group?.app?.length">{{ row.assets_group.app[0].name }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="showDetail(row)">详情</el-button>
          </template>
        </el-table-column>
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

    <!-- 详情抽屉 -->
    <el-drawer v-model="drawerVisible" title="漏洞详情" size="50%">
      <el-descriptions :column="2" border v-if="currentDetail">
        <!-- 基本信息 -->
        <el-descriptions-item label="ID">{{ currentDetail.id }}</el-descriptions-item>
        <el-descriptions-item label="漏洞名称">{{ currentDetail.vul_title }}</el-descriptions-item>
        <el-descriptions-item label="漏洞类型">{{ currentDetail.vul_type }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <el-tag :type="riskLevelType(currentDetail.risklevel)" size="small">
            {{ riskLevelText(currentDetail.risklevel) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="目标地址">{{ currentDetail.target }}</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ currentDetail.ip }}</el-descriptions-item>
        <el-descriptions-item label="端口">{{ currentDetail.port }}</el-descriptions-item>
        <el-descriptions-item label="RCE">
          <el-tag v-if="currentDetail.rce == 1" type="danger" size="small">是</el-tag>
          <el-tag v-else type="info" size="small">否</el-tag>
        </el-descriptions-item>

        <!-- 状态信息 -->
        <el-descriptions-item label="处置状态">
          <el-tag :type="statusType(currentDetail.status)" size="small">
            {{ statusText(currentDetail.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="变更状态">
          <el-tag :type="changeStateType(currentDetail.change_state)" size="small">
            {{ changeStateText(currentDetail.change_state) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="复扫状态">
          {{ verifyStateText(currentDetail.verify_state) }}
        </el-descriptions-item>
        <el-descriptions-item label="风险标签">
          <el-tag v-for="tag in currentDetail.tags" :key="tag" size="small" class="tag-item">{{ tag }}</el-tag>
          <span v-if="!currentDetail.tags?.length">-</span>
        </el-descriptions-item>

        <!-- 编号信息 -->
        <el-descriptions-item label="CVE编号">{{ currentDetail.cve || '-' }}</el-descriptions-item>
        <el-descriptions-item label="CNNVD编号">{{ currentDetail.cnnvd || '-' }}</el-descriptions-item>
        <el-descriptions-item label="BUGTRAQ编号">{{ currentDetail.bugtraq || '-' }}</el-descriptions-item>
        <el-descriptions-item label="插件ID">{{ currentDetail.plugin_id || '-' }}</el-descriptions-item>

        <!-- 详情信息 -->
        <el-descriptions-item label="漏洞描述" :span="2">
          <div class="detail-content">{{ currentDetail.vul_description || '-' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="验证信息" :span="2">
          <div class="detail-content pre-wrap">{{ currentDetail.vulinfo || '-' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="解决方案" :span="2">
          <div class="detail-content pre-wrap">{{ currentDetail.vul_solution || '-' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="参考链接" :span="2">
          <a v-if="currentDetail.url" :href="currentDetail.url" target="_blank">{{ currentDetail.url }}</a>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ currentDetail.remarks || '-' }}
        </el-descriptions-item>

        <!-- 资产组信息 -->
        <el-descriptions-item label="网络组">
          <span v-if="currentDetail.assets_group?.net?.length">
            {{ currentDetail.assets_group.net.map(g => g.name).join(', ') }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="应用组">
          <span v-if="currentDetail.assets_group?.app?.length">
            {{ currentDetail.assets_group.app.map(g => g.name).join(', ') }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>

        <!-- 时间信息 -->
        <el-descriptions-item label="首次发现">{{ currentDetail.createtime }}</el-descriptions-item>
        <el-descriptions-item label="最后发现">{{ currentDetail.uptime }}</el-descriptions-item>

        <!-- 处理信息 -->
        <el-descriptions-item label="处理人">{{ currentDetail.handler || '-' }}</el-descriptions-item>
        <el-descriptions-item label="任务ID">
          <span v-if="currentDetail.taskids?.length">{{ currentDetail.taskids.join(', ') }}</span>
          <span v-else>-</span>
        </el-descriptions-item>
      </el-descriptions>
    </el-drawer>
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

// 详情抽屉
const drawerVisible = ref(false)
const currentDetail = ref(null)

// 风险等级映射
const riskLevelMap = {
  '0': { text: '低危', type: 'info' },
  '1': { text: '中危', type: 'warning' },
  '2': { text: '高危', type: 'danger' },
  '3': { text: '严重', type: 'danger' }
}

// 处置状态映射
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

// 变更状态映射
const changeStateMap = {
  0: { text: '遗留', type: 'info' },
  1: { text: '新增', type: 'success' },
  3: { text: '减少', type: 'warning' }
}

// 复扫状态映射
const verifyStateMap = {
  0: '未在复扫',
  1: '复扫中',
  2: '复扫完成',
  3: '复扫失败'
}

const riskLevelText = (level) => riskLevelMap[level]?.text || '未知'
const riskLevelType = (level) => riskLevelMap[level]?.type || 'info'
const statusText = (status) => statusMap[status]?.text || '未知'
const statusType = (status) => statusMap[status]?.type || 'info'
const changeStateText = (state) => changeStateMap[state]?.text || '未知'
const changeStateType = (state) => changeStateMap[state]?.type || 'info'
const verifyStateText = (state) => verifyStateMap[state] || '未知'

const showDetail = (row) => {
  currentDetail.value = row
  drawerVisible.value = true
}

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

.detail-content {
  max-height: 150px;
  overflow-y: auto;
}

.pre-wrap {
  white-space: pre-wrap;
  word-break: break-all;
}

.tag-item {
  margin-right: 5px;
  margin-bottom: 3px;
}
</style>