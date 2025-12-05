<template>
  <el-dialog v-model="visible" title="个人资料" width="520px">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本信息" name="info">
        <el-form :model="formInfo" label-width="100px">
          <el-form-item label="用户名">
            <el-input v-model="formInfo.username" disabled />
          </el-form-item>
          <el-form-item label="显示名称">
            <el-input v-model="formInfo.display_name" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="formInfo.phone" />
          </el-form-item>
        </el-form>
        <div class="footer">
          <el-button @click="close">取消</el-button>
          <el-button type="primary" @click="saveInfo">保存</el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="修改密码" name="pwd">
        <el-form :model="formPwd" label-width="100px">
          <el-form-item label="旧密码">
            <el-input v-model="formPwd.old_password" type="password" />
          </el-form-item>
          <el-form-item label="新密码">
            <el-input v-model="formPwd.new_password" type="password" />
          </el-form-item>
        </el-form>
        <div class="footer">
          <el-button @click="close">取消</el-button>
          <el-button type="primary" @click="savePwd">保存</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProfile, updateProfile } from '../api'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  visible: { type: Boolean, default: false },
})
const emit = defineEmits(['update:visible'])

const visible = ref(props.visible)
watch(
  () => props.visible,
  (v) => {
    visible.value = v
    if (v) fetchProfile()
  }
)
watch(visible, (v) => emit('update:visible', v))

const activeTab = ref('info')
const formInfo = ref({
  username: '',
  display_name: '',
  phone: '',
})
const formPwd = ref({
  old_password: '',
  new_password: '',
})
const formRef = ref()
const pwdRef = ref()
const rulesInfo = {
  display_name: [{ required: true, message: '请输入显示名称', trigger: 'blur' }],
}
const rulesPwd = {
  new_password: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
}

const auth = useAuthStore()

const fetchProfile = async () => {
  try {
    const me = await getProfile()
    if (me) {
      auth.setAuth(auth.token, me)
      formInfo.value.username = me.username
      formInfo.value.display_name = me.display_name
      formInfo.value.phone = me.phone
    }
  } catch (err) {
    console.error(err)
  }
}

const close = () => {
  visible.value = false
}

const saveInfo = async () => {
  try {
    await formRef.value.validate()
    await updateProfile({
      display_name: formInfo.value.display_name,
      phone: formInfo.value.phone,
    })
    ElMessage.success('保存成功')
    close()
  } catch (err) {
    ElMessage.error(err.msg || err.response?.data?.detail || '保存失败')
  }
}

const savePwd = async () => {
  try {
    await pwdRef.value.validate()
    await updateProfile({
      password: formPwd.value.new_password,
    })
    ElMessage.success('密码已更新')
    formPwd.value.old_password = ''
    formPwd.value.new_password = ''
    close()
  } catch (err) {
    ElMessage.error(err.msg || err.response?.data?.detail || '修改失败')
  }
}

onMounted(fetchProfile)
</script>

<style scoped>
.footer {
  text-align: right;
  margin-top: 12px;
}
</style>
