<template>
  <v-row>
    <UperNavbar /> 
  </v-row>
  
  <div class="history-dashboard-container py-6 px-4 px-md-8 text-left">
    <!-- Row 1: Search Selection Card -->
    <v-row class="card-enter-anim" style="animation-delay: 50ms;">
      <v-col cols="12">
        <v-card class="rounded-xl border border-opacity-5" elevation="2" style="overflow: visible;">
          <v-card-title class="d-flex align-center px-6 pt-6 pb-2">
            <v-icon color="primary" class="mr-2">mdi-database-search-outline</v-icon>
            <span class="text-h6 font-weight-black text-slate-800">歷史數據查詢 / Historical Query</span>
          </v-card-title>
          
          <v-card-text class="px-6 py-4">
            <v-row class="align-end">
              <!-- Select Machine -->
              <v-col cols="12" md="3" class="text-left">
                <label class="text-caption font-weight-bold text-slate-600 mb-1 d-block">選擇監控機台 / Machine</label>
                <v-select
                  v-model="machineselect"
                  placeholder="請選擇監控機台"
                  :items="machineselection"
                  variant="outlined"
                  color="primary"
                  rounded="lg"
                  prepend-inner-icon="mdi-cog-outline"
                  density="comfortable"
                  hide-details
                ></v-select>
              </v-col>
              
              <!-- Start Date -->
              <v-col cols="12" md="4" class="text-left">
                <label class="text-caption font-weight-bold text-slate-600 mb-1 d-block">開始日期 / Start Date</label>
                <n-date-picker
                  v-model:value="starttime"
                  type="date"
                  clearable
                  placeholder="請選擇開始日期"
                  class="w-100 custom-naive-picker"
                />
              </v-col>
              
              <!-- Arrow Icon (Desktop only) -->
              <v-col cols="12" md="1" class="text-center pb-3 d-none d-md-block" style="font-size: 20px; color: #94a3b8; user-select: none;">
                <v-icon>mdi-arrow-right</v-icon>
              </v-col>
              
              <!-- End Date -->
              <v-col cols="12" md="4" class="text-left">
                <label class="text-caption font-weight-bold text-slate-600 mb-1 d-block">結束日期 / End Date</label>
                <n-date-picker
                  v-model:value="endtime"
                  type="date"
                  clearable
                  placeholder="請選擇結束日期"
                  class="w-100 custom-naive-picker"
                />
              </v-col>
            </v-row>
          </v-card-text>
          
          <v-card-actions class="px-6 pb-6 pt-0">
            <v-spacer></v-spacer>
            <v-btn
              :loading="searchloading"
              color="primary"
              variant="flat"
              size="large"
              rounded="lg"
              prepend-icon="mdi-magnify"
              class="px-6 mr-3 action-btn search-btn"
              @click="searchhstory();"
            >
              執行查詢 / Search
            </v-btn>
            
            <v-btn
              v-if="curvelinenamelist.length > 0"
              color="success"
              variant="flat"
              size="large"
              rounded="lg"
              prepend-icon="mdi-download"
              class="px-6 action-btn download-btn"
              @click="exportcsv();"
            >
              導出 CSV / Export CSV
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Row 2: Data Details Table Card -->
    <v-row v-if="variabledata.length > 0" class="mt-4 card-enter-anim" style="animation-delay: 150ms;">
      <v-col cols="12">
        <v-card class="rounded-xl border border-opacity-5" elevation="2">
          <v-card-title class="d-flex align-center px-6 pt-6 pb-2">
            <v-icon color="primary" class="mr-2">mdi-table-large</v-icon>
            <span class="text-h6 font-weight-black text-slate-800">數據明細表格 / Data Table</span>
          </v-card-title>
          
          <v-card-text class="px-6 pb-6">
            <div class="custom-table-wrapper border rounded-lg overflow-hidden">
              <v-data-table
                :items="variabledata"
                density="comfortable"
                item-key="id"
                :items-per-page-options="[5, 10, 15, 20]"
                class="custom-data-table"
              >
                <template v-slot:body="{ items }">
                  <tr v-for="(item) in items" :key="item.id" class="table-data-row">
                    <td v-for="(value, key) in item" :key="key" class="py-3 px-4 font-weight-medium table-cell">
                      {{ value }}
                    </td>
                  </tr>
                  <!-- Reactive hook snippet for updating chart metrics -->
                  <span v-if="updateCurrentItems(items)" style="display: none;"></span>
                </template>
              </v-data-table>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Row 3: Charts Layout Grid -->
    <v-row v-if="Object.keys(curentpagecurve).length > 0" class="mt-4 card-enter-anim" style="animation-delay: 300ms;">
      <v-col
        v-for="(value, key) in curentpagecurve"
        :key="key"
        cols="12"
        md="6"
        class="pb-4"
      >
        <v-card class="rounded-xl border border-opacity-5 chart-card" elevation="2">
          <v-card-text class="pa-4">
            <highcharts :options="createChartOptions(key, value, curentpagecurvelinename)" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios';
import UperNavbar from './layout/UperNavbar.vue';
import { NDatePicker } from "naive-ui";

export default {
  name: 'HistoryDashboard',
  components: {
    UperNavbar,
    NDatePicker
  },
  data: () => ({
    machineselect: null,
    machineselection: [],
    starttime: null,
    endtime: null,
    variabledata: [],
    curvedata: {},
    curentpageitem: [],
    curentpagecurve: {},
    curentpagecurvelinename: [],
    curvelinenamelist: [],
    searchloading: false
  }),
  methods: {
    async getmachineonlinestatus() {
      const token = this.$store.getters.getToken;
      await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/machineconnectstatus`, {
        headers: { "accesstoken": token }
      }).then((response) => {
        if (response.data.status !== 'error') {
          var res = response.data.Data;
          this.machineselection = [];
          Object.keys(res).forEach(key => {
            this.machineselection.push(key);
          });
        }
      });
    },
    formatDate(date, timedef) {
      if (date != null) {
        date = new Date(date);
        const pad = (n) => (n < 10 ? '0' + n : n);
        if (timedef !== 'start') {
          return date.getFullYear() + '-' +
            pad(date.getMonth() + 1) + '-' +
            pad(date.getDate()) + ' ' +
            '23' + ':' +
            '59' + ':' +
            '59';
        } else {
          return date.getFullYear() + '-' +
            pad(date.getMonth() + 1) + '-' +
            pad(date.getDate()) + ' ' +
            pad(date.getHours()) + ':' +
            pad(date.getMinutes()) + ':' +
            pad(date.getSeconds());
        }
      } else {
        return date;
      }
    },
    async searchhstory() {
      try {
        if (this.starttime != null && this.endtime != null && this.machineselect != null) {
          this.searchloading = true;
          var start_time = this.formatDate(this.starttime, 'start');
          var end_time = this.formatDate(this.endtime, 'end');
          var requestbody = {
            "machine_name": this.machineselect,
            "start_time": start_time,
            "end_time": end_time
          };
          const token = this.$store.getters.getToken;
          await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/history/getdata`, requestbody, {
            headers: { "accesstoken": token },
            timeout: 30000
          }).then((response) => {
            if (response.data.status === 'error') {
              console.log('get history data fail');
            } else {
              this.curvelinenamelist = response.data.Data.variable.id;
              this.variabledata = this.transformToDataTable(response.data.Data.variable);
              this.curvedata = response.data.Data.curve;
            }
          });
        }
      } finally {
        this.searchloading = false;
      }
    },
    transformToDataTable(input) {
      const length = Object.values(input)[0]?.length || 0;
      const items = Array.from({ length }, (_, i) => {
        const row = {};
        for (const key in input) {
          row[key] = input[key][i];
        }
        return row;
      });
      return items;
    },
    createChartOptions(title, yData, names) {
      const series = yData.map((arr, i) => ({
        name: names[i] || `批次 / Batch ${i + 1}`,
        data: arr.map(Number),
        lineWidth: 2,
        shadow: {
          color: 'rgba(0, 0, 0, 0.05)',
          width: 4,
          offsetX: 0,
          offsetY: 2
        }
      }));
      
      return {
        chart: {
          type: 'spline',
          backgroundColor: 'transparent',
          style: {
            fontFamily: "'Roboto', 'Inter', sans-serif"
          },
          spacing: [16, 16, 16, 16]
        },
        colors: ['#0ea5e9', '#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899'],
        title: {
          text: title,
          align: 'left',
          style: {
            fontSize: '16px',
            fontWeight: 'bold',
            color: '#1e293b'
          }
        },
        xAxis: {
          gridLineColor: '#f1f5f9',
          lineColor: '#cbd5e1',
          tickColor: '#cbd5e1',
          labels: {
            style: { color: '#64748b' }
          }
        },
        yAxis: {
          title: { text: '' },
          gridLineColor: '#f1f5f9',
          gridLineDashStyle: 'Dash',
          labels: {
            style: { color: '#64748b' }
          }
        },
        tooltip: {
          shared: true,
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderWidth: 1,
          borderColor: '#e2e8f0',
          borderRadius: 12,
          shadow: true,
          useHTML: true,
          style: {
            color: '#334155'
          }
        },
        legend: {
          enabled: series.length > 1,
          align: 'right',
          verticalAlign: 'top',
          layout: 'horizontal',
          itemStyle: {
            color: '#64748b',
            fontWeight: 'bold'
          }
        },
        credits: {
          enabled: false
        },
        plotOptions: {
          series: {
            marker: {
              enabled: false,
              states: {
                hover: {
                  enabled: true,
                  radius: 5
                }
              }
            }
          }
        },
        series: series
      };
    },
    updateCurrentItems(items) {
      this.curentpageitem = items;
      var idList = items.map(item => item.id);
      var indices = idList.map(id => this.curvelinenamelist.indexOf(id));
      var newData = {};
      Object.keys(this.curvedata).forEach(key => {
        newData[key] = indices.map(index => this.curvedata[key][index]);
      });
      this.curentpagecurve = newData;
      this.curentpagecurvelinename = idList;
      return true; // Return true to make the v-if evaluate correctly
    },
    exportcsv() {
      const length = this.curvelinenamelist.length || 0;
      const items = Array.from({ length }, (_, i) => {
        var origin = this.variabledata[i];
        const row = {};
        for (const key in origin) {
          row[key] = origin[key];
        }
        for (const curvekey in this.curvedata) {
          var curvelist = this.curvedata[curvekey][i];
          curvelist = curvelist.map(num => Math.round(num * 1000) / 1000);
          row[curvekey] = JSON.stringify(curvelist);
        }
        return row;
      });
      this.downloadCSV(items, 'machinedata.csv');
    },
    downloadCSV(data, filename) {
      if (!data || !data.length) return;
      const keys = Object.keys(data[0]);
      const csvRows = [keys.join(',')];
      data.forEach(row => {
        const values = keys.map(key => {
          let val = row[key];
          if (typeof val === 'string') {
            val = `"${val
              .replace(/\r?\n/g, '')
              .replace(/\s+/g, ' ')
              .trim()
              }"`;
          }
          return val;
        });
        csvRows.push(values.join(','));
      });
      const csvString = csvRows.join('\n');
      const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      window.URL.revokeObjectURL(url);
    }
  },
  mounted() {
    var token = this.$cookies.get('accesstoken');
    if (!token) {
      this.$router.push({ name: 'Login' });
    } else {
      this.getmachineonlinestatus();
    }
  }
}
</script>

<style scoped>
.history-dashboard-container {
  background-color: #f8fafc;
  min-height: 100vh;
  width: 100%;
}

.text-slate-800 {
  color: #1e293b !important;
}

.text-slate-600 {
  color: #475569 !important;
}

/* Naive UI Picker Alignment Overrides */
.custom-naive-picker {
  height: 56px !important;
}

:deep(.n-input) {
  --n-border: 1px solid rgba(0, 0, 0, 0.24) !important;
  --n-border-hover: 1px solid #1976d2 !important;
  --n-border-focus: 2px solid #1976d2 !important;
  --n-border-radius: 8px !important;
  --n-height: 56px !important;
  font-family: 'Roboto', sans-serif;
  background-color: white !important;
  transition: all 0.3s ease;
}

:deep(.n-input-wrapper) {
  padding-left: 12px !important;
  padding-right: 12px !important;
}

:deep(.n-input__placeholder) {
  color: rgba(0, 0, 0, 0.54) !important;
  font-size: 0.95rem !important;
}

:deep(.n-input__input-el) {
  height: 56px !important;
  font-size: 0.95rem !important;
  color: #1e293b !important;
}

/* Action button micro-animations */
.action-btn {
  font-weight: 700 !important;
  letter-spacing: 0.5px;
  height: 48px !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px -4px rgba(25, 118, 210, 0.4) !important;
}

.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px -4px rgba(76, 175, 80, 0.4) !important;
}

/* Table Card Adjustments */
.custom-table-wrapper {
  border: 1px solid rgba(0, 0, 0, 0.08) !important;
}

.custom-data-table {
  width: 100%;
  border-collapse: collapse;
}

.table-data-row {
  transition: background-color 0.2s ease;
}

.table-data-row:hover {
  background-color: rgba(25, 118, 210, 0.04) !important;
}

.table-cell {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06) !important;
  color: #334155 !important;
  font-size: 0.875rem !important;
}

:deep(.v-data-table-header) {
  background-color: #f1f5f9 !important;
}

:deep(.v-data-table-header th) {
  font-weight: 800 !important;
  color: #475569 !important;
  border-bottom: 2px solid rgba(0, 0, 0, 0.08) !important;
  font-size: 0.9rem !important;
}

/* Chart card style */
.chart-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-color: white !important;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px -8px rgba(0, 0, 0, 0.1) !important;
}

/* Card Load Animation */
.card-enter-anim {
  animation: slide-up-fade-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
}

@keyframes slide-up-fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>