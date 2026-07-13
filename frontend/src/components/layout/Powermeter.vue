<template>
  <!-- Premium Energy Observation Trigger Button -->
  <v-btn 
    class="energy-obs-btn px-5 py-2 font-weight-bold ml-5" 
    elevation="2" 
    rounded="lg"
    @click="powermeterdialog = true"
  >
    <v-icon left color="#10B981" class="mr-2 pulse-icon">mdi-leaf</v-icon>
    能耗觀測
  </v-btn>

  <!-- POWER METER DIALOG -->
  <v-dialog 
    v-model="powermeterdialog" 
    max-width="1400px" 
    width="95%"
    scrollable
    transition="dialog-bottom-transition"
    class="energy-dashboard-dialog"
  >
    <v-card class="dashboard-root-card">
      <!-- Premium Glassmorphism Header -->
      <v-card-title class="d-flex justify-space-between align-center px-6 py-4 dashboard-header">
        <div class="d-flex align-center">
          <v-icon size="28" color="#10B981" class="mr-3">mdi-chart-bell-curve-cumulative</v-icon>
          <div>
            <h2 class="text-h5 font-weight-bold gradient-title mb-0">能耗監控與優化決策系統</h2>
            <div class="text-caption text-grey-darken-1 d-flex align-center mt-1">
              <span class="pulse-dot mr-2"></span>
              <span>即時觀測中</span>
              <span class="mx-2">•</span>
              <v-icon size="14" class="mr-1">mdi-clock-outline</v-icon>
              <span>最後更新: {{ updatetime || '取得資料中...' }}</span>
            </div>
          </div>
        </div>
        <v-btn 
          size="small" 
          icon="mdi-close" 
          variant="tonal"
          color="grey-darken-2" 
          @click="powermeterdialog = false"
        ></v-btn>
      </v-card-title>

      <v-divider></v-divider>

      <!-- Scrollable Card Text -->
      <v-card-text class="pa-6 bg-slate-gray">
        <v-container fluid class="pa-0">
          
          <!-- 1. 歷史製程能耗趨勢 (History Chart) -->
          <v-row class="mb-6">
            <v-col cols="12">
              <v-card class="dashboard-card pa-5" elevation="1">
                <div class="card-header-bar mb-4">
                  <span class="card-header-decorator"></span>
                  <h3 class="text-subtitle-1 font-weight-bold">歷史製程能耗趨勢</h3>
                </div>
                <div class="chart-container">
                  <highcharts :options="createGroupedColumnOptions('製程能耗變化', processhistory.updatetime, processhistory.dataset, processhistory.displayunit)" />
                </div>
              </v-card>
            </v-col>
          </v-row>

          <!-- 2. 生產設定參數對照 (Parameter Contrast) -->
          <v-row class="mb-6">
            <v-col cols="12">
              <v-card class="dashboard-card overflow-hidden" elevation="1">
                <div class="pa-5 card-gradient-blue text-white">
                  <div class="d-flex justify-space-between align-center">
                    <div class="d-flex align-center">
                      <v-icon color="white" class="mr-2">mdi-tune-variant</v-icon>
                      <h3 class="text-subtitle-1 font-weight-bold">生產設定參數對照</h3>
                    </div>
                    <!-- Clear Initial Parameter Button -->
                    <v-btn v-if="firsttepparametersetting.length > 0" size="x-small" variant="flat" color="white" class="text-indigo-darken-4 font-weight-black" rounded="pill" @click="clearfirststep()"><v-icon size="12" class="mr-1">mdi-refresh</v-icon> 重設初始值</v-btn>
                  </div>
                </div>

                <div class="pa-5 bg-white">
                  <v-row>
                    <!-- Initial Parameters Column -->
                    <v-col cols="12" sm="6" class="border-right pr-sm-4 mb-4 mb-sm-0">
                      <div class="text-subtitle-2 font-weight-bold text-grey-darken-2 mb-3 d-flex align-center">
                        <span class="param-status-dot bg-indigo-lighten-2 mr-2"></span> 初始設定值
                      </div>
                      <div v-if="firsttepparametersetting.length > 0" class="d-flex flex-wrap gap-2">
                        <div 
                          v-for="(item, key) in firsttepparametersetting" 
                          :key="key"
                          class="param-item pa-3 rounded-lg flex-grow-1"
                          style="min-width: 140px; max-width: calc(33.3% - 8px);"
                        >
                          <div class="param-label">{{ item.name }}</div>
                          <div class="param-val-group mt-1">
                            <span class="param-value text-indigo-darken-4 font-weight-bold">{{ Math.round(item.value * 100) / 100 }}</span>
                            <span class="param-unit">{{ item.unit }}</span>
                          </div>
                        </div>
                      </div>
                      <div v-else class="text-center py-6 text-grey text-caption">
                        無初始參數紀錄
                      </div>
                    </v-col>

                    <!-- Current Parameters Column -->
                    <v-col cols="12" sm="6" class="pl-sm-4">
                      <div class="text-subtitle-2 font-weight-bold text-grey-darken-2 mb-3 d-flex align-center">
                        <span class="param-status-dot bg-light-blue mr-2"></span> 當前設定值
                      </div>
                      <div v-if="currentsetting && currentsetting.length > 0" class="d-flex flex-wrap gap-2">
                        <div 
                          v-for="(item, key) in currentsetting" 
                          :key="key"
                          class="param-item pa-3 rounded-lg flex-grow-1"
                          style="min-width: 140px; max-width: calc(33.3% - 8px);"
                        >
                          <div class="param-label">{{ item.name }}</div>
                          <div class="param-val-group mt-1">
                            <span class="param-value text-light-blue-darken-4 font-weight-bold">{{ Math.round(item.value * 100) / 100 }}</span>
                            <span class="param-unit">{{ item.unit }}</span>
                          </div>
                        </div>
                      </div>
                      <div v-else class="text-center py-6 text-grey text-caption">
                        載入當前參數中...
                      </div>
                    </v-col>
                  </v-row>
                </div>
              </v-card>
            </v-col>
          </v-row>

          <!-- 3. 智能節能優化建議 (Optimization center) -->
          <v-row v-if="Object.keys(optimization).length > 0" class="mb-6">
            <v-col cols="12">
              <v-card class="dashboard-card" elevation="1">
                <div class="pa-5 card-gradient-green text-white d-flex justify-space-between align-center">
                  <div class="d-flex align-center">
                    <v-icon color="white" class="mr-2">mdi-leaf</v-icon>
                    <h3 class="text-subtitle-1 font-weight-bold">智能節能優化建議</h3>
                  </div>
                  <v-btn size="small" elevation="2" rounded="pill" color="white" class="text-green-darken-4 font-weight-black" @click="updateparameter()"><v-icon size="16" start class="mr-1">mdi-flash-outline</v-icon> 一鍵套用優化</v-btn>
                </div>

                <div class="pa-5 bg-white">
                  <div class="section-title-sm mb-3">參數調整建議</div>
                  <div class="d-flex flex-wrap gap-2">
                    <div 
                      v-for="(item, key) in optimization" 
                      :key="key"
                      class="optimization-tag pa-3 rounded-lg flex-grow-1"
                      style="min-width: 140px; max-width: calc(25% - 8px);"
                    >
                      <div class="opt-name">{{ item.name }}</div>
                      <div class="opt-val mt-1">
                        <span class="font-weight-black text-green-darken-3">{{ Math.round(item.value * 100) / 100 }}</span>
                        <span class="text-caption ml-1">{{ item.unit }}</span>
                      </div>
                    </div>
                  </div>

                  <div v-if="isshowmessage" class="message-banner mt-3 pa-2 rounded text-center">
                    <v-icon size="16" color="success" class="mr-1">mdi-check-circle</v-icon>
                    <span class="text-caption success-text font-weight-medium">{{ messagetext }}</span>
                  </div>
                </div>
              </v-card>
            </v-col>
          </v-row>

          <!-- 4. 製程能耗指標監控 (Power & Energy Consumption Summary) -->
          <v-row v-if="Object.keys(abstractitem).length > 0" class="mb-6">
            <v-col cols="12">
              <v-card class="dashboard-card" elevation="1">
                <div class="pa-5 card-gradient-dark text-white">
                  <div class="d-flex align-center">
                    <v-icon color="white" class="mr-2">mdi-chart-donut</v-icon>
                    <h3 class="text-subtitle-1 font-weight-bold">製程能耗指標監控</h3>
                  </div>
                </div>

                <div class="pa-5 bg-white">
                  <v-row>
                    <!-- Initial Power Consumption -->
                    <v-col cols="12" md="4" class="border-right pr-md-4 mb-4 mb-md-0" v-if="Object.keys(firsttepabstractitem).length > 0">
                      <div class="metric-block-title text-orange-darken-4 mb-3">
                        <v-icon size="16" class="mr-1">mdi-history</v-icon> 初始製程能耗
                      </div>
                      <div class="d-flex flex-wrap gap-2">
                        <div 
                          v-for="(item, key) in firsttepabstractitem" 
                          :key="key"
                          class="metric-item pa-3 rounded-lg flex-grow-1"
                          style="min-width: 130px;"
                        >
                          <span class="metric-label">{{ item.name }}</span>
                          <span class="metric-val text-orange-darken-3 font-weight-bold mt-1">
                            {{ Math.round(item.value * 100) / 100 }} <span class="metric-unit ml-1">{{ item.Unit }}</span>
                          </span>
                        </div>
                      </div>
                    </v-col>

                    <!-- Current Power Consumption -->
                    <v-col cols="12" :md="Object.keys(firsttepabstractitem).length > 0 ? 4 : 6" class="border-right px-md-4 mb-4 mb-md-0">
                      <div class="metric-block-title text-green-darken-3 mb-3">
                        <v-icon size="16" class="mr-1">mdi-flash-circle</v-icon> 當前實際能耗
                      </div>
                      <div class="d-flex flex-wrap gap-2">
                        <div 
                          v-for="(item, key) in abstractitem" 
                          :key="key"
                          class="metric-item pa-3 rounded-lg flex-grow-1"
                          style="min-width: 130px;"
                        >
                          <span class="metric-label">{{ item.name }}</span>
                          <span class="metric-val text-green-darken-2 font-weight-black mt-1">
                            {{ Math.round(item.value * 100) / 100 }} <span class="metric-unit ml-1">{{ item.Unit }}</span>
                          </span>
                        </div>
                      </div>
                    </v-col>

                    <!-- Expectation (Predicted Energy Consumption under Optimization) -->
                    <v-col cols="12" :md="Object.keys(firsttepabstractitem).length > 0 ? 4 : 6" class="pl-md-4" v-if="Object.keys(expectation).length > 0">
                      <div class="metric-block-title text-teal-darken-3 mb-3">
                        <v-icon size="16" class="mr-1">mdi-lightning-bolt-outline</v-icon> 優化後節能預測
                      </div>
                      <div class="d-flex flex-wrap gap-2">
                        <div 
                          v-for="(item, key) in expectation" 
                          :key="key"
                          class="metric-item pa-3 rounded-lg flex-grow-1"
                          style="min-width: 130px;"
                        >
                          <span class="metric-label">{{ item.name }}</span>
                          <span class="metric-val text-teal-darken-2 font-weight-black mt-1">
                            {{ Math.round(item.value * 100) / 100 }} <span class="metric-unit ml-1">{{ item.unit }}</span>
                          </span>
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </div>
              </v-card>
            </v-col>
          </v-row>

          <!-- 5. 即時物理曲線 (Power Curve) -->
          <v-row>
            <v-col cols="12">
              <v-card class="dashboard-card pa-5" elevation="1">
                <div class="card-header-bar mb-4 d-flex justify-space-between align-center">
                  <div class="d-flex align-center">
                    <span class="card-header-decorator-blue"></span>
                    <h3 class="text-subtitle-1 font-weight-bold">Power Curve</h3>
                  </div>
                </div>
                
                <v-row v-if="curvedatalist.length > 0">
                  <v-col 
                    cols="12" 
                    v-for="item in curvedatalist" 
                    :key="item.Title"
                    class="py-2"
                  >
                    <div class="sub-chart-wrapper pa-2 rounded-lg border">
                      <highcharts :options="createChartOptions(item.Title, item.Data, item.Unit)" />
                    </div>
                  </v-col>
                </v-row>
                <div v-else class="text-center py-8 text-grey">
                  <v-icon size="40" color="grey-lighten-1" class="mb-2">mdi-chart-line-none</v-icon>
                  <p>目前尚無即時物理曲線數據</p>
                </div>
              </v-card>
            </v-col>
          </v-row>

        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PowerMeter',
  props: {
    machinename: String,
  },
  
  data: () => ({
    powermeterdialog: false,
    currentsetting: [],
    updatetime: '',
    abstractitem: {},
    firsttepparametersetting: [],
    firsttepabstractitem: {},
    optimization: [
      { 'nodename': 'Ijv_set1', 'value': '20', 'name': '第一段射速', 'unit': 'mm/s' },
      { 'nodename': 'Ijv_set2', 'value': '19', 'name': '第二段射速', 'unit': 'mm/s' },
    ],
    powerprediction: [
      { 'nodename': '', 'value': '20000', 'name': '充填能耗', 'unit': 'J' },
      { 'nodename': '', 'value': '19000', 'name': '保壓能耗', 'unit': 'J' },
    ],
    expectation: [
      { 'nodename': '', 'value': '21000', 'name': '充填能耗', 'unit': 'J' },
      { 'nodename': '', 'value': '19000', 'name': '保壓能耗', 'unit': 'J' },
    ],
    curvedatalist: [],
    isshowmessage: false,
    messagetext: '',
    processhistory: {
      updatetime: [],
      dataset: [],
      template: '',
      displayunit: 'KJ'
    },
    categoriestest: ['2026-05-02 11:13', '2026-05-02 11:15', '2026-05-02 11:17', '2026-05-02 11:20', '2026-05-02 11:22'],
    seriesDatatest: [
      {
        name: 'Injection Power Consumption',
        data: [35, 30, 28, 26, 25, 24]
      },
      {
        name: 'Packing Power Consumption',
        data: [30, 29, 28, 28, 26, 25]
      },
      {
        name: 'Close mold Power Consumption',
        data: [35, 30, 28, 26, 25, 24]
      },
    ]
  }),
  methods: {
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    createGroupedColumnOptions(title, categories, seriesData, unit) {
      return {
        chart: {
          type: 'column',
          backgroundColor: 'transparent',
          style: {
            fontFamily: 'Inter, system-ui, -apple-system, sans-serif'
          }
        },
        colors: ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'],
        title: {
          text: title,
          style: {
            color: '#1e293b',
            fontSize: '15px',
            fontWeight: '600'
          }
        },
        credits: { enabled: false },
        xAxis: {
          categories: categories,
          crosshair: true,
          labels: {
            style: { color: '#64748b' }
          },
          lineColor: '#e2e8f0'
        },
        yAxis: {
          min: 0,
          title: {
            text: unit,
            style: { color: '#64748b' }
          },
          labels: {
            style: { color: '#64748b' }
          },
          gridLineColor: '#f1f5f9'
        },
        tooltip: {
          backgroundColor: '#ffffff',
          borderRadius: 8,
          borderWidth: 1,
          borderColor: '#e2e8f0',
          shadow: true,
          shared: true,
          useHTML: true,
          valueSuffix: ` (${unit})`,
          style: {
            color: '#334155'
          }
        },
        plotOptions: {
          column: {
            pointPadding: 0.15,
            borderWidth: 0,
            borderRadius: 6
          }
        },
        legend: {
          itemStyle: {
            color: '#475569',
            fontWeight: '500'
          }
        },
        series: seriesData 
      }
    },
    createChartOptions(title, yData, Unit) {
      const categories = yData.map((_, i) => (i + 1).toString())
      return {
        chart: { 
          type: 'spline',
          backgroundColor: 'transparent',
          height: 240,
          style: {
            fontFamily: 'Inter, system-ui, -apple-system, sans-serif'
          }
        },
        colors: ['#10b981'],
        title: { 
          text: title,
          align: 'left',
          style: {
            color: '#334155',
            fontSize: '13px',
            fontWeight: '600'
          }
        },
        credits: { enabled: false },
        xAxis: {
          categories,
          title: { 
            text: 'Time (s)',
            style: { color: '#94a3b8', fontSize: '10px' }
          },
          labels: {
            style: { color: '#94a3b8', fontSize: '9px' }
          },
          lineColor: '#e2e8f0',
          tickColor: '#e2e8f0'
        },
        yAxis: {
          title: { 
            text: Unit,
            style: { color: '#94a3b8', fontSize: '10px' }
          },
          labels: {
            style: { color: '#94a3b8', fontSize: '9px' }
          },
          gridLineColor: '#f8fafc'
        },
        tooltip: {
          backgroundColor: '#ffffff',
          borderRadius: 8,
          borderWidth: 1,
          borderColor: '#e2e8f0',
          shadow: true,
          valueSuffix: ` ${Unit}`
        },
        legend: { enabled: false },
        series: [{
          name: title,
          data: yData,
          lineWidth: 2,
          marker: {
            enabled: false
          }
        }]
      }
    },
    update_processhistory(abstract, dataupdatetime) {
      if (this.processhistory.updatetime.length == 0) {
        this.processhistory.template = abstract
      }
      const keystemplate = Object.keys(this.processhistory.template).sort();
      const keysabstract = Object.keys(abstract).sort();
      // 如果格式檢查失敗，執行初始化重置
      if (!keystemplate.every((key, index) => key === keysabstract[index])) {
        this.processhistory.updatetime = [];
        this.processhistory.dataset = [];
        this.processhistory.template = abstract;
      }
      this.processhistory.updatetime.push(dataupdatetime);
      if (this.processhistory.updatetime.length > 5) {
        this.processhistory.updatetime.shift();
      }
      for (const item of Object.values(abstract)) {
        const { name, value } = item;
        let series = this.processhistory.dataset.find(d => d.name === name);
        if (!series) {
          // 若找不到（或剛被清空），則建立新數列
          this.processhistory.dataset.push({ name: name, data: [value] });
        } else {
          series.data.push(value); 
          if (series.data.length > 5) series.data.shift();
        }
      }
    },
    async getenergyinfo() {
      const token = this.$store.getters.getToken;
      await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/realtimepower/${this.machinename}`, {
        headers: { "accesstoken": token }
      }).then((response) => {
        if (response.data.status == 'error') {
          console.log('Get energy info fail')
        } else {
          var rawinfo = response.data.Data.machineenergy;
          try {
            var dataupdatetime = rawinfo["updatetime"]
            if (dataupdatetime != this.updatetime) {
              this.updatetime = dataupdatetime
              this.abstractitem = rawinfo?.abstract ?? {}
              this.optimization = rawinfo?.cal ?? {}
              this.powerprediction = rawinfo?.powerprediction ?? {}
              this.expectation = rawinfo?.expectation ?? {}
              var new_curvedata = []
              for (var k of Object.keys(rawinfo["curve"])) {
                var item = rawinfo.curve[k];
                var ydata = item.value.map(item => parseFloat(item));
                var curveitem = { "Title": item.name, "Data": ydata, "Unit": item.Unit };
                new_curvedata.push(curveitem);
              }
              this.curvedatalist = new_curvedata
              this.update_processhistory(this.abstractitem, this.updatetime)
            }
            var fiststep = response.data.Data.originstatus
            this.firsttepparametersetting = fiststep?.parameter_setting ?? []
            this.firsttepabstractitem = fiststep?.abstract ?? {}
            this.currentsetting = rawinfo?.parameter_setting ?? []
          } catch (err) {
            console.log(err);
          }
        }
      })
    },
    async updateparameter() {
      const token = this.$store.getters.getToken;
      let command = []
      this.optimization.forEach((item) => {
        command.push({ "target": item["nodename"], "value": item["value"] })
      })
      let machine_Protocol = "euromap77"
      const euromap63list = ["TOYO"]
      if (euromap63list.includes(this.machinename)) {
        machine_Protocol = "euromap63"
      }
      const requestbody = {
        "machine_name": this.machinename,
        "command": command,
        "machine_Protocol": machine_Protocol
      }
      await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/multicontrol`, requestbody, {
        headers: { "accesstoken": token }
      }).then((response) => {
        if (response.data.status == 'error') {
          console.log('Fail')
        } else {
          this.messagetext = "Parameter updates success"
          this.isshowmessage = true
          setTimeout(() => {
            this.isshowmessage = false
          }, 5000);
        }
      })
    },
    async clearfirststep() {
      const token = this.$store.getters.getToken;
      const requestbody = {
        "machine_name": this.machinename,
      }
      await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/resetpowerfirststep`, requestbody, {
        headers: { "accesstoken": token }
      }).then((response) => {
        if (response.data.status == 'error') {
          console.log('Fail')
        }
      })
    }
  },
  mounted() {
    var token = this.$cookies.get('accesstoken');
    if (!token) {
      this.$router.push({ name: 'Login' });
    }
    var namecheck = this.$cookies.get('setSelectMachine');
    if (!namecheck) {
      this.$router.push({ name: 'MachineOverview' });
    } else {
      this.getenergyinfotimer = setInterval(this.getenergyinfo, 1000);
    }
  },
  beforeUnmount() {
    clearInterval(this.getenergyinfotimer);
  }
}
</script>

<style scoped>
/* Button Styles */
.energy-obs-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white !important;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
  transition: all 0.3s ease;
}

.energy-obs-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35);
  background: linear-gradient(135deg, #34d399 0%, #059669 100%);
}

.pulse-icon {
  animation: leaf-pulse 2s infinite ease-in-out;
}

@keyframes leaf-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Dialog & Glassmorphism Header */
.energy-dashboard-dialog {
  border-radius: 20px;
  overflow: hidden;
}

.dashboard-root-card {
  background-color: #f8fafc !important;
  border-radius: 20px !important;
  font-family: 'Inter', 'Outfit', 'Roboto', sans-serif;
  overflow: hidden;
}

.dashboard-header {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
}

.gradient-title {
  background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 1.35rem !important;
  letter-spacing: -0.025em;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
  }
}

/* Dashboard Cards */
.dashboard-card {
  border-radius: 16px !important;
  background-color: #ffffff;
  border: 1px solid #e2e8f0 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(148, 163, 184, 0.08);
}

.card-header-bar {
  display: flex;
  align-items: center;
}

.card-header-decorator {
  width: 4px;
  height: 18px;
  background: #10b981;
  border-radius: 4px;
  margin-right: 10px;
}

.card-header-decorator-blue {
  width: 4px;
  height: 18px;
  background: #3b82f6;
  border-radius: 4px;
  margin-right: 10px;
}

/* Gradients for Card Headers */
.card-gradient-blue {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
}

.card-gradient-green {
  background: linear-gradient(135deg, #065f46 0%, #10b981 100%);
}

.card-gradient-dark {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Parameter Grid */
.border-right {
  border-right: 1px solid #f1f5f9;
}

.param-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}

.param-list {
  display: flex;
  flex-direction: column;
}

.param-item {
  padding: 6px 8px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #f1f5f9;
  transition: background-color 0.2s ease;
}

.param-item:hover {
  background: #f1f5f9;
}

.param-label {
  font-size: 0.7rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 2px;
}

.param-val-group {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.param-value {
  font-size: 1.15rem;
  line-height: 1.25;
}

.param-unit {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 2px;
}

/* Optimization suggestions */
.section-title-sm {
  font-size: 0.8rem;
  font-weight: 700;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.optimization-tag {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  flex: 1 1 calc(50% - 8px);
  min-width: 110px;
  transition: all 0.2s ease;
}

.optimization-tag:hover {
  background-color: #dcfce7;
  transform: translateY(-1px);
}

.opt-name {
  font-size: 0.72rem;
  color: #15803d;
}

.opt-val {
  font-size: 1.1rem;
}

.opt-result-row {
  border-bottom: 1px dashed #f1f5f9;
}

.opt-result-row:last-child {
  border-bottom: none;
}

/* Metric Blocks */
.metric-block-title {
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
}

.metric-item {
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid #f1f5f9;
  height: 100%;
}

.metric-label {
  font-size: 0.72rem;
  color: #64748b;
  margin-bottom: 4px;
}

.metric-val {
  font-size: 1.2rem;
  line-height: 1.1;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.metric-unit {
  font-size: 0.75rem;
  font-weight: 500;
  color: #94a3b8;
}

/* Highcharts wrapper */
.chart-container {
  width: 100%;
  overflow: hidden;
}

.sub-chart-wrapper {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  transition: border-color 0.2s ease;
}

.sub-chart-wrapper:hover {
  border-color: #cbd5e1;
}

/* Message Banner */
.message-banner {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.no-dot .v-timeline-item__dot {
  display: none !important;
}

.gap-2 {
  gap: 8px;
}

.flex-column {
  display: flex;
  flex-direction: column;
}
</style>