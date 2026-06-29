<template>
  <!-- Main Top Bar -->
  <v-app-bar theme="dark" class="cyber-navbar px-2 px-md-4" elevation="4">
    <!-- Menu Icon (Mobile only or toggle sidebar) -->
    <v-app-bar-nav-icon 
      variant="text" 
      class="text-cyan-accent-3 mr-2"
      @click.stop="drawer = !drawer"
    ></v-app-bar-nav-icon>

    <!-- Branding Section -->
    <div class="d-flex align-center cursor-pointer mr-6" @click="$router.push({ name: 'MachineOverviewV2' })">
      <v-img 
        :src="require('@/assets/logo.svg')" 
        max-width="32" 
        class="mr-2 nav-logo"
        alt="Logo"
      />
      <div class="d-flex flex-column text-left">
        <span class="text-subtitle-1 font-weight-black tracking-wider text-white mb-0 leading-tight">SMC MES</span>
        <span class="text-caption text-slate-400 d-none d-sm-inline leading-none font-weight-medium">Monitor System</span>
      </div>
    </div>

    <!-- Active Status Pulse -->
    <div class="d-none d-md-flex align-center mr-6 border border-opacity-10 rounded-pill px-3 py-1 bg-slate-900">
      <span class="pulse-dot mr-2"></span>
      <span class="text-caption font-weight-bold text-cyan-accent-2">LIVE MONITORING</span>
    </div>

    <!-- Desktop Navigation Links (Hidden on small screens) -->
    <div class="d-none d-md-flex align-center gap-2">
      <v-btn
        to="/"
        variant="text"
        class="nav-tab-btn"
        :class="{ 'active-tab': $route.name === 'MachineOverviewV2' }"
      >
        <v-icon start size="small">mdi-view-dashboard-outline</v-icon>
        系統總覽
      </v-btn>

      <v-btn
        to="/history"
        variant="text"
        class="nav-tab-btn"
        :class="{ 'active-tab': $route.name === 'HistoryDashboard' }"
      >
        <v-icon start size="small">mdi-chart-timeline-variant</v-icon>
        歷史數據分析
      </v-btn>
    </div>

    <v-spacer></v-spacer>

    <!-- Selected Machine Badge (Visible if a machine is active) -->
    <v-scale-transition>
      <v-chip
        v-if="selectedMachine"
        color="cyan-accent-3"
        variant="outlined"
        class="mr-4 px-4 font-weight-bold selected-machine-chip d-none d-sm-flex"
        @click="goToMachineDashboard"
        ripple
      >
        <v-icon start size="small" class="spinning-cog mr-1">mdi-cog-outline</v-icon>
        目前機台: {{ selectedMachine }}
      </v-chip>
    </v-scale-transition>

    <!-- Digital Clock (Visible on md and up) -->
    <div class="d-none d-lg-flex flex-column align-end justify-center mr-6 text-right time-display">
      <span class="text-body-2 font-weight-bold text-white font-mono leading-none mb-1">{{ currentTime.split(' ')[1] }}</span>
      <span class="text-caption text-slate-400 font-mono leading-none">{{ currentTime.split(' ')[0] }}</span>
    </div>

    <!-- Quick Action: Logout -->
    <v-btn
      icon="mdi-logout"
      variant="text"
      color="error"
      class="logout-icon-btn mr-1"
      @click="logout"
      title="登出系統"
    >
      <v-icon>mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>

  <!-- Side Navigation Drawer -->
  <v-navigation-drawer 
    v-model="drawer"
    theme="dark"
    class="cyber-drawer"
    temporary
  >
    <div class="drawer-header px-6 py-8 d-flex flex-column align-center border-b border-opacity-10 border-white">
      <v-img :src="require('@/assets/logo.svg')" max-width="64" class="mb-4 brand-logo-anim" />
      <h3 class="text-h6 font-weight-black text-white mb-1">SMC MES</h3>
      <p class="text-caption text-cyan-accent-2 mb-0">射出機智慧監控系統</p>
    </div>

    <v-list nav dense class="px-3 py-4 text-left">
      <v-list-item
        link
        to="/"
        prepend-icon="mdi-view-dashboard-outline"
        title="系統總覽 / Overview"
        class="mb-2 rounded-lg list-nav-item"
        :active="$route.name === 'MachineOverviewV2'"
      ></v-list-item>
      
      <v-list-item
        link
        to="/history"
        prepend-icon="mdi-chart-timeline-variant"
        title="歷史數據 / History"
        class="mb-2 rounded-lg list-nav-item"
        :active="$route.name === 'HistoryDashboard'"
      ></v-list-item>
      
      <v-list-item
        v-if="selectedMachine"
        link
        @click="goToMachineDashboard"
        prepend-icon="mdi-cog-outline"
        title="目前機台看板 / Dashboard"
        class="mb-2 rounded-lg list-nav-item select-item-active"
        :active="$route.name === 'MachineDashboard'"
      >
        <template v-slot:append>
          <v-badge color="cyan-accent-3" dot inline></v-badge>
        </template>
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-4 border-t border-opacity-10 border-white bg-slate-950">
        <v-btn
          color="error"
          variant="flat"
          block
          rounded="lg"
          prepend-icon="mdi-logout"
          @click="logout"
        >
          登出系統 / Logout
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'UperNavbar',
  data: () => ({
    drawer: false,
    currentTime: '',
    selectedMachine: '',
    timer: null,
    cookieTimer: null
  }),
  methods: {
    updateTime() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const date = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      this.currentTime = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
    },
    checkSelectedMachine() {
      this.selectedMachine = this.$cookies.get('setSelectMachine') || '';
    },
    goToMachineDashboard() {
      if (this.selectedMachine) {
        this.$router.push({ name: 'MachineDashboard' });
        this.drawer = false;
      }
    },
    logout() {
      if (confirm('確定要登出系統嗎？')) {
        this.$cookies.remove('accesstoken');
        this.$cookies.remove('setSelectMachine');
        this.$router.push({ name: 'Login' });
      }
    }
  },
  mounted() {
    this.updateTime();
    this.timer = setInterval(this.updateTime, 1000);
    this.checkSelectedMachine();
    this.cookieTimer = setInterval(this.checkSelectedMachine, 1000);
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer);
    if (this.cookieTimer) clearInterval(this.cookieTimer);
  }
}
</script>

<style scoped>
/* Navbar base styling with Glassmorphism */
.cyber-navbar {
  background: rgba(15, 23, 42, 0.85) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(6, 182, 212, 0.15) !important;
  color: white !important;
  transition: all 0.3s ease;
}

/* Nav Logo Hover Pulsing */
.nav-logo {
  transition: transform 0.5s ease-in-out;
}
.cursor-pointer:hover .nav-logo {
  transform: rotate(360deg);
}

/* Digital clock display */
.time-display {
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  padding-left: 16px;
  min-width: 140px;
}
.font-mono {
  font-family: 'SFMono-Regular', Consolas, "Liberation Mono", Menlo, Courier, monospace !important;
}

/* Pulse dot for status */
.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulse-ring 1.6s infinite cubic-bezier(0.66, 0, 0, 1);
}

@keyframes pulse-ring {
  to {
    box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
  }
}

/* Desktop tab button styles */
.nav-tab-btn {
  margin: 0 4px;
  color: #cbd5e1 !important;
  font-weight: 700;
  border-radius: 8px;
  transition: all 0.3s ease !important;
  letter-spacing: 0.5px;
}
.nav-tab-btn:hover {
  background-color: rgba(255, 255, 255, 0.05) !important;
  color: #00e5ff !important;
}
.active-tab {
  background-color: rgba(6, 182, 212, 0.1) !important;
  color: #00e5ff !important;
  border-bottom: 2px solid #00e5ff;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

/* Selected machine badge styling */
.selected-machine-chip {
  cursor: pointer;
  border-color: rgba(6, 182, 212, 0.4) !important;
  background: rgba(6, 182, 212, 0.05) !important;
  color: #00e5ff !important;
  transition: all 0.3s ease;
}
.selected-machine-chip:hover {
  background: rgba(6, 182, 212, 0.15) !important;
  transform: scale(1.03);
  box-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
}

.spinning-cog {
  animation: spin 8s infinite linear;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Logout icon button transition */
.logout-icon-btn {
  transition: all 0.3s ease;
}
.logout-icon-btn:hover {
  background-color: rgba(239, 68, 68, 0.1) !important;
  transform: rotate(15deg);
}

/* Sidebar Drawer design */
.cyber-drawer {
  background: rgba(15, 23, 42, 0.95) !important;
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.list-nav-item {
  color: #cbd5e1 !important;
  transition: all 0.2s ease;
}
.list-nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05) !important;
  color: #00e5ff !important;
}
.list-nav-item.v-list-item--active {
  background-color: rgba(6, 182, 212, 0.1) !important;
  color: #00e5ff !important;
}

.select-item-active {
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.bg-slate-900 {
  background-color: rgba(15, 23, 42, 0.6) !important;
}

.bg-slate-950 {
  background-color: rgba(9, 15, 29, 0.8) !important;
}

.text-cyan-accent-2 {
  color: #00e5ff !important;
}

.text-cyan-accent-3 {
  color: #18ffff !important;
}

.gap-2 {
  gap: 8px;
}

.brand-logo-anim {
  animation: float 6s infinite ease-in-out;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}
</style>