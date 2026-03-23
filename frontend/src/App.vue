<template>
  <el-config-provider :locale="zhCn">
    <el-container class="app-container">
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
        </el-header>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </el-config-provider>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const route = useRoute()

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
  padding: 0 20px;
}

.header-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
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