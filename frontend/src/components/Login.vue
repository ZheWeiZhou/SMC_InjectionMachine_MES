<template>
  <div class="login-background d-flex align-center justify-center">
    <v-container class="d-flex align-center justify-center px-4" fluid>
      <v-card theme="dark" class="login-card px-6 py-8 px-md-10 py-md-12 rounded-xl elevation-24 border border-opacity-10 border-white text-center">
        <!-- Brand Header inside Card -->
        <div class="d-flex flex-column align-center mb-8">
          <v-img :src="require('@/assets/logo.svg')" max-width="64" class="mb-4 brand-logo" alt="Logo" />
          <h1 class="text-h4 font-weight-black text-white tracking-wider mb-2 leading-none">SMC MES</h1>
          <p class="text-subtitle-2 text-cyan-accent-2 font-weight-bold mb-0">智能射出機製造執行系統</p>
        </div>

        <v-form @submit.prevent="login" class="mt-4">
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
                class="rounded-lg text-body-2 font-weight-bold text-left"
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

        <div class="text-slate-500 text-caption mt-8 mb-0">
          © 2026 SMC Injection Machine MES. All rights reserved.
        </div>
      </v-card>
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
  max-width: 460px;
  animation: slide-up-fade-in 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  z-index: 2;
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
  top: 15%;
  left: 10%;
  animation: float-slow 15s infinite ease-in-out;
}

.glow-2 {
  width: 500px;
  height: 500px;
  background: #3b82f6;
  bottom: 15%;
  right: 10%;
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
