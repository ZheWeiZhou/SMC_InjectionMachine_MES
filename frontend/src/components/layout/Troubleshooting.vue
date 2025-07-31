<template>
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
                        <v-card-title class="text-h5">Diagnosis Result : {{ processlinesloveabstract.DefectReason }}</v-card-title>
                        <v-card-text class="text-h6">
                             <v-list >
                                <v-list-item
                                v-for="(item, index) in processlinesloveabstract.SloveAbstract"
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
                                v-for="(item, index) in this.processlineslovetimeline"
                                :key="index"
                                icon=""
                                color="primary"
                                >
                                <div>
                                     {{ item.DefectReason }}<br />
                                    {{ item.AdjustParameter }}<br />
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

<v-dialog v-model="troubleshootingdisplay" width="95%" height="90%" transition="dialog-bottom-transition" >
    <v-card>
        <v-card-title class="d-flex justify-end">
            <v-btn size="x-small" icon="mdi-close" color="blue darken-1" @click="troubleshootingdisplay = false"></v-btn>
        </v-card-title>
    <v-row class="mr-1 ml-1">
        <v-col >
            <v-row >
                <v-col>
                    <v-card class="h-100">
                        <v-card-title class="text-h5">Defect Report</v-card-title>
                        <v-card-text class="text-h6">
                            <v-row>
                                <v-col>
                                    <v-select
                                    v-model="Troubleshootingreport.Defect"
                                    label="Select Defect"
                                    :items="['Short shot']"
                                    variant="underlined"
                                    ></v-select>
                                </v-col>
                                <v-col>
                                    <v-select
                                    v-model="Troubleshootingreport.DefectLevel"
                                    label="Select Defect Level"
                                    :items="['Minor','Moderate','Severe','Critical']"
                                    variant="underlined"
                                    ></v-select>
                                </v-col>
                            </v-row>
                        </v-card-text>
                        <v-card-actions>
                            <v-row>
                                <v-col>
                                    <v-btn v-if="Troubleshootingreport.Defect != '' && Troubleshootingreport.DefectLevel != '' " class="mr-2 ml-3" color="info" @click ="sendtroubleshootingcommand()" rounded="xl">
                                        Send
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-card-actions>
                    </v-card>
                </v-col>
                <v-col>
                    <v-card class="h-100">
                        <v-card-title class="text-h5">Diagnosis Result : {{ manualsloveabstract.DefectReason }}</v-card-title>
                        <v-card-text>
                            <v-row>
                                <v-col>
                                    <v-list >
                                        <v-list-item
                                        v-for="(item, index) in manualsloveabstract.SloveAbstract"
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
                                </v-col>
                            </v-row>
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
                                v-for="(item, index) in this.manualslovetimeline"
                                :key="index"
                                icon=""
                                color="primary"
                                >
                                <div>
                                     {{ item.DefectReason }}<br />
                                    {{ item.AdjustParameter }}<br />                                  
                                </div>
                                </v-timeline-item>
                            </v-timeline>
                        </v-card-text>
                        <v-card-actions>
                            <v-row>
                                <v-col>
                                    <v-btn v-if="this.manualslovetimeline.length !=0"  class="mr-2 ml-3" color="info" @click ="reportproblemslove()" rounded="xl">
                                        Report problem resolved
                                    </v-btn>
                                </v-col>
                            </v-row>                            
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>    
        </v-col>
    </v-row>
    </v-card>
    </v-dialog>


    <v-card class="h-100">
        <v-card-title class="text-h4">Trouble Shooting</v-card-title>
        <v-card-actions>
            <v-btn  class="mr-2 ml-3" color="info" rounded="xl" @click = "troubleshootingdisplay = true">
                Diagnosis
            </v-btn>
            <v-btn class="mr-2 ml-3" color="info" v-if="aoimoduleavailable =='True' " @click ="clickprocessline" rounded="xl">
                Auto Mode Monitor
            </v-btn>
            </v-card-actions>
    </v-card>

    <!-- Process Line status display -->
 
</template>
  

<style scoped>
</style>
  <script>
import axios from 'axios';
// import { computed } from 'vue'
  export default {
    name: 'TroubleShooting',
    props: {
        machineonline: String,
        machinename:String,
        aoimoduleavailable: String,
        feedbacktabledata: Array
    },
    data: () => ({
        troubleshootingdisplay : false,
        processlinedisplay : false,
        processlinestauts: "standby",
        processlinemessage : {"created_time":"NA","image_str":"","product_weight":"NA","quality":"NA","shortshotratio":"NA"},
        processlinesloveabstract:{"DefectReason":"None","SloveAbstract":[]},
        processlineslovetimeline:[],
        Troubleshootingreport:{"Defect":'',"DefectLevel":''},
        manualsloveabstract:{"DefectReason":"None","SloveAbstract":[]},
        manualslovetimeline:[],
    }),
    methods: {
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
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
                    rawinfo.quality  = "Short Shot";
                    console.log("Detect Short shot start to get slove abstract!!!!");
                    this.get_processline_sloveabstract();
                }
                else{
                    this.processlinesloveabstract = {"DefectReason":"None","SloveAbstract":[]};
                    if(this.processlineslovetimeline.length < 1 ){
                        this.processlineslovetimeline.push({"DefectReason":"Normal","AdjustParameter":" ","image_str":rawinfo.image_str});
                    }
                    else{
                        var lastone = this.processlineslovetimeline[this.processlineslovetimeline.length -1];
                        if (lastone["DefectReason"] != "Normal"){
                            this.processlineslovetimeline.push({"DefectReason":"Normal","AdjustParameter":" ","image_str":rawinfo.image_str})
                        }
                    }
                }
                rawinfo.product_weight  = rawinfo.product_weight.toFixed(2)
                rawinfo.shortshotratio  = rawinfo.shortshotratio.toFixed(2)
                this.processlinemessage = rawinfo;

            }
            })
    },
    async get_processline_sloveabstract(){
        var requestbody = {"machine_name":this.machinename};
        const token = this.$store.getters.getToken;
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/troubleshooting/getabstract`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status=='error'){
                    console.log('Get Slove abstract fail');
                    this.processlinesloveabstract={"DefectReason":"None","SloveAbstract":[]};

            }
            else{
                this.processlinesloveabstract  = response.data.Data.SloveAbstract;
                var adjsutparameter = "";
                for(const item of response.data.Data.SloveAbstract.SloveAbstract){
                    adjsutparameter = adjsutparameter + item["Parameter"]+"; "
                }
                if (this.processlinesloveabstract.length > 0){
                    var lastone = this.processlinesloveabstract[this.processlinesloveabstract.length -1];
                    if (lastone["DefectReason"] == "Normal"){
                        this.processlineslovetimeline = [];
                    }
                }
                var timelinedata = {"DefectReason":"DefectReason: " + this.processlinesloveabstract.DefectReason,"AdjustParameter":"AdjustParameter: "+adjsutparameter,"image_str":this.processlinemessage.image_str};
                this.processlineslovetimeline.push(timelinedata);

            }
            })
    },
    async getprocesslinestatus(){
        if(this.aoimoduleavailable =='True'){
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
    async sendtroubleshootingcommand(){
        if(this.machineonline == "Online" && this.feedbacktabledata != []){
            var defect      = this.Troubleshootingreport.Defect;
            var defectlevel = this.Troubleshootingreport.DefectLevel;
            var defectlevelmapping = {"Minor":"1","Moderate":"2","Severe":"3","Critical":"4"}
            var defectmapping = {"Short shot":"shortshot"}
            defectlevel = defectlevelmapping[defectlevel];
            defect = defectmapping[defect]
            var requestbody = {"machine_name":this.machinename,"defect":defect,"defectlevel":defectlevel};
            const token = this.$store.getters.getToken;

            await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/troubleshooting/send_diagnosis_command`,requestbody,{
                    headers:{"accesstoken":token}
                }
                ).then( (response) => {
                if (response.data.status=='error'){
                        console.log('Get process line status fail');
                        this.processlinestauts = "NA";
                    }
                else{
                        this.get_manual_sloveabstract();
                    }
                })
        }
    },
    async get_manual_sloveabstract(){
        var requestbody = {"machine_name":this.machinename};
        const token = this.$store.getters.getToken;
        await this.sleep(2000)
        await axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/troubleshooting/getabstract`,requestbody,{
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status=='error'){
                    console.log('Get Slove abstract fail');
                    this.manualsloveabstract={"DefectReason":"None","SloveAbstract":[]};
            }
            else{
                this.manualsloveabstract  = response.data.Data.SloveAbstract;
                var adjsutparameter = "";
                for(const item of response.data.Data.SloveAbstract.SloveAbstract){
                    adjsutparameter = adjsutparameter + item["Parameter"]+"; "
                }
                if (this.manualslovetimeline.length > 0){
                    var lastone = this.manualslovetimeline[this.manualslovetimeline.length -1];
                    if (lastone["DefectReason"] == "Deffect Sloved"){
                        this.manualslovetimeline = [];
                    }
                }
                var timelinedata = {"DefectReason":"DefectReason: " + response.data.Data.SloveAbstract.DefectReason,"AdjustParameter":"AdjustParameter: "+adjsutparameter};
                this.manualslovetimeline.push(timelinedata);
            }
            })
    },
    reportproblemslove(){
        var timelinedata = {"DefectReason":"Deffect Sloved","AdjustParameter":""};
        this.manualslovetimeline.push(timelinedata);
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
        this.processlinetimer = setInterval(this.getprocesslinestatus,1000)
        }
    },
    beforeDestory(){
      clearInterval(this.processlinetimer);
  },    
  }
</script>

<style scoped>
.no-dot .v-timeline-item__dot {
  display: none !important;
}
</style>