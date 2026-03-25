<template>
  <el-config-provider :locale="zhCn">
    <!-- 登录页面不显示侧边栏 -->
    <template v-if="route.path === '/login'">
      <router-view />
    </template>

    <!-- 主界面布局 -->
    <el-container v-else class="app-container">
      <el-aside width="220px" class="sidebar">
        <div class="logo">
          <h1>SOP Platform</h1>
        </div>
        <el-menu
          :default-active="activeMenu"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/">
            <el-icon><DataAnalysis /></el-icon>
            <span>总览</span>
          </el-menu-item>

          <el-sub-menu index="assets">
            <template #title>
              <el-icon><Monitor /></el-icon>
              <span>资产管理</span>
            </template>
            <el-menu-item index="/assets/ip">IP资产</el-menu-item>
            <el-menu-item index="/assets/domain">域名资产</el-menu-item>
            <el-menu-item index="/assets/portserver">端口服务</el-menu-item>
            <el-menu-item index="/assets/webapp">站点列表</el-menu-item>
            <el-menu-item index="/assets/ssl">SSL证书</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="risks">
            <template #title>
              <el-icon><Warning /></el-icon>
              <span>安全风险</span>
            </template>
            <el-menu-item index="/risks/poc">PoC漏洞</el-menu-item>
            <el-menu-item index="/risks/version">版本漏洞</el-menu-item>
            <el-menu-item index="/risks/thirdvuln">第三方漏洞</el-menu-item>
            <el-menu-item index="/risks/riskport">高危端口</el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="intel">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>安全情报</span>
            </template>
            <el-menu-item index="/intel/vulinfo">漏洞情报</el-menu-item>
            <el-menu-item index="/intel/darkweb">暗网监控</el-menu-item>
            <el-menu-item index="/intel/git">开源社区</el-menu-item>
            <el-menu-item index="/intel/shadow">影子资产</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="/reports">
            <el-icon><DataLine /></el-icon>
            <span>数据报表</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header class="header">
          <div class="header-title">{{ pageTitle }}</div>
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <el-icon><User /></el-icon>
                <span class="username">{{ userStore.username }}</span>
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    个人信息
                  </el-dropdown-item>
                  <el-dropdown-item command="password">
                    <el-icon><Lock /></el-icon>
                    修改密码
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="400px">
      <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-width="80px">
        <el-form-item label="原密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">确定</el-button>
      </template>
    </el-dialog>
  </el-config-provider>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Lock, ArrowDown, SwitchButton } from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const pageTitle = computed(() => {
  const titles = {
    '/': '总览',
    '/assets/ip': 'IP资产',
    '/assets/domain': '域名资产',
    '/assets/portserver': '端口服务',
    '/assets/webapp': '站点列表',
    '/assets/ssl': 'SSL证书',
    '/risks/poc': 'PoC漏洞',
    '/risks/version': '版本漏洞',
    '/risks/thirdvuln': '第三方漏洞',
    '/risks/riskport': '高危端口',
    '/intel/vulinfo': '漏洞情报',
    '/intel/darkweb': '暗网监控',
    '/intel/git': '开源社区监控',
    '/intel/shadow': '影子资产监控',
    '/reports': '数据报表'
  }
  return titles[route.path] || 'SOP Platform'
})

// 下拉菜单命令处理
const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      await userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/login')
    } catch (error) {
      if (error !== 'cancel') {
        console.error('登出失败:', error)
      }
    }
  } else if (command === 'password') {
    passwordDialogVisible.value = true
  } else if (command === 'profile') {
    ElMessage.info('个人信息功能开发中')
  }
}

// 修改密码
const passwordDialogVisible = ref(false)
const passwordLoading = ref(false)
const passwordFormRef = ref(null)
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return

    passwordLoading.value = true
    try {
      await userStore.changePassword(passwordForm.oldPassword, passwordForm.newPassword)
      ElMessage.success('密码修改成功，请重新登录')
      passwordDialogVisible.value = false
      // 重置表单
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
      // 退出登录
      await userStore.logout()
      router.push('/login')
    } catch (error) {
      ElMessage.error(error.message || '密码修改失败')
    } finally {
      passwordLoading.value = false
    }
  })
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
}

.app-container {
  height: 100%;
}

.sidebar {
  background-color: #304156;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #3a4758;
}

.logo h1 {
  font-size: 18px;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #606266;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.user-dropdown .username {
  margin: 0 8px;
  font-size: 14px;
}

.main {
  background-color: #f5f7fa;
  padding: 20px;
}

.el-menu {
  border-right: none;
}

.el-sub-menu .el-menu-item {
  min-width: auto;
  padding-left: 50px !important;
}
</style>