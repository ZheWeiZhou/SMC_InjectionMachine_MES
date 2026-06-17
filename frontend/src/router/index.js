import LoginPage from '@/components/Login';
// import MachineOverviewPage from '@/components/MachineOverview';
import MachineDashboard from '@/components/Machinedashboard';
import HistoryDashboard from '@/components/HistoryDashboard';
import MachineOverviewPageV2 from '@/components/MachineOverviewV2';
import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'MachineOverviewV2',
    component: MachineOverviewPageV2
  },
  // {
  //   path: '/v2',
  //   name: 'MachineOverviewV2',
  //   component: MachineOverviewV2
  // },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/dashboard',
    name: 'MachineDashboard',
    component: MachineDashboard
  },
  {
    path: '/history',
    name: 'HistoryDashboard',
    component: HistoryDashboard
  },
];

const router = createRouter({
    history: createWebHistory(),
    routes
  })
  
  export default router