<template>
  <div class="user-management-page py-6 px-4 px-md-8 text-left">
    <!-- Top Global Navbar -->
    <v-row class="mb-4">
      <UperNavbar />
    </v-row>

    <!-- Main Container -->
    <v-container fluid class="max-width-wrapper py-2">
      <!-- Title Header Card -->
      <v-card class="rounded-xl border border-opacity-10 mb-6 pa-5 card-enter-anim" elevation="2">
        <div class="d-flex flex-column flex-md-row justify-space-between align-start align-md-center">
          <div class="d-flex align-center mb-3 mb-md-0">
            <v-avatar color="blue-lighten-5" size="52" class="mr-4">
              <v-icon size="30" color="primary">mdi-account-cog-outline</v-icon>
            </v-avatar>
            <div>
              <h1 class="text-h5 font-weight-black text-slate-800 mb-1">使用者管理系統 / User Management</h1>
              <p class="text-caption text-slate-500 mb-0 font-weight-medium">
                僅系統管理員（Admin）可進行使用者帳號建立、權限設定與帳號刪除
              </p>
            </div>
          </div>
          <v-chip color="primary" variant="tonal" class="font-weight-bold px-4 py-2">
            <v-icon start size="small">mdi-shield-check</v-icon>
            當前身份: {{ useraccount }} ({{ userrole.toUpperCase() }})
          </v-chip>
        </div>
      </v-card>

      <!-- Main Content Grid -->
      <v-row class="match-height">
        <!-- Left Column: Add New User Form -->
        <v-col cols="12" md="5" lg="4">
          <v-card class="rounded-xl border border-opacity-10 pa-6 h-100 card-enter-anim" elevation="2" style="animation-delay: 100ms;">
            <div class="d-flex align-center mb-5 pb-3 border-b">
              <v-icon color="primary" class="mr-2" size="24">mdi-account-plus-outline</v-icon>
              <h2 class="text-h6 font-weight-black text-slate-800 mb-0">新增使用者帳號</h2>
            </div>

            <v-form ref="form" v-model="valid" @submit.prevent="createUser">
              <!-- Username -->
              <div class="mb-4">
                <label class="text-caption font-weight-bold text-slate-600 mb-1 d-block">使用者姓名 / Name</label>
                <v-text-field
                  v-model="newUser.username"
                  placeholder="請輸入使用者姓名"
                  prepend-inner-icon="mdi-account"
                  variant="outlined"
                  color="primary"
                  density="comfortable"
                  rounded="lg"
                  hide-details="auto"
                  :rules="[v => !!v || '請輸入使用者姓名']"
                  :disabled="isLoading"
                ></v-text-field>
              </div>

              <!-- Account -->
              <div class="mb-4">
                <label class="text-caption font-weight-bold text-slate-600 mb-1 d-block">登入帳號 / Account</label>
                <v-text-field
                  v-model="newUser.useraccount"
                  placeholder="請輸入登入帳號 (至少3位)"
                  prepend-inner-icon="mdi-badge-account-outline"
                  variant="outlined"
                  color="primary"
                  density="comfortable"
                  rounded="lg"
                  hide-details="auto"
                  :rules="[
                    v => !!v || '請輸入登入帳號',
                    v => (v && v.length >= 3) || '帳號長度至少需 3 個字元'
                  ]"
                  :disabled="isLoading"
                ></v-text-field>
              </div>

              <!-- Password -->
              <div class="mb-4">
                <label class="text-caption font-weight-bold text-slate-600 mb-1 d-block">登入密碼 / Password</label>
                <v-text-field
                  v-model="newUser.userpassword"
                  placeholder="請輸入登入密碼 (至少4位)"
                  :type="showPassword ? 'text' : 'password'"
                  prepend-inner-icon="mdi-lock-outline"
                  :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                  @click:append-inner="showPassword = !showPassword"
                  variant="outlined"
                  color="primary"
                  density="comfortable"
                  rounded="lg"
                  hide-details="auto"
                  :rules="[
                    v => !!v || '請輸入登入密碼',
                    v => (v && v.length >= 4) || '密碼長度至少需 4 個字元'
                  ]"
                  :disabled="isLoading"
                ></v-text-field>
              </div>

              <!-- Role Selector -->
              <div class="mb-6">
                <label class="text-caption font-weight-bold text-slate-600 mb-1 d-block">權限角色 / Role</label>
                <v-select
                  v-model="newUser.role"
                  :items="roleOptions"
                  item-title="title"
                  item-value="value"
                  prepend-inner-icon="mdi-shield-account-outline"
                  variant="outlined"
                  color="primary"
                  density="comfortable"
                  rounded="lg"
                  hide-details="auto"
                  :disabled="isLoading"
                ></v-select>
              </div>

              <!-- Alert Messages -->
              <v-expand-transition>
                <v-alert
                  v-if="formAlert.message"
                  :type="formAlert.type"
                  variant="tonal"
                  density="comfortable"
                  closable
                  @click:close="formAlert.message = ''"
                  class="mb-4 rounded-lg font-weight-bold text-caption text-left"
                >
                  {{ formAlert.message }}
                </v-alert>
              </v-expand-transition>

              <!-- Submit Button -->
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                rounded="lg"
                class="font-weight-bold text-white elevation-2"
                :loading="isLoading"
              >
                <v-icon start>mdi-check-circle-outline</v-icon>
                確認建立帳號 / Create User
              </v-btn>
            </v-form>
          </v-card>
        </v-col>

        <!-- Right Column: User List Table -->
        <v-col cols="12" md="7" lg="8">
          <v-card class="rounded-xl border border-opacity-10 pa-6 h-100 card-enter-anim" elevation="2" style="animation-delay: 200ms;">
            <div class="d-flex justify-space-between align-center mb-5 pb-3 border-b">
              <div class="d-flex align-center">
                <v-icon color="primary" class="mr-2" size="24">mdi-account-group-outline</v-icon>
                <h2 class="text-h6 font-weight-black text-slate-800 mb-0">系統使用者列表</h2>
              </div>
              <v-btn
                variant="outlined"
                color="primary"
                size="small"
                class="font-weight-bold rounded-lg"
                @click="fetchUserList"
                :loading="isFetching"
              >
                <v-icon start>mdi-refresh</v-icon>
                重新整理
              </v-btn>
            </div>

            <!-- Users Table -->
            <div class="table-responsive">
              <v-table class="custom-user-table">
                <thead>
                  <tr>
                    <th class="text-left font-weight-bold">ID</th>
                    <th class="text-left font-weight-bold">姓名</th>
                    <th class="text-left font-weight-bold">帳號</th>
                    <th class="text-left font-weight-bold">權限角色</th>
                    <th class="text-left font-weight-bold">建立時間</th>
                    <th class="text-center font-weight-bold">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="userList.length === 0">
                    <td colspan="6" class="text-center py-6 text-slate-500">
                      {{ isFetching ? '載入使用者資料中...' : '目前尚無使用者資料' }}
                    </td>
                  </tr>
                  <tr v-for="user in userList" :key="user.id" class="table-row-hover">
                    <td class="font-mono text-caption text-slate-500">#{{ user.id }}</td>
                    <td class="font-weight-bold text-slate-800">{{ user.username || user.useraccount }}</td>
                    <td class="font-mono text-primary font-weight-bold">{{ user.useraccount }}</td>
                    <td>
                      <v-chip
                        size="small"
                        :color="user.role === 'admin' ? 'purple-darken-1' : 'primary'"
                        variant="tonal"
                        class="font-weight-bold"
                      >
                        <v-icon start size="x-small">
                          {{ user.role === 'admin' ? 'mdi-shield-crown' : 'mdi-account' }}
                        </v-icon>
                        {{ user.role ? user.role.toUpperCase() : 'USER' }}
                      </v-chip>
                    </td>
                    <td class="text-caption text-slate-500 font-mono">{{ formatDate(user.created_at) }}</td>
                    <td class="text-center">
                      <v-btn
                        v-if="user.useraccount !== 'admin'"
                        size="small"
                        icon="mdi-delete-outline"
                        color="error"
                        variant="text"
                        @click="confirmDelete(user)"
                        title="刪除帳號"
                      ></v-btn>
                      <span v-else class="text-caption text-slate-400 font-italic">系統保護</span>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog.show" max-width="420">
      <v-card class="rounded-xl pa-4 text-center">
        <v-card-title class="text-h6 font-weight-bold text-red-darken-1">
          <v-icon color="error" class="mr-2" size="28">mdi-alert-circle-outline</v-icon>
          確認刪除使用者？
        </v-card-title>
        <v-card-text class="text-body-2 text-slate-600 py-4">
          確定要刪除帳號 <strong class="text-primary">{{ deleteDialog.target?.useraccount }}</strong> ({{ deleteDialog.target?.username }}) 嗎？刪除後無法復原。
        </v-card-text>
        <v-card-actions class="justify-center gap-3">
          <v-btn color="grey-darken-1" variant="text" rounded="lg" class="px-6" @click="deleteDialog.show = false">取消</v-btn>
          <v-btn color="error" variant="flat" rounded="lg" class="px-6 font-weight-bold" :loading="deleteDialog.loading" @click="executeDelete">確認刪除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import UperNavbar from './layout/UperNavbar.vue';

export default {
  name: 'UserManagement',
  components: {
    UperNavbar
  },
  data: () => ({
    valid: false,
    useraccount: '',
    userrole: '',
    showPassword: false,
    isLoading: false,
    isFetching: false,
    newUser: {
      username: '',
      useraccount: '',
      userpassword: '',
      role: 'user'
    },
    roleOptions: [
      { title: '一般使用者 (User)', value: 'user' },
      { title: '系統管理員 (Admin)', value: 'admin' }
    ],
    formAlert: {
      type: 'info',
      message: ''
    },
    userList: [],
    deleteDialog: {
      show: false,
      target: null,
      loading: false
    }
  }),
  methods: {
    checkPermission() {
      const token = this.$cookies.get('accesstoken');
      const role = this.$cookies.get('userrole');
      const account = this.$cookies.get('useraccount');

      if (!token) {
        this.$router.push({ name: 'Login' });
        return false;
      }

      this.userrole = role || (account === 'admin' ? 'admin' : 'user');
      this.useraccount = account || '';

      if (this.userrole !== 'admin' && this.useraccount !== 'admin') {
        alert('權限不足：僅系統管理員 (Admin) 可進入使用者管理頁面');
        this.$router.push({ name: 'MachineOverviewV2' });
        return false;
      }
      return true;
    },

    async fetchUserList() {
      if (!this.checkPermission()) return;
      this.isFetching = true;
      const token = this.$cookies.get('accesstoken') || '';
      const account = this.$cookies.get('useraccount') || '';

      try {
        const response = await axios.get(
          `${this.$store.getters.getHost}/smc/injectionmachinemes/user/list`,
          { 
            headers: { 
              accesstoken: token,
              useraccount: account
            },
            params: {
              token: token,
              useraccount: account
            }
          }
        );

        this.isFetching = false;
        if (response.data.status === 'success') {
          this.userList = response.data.Data || [];
        } else {
          console.error("Fetch user list error:", response.data);
        }
      } catch (err) {
        this.isFetching = false;
        console.error("Fetch user list API failed:", err);
      }
    },

    async createUser() {
      const { valid } = await this.$refs.form.validate();
      if (!valid) return;

      this.isLoading = true;
      this.formAlert.message = '';

      const token = this.$cookies.get('accesstoken') || '';
      const account = this.$cookies.get('useraccount') || '';
      const requestbody = {
        username: this.newUser.username,
        useraccount: this.newUser.useraccount,
        userpassword: this.newUser.userpassword,
        role: this.newUser.role
      };

      try {
        const response = await axios.post(
          `${this.$store.getters.getHost}/smc/injectionmachinemes/user/createuser`,
          requestbody,
          {
            headers: { accesstoken: token, useraccount: account },
            params: { token: token, useraccount: account }
          }
        );

        this.isLoading = false;
        if (response.data.status === 'success') {
          this.formAlert = {
            type: 'success',
            message: `成功建立帳號: ${this.newUser.useraccount}`
          };
          this.newUser = {
            username: '',
            useraccount: '',
            userpassword: '',
            role: 'user'
          };
          this.$refs.form.resetValidation();
          this.fetchUserList();
        } else {
          this.formAlert = {
            type: 'error',
            message: response.data.message || '建立失敗，請稍後再試'
          };
        }
      } catch (err) {
        this.isLoading = false;
        console.error("Create user API error:", err);
        const errorMsg = err.response?.data?.message || '新增失敗：權限不足或伺服器錯誤';
        this.formAlert = {
          type: 'error',
          message: errorMsg
        };
      }
    },

    confirmDelete(user) {
      this.deleteDialog.target = user;
      this.deleteDialog.show = true;
    },

    async executeDelete() {
      if (!this.deleteDialog.target) return;
      this.deleteDialog.loading = true;

      const token = this.$cookies.get('accesstoken') || '';
      const account = this.$cookies.get('useraccount') || '';
      try {
        const response = await axios.post(
          `${this.$store.getters.getHost}/smc/injectionmachinemes/user/delete`,
          { user_id: this.deleteDialog.target.id },
          {
            headers: { accesstoken: token, useraccount: account },
            params: { token: token, useraccount: account }
          }
        );

        this.deleteDialog.loading = false;
        this.deleteDialog.show = false;

        if (response.data.status === 'success') {
          this.fetchUserList();
        } else {
          alert(response.data.message || '刪除失敗');
        }
      } catch (err) {
        this.deleteDialog.loading = false;
        this.deleteDialog.show = false;
        console.error("Delete user API failed:", err);
        alert(err.response?.data?.message || '刪除失敗：伺服器錯誤');
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return '無資料';
      return dateStr.replace('T', ' ').substring(0, 16);
    }
  },

  mounted() {
    if (this.checkPermission()) {
      this.fetchUserList();
    }
  }
}
</script>

<style scoped>
.user-management-page {
  min-height: 100vh;
  background-color: #f8fafc;
}

.max-width-wrapper {
  max-width: 1600px;
}

.text-slate-800 {
  color: #1e293b !important;
}

.text-slate-600 {
  color: #475569 !important;
}

.text-slate-500 {
  color: #64748b !important;
}

.text-slate-400 {
  color: #94a3b8 !important;
}

.custom-user-table {
  width: 100%;
  border-collapse: collapse;
}

.custom-user-table th {
  background-color: #f1f5f9 !important;
  font-weight: 800 !important;
  color: #475569 !important;
  border-bottom: 2px solid rgba(0, 0, 0, 0.08) !important;
  padding: 14px 16px !important;
}

.custom-user-table td {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06) !important;
  padding: 14px 16px !important;
}

.table-row-hover:hover {
  background-color: rgba(25, 118, 210, 0.04) !important;
}

.font-mono {
  font-family: 'SFMono-Regular', Consolas, monospace !important;
}

/* Card Load Animation matching HistoryDashboard */
.card-enter-anim {
  animation: slide-up-fade-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

@keyframes slide-up-fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
