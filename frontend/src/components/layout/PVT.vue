<template>
<v-btn class="ml-5" text @click="pvtdialog = true">
    <v-icon left  color="#39CC64">mdi-chart-bell-curve-cumulative</v-icon>
    PVT 觀測
</v-btn>
<!-- POWER METER DIALOG -->
    <v-dialog v-model="pvtdialog" width="95%" height="150%" transition="dialog-bottom-transition" >
        <v-card>
            <v-card-title class="d-flex justify-end">
                <v-btn size="x-small" icon="mdi-close" color="blue darken-1" @click="pvtdialog = false"></v-btn>
            </v-card-title>
            <v-card-text>
            <v-row>
                <v-col>
                    <highcharts :options="createPvtChartOptions('PVT',chartxlist, chartylist,'temp','v')" style="width: 100%; height: 80vh;" />
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
    name: 'PVT',
    props: {
        machinename:String,
    },
    
    data: () => ({
        pvtdialog:false,
        v1list:[],
        v2list:[],
        v3list:[],
        t1list:[],
        t2list:[],
        t3list:[],
        v_0_list:[],
        v_50_list:[],
        v_100_list:[],
        temprange:[50,75,100,125,150,175,200,225,250,275,300],
        updatetime:'',
        chartxlist :[],
        chartylist:[],
    }),
    methods: {
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },
    createPvtChartOptions(title, xLists, yLists, xTitle, yTitle) {
    // xLists: [x1, x2, x3, x4, x5]
    // yLists: [y1, y2, y3, y4, y5]
    
    const series = xLists.map((xList, index) => {
        const yList = yLists[index];
        const myColors = ['#FF5733', '#33FF57', '#3357FF', '#BEBEBE', '#BEBEBE', '#BEBEBE'];
        // 將 [1,2] 和 [1,2] 組合成 [[1,1], [2,2]] 格式
        const combinedData = xList.map((x, i) => [x, yList[i]]);
        const nm = ['sensor1','sensor2','sensor3','0 Mpa','50 Mpa','100 Mpa']
        return {
            name: nm[index],
            data: combinedData,
            type: 'spline',
            color: myColors[index],
            marker: { enabled: false }
        };
    });

    return {
        chart: { zoomType: 'xy' },
        title: { text: title },
        xAxis: { title: { text: xTitle }, gridLineWidth: 1 },
        yAxis: { title: { text: yTitle },tickInterval: 0.005, },
        series: series,
        tooltip: {
            shared: true,
            crosshairs: true,
            valueDecimals: 4
        }
    };
    },
    async getpvtinfo(){
        const token = this.$store.getters.getToken;
        await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/pvtcurve/${this.machinename}`,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
                if (response.data.status=='error'){
                    console.log('Get pvt info fail')
            }
            else{
                var rawinfo = response.data.Data.current;
                try{
                    console.log('pvt',rawinfo)
                    if(rawinfo.updatetime != this.updatetime){
                        this.updatetime = rawinfo.updatetime;
                        this.v1list = rawinfo.V1;
                        this.v2list = rawinfo.V2;
                        this.v3list = rawinfo.V3;
                        this.t1list = rawinfo.T1;
                        this.t2list = rawinfo.T2;
                        this.t3list = rawinfo.T3;
                        this.v_0_list = rawinfo.V_support_0;
                        this.v_50_list = rawinfo.V_support_50;
                        this.v_100_list = rawinfo.V_support_100;
                        this.chartxlist = [this.t1list,this.t2list, this.t3list,this.temprange,this.temprange,this.temprange]
                        this.chartylist = [this.v1list,this.v2list,this.v3list,this.v_0_list,this.v_50_list,this.v_100_list]
                    }
                } catch (err) {
                    console.log(err);
                }
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
            this.getenergyinfotimer=setInterval(this.getpvtinfo,1000);
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