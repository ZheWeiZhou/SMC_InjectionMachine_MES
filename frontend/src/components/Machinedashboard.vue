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
<!-- PROCESS LINE DIALOG -->
    <v-dialog v-model="processlinedisplay" width="95%" height="150%" transition="dialog-bottom-transition" >
    <v-card>
        <v-card-title class="d-flex justify-end">
            <v-btn size="x-small" icon="mdi-close" color="blue darken-1" @click="processlinedisplay = false"></v-btn>
        </v-card-title>
    <v-row class="mr-1 ml-1">
        <v-col>
            <v-card>
                <v-card-title class="text-h6">Updated Time : {{ processlinemessage.created_time }}</v-card-title>
                <v-card-text>
                        <v-img
                            contain
                            max-height="280"
                            max-width="650"    
                            :src="`data:image/png;base64,${processlinemessage.image_str}`"
                            alt="Base64 Image"
                            align="center"
                            justify="center"
                        ></v-img>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title class="text-h5">Quality</v-card-title>
                        <v-card-text class="text-h6">
                            <span>{{ processlinemessage.quality }}</span>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title class="text-h5">Weight</v-card-title>
                        <v-card-text class="text-h6">
                            <span>{{ processlinemessage.product_weight }} g</span>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title class="text-h5">Short Shot Ratio</v-card-title>
                        <v-card-text class="text-h6">
                            <span>{{ processlinemessage.shortshotratio }}</span>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
    <!-- Process Line AUTO Trouble shooting -->
    <v-row class="mr-1 ml-1">
        <v-col >
            <v-row >
                <v-col>
                    <v-card>
                        <v-card-title class="text-h5">Diagnosis Result : {{ sloveabstract.DefectReason }}</v-card-title>
                        <v-card-text class="text-h6">
                             <v-list >
                                <v-list-item
                                v-for="(item, index) in sloveabstract.SloveAbstract"
                                :key="index"
                                >
                                    <v-list-item-content>
                                        <v-list-item-title class="text-h6">
                                            <span> {{ item.Parameter }}</span> : 
                                            <span >
                                                {{ item.Origin }}
                                            </span>
                                            →
                                            <span>
                                                {{ item.New }}
                                            </span>
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                             </v-list>
                        </v-card-text>
                    </v-card>
                </v-col>

            </v-row>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-text class="text-h6"> 
                            <v-timeline align="start" direction="horizontal">
                                <v-timeline-item
                                class="no-dot"
                                v-for="(item, index) in this.slovetimeline"
                                :key="index"
                                icon=""
                                color="primary"
                                >
                                <div>
                                    Reason: {{ item.DefectReason }}<br />
                                    Adjust Parameter ：{{ item.AdjustParameter }}<br />
                                    <v-img
                                        contain
                                        max-height="70"
                                        max-width="70"    
                                        :src="`data:image/png;base64,${item.image_str}`"
                                        alt="Base64 Image"
                                        align="center"
                                        justify="center"
                                    ></v-img>                                    
                                </div>
                                </v-timeline-item>
                            </v-timeline>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>    
        </v-col>
    </v-row>
    </v-card>
    </v-dialog>


    <v-row class="mt-5 mr-1 ml-1">
        <v-col>
            <v-card class="h-100">
                <v-card-title class="text-h4">Machine Name</v-card-title>
                <v-card-text class="text-h5">{{machinename}}</v-card-text>
            </v-card>
        </v-col>
        <v-col>
            <v-card class="h-100">
                <v-card-title class="text-h4">Connect Status</v-card-title>
                <v-card-text class="text-h5" :style="{color:offlinecolor}" >{{machineonline}}</v-card-text>
            </v-card>
        </v-col>
        <v-col v-if = "troubleshootingavailable =='True'">
            <v-card class="h-100">
                <v-card-title class="text-h4">Trouble Shooting</v-card-title>
                <v-card-actions>
                <v-btn  class="mr-2 ml-3" color="info" rounded="xl">
                    Diagnosis
                </v-btn>
                <v-btn class="mr-2 ml-3" color="info" v-if="machinename =='FCS-150' || machinename =='TOYO'" @click ="clickprocessline" rounded="xl">
                    Auto Mode Monitor
                </v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
    <!-- Process Line status display -->
    <v-row class="mr-1 ml-1" v-if ="processlinedisplay">
        <v-col>
            <v-card>
                <v-card-title class="text-h6">Updated Time : {{ processlinemessage.created_time }}</v-card-title>
                <v-card-text>
                        <v-img
                            contain
                            max-height="350"
                            max-width="700"    
                            :src="`data:image/png;base64,${processlinemessage.image_str}`"
                            alt="Base64 Image"
                            align="center"
                            justify="center"
                        ></v-img>
                </v-card-text>
            </v-card>
        </v-col>
        <v-col>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title class="text-h4">Quality</v-card-title>
                        <v-card-text class="text-h5">
                            <span>{{ processlinemessage.quality }}</span>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title class="text-h4">Weight</v-card-title>
                        <v-card-text class="text-h5">
                            <span>{{ processlinemessage.product_weight }} g</span>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title class="text-h4">Short Shot Ratio</v-card-title>
                        <v-card-text class="text-h5">
                            <span>{{ processlinemessage.shortshotratio }}</span>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
    <v-row class="mr-1 ml-1" style="min-height: 600px;">
    <v-col>
    <svg width="100%" height="100%" >
        <rect x="0" y="0" rx="15" ry="15" width="100%" height="100%" fill="#82AE39" fill-opacity="0.6"/>
        <text x="1%" y="9%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="195%" >Barrel Temperature(&deg;C)</text>
        <text x="73%" y="7%" fill="black" text-anchor="start" font-family="monospace" font-weight="bold" font-size="16" >!!! Click the settings icon to adjust parameters</text>
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
                <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="9%" height="9%" :x="holdgetX(index) -7 + '%'" y="38.5%" @click="handleClick(key)"/>
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
                <image  style="cursor: pointer;" v-if="value.edit == 'acctivate'" :href="require('@/assets/settings.png')"  width="9%" height="9%" :x="holdgetX(index) -7 + '%'" y="85.5%" @click="handleClick(key)"/>
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
        troubleshootingavailable : "False",
        processlinedisplay : false,
        processlinestauts: "standby",
        processlinemessage : {"created_time":"NA","image_str":"","product_weight":"NA","quality":"NA","shortshotratio":"NA"},
        sloveabstract:{"DefectReason":"None","SloveAbstract":[]},
        slovetimeline:[]
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
    async getprocesslineinfo(){
        var requestbody = {"machine_name":this.machinename};
        const token = this.$store.getters.getToken;
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/processlineinfo`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
                if (response.data.status=='error'){
                    console.log('Get process line info fail')
            }
            else{
                var rawinfo             = response.data.Data.processlinemessage;
                if (response.data.Data.processlinemessage.quality == "shortshot"){
                    rawinfo.quality  = "Short Shot"
                    // 如果偵測到是短射那就要撈取診斷資料拿來做timeline
                    this.getsloveabstract();
                }
                else{
                    // 如果產品已經沒問題了，那就把跟abstract清空，然後給timeline一個好結局
                    this.sloveabstract = {"DefectReason":"None","SloveAbstract":[]};
                    if(this.slovetimeline.length < 1 ){
                        this.slovetimeline.push({"DefectReason":"Finish","AdjustParameter":"None","image_str":rawinfo.image_str});
                        // var lastone = this.slovetimeline[this.slovetimeline.length -1];
                        // if (lastone["DefectReason"] == "Finish"){
                        //     this.slovetimeline = [];
                        // }
                    }
                    else{
                        var lastone = this.slovetimeline[this.slovetimeline.length -1];
                        if (lastone["DefectReason"] != "Finish"){
                            this.slovetimeline.push({"DefectReason":"Finish","AdjustParameter":"None","image_str":rawinfo.image_str})
                        }
                    }
                }
                rawinfo.product_weight  = rawinfo.product_weight.toFixed(2)
                rawinfo.shortshotratio  = rawinfo.shortshotratio.toFixed(2)
                this.processlinemessage = rawinfo;

            }
            })
    },
    async getsloveabstract(){
        var requestbody = {"machine_name":this.machinename};
        const token = this.$store.getters.getToken;
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/troubleshooting/getabstract`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status=='error'){
                    console.log('Get Slove abstract fail');
                    this.sloveabstract={"DefectReason":"None","SloveAbstract":[]};
            }
            else{
                this.sloveabstract  = response.data.Data.SloveAbstract;
                var adjsutparameter = "";
                for(const item of response.data.Data.SloveAbstract.SloveAbstract){
                    adjsutparameter = adjsutparameter + item["Parameter"]+"; "
                }
                if (this.slovetimeline.length > 0){
                    var lastone = this.slovetimeline[this.slovetimeline.length -1];
                    if (lastone["DefectReason"] == "Finish"){
                        this.slovetimeline = [];
                    }
                }
                var timelinedata = {"DefectReason":this.sloveabstract.DefectReason,"AdjustParameter":adjsutparameter,"image_str":this.processlinemessage.image_str};
                this.slovetimeline.push(timelinedata);

            }
            })
    },
    async getprocesslinestatus(){
        if(this.troubleshootingavailable =='True'){
            var requestbody = {"machine_name":this.machinename};
            const token = this.$store.getters.getToken;
            await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/processlinestatus`,requestbody,{
                    headers:{"accesstoken":token}
                }
                ).then( (response) => {
                if (response.data.status=='error'){
                        console.log('Get process line status fail');
                        this.processlinestauts = "NA";
                }
                else{
                    var currentprocesslinestatus = response.data.Data.processlinestatus;
                    if (currentprocesslinestatus != "NA"){
                        if (this.processlinestauts != currentprocesslinestatus ){
                            if(currentprocesslinestatus == "standby"){
                                this.getprocesslineinfo();
                            }
                        }
                        this.processlinestauts = currentprocesslinestatus;
                    }
                    else{
                        this.processlinestauts = currentprocesslinestatus;
                    }

                }
            })
        }
    },
    clickprocessline(){
        this.processlinedisplay = !this.processlinedisplay
        this.processlinemessage = {"created_time":"NA","image_str":"","product_weight":"NA","quality":"NA","shortshotratio":"NA"}
        if (this.processlinedisplay){
            this.getprocesslineinfo();
        }
        else {
            this.processlinestauts = "NA"
        }
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
    },

    async checktroubleshhotingavailable(){
        var name = this.$cookies.get('setSelectMachine');
        const token = this.$store.getters.getToken;
        this.machinename = name;
        var requestbody = {"machine_name":this.machinename};
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/checktroubleshootingfunction`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
        if (response.data.status=='error'){
                console.log('Fail')
        }
        else{
                this.troubleshootingavailable = response.data.Data.activate
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
        this.checktroubleshhotingavailable();
        this.processlinetimer = setInterval(this.getprocesslinestatus,1000)
        }
    },
    beforeDestory(){
      clearInterval(this.timer);
      clearInterval(this.processlinetimer);
  },    
  }
</script>

<style scoped>
.no-dot .v-timeline-item__dot {
  display: none !important;
}
</style>