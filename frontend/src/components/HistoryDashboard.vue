<template>
    <v-row>
        <UperNavbar /> 
    </v-row>
    <v-row class="mt-7 mr-1 ml-1">
        <v-col>
            <v-card style="overflow: visible;">
                <v-card-title class="text-h5">Search Selection</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col cols="3">
                            <v-select
                                    v-model="machineselect"
                                    label="Select Machine"
                                    :items="this.machineselection"
                                    density="compact"
                            ></v-select>
                        </v-col>
                        <v-col cols="4">
                          <div>

                                <n-date-picker
                                v-model:value="starttime"
                                type="date"
                                clearable
                                placeholder="Select Start Time"
                                />
                            </div>
                        </v-col>
                        
                        <v-col cols="1" class="text-center" style="font-size: 24px; user-select: none;">
                        ➔
                        </v-col>
                        <v-col cols="4">
                         <div>
                                <n-date-picker
                                v-model:value="endtime"
                                type="date"
                                clearable
                                placeholder="Select End Time"
                                />
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-row>
                        <v-col class="d-flex justify-end">
                            <v-btn :loading="searchloading" color="blue darken-1" text @click="searchhstory();">Search</v-btn>
                            <v-btn v-if="this.curvelinenamelist.length > 0" color="blue darken-1" text @click="exportcsv();">Download</v-btn>
                        </v-col>
                        
                    </v-row>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
    <v-row class="mt-2 mr-1 ml-1">
        <v-col>
            <v-card>
                <v-card-text>
                    <v-data-table
                        :items="this.variabledata"
                        density="compact"
                        item-key="id"
                        :items-per-page-options="[5,10, 15, 20]"
                    >
                        <template v-slot:body="{ items }">
                            <tr v-for="(item) in items" :key="item.id">
                                <td v-for="(value, key) in item" :key="key">{{ value }}</td>
                            </tr>
                            <span v-if="updateCurrentItems(items)" style="display: none;"></span>
                        </template>
                    </v-data-table>
            </v-card-text>
            </v-card>
        </v-col>
    </v-row>
    <v-row class="mt-2 mr-1 ml-1">
        <v-col
            v-for="(value, key) in curentpagecurve" :key="key"
        >
        <highcharts :options="createChartOptions(key,value,this.curentpagecurvelinename)" />
        </v-col>

    </v-row>
</template>
  

<style scoped>
.custom-datepicker {
  border: 1px solid #ccc;
  border-radius: 4px;
  height: 56px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  font-family: Roboto, sans-serif;
  background-color: white;
  transition: border-color 0.3s ease;
}

.custom-datepicker:focus-within {
  border-color: #1976d2; /* Vuetify primary 色 */
}
</style>
  <script>
import axios from 'axios';
import UperNavbar  from './layout/UperNavbar.vue';
import { NDatePicker } from "naive-ui";
  export default {
    name: 'HistoryDashboard',
    components: {
            UperNavbar,
            NDatePicker
    },
    data: () => ({
        machineselect:null,
        machineselection:[],
        starttime:null,
        endtime:null,
        variabledata : [],
        curvedata : {},
        curentpageitem:[],
        curentpagecurve:{},
        curentpagecurvelinename:[],
        curvelinenamelist:[],
        searchloading:false
    }),
    methods: {
        async getmachineonlinestatus(){
            const token = this.$store.getters.getToken;
            await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/machineconnectstatus`,
            {
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status!='error'){
                var res = response.data.Data;
                Object.keys(res).forEach(key => {
                    this.machineselection.push(key);
                });
            }
        })
        },
        formatDate(date,timedef) {
            if(date != null){
                date = new Date(date);
                const pad = (n) => (n < 10 ? '0' + n : n);
                if (timedef != 'start'){
                        return date.getFullYear() + '-' +
                        pad(date.getMonth() + 1) + '-' +
                        pad(date.getDate()) + ' ' +
                        '23' + ':' +
                        '59' + ':' +
                        '59';
                }
                else{
                        return date.getFullYear() + '-' +
                        pad(date.getMonth() + 1) + '-' +
                        pad(date.getDate()) + ' ' +
                        pad(date.getHours()) + ':' +
                        pad(date.getMinutes()) + ':' +
                        pad(date.getSeconds());
                }

            }
            else{
                return date
            }
        },
        async searchhstory(){
        
        try{
            if(this.starttime != null && this.endtime != null && this.machineselect != null ){
                this.searchloading = true
                var start_time  = this.formatDate(this.starttime,'start')
                var end_time    = this.formatDate(this.endtime,'end')
                var requestbody = {"machine_name":this.machineselect,"start_time":start_time,"end_time":end_time};
                const token     = this.$store.getters.getToken;
                await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/history/getdata`,requestbody,{
                        headers:{"accesstoken":token},
                        timeout: 30000
                    }
                    ).then( (response) => {
                        if (response.data.status=='error'){
                            console.log('get history data fail')
                    }
                    else{
                        this.curvelinenamelist = response.data.Data.variable.id
                        this.variabledata      = this.transformToDataTable(response.data.Data.variable)
                        this.curvedata         = response.data.Data.curve
                    }
                    })
            }            
        }
        finally{
            this.searchloading = false
        }
    },
        transformToDataTable(input){
            const length = Object.values(input)[0]?.length || 0

            const items = Array.from({ length }, (_, i) => {
                const row = {}
                for (const key in input) {
                row[key] = input[key][i]
                }
                return row
            
            })

            return items
        },
        createChartOptions(title, yData,names) {
            const series = yData.map((arr, i) => ({
            name: names[i] || `Series ${i + 1}`,
            data: arr.map(Number)
            }))
            return {
                chart: { type: 'spline' },
                title: { text: title },
                series: series,
                legend: {
                    enabled: false
                },
            }
        },
        updateCurrentItems(items) {
            this.curentpageitem = items
            var idList = items.map(item => item.id);
            var indices = idList.map(id => this.curvelinenamelist.indexOf(id));
            var newData = {};
            Object.keys(this.curvedata).forEach(key => {
                newData[key] = indices.map(index => this.curvedata[key][index]);
            });
            this.curentpagecurve = newData
            this.curentpagecurvelinename = idList
        },
        exportcsv(){
            const length = this.curvelinenamelist.length || 0
            const items = Array.from({ length }, (_, i) => {
                var origin = this.variabledata[i]
                const row = {}
                for (const key in origin){
                    row[key] = origin[key]
                }
                for (const curvekey in this.curvedata) {
                    var curvelist = this.curvedata[curvekey][i]
                    curvelist = curvelist.map(num => Math.round(num * 1000) / 1000);
                    row[curvekey] =JSON.stringify(curvelist)
                }
                return row
            })
            this.downloadCSV(items,'machinedata.csv')
        },
        downloadCSV(data, filename) {
            if (!data || !data.length) return
            const keys = Object.keys(data[0])
            const csvRows = [keys.join(',')]
            data.forEach(row => {
                const values = keys.map(key => {
                let val = row[key] ;
                if (typeof val === 'string') {
                    val = `"${val
                    .replace(/\r?\n/g, '')   
                    .replace(/\s+/g, ' ')
                    .trim()
                    }"`
                }
                return val
                })
                csvRows.push(values.join(','))
            })
            const csvString = csvRows.join('\n')
            const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8' })
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = filename
            a.click()
            window.URL.revokeObjectURL(url)
    }    
            
},
    mounted(){
        var token = this.$cookies.get('accesstoken');
        if (!token){
            this.$router.push({ name: 'Login' });
        }
        else{
            this.getmachineonlinestatus();
        }
    },
  }
</script>

<style scoped>
.no-dot .v-timeline-item__dot {
  display: none !important;
}
</style>