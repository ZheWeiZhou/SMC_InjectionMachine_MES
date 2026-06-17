<template>
    <v-overlay
      :model-value="isLoading"
      class="align-center justify-center"
      persistent
    >
      <v-progress-circular
        color="primary"
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

    <v-row>
        <UperNavbar /> 
    </v-row>    
    <v-row  class="mt-10 mr-1 ml-1">
        <v-col 
          v-for="(data, machineName, index) in machinedata" 
          :key="machineName"
          cols="12" sm="6" md="4" lg="3"
          class="card-enter-animation"
          :style="{ animationDelay: `${index * 100}ms` }"
        >
            <v-card 
  v-ripple
  elevation="3" 
  max-width="350"
  :class="['machine-card', 'rounded-xl', 'mx-auto', { 'is-offline': data[1] === 'Offline' }]"
  :style="{ 
    borderTop: '6px solid ' + (data[1] === 'Offline' ? '#9E9E9E' : data[0]),
    opacity: data[1] === 'Offline' ? 0.6 : 1,
    cursor: data[1] === 'Offline' ? 'default' : 'pointer',
    '--status-color': data[0]
  }"
  @click="data[1] !== 'Offline' && selectmachine(machineName)"
>
  <!-- 頂部：機台名稱與連線狀態 -->
  <div class="d-flex justify-space-between align-center px-4 pt-5 pb-2">
    <span class="text-h6 font-weight-black text-truncate" style="color: #2c3e50;">
      {{ machineName }}
    </span>
    <div class="d-flex align-center" :class="data[1] === 'Online' ? 'text-success' : 'text-grey'">
      <v-icon size="small" class="mr-1 breathing-circle wifi-icon">
        {{ data[1] === 'Online' ? 'mdi-wifi' : 'mdi-wifi-off' }}
      </v-icon>
      <span class="text-caption font-weight-bold">{{ data[1].toUpperCase() }}</span>
    </div>
  </div>

  <!-- 中間：圖片展示區 (保持原樣) -->
  <v-img
    :src="require('@/assets/ijmachine.png')"
    height="120"
    class="mt-2 mb-2"
    style="mix-blend-mode: multiply;"
  ></v-img>

  <!-- 底部：運作狀態大標籤 -->
  <div class="glass-bar px-4 py-3 d-flex justify-center rounded-b-xl">
    <v-chip 
      :color="data[1] === 'Offline' ? 'grey-darken-1' : data[0]" 
      variant="elevated" 
      elevation="2"
      size="large"
      class="font-weight-bold px-6 text-white"
    >
      <v-icon start :class="{ 'spin-animation': data[1] === 'Online' && data[2] === 'Work' }">
        {{ 
          data[1] === 'Offline' ? 'mdi-power-plug-off' : 
          data[2] === 'Work' ? 'mdi-cog-play' : 
          data[2] === 'Stay' ? 'mdi-pause-circle' : 
          'mdi-sleep' 
        }}
      </v-icon>
      {{ data[1] === 'Offline' ? 'OFFLINE' : data[2].toUpperCase() }}
    </v-chip>
  </div>

</v-card>
        </v-col>
    </v-row>
</template>
  

  <style>
    .machine-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .machine-card:hover {
      transform: translateY(-6px);
      /* 當滑鼠懸停時，根據機台狀態顏色顯示對應的"光暈"陰影 */
      box-shadow: 0px 10px 20px -5px var(--status-color) !important;
    }
    /* 如果是離線狀態，則使用較柔和的灰色陰影 */
    .machine-card.is-offline:hover {
      box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1) !important;
    }
    .machine-card:active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2) !important;
    }

    /* WiFi 圖示的旋轉動畫設定 */
    .wifi-icon {
      transition: transform 0.5s ease-in-out;
    }
    .machine-card:hover .wifi-icon {
      transform: rotate(360deg);
    }

    .breathing-circle {
      animation: breathe 2s infinite ease-in-out;
      transform-origin: center;
    }

    @keyframes breathe {
      0% {
        opacity: 0.5;
      }
      50% {
        opacity: 1;
      }
      100% {
        opacity: 0.5;
      }
    }
    svg g {
      cursor: pointer;
    }
    .glass-bar {
      background-color: rgba(255, 255, 255, 0.4);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px); /* 支援 Safari */
      border-top: 1px solid rgba(255, 255, 255, 0.2);
    }

    .card-enter-animation {
      animation: slide-up-fade-in 0.6s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
      opacity: 0; /* 動畫開始前保持透明 */
    }

    @keyframes slide-up-fade-in {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  </style>
  <script>
import axios from 'axios';
import UperNavbar  from './layout/UperNavbar.vue';
  export default {
    name: 'MachineOverviewPageV2',
    components: {
            UperNavbar
    },
    data: () => ({
        isLoading: false,
        machinedata: {},
        offlinecolor:"#121212",
        onlinecolor:"rgba(255,196,51,0.6)",
        workcolor: "#4CAF50",
        staycolor:"#BDBDBD",

    }),
    methods: {
        async getmachineonlinestatus(){
            const token = this.$store.getters.getToken;

            await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/machineconnectstatus`,
            {
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status=='error'){
            this.machinedata = {};
            }
            else{
                var res = response.data.Data;
            var newMachineData = {};
                Object.keys(res).forEach(key => {
                    var machinestatus = res[key]
                    if (machinestatus['Online'] == 'Offline'){
                    newMachineData[key] =  ["#000000",'Offline','Sleep',"#000000"];
                    }
                    else{
                        var machinework = machinestatus['Status'].charAt(0).toUpperCase() + machinestatus['Status'].slice(1)
                        var statuscolor = this.staycolor
                        if (machinework == "Work"){
                            statuscolor = this.workcolor
                        }
                        newMachineData[key] =  [statuscolor,'Online',machinework,statuscolor];
                    }
                });
                this.machinedata = newMachineData;
            }
        })
        },
        selectmachine(name){
            var machinename = name;
            
            this.$cookies.set('setSelectMachine', machinename, '1d');

            this.isLoading = true;
            
            // 延遲 250 毫秒再跳轉，讓使用者能看見完整的點擊回饋動畫
            setTimeout(() => {
                this.$router.push({ name: 'MachineDashboard' });
            }, 250);
        }
    },
    mounted(){   
        var token = this.$cookies.get('accesstoken');
        if (!token){
            console.log("Not Login");
            this.$router.push({ name: 'Login' });
        }
        else{
        this.getmachineonlinestatus();
        this.timer=setInterval(this.getmachineonlinestatus,1000);     
        }
    },
    beforeDestory(){
      clearInterval(this.timer);
  },    
  }
</script>
