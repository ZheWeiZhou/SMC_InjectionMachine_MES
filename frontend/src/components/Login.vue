<template>
  <div class="login-background d-flex align-center justify-center">
    <v-container class="fill-height fill-width py-0 px-4 px-md-12" fluid>
      <v-row class="fill-height align-center justify-center" no-gutters>
        
        <!-- Left Side: Brand & Visuals (Visible only on md and up) -->
        <v-col cols="12" md="6" lg="7" class="d-none d-md-flex flex-column justify-space-between fill-height py-8 pr-8 text-left">
          <div class="brand-header d-flex align-center mb-6">
            <v-img :src="require('@/assets/logo.svg')" max-width="50" class="mr-3 brand-logo" />
            <div>
              <h1 class="text-h4 font-weight-black text-white tracking-wider mb-0">SMC MES</h1>
              <p class="text-caption text-cyan-accent-2 font-weight-bold mb-0">Smart Injection Machine Monitor System</p>
            </div>
          </div>
          
          <div class="d-flex flex-column justify-center flex-grow-1">
            <h2 class="text-h3 font-weight-black text-white mb-6 leading-tight">
              智慧射出成型監控系統
            </h2>
            <p class="text-subtitle-1 text-slate-300 mb-8 max-width-lg">
              即時掌控射出機運轉參數、製程大數據與生產效能，協助企業達成數位轉型與智慧化生產。
            </p>
            
            <!-- Highlight Badges -->
            <div class="features-container">
              <div class="feature-item d-flex align-center mb-4">
                <v-avatar color="rgba(6, 182, 212, 0.15)" size="48" class="mr-4 text-cyan-accent-2">
                  <v-icon size="24" color="#06b6d4">mdi-monitor-dashboard</v-icon>
                </v-avatar>
                <div>
                  <h4 class="text-subtitle-1 font-weight-bold text-white mb-0">即時監控數據</h4>
                  <p class="text-body-2 text-slate-400 mb-0">高頻率採集壓力、溫度、速度等核心製程參數</p>
                </div>
              </div>
              
              <div class="feature-item d-flex align-center mb-4">
                <v-avatar color="rgba(59, 130, 246, 0.15)" size="48" class="mr-4 text-blue-accent-2">
                  <v-icon size="24" color="#3b82f6">mdi-chart-timeline-variant</v-icon>
                </v-avatar>
                <div>
                  <h4 class="text-subtitle-1 font-weight-bold text-white mb-0">生產歷史分析</h4>
                  <p class="text-body-2 text-slate-400 mb-0">完整記錄每次射出成型週期，提供良率與產能優化決策</p>
                </div>
              </div>
              
              <div class="feature-item d-flex align-center">
                <v-avatar color="rgba(16, 185, 129, 0.15)" size="48" class="mr-4 text-emerald-accent-2">
                  <v-icon size="24" color="#10b981">mdi-shield-check-outline</v-icon>
                </v-avatar>
                <div>
                  <h4 class="text-subtitle-1 font-weight-bold text-white mb-0">異常即時告警</h4>
                  <p class="text-body-2 text-slate-400 mb-0">智慧型門檻偵測，異常狀況即時通知，減少停機損失</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="brand-footer text-slate-500 text-caption mt-6">
            © 2026 SMC Injection Machine MES. All rights reserved.
          </div>
        </v-col>
        
        <!-- Right Side: Login Form (Responsive) -->
        <v-col cols="12" md="6" lg="5" class="d-flex align-center justify-center py-8">
          <v-card theme="dark" class="login-card px-6 py-8 rounded-xl elevation-24 border border-opacity-10 border-white width-100">
            <!-- Mobile Brand Header (Visible only on sm and down) -->
            <div class="d-flex d-md-none align-center justify-center mb-8">
              <v-img :src="require('@/assets/logo.svg')" max-width="40" class="mr-2 brand-logo" />
              <div class="text-left">
                <h1 class="text-h5 font-weight-black text-white mb-0">SMC MES</h1>
                <p class="text-caption text-cyan-accent-2 mb-0">Monitor System</p>
              </div>
            </div>

            <div class="text-center mb-8 d-none d-md-block">
              <h3 class="text-h4 font-weight-black mb-2 text-white">歡迎回來</h3>
              <p class="text-subtitle-2 text-slate-400">請登入您的帳戶以開始監控系統</p>
            </div>
            
            <div class="text-center mb-8 d-block d-md-none">
              <h3 class="text-h5 font-weight-bold mb-1 text-white">帳戶登入</h3>
            </div>

            <v-form @submit.prevent="login">
              <!-- Account Input -->
              <v-text-field
                label="使用者帳號 / Account"
                v-model="account"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
                color="#06b6d4"
                class="mb-4 text-left"
                rounded="lg"
                clearable
                @input="error_message = ''"
                :disabled="isLoading"
              ></v-text-field>

              <!-- Password Input -->
              <v-text-field
                label="使用者密碼 / Password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-outline"
                :append-inner-icon="showPassword ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                color="#06b6d4"
                class="mb-6 text-left"
                rounded="lg"
                @input="error_message = ''"
                :disabled="isLoading"
              ></v-text-field>

              <!-- Error Alert -->
              <v-expand-transition>
                <div v-if="error_message" class="mb-4">
                  <v-alert
                    type="error"
                    variant="tonal"
                    density="comfortable"
                    closable
                    @click:close="error_message = ''"
                    class="rounded-lg text-body-2 font-weight-bold"
                  >
                    {{ error_message }}
                  </v-alert>
                </div>
              </v-expand-transition>

              <!-- Login Button -->
              <v-btn
                type="submit"
                :loading="isLoading"
                class="login-btn text-none font-weight-bold mt-2"
                block
                size="large"
                rounded="lg"
              >
                登入系統 / Sign In
              </v-btn>
            </v-form>
          </v-card>
        </v-col>
        
      </v-row>
    </v-container>
    
    <!-- Background Tech Glow Circles -->
    <div class="glow-circle glow-1"></div>
    <div class="glow-circle glow-2"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',

  data: () => ({
    account: '',
    password: '',
    error_message: '',
    showPassword: false,
    isLoading: false
  }),
  methods: {
    login() {
      if (this.account === '' || this.password === '') {
        this.error_message = '請輸入帳號與密碼';
        return;
      }
      
      this.isLoading = true;
      this.error_message = '';
      
      const requestbody = {
        useraccount: this.account,
        userpassword: this.password
      };
      
      axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/user/login`, requestbody)
        .then((response) => {
          this.isLoading = false;
          if (response.data.status === 'error') {
            this.error_message = '登入失敗，請檢查帳號與密碼';
          } else {
            const token = response.data.Data.token;
            this.$cookies.set('accesstoken', token, '1d');
            setTimeout(() => {
              this.$router.push({ name: 'MachineOverviewV2' });
            }, 500); // Reduced delay to feel snappier
          }
        })
        .catch((error) => {
          this.isLoading = false;
          console.error("Login request error:", error);
          this.error_message = '連線失敗或伺服器錯誤，請稍後再試';
        });
    }
  }
}
</script>

<style scoped>
.login-background {
  position: relative;
  background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%);
  min-height: 100vh;
  width: 100vw;
  overflow: hidden;
  font-family: 'Roboto', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.brand-logo {
  animation: pulse 4s infinite ease-in-out;
}

.max-width-lg {
  max-width: 500px;
}

/* Feature card styling */
.feature-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 12px 16px;
  border-radius: 16px;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);
}
.feature-item:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(6, 182, 212, 0.3);
  transform: translateX(6px);
}

.text-slate-300 {
  color: #cbd5e1 !important;
}

.text-slate-400 {
  color: #94a3b8 !important;
}

.text-slate-500 {
  color: #64748b !important;
}

.text-cyan-accent-2 {
  color: #00e5ff !important;
}

/* Glassmorphic Login Card */
.login-card {
  background: rgba(15, 23, 42, 0.65) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
  width: 100%;
  max-width: 450px;
  animation: slide-up-fade-in 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.width-100 {
  width: 100%;
}

/* Premium Gradient Login Button */
.login-btn {
  background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
  color: white !important;
  letter-spacing: 1px;
  font-size: 1rem !important;
  height: 52px !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(6, 182, 212, 0.5) !important;
}

.login-btn:active {
  transform: translateY(1px);
}

/* Glowing Background Accents */
.glow-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  pointer-events: none;
  opacity: 0.15;
}

.glow-1 {
  width: 400px;
  height: 400px;
  background: #06b6d4;
  top: 10%;
  left: 5%;
  animation: float-slow 15s infinite ease-in-out;
}

.glow-2 {
  width: 500px;
  height: 500px;
  background: #3b82f6;
  bottom: 10%;
  right: 5%;
  animation: float-slow 20s infinite ease-in-out alternate;
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

@keyframes float-slow {
  0% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(30px, -50px) scale(1.1);
  }
  100% {
    transform: translate(0, 0) scale(1);
  }
}

@keyframes slide-up-fade-in {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Ensure layout content sits above glow elements */
.v-container {
  position: relative;
  z-index: 1;
}
</style>

