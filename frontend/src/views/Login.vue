<template>
  <div class="login-container">
    <!-- 左侧品牌展示区 -->
    <div class="login-left">
      <div class="brand-header">
        <div class="logo">
          <el-icon size="32"><Aim /></el-icon>
        </div>
        <span class="brand-name">SOP Platform</span>
      </div>

      <div class="brand-content">
        <h1>安全运营平台</h1>
        <p>资产数据管理 · 安全风险监测 · 安全情报分析</p>

        <!-- 动画角色 -->
        <div class="characters-wrapper">
          <AnimatedCharacters
            :isTyping="isTyping"
            :showPassword="showPassword"
            :passwordLength="form.password.length"
          />
        </div>
      </div>

      <div class="brand-footer">
        <span>© 2026 SOP Platform. All rights reserved.</span>
      </div>
    </div>

    <!-- 右侧登录表单 -->
    <div class="login-right">
      <div class="login-form-wrapper">
        <div class="login-header">
          <h2>欢迎回来</h2>
          <p>请输入您的账号信息登录</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin">
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名 / 邮箱"
              size="large"
              :prefix-icon="User"
              @focus="isTyping = false"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              @focus="isTyping = true"
              @blur="isTyping = false"
              @input="handlePasswordInput"
              @change="showPassword = false"
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <div class="login-options">
              <el-checkbox v-model="form.remember">记住我</el-checkbox>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-btn"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-tips">
          <p>默认管理员账号: admin / admin123</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Aim } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import AnimatedCharacters from '@/components/AnimatedCharacters.vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const isTyping = ref(false)
const showPassword = ref(false)

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

// 监听密码输入，检测是否显示密码
const handlePasswordInput = () => {
  // 检查密码输入框是否处于显示密码状态
  const passwordInput = document.querySelector('input[type="text"]')
  if (passwordInput && passwordInput.placeholder === '密码') {
    showPassword.value = true
  } else {
    showPassword.value = false
  }
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await userStore.login(form.username, form.password, form.remember)

      ElMessage.success('登录成功')

      // 跳转到之前的页面或首页
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    } catch (error) {
      ElMessage.error(error.message || '登录失败')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
}

/* 左侧品牌区域 */
.login-left {
  flex: 1;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: #fff;
  position: relative;
  overflow: hidden;
}

.login-left::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

.brand-header {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 1;
}

.logo {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #409eff, #67c23a);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
}

.brand-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
}

.brand-content h1 {
  font-size: 42px;
  margin-bottom: 16px;
  font-weight: 700;
  text-align: center;
}

.brand-content p {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 40px;
  text-align: center;
}

.characters-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin-top: 20px;
}

.brand-footer {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  position: relative;
  z-index: 1;
  text-align: center;
}

/* 右侧登录表单区域 */
.login-right {
  width: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  padding: 40px;
}

.login-form-wrapper {
  width: 100%;
  max-width: 360px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h2 {
  font-size: 28px;
  color: #303133;
  margin-bottom: 8px;
}

.login-header p {
  font-size: 14px;
  color: #909399;
}

.login-options {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.login-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
}

.login-tips {
  text-align: center;
  margin-top: 20px;
}

.login-tips p {
  font-size: 12px;
  color: #909399;
}

/* 响应式 */
@media (max-width: 900px) {
  .login-left {
    display: none;
  }

  .login-right {
    width: 100%;
  }
}
</style>