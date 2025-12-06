<template>
  <el-container class="layout">
    <el-aside width="230px" class="sidebar">
      <div class="logo">消息中台</div>
      <el-menu :default-active="active" router class="menu" :unique-opened="true">
        <el-menu-item index="/">仪表盘</el-menu-item>
        <el-menu-item index="/admin-users">管理员</el-menu-item>
        <el-menu-item index="/roles">角色</el-menu-item>
        <el-menu-item index="/admin-user-roles">管理员角色绑定</el-menu-item>
        <el-menu-item index="/apps">业务系统</el-menu-item>
        <el-menu-item index="/channels">通道</el-menu-item>
        <el-menu-item index="/message-types">系统消息类型</el-menu-item>
        <el-menu-item index="/channel-message-types">通道消息类型</el-menu-item>
        <el-menu-item index="/templates">模板</el-menu-item>
        <el-menu-item index="/subscriptions">订阅</el-menu-item>
        <el-menu-item index="/users">业务用户</el-menu-item>
        <el-menu-item index="/messages">历史消息</el-menu-item>
        <el-menu-item index="/deliveries">投递记录</el-menu-item>
        <el-menu-item index="/send-message">发送消息</el-menu-item>
        <el-menu-item index="/instances">实例心跳</el-menu-item>
        <el-menu-item index="/ws-tester">WS 测试</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="title">后台管理</div>
        <div class="actions">
          <el-button type="text" @click="profileVisible = true">个人资料</el-button>
          <el-button type="text" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-main class="content">
        <RouterView />
      </el-main>
    </el-container>
    <ProfileDialog v-model:visible="profileVisible" />
  </el-container>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ProfileDialog from './ProfileDialog.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const active = computed(() => route.path)
const profileVisible = ref(false)

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.logo {
  padding: 18px;
  font-weight: 700;
  text-align: center;
  border-bottom: 1px solid #e6e8ec;
  background: linear-gradient(135deg, #1f7ae0, #62b0ff);
  color: #fff;
}
.layout {
  height: 100vh;
}
.sidebar {
  background: #f7f8fa;
  border-right: 1px solid #e6e8ec;
}
.menu :deep(.el-menu-item) {
  height: 44px;
  line-height: 44px;
  border-radius: 6px;
  margin: 4px 8px;
}
.menu :deep(.el-menu-item.is-active) {
  background: rgba(31, 122, 224, 0.12);
  color: #1f7ae0;
  border: 1px solid rgba(31, 122, 224, 0.25);
}
.menu :deep(.el-menu-item:hover) {
  background: rgba(0, 0, 0, 0.04);
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 20px;
  border-bottom: 1px solid #e6e8ec;
  background: #fff;
}
.actions > .el-button {
  margin-left: 8px;
}
.content {
  background: #f5f6f8;
  padding: 16px;
}
</style>
