import LoginPage from '@/components/Login';
import MachineOverviewPage from '@/components/MachineOverview';
import MachineDashboard from '@/components/Machinedashboard';
import HistoryDashboard from '@/components/HistoryDashboard';
import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'MachineOverview',
    component: MachineOverviewPage
  },
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