<template>
  <!-- 登录页面不显示侧边栏 -->
  <template v-if="route.path === '/login'">
    <router-view />
  </template>

  <!-- 主界面布局 -->
  <div v-else class="app-layout">
    <!-- 侧边栏 -->
    <aside
      class="sidebar"
      :class="{ 'sidebar-expanded': sidebarOpen }"
      @mouseenter="sidebarOpen = true"
      @mouseleave="sidebarOpen = false"
    >
      <!-- Logo -->
      <div class="sidebar-logo">
        <div class="logo-icon">
          <el-icon size="20"><Aim /></el-icon>
        </div>
        <transition name="fade">
          <span v-if="sidebarOpen" class="logo-text">SOP Platform</span>
        </transition>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <div class="nav-item" :class="{ active: route.path === '/' }" @click="navigateTo('/')">
          <el-icon><DataAnalysis /></el-icon>
          <transition name="fade">
            <span v-if="sidebarOpen">总览</span>
          </transition>
        </div>

        <div class="nav-group">
          <div class="nav-group-title" v-if="sidebarOpen">资产管理</div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/assets/ip') }" @click="navigateTo('/assets/ip')">
            <el-icon><Monitor /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">IP资产</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/assets/domain') }" @click="navigateTo('/assets/domain')">
            <el-icon><Link /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">域名资产</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/assets/portserver') }" @click="navigateTo('/assets/portserver')">
            <el-icon><Connection /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">端口服务</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/assets/webapp') }" @click="navigateTo('/assets/webapp')">
            <el-icon><Platform /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">站点列表</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/assets/ssl') }" @click="navigateTo('/assets/ssl')">
            <el-icon><Lock /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">SSL证书</span>
            </transition>
          </div>
        </div>

        <div class="nav-group">
          <div class="nav-group-title" v-if="sidebarOpen">安全风险</div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/risks/poc') }" @click="navigateTo('/risks/poc')">
            <el-icon><Warning /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">PoC漏洞</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/risks/version') }" @click="navigateTo('/risks/version')">
            <el-icon><Document /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">版本漏洞</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/risks/thirdvuln') }" @click="navigateTo('/risks/thirdvuln')">
            <el-icon><Files /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">第三方漏洞</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/risks/riskport') }" @click="navigateTo('/risks/riskport')">
            <el-icon><Open /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">高危端口</span>
            </transition>
          </div>
        </div>

        <div class="nav-group">
          <div class="nav-group-title" v-if="sidebarOpen">安全情报</div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/intel/vulinfo') }" @click="navigateTo('/intel/vulinfo')">
            <el-icon><InfoFilled /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">漏洞情报</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/intel/darkweb') }" @click="navigateTo('/intel/darkweb')">
            <el-icon><Hide /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">暗网监控</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/intel/git') }" @click="navigateTo('/intel/git')">
            <el-icon><Promotion /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">开源社区</span>
            </transition>
          </div>
          <div class="nav-item" :class="{ active: route.path.startsWith('/intel/shadow') }" @click="navigateTo('/intel/shadow')">
            <el-icon><Search /></el-icon>
            <transition name="fade">
              <span v-if="sidebarOpen">影子资产</span>
            </transition>
          </div>
        </div>

        <div class="nav-item" :class="{ active: route.path.startsWith('/reports') }" @click="navigateTo('/reports')">
          <el-icon><DataLine /></el-icon>
          <transition name="fade">
            <span v-if="sidebarOpen">数据报表</span>
          </transition>
        </div>
      </nav>
    </aside>

    <!-- 主内容区域 -->
    <div class="main-container">
      <!-- 顶部栏 -->
      <header class="header">
        <div class="header-left">
          <h1 class="page-title">{{ pageTitle }}</h1>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-menu">
              <el-avatar :size="32" class="user-avatar">
                {{ userStore.username?.charAt(0)?.toUpperCase() || 'U' }}
              </el-avatar>
              <span class="username">{{ userStore.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
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
      </header>

      <!-- 内容区域 -->
      <main class="content">
        <router-view />
      </main>
    </div>

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
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User, Lock, ArrowDown, SwitchButton, Aim, DataAnalysis, Monitor, Warning,
  Document, DataLine, Link, Connection, Platform, Files, Open, InfoFilled,
  Hide, Promotion, Search
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const sidebarOpen = ref(false)

const navigateTo = (path) => {
  router.push(path)
}

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
      passwordForm.oldPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''
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
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
}

/* 侧边栏 */
.sidebar {
  width: 70px;
  height: 100%;
  background: #1e1e2d;
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
  transition: width 0.3s ease;
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar:hover,
.sidebar.sidebar-expanded {
  width: 250px;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 4px;
  margin-bottom: 24px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: white;
  white-space: nowrap;
}

/* 导航 */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 8px;
  color: #9ca3af;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.nav-item.active {
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
}

.nav-item .el-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.nav-item span {
  white-space: nowrap;
  font-size: 14px;
}

.nav-group {
  margin-top: 16px;
}

.nav-group-title {
  font-size: 11px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 8px;
  margin-bottom: 4px;
}

/* 主内容区域 */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #fff;
  border-radius: 24px 0 0 24px;
  margin: 12px 0 12px 0;
}

/* 顶部栏 */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: #fff;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background 0.2s;
}

.user-menu:hover {
  background: #f3f4f6;
}

.user-avatar {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  font-weight: 600;
}

.username {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.user-menu .el-icon {
  color: #9ca3af;
  font-size: 12px;
}

/* 内容区域 */
.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background: #f9fafb;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>