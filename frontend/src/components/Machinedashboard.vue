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
    <v-row class="mr-1 ml-1" style="min-height: 600px;">
    <v-col>
    <svg width="100%" height="100%" >
        <rect x="0" y="0" rx="15" ry="15" width="100%" height="100%" fill="#82AE39" fill-opacity="0.6"/>
        <text x="1%" y="9%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="195%" >Barrel Temperature(&deg;C)</text>
        <text x="76%" y="7%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="16" >!!! Click the settings icon to adjust parameters</text>
        <text x="1%" y="23%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="190%" >Settings</text>
        <g v-for="([key, value], index) in barreltempset" :key="key">
        <text
            :x="barrelsetgetX(index) +3.5 +'%'"
            y="23%"
            text-anchor="middle"
            font-size="180%"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ value.value }}
        </text>
        <image style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="4%" height="4%" :x="barrelsetgetX(index) -4 + '%'" y="20%" @click="handleClick(key)"/>
        </g>
        <text x="1%" y="35%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="190%" >Actual </text>
        <g v-for="([key, value], index) in barreltempact" :key="key">
        <text
            :x="barrelsetgetX(index) +3.5 +'%'"
            y="35%"
            text-anchor="middle"
            font-size="180%"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10 }}
        </text>
        </g>
        <image :href="require('@/assets/screw.png')"  width="75%" height="11%" x="10%" y="40%" />
        <text x="1%" y="62%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="190%" >Position</text>
        <g v-for="([key, value], index) in ijpos" :key="key">
        <text
            :x="possetsetgetX(index) +11 +'%'"
            y="62%"
            text-anchor="middle"
            font-size="180%"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10  }}
        </text>
        <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')" width="4%" height="4%" :x="possetsetgetX(index) +6 + '%'" y="58.5%" @click="handleClick(key)"/>
        </g>
        <text x="1%" y="73%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="190%" >Speed</text>
        <g v-for="([key, value], index) in ispe" :key="key">
        <text
            :x="ijspsetgetX(index) +11 +'%'"
            y="73%"
            text-anchor="middle"
            font-size="180%"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10  }}
        </text>
        <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"   width="4%" height="4%" :x="ijspsetgetX(index) +6 + '%'" y="69.5%" @click="handleClick(key)"/>
        </g>
        <text x="1%" y="84%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="190%" >Pressure</text>
        <g v-for="([key, value], index) in ijprelist" :key="key">
        <text
            :x="ijspsetgetX(index) +11 +'%'"
            y="84%"
            text-anchor="middle"
            font-size="180%"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10  }}
        </text>
        <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="4%" height="4%" :x="ijspsetgetX(index) +6 + '%'" y="80.5%" @click="handleClick(key)"/>
        </g>   
        <text x="1%" y="95%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="180%" >Backpressure</text>
        <g v-for="([key, value], index) in backpressure" :key="key">
        <text
            :x="backgetX(index) +11 +'%'"
            y="95%"
            text-anchor="middle"
            font-size="180%"
            fill="black"
            font-family="monospace" font-weight="bold"
        >
            {{ Math.round(value.value * 10) / 10  }}
        </text>
        <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"   width="4%" height="4%" :x="backgetX(index) +6 + '%'" y="91.5%" @click="handleClick(key)"/>
        </g>      
    </svg>
    </v-col>
    </v-row>
    <v-row class="mr-1 ml-1" style="min-height: 20%;">
    <v-col>
        <svg width="100%" height="100%">
            <rect x="0" y="0" rx="15" ry="15" width="100%" height="100%" fill="#FEEE81" fill-opacity="0.6"/>
            <text x="1%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Holding Pressure</text>
            <g v-for="([key, value], index) in holdp" :key="key">
                <text
                    :x="holdgetX(index) +2.5 +'%'"
                    y="46%"
                    text-anchor="middle"
                    font-size="25"
                    fill="black"
                    font-family="monospace" font-weight="bold"
                >
                    {{ Math.round(value.value * 10) / 10  }}
                </text>
                <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="12%" height="12%" :x="holdgetX(index) -8 + '%'" y="36%" @click="handleClick(key)"/>
            </g>
            <text x="1%" y="70%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Holding Time</text>
            <g v-for="([key, value], index) in holdt" :key="key">
                <text
                    :x="holdgetX(index) +2.5 +'%'"
                    y="93%"
                    text-anchor="middle"
                    font-size="25"
                    fill="black"
                    font-family="monospace" font-weight="bold"
                >
                    {{ Math.round(value.value * 10) / 10  }}
                </text>
                <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="12%" height="12%" :x="holdgetX(index) -8 + '%'" y="83%" @click="handleClick(key)"/>
            </g>
        </svg>
    </v-col>
    <v-col>
        <svg width="100%" height="100%">
            <rect x="0" y="0" rx="15" ry="15" width="100%" height="100%" fill="#C0E3E1" fill-opacity="0.6"/>
            <text x="5%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="200%" >Cooling Time</text>
            <!-- <image  :href="require('@/assets/coldwater.png')"  width="18%" height="18%" x="18%" y="6%" /> -->
            <image  style="cursor: pointer;" v-if="coolingtime.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="13%" height="13%" x="0%" y="28%" @click="handleClick('cooling_time')"/>
            <text x="17%" y="73%" fill="#0071BC" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="600%" >{{ Math.round(coolingtime.value * 10) / 10 }}</text>
            <!-- <text x="12.5%" y="90%" fill="#0071BC" text-anchor="start" font-family="monospace" font-weight="bold" font-size="30" >Sec</text> -->
            <text x="33%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="200%" >Clamping Force</text>
            <image  style="cursor: pointer;" v-if="clamp_force_set.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="13%" height="13%" x="25%" y="25%" @click="handleClick('clamp_force_set')"/>
            <text x="47%" y="73%" fill="#D27D00" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="600%" >{{ Math.round(clamp_force_set.value * 10) / 10 }}</text>
            <text x="65%" y="20%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="190%" >Filling time set</text>
            <image  style="cursor: pointer;" v-if="filling_time_set.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="13%" height="13%" x="60%" y="25%" @click="handleClick('filling_time_set')"/>
            <text x="82%" y="73%" fill="#44B678" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="600%" >{{filling_time_set.value }}</text>
        </svg>
    </v-col>
    </v-row>
    <v-row class="mr-1 ml-1">
        <v-col>
            <v-card>
                <v-card-title>Process Feedback Data</v-card-title>
                <v-card-text>
                    <v-row>
                            <v-col>
                        <v-table density="compact" fixed-header style="width: 100%;">
                            <thead>
                                <tr>
                                    <th class="text-left" style="background-color:#333333; color:white">Name</th>
                                    <th class="text-left" style="background-color:#333333; color:white">Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="item in feedbacktabledata.slice(0, 15)"
                                    :key="item.Name"
                                >
                                    <td class="text-left" style="background-color: #F5F5F5;">{{ item.Name }}</td>
                                    <td class="text-left" style="background-color: #F5F5F5;">{{ item.Value }}</td>
                                </tr>
                            </tbody>
                        </v-table>
                    </v-col>
                    <v-col>
                        <v-table density="compact" fixed-header style="width: 100%;">
                        <thead>
                            <tr>
                                <th class="text-left" style="background-color:#333333; color:white">Name</th>
                                <th class="text-left" style="background-color:#333333; color:white">Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="item in feedbacktabledata.slice(15)"
                                :key="item.Name"
                            >
                                <td class="text-left" style="background-color: #F5F5F5;">{{ item.Name }}</td>
                                <td class="text-left" style="background-color: #F5F5F5;">{{ item.Value }}</td>
                            </tr>
                        </tbody>
                    </v-table>
                    </v-col>
                    </v-row>
            </v-card-text>
        </v-card>
        </v-col>
    </v-row>
    <v-row class="mr-1 ml-1" >
        <v-col>
            <v-card>
                <v-card-title>Curve Data</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col
                            v-for = "item in curvedatalist"
                            :key="item.Title"
                        >
                        <highcharts :options="createChartOptions(item.Title, item.Data)" />
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
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
        ijprelist:[],
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
        feedbacktabledata :[],
        curvedatalist:[],
        clamp_force_set:{"value":'',"edit":''},
        filling_time_set : {"value":'NA',"edit":''},



        
    }),
    methods: {
        createChartOptions(title, yData) {
            const categories = yData.map((_, i) => (i + 1).toString())
            return {
                chart: { type: 'spline' },  // 曲線圖
                title: { text: title },
                xAxis: {
                categories,
                title: { text: 'time' }
                },
                yAxis: {
                title: { text: 'value' }
                },
                series: [{
                name: title,
                data: yData
                }]
            }
            },
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
                // console.log(resdata)
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
                    this.possetgap = computed(() => 80/ (this.ijpos.length + 1))
                    this.possetsetgetX = (index) => this.possetgap * (index + 1)
                }
                if ('injection_speed' in resdata["machinestatus"]){
                    this.ispe = Object.entries(resdata["machinestatus"]['injection_speed']);
                    this.ijspsetgap = computed(() => 80/ (this.ispe.length + 1))
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
                    this.ijprelist = [["injection_pressure_set",resdata["machinestatus"]['injection_pressure_set']]];
                }
                if ("injection_pressure_list" in resdata["machinestatus"]){
                    this.ijprelist = Object.entries(resdata["machinestatus"]['injection_pressure_list']);

                }
                if ('backpressure' in resdata["machinestatus"]){
                    this.backpressure = Object.entries(resdata["machinestatus"]['backpressure']);
                    this.backgap = computed(() => 80/ (this.backpressure.length + 1))
                    this.backgetX = (index) => this.backgap * (index + 1)
                }
                if ('clamp_force_set' in resdata["machinestatus"]){
                    this.clamp_force_set = resdata["machinestatus"]['clamp_force_set']
                }
                if ('filling_time_set' in resdata["machinestatus"]){
                    this.filling_time_set = resdata["machinestatus"]['filling_time_set']
                }
                this.feedbacktabledata =[]
                for (var key of Object.keys(resdata["machinefeedback"])) {
                    var value = parseFloat(resdata["machinefeedback"][key])
                    value     = Math.floor(value * 10) / 10
                    var item  = {"Name":key,"Value": value}
                    this.feedbacktabledata.push(item)
                }
                var new_curvedata = []
                for (var k of Object.keys(resdata["machinecurve"])){
                    var curvetitle = k
                    var ydata = resdata["machinecurve"][k]
                    ydata = ydata.map(item => parseFloat(item))
                    var curveitem = {"Title":curvetitle,"Data":ydata}
                    new_curvedata.push(curveitem)
                }
                 this.curvedatalist = new_curvedata
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
