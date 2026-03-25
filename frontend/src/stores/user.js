import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const username = computed(() => userInfo.value?.username || '')

  // 登录
  async function login(username, password, remember = false) {
    try {
      const res = await authApi.login({ username, password, remember })

      if (res.status) {
        token.value = res.data.token
        userInfo.value = res.data.user

        // 保存到本地存储
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('userInfo', JSON.stringify(res.data.user))

        return res
      } else {
        throw new Error(res.message || '登录失败')
      }
    } catch (error) {
      throw error
    }
  }

  // 登出
  async function logout() {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 清除本地状态
      token.value = ''
      userInfo.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  }

  // 获取用户信息
  async function fetchUserInfo() {
    try {
      const res = await authApi.getMe()
      if (res.status) {
        userInfo.value = res.data
        localStorage.setItem('userInfo', JSON.stringify(res.data))
      }
      return res
    } catch (error) {
      // Token无效，清除登录状态
      logout()
      throw error
    }
  }

  // 修改密码
  async function changePassword(oldPassword, newPassword) {
    try {
      const res = await authApi.changePassword({
        old_password: oldPassword,
        new_password: newPassword
      })
      return res
    } catch (error) {
      throw error
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    username,
    login,
    logout,
    fetchUserInfo,
    changePassword
  }
})