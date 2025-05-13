<template>
    <v-row>
        <UperNavbar /> 
    </v-row>    
    <v-row class="mt-5">
        <v-col>
            <v-card>
                <v-card-title class="text-h4">Machine Name</v-card-title>
                <v-card-text class="text-h5">{{machinename}}</v-card-text>
            </v-card>
        </v-col>
        <v-col>
            <v-card>
                <v-card-title class="text-h4">Connect Status</v-card-title>
                <v-card-text class="text-h5" :style="{color:offlinecolor}" >{{machineonline}}</v-card-text>
            </v-card>
        </v-col>
    </v-row>
    <v-row>
        <v-col>
            <svg width="100%" height="100" style="border: 1px solid #ccc;">
    <g v-for="([key, value], index) in barreltempset" :key="key">
      <!-- 顯示 value -->
      <text
        :x="barrelsetgetX(index) +2.5 +'%'"
        y="50"
        text-anchor="middle"
        font-size="32"
        fill="black"
        font-family="monospace" font-weight="bold"
      >
        {{ value.value }}
      </text>

      <!-- 點擊圓形 -->
      <circle
        :cx="barrelsetgetX(index) + '%'"
        cy="40"
        r="10"
        fill="blue"
        style="cursor: pointer;"
        @click="handleClick(key)"
      />
    </g>
  </svg>
        </v-col>
    </v-row>
</template>
  

<style scoped>
</style>
  <script>
import axios from 'axios';
import UperNavbar  from './layout/UperNavbar.vue';
import { computed } from 'vue'
  export default {
    name: 'MachineDashboard',
    components: {
            UperNavbar
    },
    data: () => ({
        machinename :'',
        machineonline : 'Offline',
        offlinecolor:'#C8CAD3',
        machinedata:{},
        barreltempset:{},
        barrelsetgap:'',
        barrelsetgetX:''

        
    }),
    methods: {
        async getmachinedata(){
            var name = this.$cookies.get('setSelectMachine');
            this.machinename = name;
            await axios.get(`http://${this.$store.getters.getHost}/smc/injectionmachinemes/realtimedata/${name}`,
            ).then( (response) => {
            if (response.data.status=='error'){
                console.log('Fail')
            }
            else{
                console.log(response.data.Data)
                var resdata = response.data.Data;
                this.machineonline = resdata["Online"]
                if(this.machineonline == "Online"){
                    this.offlinecolor = "#39CC64"
                }
                else{
                    this.offlinecolor = "#C8CAD3"
                }
                if ('barrel_temp_set' in resdata["machinestatus"]){
                    console.log('1111')
                    this.barreltempset = Object.entries(resdata["machinestatus"]['barrel_temp_set']);
                    console.log(this.barreltempset)
                    this.barrelsetgap = computed(() => 100/ (this.barreltempset.length + 1))
                    console.log(this.barrelsetgap)
                    this.barrelsetgetX = (index) => this.barrelsetgap * (index + 1)
                }

            }

        })
    },
    handleClick(key){
        console.log(key)
    }
},
    mounted(){
        var loginstate = this.$store.getters.isLoggedIn;
        if (!loginstate){
            this.$router.push({ name: 'Login' });
        }
        this.getmachinedata()
        // this.timer=setInterval(this.getmachineonlinestatus,100);
    },
//     beforeDestory(){
//       clearInterval(this.timer);
//   },    
  }
</script>