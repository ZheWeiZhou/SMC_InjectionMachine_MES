
import LoginPage from '@/components/Login';
import MachineOverviewPage from '@/components/MachineOverview';
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
  }
];

const router = createRouter({
    history: createWebHistory(),
    routes
  })
  
  export default router