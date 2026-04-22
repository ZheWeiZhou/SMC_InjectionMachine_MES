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
                    <v-btn color = "light-green-accent-1">
                        <v-icon color="#39CC64">mdi-leaf</v-icon>
                        Energy optimization
                    </v-btn>
                </v-col>
            </v-row>
            <v-row>
                <v-col v-for="(item, key) in abstractitem" :key="key" cols="12" sm="6" md="3">
                    <v-card elevation="2" class="pa-4">
                    <v-card-title class="text-subtitle-1">
                        {{ item.name }}
                    </v-card-title>
                    
                    <v-card-text class="text-h6 font-weight-bold">
                     {{ Math.round( item.value  * 100 / 100) }} {{ item.Unit  }} 
                    </v-card-text>
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
        plasticpower:'',
        injectionpower:'',
        clampingpower:'',
        totalpower:'',
        updatetime:'',
        abstractitem:{},
        curvedatalist:[]
        
    }),
    methods: {
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
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
                        this.abstractitem       = rawinfo?.abstract

            
                        this.plasticpower       = rawinfo?.abstract?.plasticmotorenergy ?? 0
                        this.plasticpower       = Math.round(this.plasticpower  * 100) / 100;
                        this.injectionpower     = rawinfo?.abstract?.injection_energy ?? 0
                        this.injectionpower     = Math.round(this.injectionpower  * 100) / 100;
                        this.clampingpower      = rawinfo?.abstract?.closemoldenergy ?? 0
                        this.clampingpower      = Math.round(this.clampingpower  * 100) / 100;
                        this.totalpower         = rawinfo?.abstract?.total ?? 0
                        this.totalpower         = Math.round(this.totalpower  * 100) / 100;
                        var new_curvedata = []
                        for (var k of Object.keys(rawinfo["curve"])) {
                            var item = rawinfo.curve[k];
                            var ydata = item.value.map(item => parseFloat(item));
                            var curveitem = { "Title": item.name, "Data": ydata, "Unit":item.Unit };
                            new_curvedata.push(curveitem);
                        }
                        this.curvedatalist = new_curvedata
                    }
                } catch (err) {
                    console.log(err);
                }
            }
            })
    },
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