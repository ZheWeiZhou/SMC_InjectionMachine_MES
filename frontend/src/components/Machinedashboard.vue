<template>
    <v-row>
        <UperNavbar /> 
    </v-row>
    <v-dialog v-model="dialog" max-width="700"  transition="dialog-bottom-transition" >
      <v-card>
        <v-toolbar :title="'Edit &nbsp;&nbsp;&nbsp;'+ selectparameter" color="primary"></v-toolbar>
        <v-card-text>
            <v-row>
                <v-col>
                    <v-text-field label="Value" v-model="parametervalue" type="number" min="0"></v-text-field>
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false;changeparameter();">Submit</v-btn>
          <v-btn color="blue darken-1" text @click="dialog = false;">Cancle</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-row class="mt-5 mr-1 ml-1">
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
    <v-row class="mr-1 ml-1" style="min-height: 70%;">
    <v-col>
    <svg width="100%" height="100%" >
        <rect x="0" y="0" rx="15" ry="15" width="100%" height="100%" fill="#82AE39" fill-opacity="0.6"/>
        <text x="1%" y="9%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="32" >Barrel Temperature(&deg;C)</text>
        <text x="76%" y="7%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="16" >!!! Click the settings icon to adjust parameters</text>
        <text x="1%" y="23%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Settings</text>
        <g v-for="([key, value], index) in barreltempset" :key="key">
        <text
            :x="barrelsetgetX(index) +2.5 +'%'"
            y="23%"
            text-anchor="middle"
            font-size="28"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ value.value }}
        </text>
        <image style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="7%" height="7%" :x="barrelsetgetX(index) -5 + '%'" y="18%" @click="handleClick(key)"/>
        </g>
        <text x="1%" y="35%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Actual </text>
        <g v-for="([key, value], index) in barreltempact" :key="key">
        <text
            :x="barrelsetgetX(index) +2.5 +'%'"
            y="35%"
            text-anchor="middle"
            font-size="28"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10 }}
        </text>
        </g>
        <image :href="require('@/assets/screw.png')"  width="80%" height="20%" x="10%" y="40%" />
        <text x="1%" y="63%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="32" >Filling Setting</text>
        <text x="1%" y="77%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Position</text>
        <g v-for="([key, value], index) in ijpos" :key="key">
        <text
            :x="possetsetgetX(index) +2.5 +'%'"
            y="77%"
            text-anchor="middle"
            font-size="28"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10  }}
        </text>
        <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="7%" height="7%" :x="possetsetgetX(index) -5 + '%'" y="72%" @click="handleClick(key)"/>
        </g>
        <text x="1%" y="90%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Speed</text>
        <g v-for="([key, value], index) in ispe" :key="key">
        <text
            :x="ijspsetgetX(index) +2.5 +'%'"
            y="90%"
            text-anchor="middle"
            font-size="28"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10  }}
        </text>
        <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="7%" height="7%" :x="ijspsetgetX(index) -5 + '%'" y="85%" @click="handleClick(key)"/>
        </g>
    </svg>
    </v-col>
    </v-row>
    <v-row class="mr-1 ml-1" style="min-height: 28%;">
    <v-col>
        <svg width="100%" height="100%">
            <rect x="0" y="0" rx="15" ry="15" width="100%" height="100%" fill="#FEEE81" fill-opacity="0.6"/>
            <text x="1%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Holding Pressure</text>
            <g v-for="([key, value], index) in holdp" :key="key">
                <text
                    :x="holdgetX(index) +2.5 +'%'"
                    y="46%"
                    text-anchor="middle"
                    font-size="28"
                    fill="black"
                    font-family="monospace" font-weight="bold"
                >
                    {{ Math.round(value.value * 10) / 10  }}
                </text>
                <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="14%" height="14%" :x="holdgetX(index) -10 + '%'" y="35%" @click="handleClick(key)"/>
            </g>
            <text x="1%" y="70%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Holding Time</text>
            <g v-for="([key, value], index) in holdt" :key="key">
                <text
                    :x="holdgetX(index) +2.5 +'%'"
                    y="93%"
                    text-anchor="middle"
                    font-size="28"
                    fill="black"
                    font-family="monospace" font-weight="bold"
                >
                    {{ Math.round(value.value * 10) / 10  }}
                </text>
                <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="14%" height="14%" :x="holdgetX(index) -10 + '%'" y="82%" @click="handleClick(key)"/>
            </g>
        </svg>
    </v-col>
    <v-col>
        <svg width="100%" height="100%">
            <rect x="0" y="0" rx="15" ry="15" width="100%" height="100%" fill="#C0E3E1" fill-opacity="0.6"/>
            <text x="3%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Cooling Time</text>
            <image  :href="require('@/assets/coldwater.png')"  width="18%" height="18%" x="18%" y="6%" />
            <image  style="cursor: pointer;" v-if="coolingtime.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="13%" height="13%" x="-2%" y="25%" @click="handleClick('cooling_time')"/>
            <text x="15%" y="70%" fill="#0071BC" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="90" >{{ Math.round(coolingtime.value * 10) / 10 }}</text>
            <text x="12.5%" y="90%" fill="#0071BC" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Sec</text>

            <text x="32%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Injection Pressure</text>
            <image  :href="require('@/assets/pressure.png')"  width="18%" height="18%" x="59%" y="6%" />
            <image  style="cursor: pointer;" v-if="ijpressure.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="13%" height="13%" x="28%" y="25%" @click="handleClick('injection_pressure_set')"/>
            <text x="50%" y="70%" fill="#D27D00" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="90" >{{ Math.round(ijpressure.value * 10) / 10 }}</text>
            <text x="47.5%" y="90%" fill="#D27D00" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Bar</text>

            <text x="73%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Back Pressure</text>
            <g v-for="([key, value], index) in backpressure" :key="key">
                <text
                    x="85%"
                    :y="backgetX(index) +13 +'%'"
                    text-anchor="middle"
                    font-size="28"
                    fill="black"
                    font-family="monospace" font-weight="bold"
                >
                    {{ Math.round(value.value * 10) / 10  }}
                </text>
                <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="14%" height="14%" x="70%" :y="backgetX(index) +2 +'%'" @click="handleClick(key)"/>
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
        dialog: false,
        machinename :'',
        selectparameter:'',
        parametervalue:'',
        machineonline : 'Offline',
        offlinecolor:'#C8CAD3',
        machinedata:{},
        barreltempset:[],
        barreltempact:[],
        ijpos:[],
        ispe:[],
        holdp:[],
        holdt:[],
        barrelsetgap:'',
        barrelsetgetX:'',
        possetgap:'',
        possetsetgetX:'',
        ijspsetgap:'',
        ijspsetgetX:'',
        holdgap:'',
        holdgetX:'',
        coolingtime:{"value":'',"edit":''},
        ijpressure:{"value":'',"edit":''},
        backpressure:[],
        backgap:'',
        backgetX:'',


        
    }),
    methods: {
        async getmachinedata(){
            var name = this.$cookies.get('setSelectMachine');
            this.machinename = name;
            await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/realtimedata/${name}`,
            ).then( (response) => {
            if (response.data.status=='error'){
                console.log('Fail')
            }
            else{
                var resdata = response.data.Data;
                this.machineonline = resdata["Online"]
                if(this.machineonline == "Online"){
                    this.offlinecolor = "#39CC64"
                }
                else{
                    this.offlinecolor = "#C8CAD3"
                }
                if ('barrel_temp_set' in resdata["machinestatus"]){
                    this.barreltempset = Object.entries(resdata["machinestatus"]['barrel_temp_set']);
                    this.barrelsetgap = computed(() => 100/ (this.barreltempset.length + 1))
                    this.barrelsetgetX = (index) => this.barrelsetgap * (index + 1)
                }
                if ('barrel_temp_real' in resdata["machinestatus"]){
                    this.barreltempact = Object.entries(resdata["machinestatus"]['barrel_temp_real']);
                }
                if ('injection_pos' in resdata["machinestatus"]){
                    this.ijpos = Object.entries(resdata["machinestatus"]['injection_pos']);
                    this.possetgap = computed(() => 100/ (this.ijpos.length + 1))
                    this.possetsetgetX = (index) => this.possetgap * (index + 1)
                }
                if ('injection_speed' in resdata["machinestatus"]){
                    this.ispe = Object.entries(resdata["machinestatus"]['injection_speed']);
                    this.ijspsetgap = computed(() => 100/ (this.ispe.length + 1))
                    this.ijspsetgetX = (index) => this.ijspsetgap * (index + 1)
                }
                if ('holdingpressureset' in resdata["machinestatus"]){
                    this.holdp = Object.entries(resdata["machinestatus"]['holdingpressureset']);
                    this.holdgap = computed(() => 100/ (this.holdp.length + 1))
                    this.holdgetX = (index) => this.holdgap * (index + 1)
                }
                if ('holdingtimeset' in resdata["machinestatus"]){
                    this.holdt = Object.entries(resdata["machinestatus"]['holdingtimeset']);
                    this.holdgap = computed(() => 100/ (this.holdt.length + 1))
                    this.holdgetX = (index) => this.holdgap * (index + 1)
                }
                if ('cooling_time' in resdata["machinestatus"]){
                    this.coolingtime = resdata["machinestatus"]['cooling_time'];
                }
                if ('injection_pressure_set' in resdata["machinestatus"]){
                    this.ijpressure = resdata["machinestatus"]['injection_pressure_set'];
                }
                if ('backpressure' in resdata["machinestatus"]){
                    this.backpressure = Object.entries(resdata["machinestatus"]['backpressure']);
                    this.backgap = computed(() => 100/ (this.backpressure.length + 1))
                    this.backgetX = (index) => this.backgap * (index + 1)
                }
            }

        })
    },
    handleClick(key){
        this.selectparameter = key
        this.dialog = true
    },
    async changeparameter(){
        var requestbody = {"machine_name":this.machinename,"target":this.selectparameter,"value":this.parametervalue};
        const token = this.$store.getters.getToken;
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/control`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
                if (response.data.status=='error'){
                    console.log('edit parameter fail')
            }
            else{
                console.log('edit parameter success')
            }
            })
    }
},
    mounted(){
        var token = this.$cookies.get('accesstoken');
        if (!token){
            this.$router.push({ name: 'Login' });
        }
        var namecheck = this.$cookies.get('setSelectMachine');
        if (!namecheck){
            this.$router.push({ name: 'MachineOverview' });
        }
        else{
        this.getmachinedata();
        this.timer=setInterval(this.getmachinedata,1000);
        }
    },
    beforeDestory(){
      clearInterval(this.timer);
  },    
  }
</script>
