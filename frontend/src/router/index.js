import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../views/Login.vue'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import AdminUsers from '../views/AdminUsers.vue'
import Roles from '../views/Roles.vue'
import Apps from '../views/Apps.vue'
import Channels from '../views/Channels.vue'
import MessageTypes from '../views/MessageTypes.vue'
import ChannelMessageTypes from '../views/ChannelMessageTypes.vue'
import Templates from '../views/Templates.vue'
import Subscriptions from '../views/Subscriptions.vue'
import UsersMapping from '../views/UsersMapping.vue'
import Messages from '../views/Messages.vue'
import Deliveries from '../views/Deliveries.vue'
import Instances from '../views/Instances.vue'
import WsTester from '../views/WsTester.vue'
import SendMessage from '../views/SendMessage.vue'

const routes = [
  { path: '/login', name: 'login', component: Login },
  {
    path: '/',
    component: Layout,
    children: [
      { path: '', name: 'dashboard', component: Dashboard },
      { path: 'admin-users', name: 'admin-users', component: AdminUsers },
      { path: 'roles', name: 'roles', component: Roles },
      { path: 'apps', name: 'apps', component: Apps },
      { path: 'channels', name: 'channels', component: Channels },
      { path: 'message-types', name: 'message-types', component: MessageTypes },
      { path: 'channel-message-types', name: 'channel-message-types', component: ChannelMessageTypes },
      { path: 'templates', name: 'templates', component: Templates },
      { path: 'subscriptions', name: 'subscriptions', component: Subscriptions },
      { path: 'users', name: 'users', component: UsersMapping },
      { path: 'messages', name: 'messages', component: Messages },
      { path: 'deliveries', name: 'deliveries', component: Deliveries },
      { path: 'instances', name: 'instances', component: Instances },
      { path: 'ws-tester', name: 'ws-tester', component: WsTester },
      { path: 'send-message', name: 'send-message', component: SendMessage },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.name !== 'login' && !auth.token) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
