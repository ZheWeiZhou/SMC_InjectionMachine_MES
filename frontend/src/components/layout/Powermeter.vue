<template>
<v-btn class="ml-5" icon @click="powermeterdialog = true">
    <v-icon color="#39CC64">mdi-leaf</v-icon>
</v-btn>
<!-- POWER METER DIALOG -->
    <v-dialog v-model="powermeterdialog" width="95%" height="150%" transition="dialog-bottom-transition" >
        <v-card>
            <v-card-title class="d-flex justify-end">
                <v-btn size="x-small" icon="mdi-close" color="blue darken-1" @click="powermeterdialog = false"></v-btn>
            </v-card-title>
            <v-card-text>
            <v-row>
                <v-col>
                    <highcharts :options="createGroupedColumnOptions('製程能耗變化',processhistory.updatetime, processhistory.dataset
                    ,processhistory.displayunit)" />
                </v-col>
            </v-row>
            <v-row v-if="Object.keys(optimization).length > 0" >
                <v-col>
                    <v-row>
                        <v-col>
                    <v-card class="pa-6 mb-4" rounded="xl" variant="flat" color="#DCEDC8">
                        <div class="d-flex justify-space-between align-center mb-6">
                        <h3 class="text-h6 font-weight-bold" style="color:#33691E;" >Adjustments Suggestion</h3>
                            <v-btn
                            size="small"
                            elevation="0"
                            rounded="lg"
                            color="#C5E1A5" 
                            class="text-green-darken-4 font-weight-bold"
                            @click="updateparameter()"
                            >
                                <v-icon start>mdi-leaf</v-icon>
                                APPLY TO MACHINE
                            </v-btn>
                        </div>
                        <div class="d-flex flex-wrap" style="gap: 80px;">
                        <div  v-for="(item, key) in optimization" :key="key">
                        <div class="text-right">
                            <div class="text-caption">{{ item.name }}</div>
                            <div class="text-h4 font-weight-bold" style="color:#689F38;">
                            {{ Math.round( item.value  * 100 / 100) }} <span class="text-body-2 ml-1">{{ item.unit }} </span>
                            </div>
                        </div>
                        </div>
                        </div>

                            <v-card class="mt-4" variant="flat" color="#DCEDC8" v-if="Object.keys(powerprediction).length > 0" >
                                <div class="d-flex justify-space-between align-center mb-6">
                                <h3 class="text-h6 font-weight-bold" style="color:#33691E;" >Expected Optimization Results</h3>
                                </div>
                                <div class="d-flex flex-wrap" style="gap: 80px;">
                                <div  v-for="(item, key) in powerprediction" :key="key">
                                <div class="text-right">
                                    <div class="text-caption">{{ item.name }}</div>
                                    <div class="text-h4 font-weight-bold" style="color:#689F38;">
                                    {{ Math.round( item.value  * 100 / 100) }} <span class="text-body-2 ml-1">{{ item.unit }} </span>
                                    </div>
                                </div>
                                </div>
                                </div>
                            </v-card>

                        <v-card-actions v-if="isshowmessage">
                            <v-spacer></v-spacer>
                            <span class="text-caption">{{ messagetext }}</span>
                        </v-card-actions>
                    </v-card>
                    </v-col>
                    </v-row>
                </v-col>                
            </v-row>
            <v-row v-if="Object.keys(abstractitem).length > 0">
                <v-col>
                    <v-card class="pa-6 mb-4" rounded="xl" variant="flat" color="#F1F8E9">
                        <div class="d-flex justify-space-between align-center mb-6">
                        <h3 class="text-h6 font-weight-bold" style="color:#2E7D32;">Power Consumption</h3>
                        </div>
                        <div class="d-flex flex-wrap" style="gap: 80px;">
                        <div  v-for="(item, key) in abstractitem" :key="key">
                        <div class="text-right">
                            <div class="text-caption ">{{ item.name }}</div>
                            <div class="text-h4 font-weight-bold text-green-accent-3">
                            {{ Math.round( item.value  * 100 / 100) }} <span class="text-body-2 ml-1">{{ item.Unit  }} </span>
                            </div>
                        </div>
                        </div>
                        </div>
                        <v-card v-if="Object.keys(expectation).length > 0"  class="mt-4"  variant="flat" color="#F1F8E9">
                        <div class="d-flex justify-space-between align-center mb-6">
                        <h3 class="text-h6 font-weight-bold" style="color:#2E7D32;">Predicted Energy Consumption</h3>
                        </div>
                        <div class="d-flex flex-wrap" style="gap: 80px;">
                        <div  v-for="(item, key) in expectation" :key="key">
                        <div class="text-right">
                            <div class="text-caption ">{{ item.name }}</div>
                            <div class="text-h4 font-weight-bold text-green-accent-3">
                            {{ Math.round( item.value  * 100 / 100) }} <span class="text-body-2 ml-1">{{ item.unit  }} </span>
                            </div>
                        </div>
                        </div>
                        </div>
                    </v-card>
                    </v-card>
                </v-col>
            </v-row>
                <v-row>
                    <v-col>
                        <v-card>
                            <v-card-title>
                                Power Curve
                            </v-card-title>
                            <v-card-text>
                                <v-row
                                    v-for = "item in curvedatalist"
                                    :key="item.Title">
                                    <v-col>
                                        <highcharts :options="createChartOptions(item.Title, item.Data,item.Unit)" />
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-dialog>

 
</template>
  

<style scoped>
</style>
  <script>
import axios from 'axios';
  export default {
    name: 'PowerMeter',
    props: {
        machinename:String,
    },
    
    data: () => ({
        powermeterdialog:false,
        updatetime:'',
        abstractitem:{},

        optimization:[
            {'nodename':'Ijv_set1','value':'20','name':'第一段射速','unit':'mm/s'},
            {'nodename':'Ijv_set2','value':'19','name':'第二段射速','unit':'mm/s'},
        ],
        powerprediction:[
            {'nodename':'','value':'20000','name':'充填能耗','unit':'J'},
            {'nodename':'','value':'19000','name':'保壓能耗','unit':'J'},
        ],
        expectation:[
            {'nodename':'','value':'21000','name':'充填能耗','unit':'J'},
            {'nodename':'','value':'19000','name':'保壓能耗','unit':'J'},
        ],
        curvedatalist:[],
        isshowmessage:false,
        messagetext:'',
        processhistory:{
            updatetime:[],
            dataset:[],
            template:'',
            displayunit:'KJ'
        },
        categoriestest: ['2026-05-02 11:13', '2026-05-02 11:15', '2026-05-02 11:17', '2026-05-02 11:20', '2026-05-02 11:22'],
        seriesDatatest:[
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
            type: 'column' // 改為柱狀圖
        },
        title: {
            text: title
        },
        xAxis: {
            categories: categories, // 傳入 ['USA', 'China', ...]
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: unit // 傳入單位，例如 '1000 metric tons (MT)'
            }
        },
        tooltip: {
            valueSuffix: ` (${unit})` // 滑鼠移上去時顯示單位
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        // seriesData 預期是一個陣列物件: [{ name: 'Corn', data: [...] }, { name: 'Wheat', data: [...] }]
        series: seriesData 
        }
        },
    createChartOptions(title, yData,Unit) {
        const categories = yData.map((_, i) => (i + 1).toString())
        return {
                chart: { type: 'spline' },  // 曲線圖
                title: { text: title },
                xAxis: {
                categories,
                title: { text: 'time' }
                },
                yAxis: {
                title: { text: Unit }
                },
                series: [{
                name: title,
                data: yData
                }]
            }
            },
    update_processhistory(abstract,dataupdatetime){
        if(this.processhistory.updatetime.length == 0){
            this.processhistory.template = abstract
        }
        const keystemplate = Object.keys(this.processhistory.template).sort();
        const keysabstract = Object.keys(abstract).sort();
        //如果格式檢查失敗，執行初始化重置
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
    async getenergyinfo(){
        const token = this.$store.getters.getToken;
        await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/realtimepower/${this.machinename}`,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
                if (response.data.status=='error'){
                    console.log('Get energy info fail')
            }
            else{
                var rawinfo             = response.data.Data.machineenergy;
                try{
                    var dataupdatetime = rawinfo["updatetime"]
                    if (dataupdatetime != this.updatetime){
                        this.updatetime         = dataupdatetime
                        this.abstractitem       = rawinfo?.abstract ?? {}
                        this.optimization       = rawinfo?.cal ?? {}
                        this.powerprediction = rawinfo?.powerprediction ?? {}
                        this.expectation = rawinfo?.expectation ?? {}
                        var new_curvedata = []
                        for (var k of Object.keys(rawinfo["curve"])) {
                            var item = rawinfo.curve[k];
                            var ydata = item.value.map(item => parseFloat(item));
                            var curveitem = { "Title": item.name, "Data": ydata, "Unit":item.Unit };
                            new_curvedata.push(curveitem);
                        }
                        this.curvedatalist = new_curvedata
                        this.update_processhistory(this.abstractitem,this.updatetime)

                    }
                } catch (err) {
                    console.log(err);
                }
            }
            })
    },
    async updateparameter(){
        const token = this.$store.getters.getToken;
        let command = []
        this.optimization.forEach((item) =>{
            command.push({"target":item["nodename"],"value":item["value"]})
        })
        let machine_Protocol = "euromap77"
        const euromap63list = ["TOYO"]
        if(euromap63list.includes(this.machinename)){
            machine_Protocol = "euromap63"
        }
        const requestbody = {
           "machine_name":this.machinename,
           "command":command,
           "machine_Protocol":machine_Protocol
        }
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/multicontrol`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status=='error'){
                    console.log('Fail')
            }else{
                this.messagetext = "Parameter updates success"
                this.isshowmessage = true
                setTimeout(() => {
                this.isshowmessage = false
                }, 5000);
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
            this.getenergyinfotimer=setInterval(this.getenergyinfo,1000);
        }
    },
    beforeDestory(){
      clearInterval(this.getenergyinfotimer);
  },    
  }
</script>

<style scoped>
.no-dot .v-timeline-item__dot {
  display: none !important;
}
</style>