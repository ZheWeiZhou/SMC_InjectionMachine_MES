<template>
    <v-row>
        <UperNavbar /> 
    </v-row>
    <v-dialog v-model="dialog" max-width="500" transition="dialog-bottom-transition">
      <v-card style="border-radius: 16px; overflow: hidden;" class="elevation-10">
        <v-toolbar color="blue-darken-3" dark class="px-4">
          <v-icon class="mr-2">mdi-cog</v-icon>
          <span class="text-h6 font-weight-bold">調整參數 Edit Parameter</span>
        </v-toolbar>
        <v-card-text class="pa-6">
          <div class="text-subtitle-1 font-weight-bold text-grey-darken-3 mb-2">
            正在編輯參數: <span class="text-blue-darken-3">{{ formatParameterKey(selectparameter) }}</span>
          </div>
          <v-text-field 
            label="設定數值 New Value" 
            v-model="parametervalue" 
            type="number" 
            min="0" 
            variant="outlined" 
            color="blue-darken-3" 
            focused 
            class="mt-4"
          ></v-text-field>
        </v-card-text>
        <v-card-actions class="px-6 pb-6">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" class="px-4" @click="dialog = false;">Cancel</v-btn>
          <v-btn color="blue-darken-3" variant="elevated" class="px-6" @click="dialog = false;changeparameter();">Submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-row class="mt-10 mr-1 ml-1">
        <PowerMeter v-if="powermeteravailable == 'True' && machineonline == 'Online'" :machinename="machinename"/>
        <PVT v-if="machineonline == 'Online'" :machinename="machinename"/>

        <v-btn v-if="machineonline == 'Online'&& machinename =='FCS-150'" @click="clickheaterbutton"  class="ml-5" text >
            <v-icon left  color="#39CC64">mdi-power</v-icon>
                電熱開關
        </v-btn>
    </v-row>
    <v-row class="mt-5 mr-1 ml-1">
        <v-col>
            <v-card class="h-100">
                <v-card-title class="text-h4">Machine Name</v-card-title>
                <v-card-text class="text-h5">
                    {{machinename}} 
                </v-card-text>
            </v-card>
        </v-col>
        <v-col>
            <v-card class="h-100">
                <v-card-title class="text-h4">Connect Status</v-card-title>
                <v-card-text class="text-h5" :style="{color:offlinecolor}" >{{machineonline}}</v-card-text>
            </v-card>
        </v-col>
        <v-col v-if = "troubleshootingavailable =='True'">
            <TroubleShooting :machineonline="this.machineonline" :machinename="this.machinename" :aoimoduleavailable="this.aoimoduleavailable" :feedbacktabledata="this.feedbacktabledata" />
        </v-col>
    </v-row>
    <!-- Panel 1: Barrel & Injection Profile -->
    <v-row class="mr-1 ml-1 mt-4">
      <v-col cols="12">
        <v-card style="background: linear-gradient(135deg, #F0F7FC 0%, #D6E9F7 100%); border-radius: 16px;" class="elevation-2 hover-lift">
          <v-card-title class="d-flex flex-wrap align-center justify-space-between py-4 px-6">
            <span class="text-h5 font-weight-bold text-blue-darken-4">Barrel Temperature & Injection Profile (料筒溫度與射出設定)</span>
            <v-chip color="amber-darken-4" class="font-weight-bold" prepend-icon="mdi-information-outline">
              Click the settings icon to adjust parameters
            </v-chip>
          </v-card-title>
          
          <v-card-text class="px-6 pb-6">
            <!-- Barrel Heaters Section -->
            <v-card class="pa-4 mb-6 border-0 elevation-1" style="background: rgba(255, 255, 255, 0.65); border-radius: 12px;">
              <div class="text-subtitle-1 font-weight-bold text-blue-darken-3 mb-4">Barrel Temperature (料筒加熱區溫度 &deg;C)</div>
              
              <!-- Screw Schematic Illustration -->
              <div class="d-flex justify-center align-center py-4 mb-4" style="background: rgba(255,255,255,0.5); border-radius: 8px;">
                <v-img :src="require('@/assets/screw3.png')" max-height="60" max-width="400" opacity="0.3" contain></v-img>
              </div>

              <!-- Zones Flex Layout -->
              <div class="d-flex flex-wrap flex-row-reverse justify-space-around">
                <v-card 
                  v-for="([key, value], index) in barreltempset" 
                  :key="key" 
                  class="mx-1 my-2 text-center elevation-1" 
                  min-width="120" 
                  style="background: white; border-radius: 8px; flex: 1 1 120px;"
                >
                  <div class="bg-blue-lighten-4 py-1 text-subtitle-2 font-weight-bold text-blue-darken-4 d-flex align-center justify-center">
                    <span class="heater-led-dot" :class="getHeaterStatus(value.value, barreltempact[index] ? barreltempact[index][1].value : null)"></span>
                    {{ formatParameterKey(key) }}
                  </div>
                  <div class="pa-2">
                    <div class="text-caption text-grey-darken-1">設定 Set</div>
                    <div class="d-flex align-center justify-center py-1">
                      <span class="text-h6 font-weight-bold text-blue-darken-3">{{ value.value }}</span>
                      <v-btn 
                        v-if="value.edit === 'acctivate'" 
                        icon 
                        size="x-small" 
                        variant="text" 
                        color="blue-darken-3" 
                        class="ml-1" 
                        @click="handleClick(key)"
                      >
                        <v-icon size="small">mdi-cog</v-icon>
                      </v-btn>
                    </div>
                    <v-divider class="my-1"></v-divider>
                    <div class="text-caption text-grey-darken-1">實際 Act</div>
                    <div class="text-h6 font-weight-bold text-success py-1">
                      {{ barreltempact[index] ? Math.round(barreltempact[index][1].value * 10) / 10 : '-' }}
                    </div>
                  </div>
                </v-card>
              </div>
            </v-card>

            <!-- Injection Stages Profile Section (Fishbone Layout) -->
            <div class="text-h6 font-weight-bold text-blue-darken-3 mb-4 mt-6 d-flex align-center">
              <v-icon class="mr-2" color="blue-darken-3">mdi-ray-start-arrow</v-icon>
            Injection Setting
            </div>
            
            <div class="fishbone-container mb-6">
              <div class="fishbone-wrapper">
                <div class="fishbone-spine"></div>
                <div class="fishbone-spine-head"></div>
                
                <div 
                  v-for="([posKey, posVal], index) in ijpos" 
                  :key="posKey" 
                  class="fishbone-stage"
                >
                  <!-- Upper branch: Position -->
                  <div class="fishbone-branch upper">
                    <v-card class="fishbone-card position elevation-1">
                      <div class="text-caption font-weight-bold text-blue-darken-3">位置 Position</div>
                      <div class="d-flex align-center justify-center py-1">
                        <span class="text-body-1 font-weight-bold text-blue-darken-3">{{ Math.round(posVal.value * 10) / 10 }}</span>
                        <span class="text-caption ml-1 text-grey font-weight-bold">mm</span>
                        <v-btn 
                          :style="{ visibility: posVal.edit === 'acctivate' ? 'visible' : 'hidden' }" 
                          icon 
                          size="x-small" 
                          variant="text" 
                          color="blue-darken-3" 
                          class="ml-1" 
                          @click="handleClick(posKey)"
                        >
                          <v-icon size="small">mdi-cog</v-icon>
                        </v-btn>
                      </div>
                    </v-card>
                    <div class="fishbone-line"></div>
                  </div>
                  
                  <!-- Central Stage Node -->
                  <div class="fishbone-node">
                    {{ index + 1 }}
                  </div>
                  
                  <!-- Lower branch: Speed & Pressure -->
                  <div class="fishbone-branch lower">
                    <div class="fishbone-line"></div>
                    <v-card class="fishbone-card speed-pressure elevation-1">
                      <!-- Speed -->
                      <div class="text-caption font-weight-bold text-green-darken-3">速度 Speed</div>
                      <div class="d-flex align-center justify-center py-1">
                        <span class="text-body-1 font-weight-bold text-success-darken-3">
                          {{ ispe[index] ? Math.round(ispe[index][1].value * 10) / 10 : '-' }}
                        </span>
                        <span class="text-caption ml-1 text-grey font-weight-bold">mm/s</span>
                        <v-btn 
                          :style="{ visibility: (ispe[index] && ispe[index][1].edit === 'acctivate') ? 'visible' : 'hidden' }" 
                          icon 
                          size="x-small" 
                          variant="text" 
                          color="success" 
                          class="ml-1" 
                          @click="handleClick(ispe[index][0])"
                        >
                          <v-icon size="small">mdi-cog</v-icon>
                        </v-btn>
                      </div>
                      
                      <v-divider class="my-1"></v-divider>
                      
                      <!-- Pressure -->
                      <div class="text-caption font-weight-bold text-orange-darken-4">壓力 Pressure</div>
                      <div class="d-flex align-center justify-center py-1">
                        <span class="text-body-1 font-weight-bold text-orange-darken-4">
                          {{ getPressureValue(index) }}
                        </span>
                        <span class="text-caption ml-1 text-grey font-weight-bold">bar</span>
                        <v-btn 
                          :style="{ visibility: showPressureEdit(index) ? 'visible' : 'hidden' }" 
                          icon 
                          size="x-small" 
                          variant="text" 
                          color="orange" 
                          class="ml-1" 
                          @click="handleClick(getPressureKey(index))"
                        >
                          <v-icon size="small">mdi-cog</v-icon>
                        </v-btn>
                      </div>
                    </v-card>
                  </div>
                </div>
              </div>
            </div>

            <!-- Backpressure Deck -->
            <v-card class="pa-4 border-0 elevation-1" style="background: rgba(255, 255, 255, 0.65); border-radius: 12px;">
              <div class="text-subtitle-1 font-weight-bold mb-3 text-indigo-darken-3 d-flex align-center">
                <v-icon class="mr-1" color="indigo">mdi-arrow-collapse-left</v-icon>
                Backpressure (背壓 bar)
              </div>
              <div class="d-flex flex-wrap flex-row-reverse justify-end">
                <v-card 
                  v-for="([key, value], index) in backpressure" 
                  :key="key" 
                  class="ma-1 pa-2 text-center elevation-1 bg-white" 
                  style="min-width: 120px; border-radius: 8px; border-top: 4px solid #3F51B5 !important; flex: 1 1 auto; max-width: 180px;"
                >
                  <div class="text-caption text-grey font-weight-bold">段 {{ index + 1 }}</div>
                  <div class="d-flex align-center justify-center mt-1">
                    <span class="text-h6 font-weight-bold text-indigo">{{ Math.round(value.value * 10) / 10 }}</span>
                    <v-btn 
                      v-if="value.edit === 'acctivate'" 
                      icon 
                      size="x-small" 
                      variant="text" 
                      color="indigo" 
                      class="ml-1" 
                      @click="handleClick(key)"
                    >
                      <v-icon size="small">mdi-cog</v-icon>
                    </v-btn>
                  </div>
                </v-card>
              </div>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Panel 2 & Panel 3: Holding Settings & Cycle Settings -->
    <v-row class="mr-1 ml-1 mt-4">
      <!-- Holding Settings -->
      <v-col cols="12" md="6">
        <v-card style="background: linear-gradient(135deg, #FFFDE7 0%, #FEEE81 100%); border-radius: 16px; min-height: 380px;" class="elevation-2 h-100 pa-4 hover-lift">
          <v-card-title class="text-h5 font-weight-bold text-amber-darken-4 mb-4">
            <v-icon color="amber-darken-4" class="mr-2">mdi-lock-pattern</v-icon>
            Holding Settings (保壓參數設定)
          </v-card-title>
          
          <v-card-text>
            <!-- Holding Pressure -->
            <div class="mb-6">
              <div class="text-subtitle-1 font-weight-bold mb-2 text-amber-darken-4">保壓壓力 Holding Pressure (bar)</div>
              <div class="d-flex flex-wrap flex-row-reverse justify-end">
                <v-card v-for="([key, value], index) in holdp" :key="key" class="ma-1 pa-2 text-center elevation-1 bg-white" style="min-width: 90px; flex: 1 1 auto; border-radius: 8px;">
                  <div class="text-caption text-grey font-weight-bold">段 {{ index + 1 }}</div>
                  <div class="d-flex align-center justify-center mt-1">
                    <span class="text-h6 font-weight-bold text-amber-darken-3">{{ Math.round(value.value * 10) / 10 }}</span>
                    <v-btn 
                      v-if="value.edit === 'acctivate'" 
                      icon 
                      size="x-small" 
                      variant="text" 
                      color="amber-darken-3" 
                      class="ml-1" 
                      @click="handleClick(key)"
                    >
                      <v-icon size="small">mdi-cog</v-icon>
                    </v-btn>
                  </div>
                </v-card>
              </div>
            </div>

            <!-- Holding Time -->
            <div>
              <div class="text-subtitle-1 font-weight-bold mb-2 text-amber-darken-4">保壓時間 Holding Time (s)</div>
              <div class="d-flex flex-wrap flex-row-reverse justify-end">
                <v-card v-for="([key, value], index) in holdt" :key="key" class="ma-1 pa-2 text-center elevation-1 bg-white" style="min-width: 90px; flex: 1 1 auto; border-radius: 8px;">
                  <div class="text-caption text-grey font-weight-bold">段 {{ index + 1 }}</div>
                  <div class="d-flex align-center justify-center mt-1">
                    <span class="text-h6 font-weight-bold text-amber-darken-3">{{ Math.round(value.value * 10) / 10 }}</span>
                    <v-btn 
                      v-if="value.edit === 'acctivate'" 
                      icon 
                      size="x-small" 
                      variant="text" 
                      color="amber-darken-3" 
                      class="ml-1" 
                      @click="handleClick(key)"
                    >
                      <v-icon size="small">mdi-cog</v-icon>
                    </v-btn>
                  </div>
                </v-card>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Cycle Settings -->
      <v-col cols="12" md="6">
        <v-card style="background: linear-gradient(135deg, #E0F2F1 0%, #C0E3E1 100%); border-radius: 16px; min-height: 380px;" class="elevation-2 h-100 pa-4 hover-lift">
          <v-card-title class="text-h5 font-weight-bold text-teal-darken-4 mb-4">
            <v-icon color="teal-darken-4" class="mr-2">mdi-sync</v-icon>
            Cycle Settings (週期及其他設定)
          </v-card-title>
          
          <v-card-text>
            <v-row dense>
              <!-- Cooling Time -->
              <v-col cols="12" sm="4" class="py-1">
                <v-card class="pa-3 text-center elevation-1 bg-white h-100 d-flex flex-column justify-center align-center" style="border-radius: 8px;">
                  <div class="text-caption font-weight-bold text-teal-darken-4 mb-1">冷卻時間 Cooling Time</div>
                  <div class="d-flex align-baseline justify-center my-2">
                    <span class="text-h4 font-weight-bold text-blue-darken-2">{{ Math.round(coolingtime.value * 10) / 10 }}</span>
                    <span class="text-caption ml-1 font-weight-bold text-grey">Sec</span>
                  </div>
                  <v-btn 
                    v-if="coolingtime.edit === 'acctivate'" 
                    icon 
                    size="small" 
                    variant="text" 
                    color="blue-darken-2" 
                    @click="handleClick('cooling_time')"
                  >
                    <v-icon>mdi-cog</v-icon>
                  </v-btn>
                </v-card>
              </v-col>

              <!-- Clamping Force -->
              <v-col cols="12" sm="4" class="py-1">
                <v-card class="pa-3 text-center elevation-1 bg-white h-100 d-flex flex-column justify-center align-center" style="border-radius: 8px;">
                  <div class="text-caption font-weight-bold text-teal-darken-4 mb-1">關模力 Clamping Force</div>
                  <div class="d-flex align-baseline justify-center my-2">
                    <span class="text-h4 font-weight-bold text-orange-darken-3">{{ Math.round(clamp_force_set.value * 10) / 10 }}</span>
                    <span class="text-caption ml-1 font-weight-bold text-grey">Tons</span>
                  </div>
                  <v-btn 
                    v-if="clamp_force_set.edit === 'acctivate'" 
                    icon 
                    size="small" 
                    variant="text" 
                    color="orange-darken-3" 
                    @click="handleClick('clamp_force_set')"
                  >
                    <v-icon>mdi-cog</v-icon>
                  </v-btn>
                </v-card>
              </v-col>

              <!-- Filling Time Set -->
              <v-col cols="12" sm="4" class="py-1">
                <v-card class="pa-3 text-center elevation-1 bg-white h-100 d-flex flex-column justify-center align-center" style="border-radius: 8px;">
                  <div class="text-caption font-weight-bold text-teal-darken-4 mb-1">充填時間 Filling Time Set</div>
                  <div class="d-flex align-baseline justify-center my-2">
                    <span class="text-h4 font-weight-bold text-success">{{ Math.round(filling_time_set.value * 100) / 100 }}</span>
                    <span class="text-caption ml-1 font-weight-bold text-grey">Sec</span>
                  </div>
                  <v-btn 
                    v-if="filling_time_set.edit === 'acctivate'" 
                    icon 
                    size="small" 
                    variant="text" 
                    color="success" 
                    @click="handleClick('filling_time_set')"
                  >
                    <v-icon>mdi-cog</v-icon>
                  </v-btn>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="mr-1 ml-1" v-if="feedbacktabledata.length>0">
      <v-col cols="12">
        <v-card style="border-radius: 16px; overflow: hidden;" class="elevation-2 hover-lift">
          <v-card-title class="bg-blue-grey-lighten-5 py-3 px-6 text-h6 font-weight-bold text-blue-grey-darken-4 d-flex align-center">
            <v-icon class="mr-2" color="blue-grey-darken-4">mdi-table-large</v-icon>
            Process Feedback Data (生產反饋數據)
          </v-card-title>
          <v-card-text class="pa-4">
            <v-row>
              <v-col cols="12">
                <v-table density="compact" fixed-header style="width: 100%; border: 1px solid rgba(0,0,0,0.06); border-radius: 8px; overflow: hidden;">
                  <thead>
                    <tr>
                      <th v-for="item in feedbacktabledata.slice(0, 15)" :key="item.Name" class="text-center font-weight-bold py-2" style="background-color: #ECEFF1; color: #37474F; border-bottom: 2px solid #CFD8DC;">{{ item.Name }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td v-for="item in feedbacktabledata.slice(0, 15)" :key="item.Name" class="text-center py-2 text-body-2 font-weight-bold" style="background-color: #ffffff; color: #455A64; border-right: 1px solid rgba(0,0,0,0.05);">{{ item.Value }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </v-col>
            </v-row>
            <v-row class="mt-4">
              <v-col cols="12">
                <v-table density="compact" fixed-header style="width: 100%; border: 1px solid rgba(0,0,0,0.06); border-radius: 8px; overflow: hidden;">
                  <thead>
                    <tr>
                      <th v-for="item in feedbacktabledata.slice(15)" :key="item.Name" class="text-center font-weight-bold py-2" style="background-color: #ECEFF1; color: #37474F; border-bottom: 2px solid #CFD8DC;">{{ item.Name }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td v-for="item in feedbacktabledata.slice(15)" :key="item.Name" class="text-center py-2 text-body-2 font-weight-bold" style="background-color: #ffffff; color: #455A64; border-right: 1px solid rgba(0,0,0,0.05);">{{ item.Value }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="mr-1 ml-1" v-if="curvedatalist.length>0" >
        <v-col>
            <v-card style="border-radius: 16px; overflow: hidden;" class="elevation-2 hover-lift">
                <v-card-title class="bg-blue-grey-lighten-5 py-3 px-6 text-h6 font-weight-bold text-blue-grey-darken-4 d-flex align-center">
                    <v-icon class="mr-2" color="blue-grey-darken-4">mdi-chart-bell-curve-cumulative</v-icon>
                    Curve Data (特徵曲線圖)
                </v-card-title>
                <v-card-text class="pa-6">
                    <v-row>
                        <v-col
                            v-for = "item in curvedatalist"
                            :key="item.Title"
                            cols="12"
                            md="6"
                        >
                            <v-card class="pa-2 border" style="border-radius: 8px;">
                                <highcharts :options="createChartOptions(item.Title, item.Data)" />
                            </v-card>
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
import TroubleShooting  from './layout/Troubleshooting.vue';
import PowerMeter from './layout/Powermeter.vue'
import PVT from './layout/PVT.vue'
import { computed } from 'vue'
  export default {
    name: 'MachineDashboard',
    components: {
            UperNavbar,
            TroubleShooting,
            PowerMeter,
            PVT
    },
    data: () => ({
        powermeterdialog:false,
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
        aoimoduleavailable : "False",
        powermeteravailable : "Faslse",
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
    formatParameterKey(key) {
        if (!key) return '';
        const mapping = {
            'cooling_time': 'Cooling Time',
            'clamp_force_set': 'Clamping Force Set',
            'filling_time_set': 'Filling Time Set',
            'injection_pressure_set': 'Injection Pressure Set'
        };
        if (mapping[key]) return mapping[key];

        let name = key.replace(/_/g, ' ').toLowerCase();
        
        if (name.includes('barrel temp') || name.includes('barrel_temp')) {
            const num = key.match(/\d+/);
            return num ? `Zone ${num[0]}` : 'Zone';
        }
        if (name.includes('injection pos') || name.includes('injectionpos')) {
            const num = key.match(/\d+/);
            return num ? `Pos Stage ${num[0]}` : 'Position';
        }
        if (name.includes('injection speed') || name.includes('injectionspeed') || name.includes('ispe')) {
            const num = key.match(/\d+/);
            return num ? `Speed Stage ${num[0]}` : 'Speed';
        }
        if (name.includes('holdingpressureset') || name.includes('holding pressure')) {
            const num = key.match(/\d+/);
            return num ? `Press Stage ${num[0]}` : 'Pressure';
        }
        if (name.includes('holdingtimeset') || name.includes('holding time')) {
            const num = key.match(/\d+/);
            return num ? `Time Stage ${num[0]}` : 'Time';
        }
        if (name.includes('backpressure') || name.includes('back pressure')) {
            const num = key.match(/\d+/);
            return num ? `Backpress Stage ${num[0]}` : 'Backpressure';
        }
        if (name.includes('injection pressure') || name.includes('ijpre')) {
            const num = key.match(/\d+/);
            return num ? `Press Stage ${num[0]}` : 'Pressure';
        }
        
        return name.replace(/\b\w/g, c => c.toUpperCase());
    },
    getPressureValue(index) {
        if (!this.ijprelist || this.ijprelist.length === 0) return '-';
        let val;
        if (this.ijprelist.length === 1) {
            val = this.ijprelist[0][1].value;
        } else {
            val = this.ijprelist[index] ? this.ijprelist[index][1].value : '-';
        }
        if (val === '-' || val === null || val === undefined || val === '') return '-';
        return Math.round(Number(val) * 10) / 10;
    },
    showPressureEdit(index) {
        if (!this.ijprelist || this.ijprelist.length === 0) return false;
        if (this.ijprelist.length === 1) {
            return index === 0 && this.ijprelist[0][1].edit === 'acctivate';
        }
        return this.ijprelist[index] && this.ijprelist[index][1].edit === 'acctivate';
    },
    getPressureKey(index) {
        if (!this.ijprelist || this.ijprelist.length === 0) return '';
        if (this.ijprelist.length === 1) {
            return this.ijprelist[0][0];
        }
        return this.ijprelist[index] ? this.ijprelist[index][0] : '';
    },
    getHeaterStatus(setVal, actVal) {
        if (setVal === undefined || actVal === undefined || setVal === null || actVal === null) return 'stable';
        const set = parseFloat(setVal);
        const act = parseFloat(actVal);
        if (isNaN(set) || isNaN(act)) return 'stable';
        
        const diff = act - set;
        if (diff < -5) {
            return 'heating';
        } else if (diff > 5) {
            return 'cooling';
        }
        return 'stable';
    },

    async changeparameter(){
        if(this.machineonline == "Online"){
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
    async clickheaterbutton(){
        if(this.machineonline == "Online"){
            var requestbody = {"machine_name":this.machinename,"target":"heater_button","value":"1"};
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

    async checktroubleshhotingavailable(){
        var name = this.$cookies.get('setSelectMachine');
        const token = this.$store.getters.getToken;
        this.machinename = name;
        var requestbody = {"machine_name":this.machinename};
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/checkmodule`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
        if (response.data.status=='error'){
                console.log('Fail')
        }
        else{
                this.troubleshootingavailable = response.data.Data.troubleshooting
                this.aoimoduleavailable  = response.data.Data.aoimodule
                this.powermeteravailable = response.data.Data.powermeter
                console.log("11111",this.powermeteravailable)

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
        }
    },
    beforeDestory(){
      clearInterval(this.timer);
  },    
  }
</script>

<style scoped>
.no-dot .v-timeline-item__dot {
  display: none !important;
}

/* Hover lift effect for dashboard cards */
.hover-lift {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

.hover-lift:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12) !important;
}

/* Heater Status LED dot */
.heater-led-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
  transition: all 0.3s ease;
}

.heater-led-dot.stable {
  background-color: #4CAF50;
  box-shadow: 0 0 8px #4CAF50;
}

.heater-led-dot.heating {
  background-color: #FF9800;
  box-shadow: 0 0 8px #FF9800;
  animation: pulse-orange 1.5s infinite alternate;
}

.heater-led-dot.cooling {
  background-color: #F44336;
  box-shadow: 0 0 8px #F44336;
  animation: pulse-red 1.5s infinite alternate;
}

@keyframes pulse-orange {
  0% { opacity: 0.4; transform: scale(0.85); }
  100% { opacity: 1; transform: scale(1.15); box-shadow: 0 0 12px #FF9800; }
}

@keyframes pulse-red {
  0% { opacity: 0.4; transform: scale(0.85); }
  100% { opacity: 1; transform: scale(1.15); box-shadow: 0 0 12px #F44336; }
}

/* Fishbone Diagram Container */
.fishbone-container {
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  background: rgba(255, 255, 255, 0.5);
  min-height: 400px;
  direction: rtl;
}

/* Fishbone Inner Wrapper (stretches to full scroll content) */
.fishbone-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 60px 40px;
  min-width: 100%;
  gap: 32px;
  width: max-content;
  direction: rtl;
}

/* Spine line with glowing neon styling */
.fishbone-spine {
  position: absolute;
  left: 80px;
  right: 40px;
  top: 50%;
  height: 6px;
  background: linear-gradient(270deg, #26C6DA 0%, #0288D1 100%);
  transform: translateY(-50%);
  z-index: 1;
  border-radius: 3px;
  box-shadow: 0 0 8px rgba(38, 198, 218, 0.4);
}

/* Spine head (Arrow at the end representing injection direction pointing left) */
.fishbone-spine-head {
  position: absolute;
  left: 55px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-top: 12px solid transparent;
  border-bottom: 12px solid transparent;
  border-right: 20px solid #0288D1;
  z-index: 1;
  filter: drop-shadow(0 0 4px rgba(2, 136, 209, 0.4));
}

/* Stage Columns */
.fishbone-stage {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  width: 165px;
  flex-shrink: 0;
  direction: ltr;
}

/* Central node along the spine with hover glows */
.fishbone-node {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #0288D1;
  border: 4px solid #fff;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: bold;
  box-shadow: 0 3px 6px rgba(0,0,0,0.16);
  margin: 12px 0;
  transition: all 0.3s ease;
}

.fishbone-stage:hover .fishbone-node {
  background: #26C6DA;
  transform: scale(1.2);
  box-shadow: 0 0 15px rgba(38, 198, 218, 0.8), 0 3px 6px rgba(0,0,0,0.16);
}

/* Branches (tilted bone lines) */
.fishbone-branch {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.fishbone-branch.upper {
  justify-content: flex-end;
  height: 110px;
}

.fishbone-branch.lower {
  justify-content: flex-start;
  height: 170px;
}

/* Connector Bone lines */
.fishbone-line {
  width: 2px;
  background: #B0BEC5;
  transition: background-color 0.3s ease, width 0.3s ease;
}

.fishbone-branch.upper .fishbone-line {
  height: 30px;
  transform: skewX(20deg);
  transform-origin: bottom center;
}

.fishbone-branch.lower .fishbone-line {
  height: 30px;
  transform: skewX(-20deg);
  transform-origin: top center;
}

.fishbone-stage:hover .fishbone-line {
  background: #26C6DA;
  width: 3px;
}

/* Custom Cards */
.fishbone-card {
  width: 100%;
  border-radius: 12px !important;
  background: #ffffff !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
  border: 1px solid rgba(0, 0, 0, 0.05) !important;
  padding: 10px !important;
  text-align: center;
  transition: all 0.3s ease !important;
}

.fishbone-stage:hover .fishbone-card {
  box-shadow: 0 8px 20px rgba(2, 136, 209, 0.12) !important;
  border-color: rgba(2, 136, 209, 0.2) !important;
  transform: translateY(2px);
}

.fishbone-card.position {
  border-top: 4px solid #0288D1 !important;
}

.fishbone-card.speed-pressure {
  border-top: 4px solid #4CAF50 !important;
}
</style>