<template>
    <v-row>
        <UperNavbar /> 
    </v-row>    
    <v-row>
        <v-col>
            <div>
                <svg viewBox="0 0 700 312">
                    <defs>
                        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#7DE2FC; stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#B9B6E5; stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <rect x="0" y="0" width="100%" height="100%" fill="#F4FBF9" />
                    <text fill="#74ACFA"   x="5%" y="8%" font-size="70%" font-weight="bold" text-anchor="middle" >Factory 101 </text>
                    <text fill="#74ACFA"   x="55%" y="8%" font-size="70%" font-weight="bold" text-anchor="middle" >Factory 106 </text>
                    <!-- MULTIPAS-MuCell -->
                    <image  @click="selectmachine('MULTIPAS-MuCell')" :href="require('@/assets/machine.png')" x="3%"  y="20%"  width="10%"  height="10%" />
                    <text fill="#121212" x="8%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle">MULTIPAS-MuCell</text>
                    <circle :fill="machinedata['MULTIPAS-MuCell'][0]" class="breathing-circle" cx="6%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['MULTIPAS-MuCell'][0]"  x="8.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['MULTIPAS-MuCell'][1] }}</text> 
                    <text  :fill="machinedata['MULTIPAS-MuCell'][3]"  x="8%" y="19%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['MULTIPAS-MuCell'][2] }}</text>
                    <!-- <rect x="5%" y="25%" width="6%" height="10%" rx="5" ry="5" fill="#BFCEEB" /> -->
                    <!-- Engel-120 -->
                    <image  @click="selectmachine('Engel-120')" :href="require('@/assets/machine.png')" x="13%"  y="20%"  width="10%"  height="10%" />
                    <text fill="#121212" x="18%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >Engel-120</text>
                    <circle :fill="machinedata['Engel-120'][0]" class="breathing-circle" cx="16%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['Engel-120'][0]"  x="18.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-120'][1] }}</text>  
                    <text  :fill="machinedata['Engel-120'][3]"  x="18%" y="19%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-120'][2] }}</text>  
                    <!-- Engel-80 -->
                    <image  @click="selectmachine('Engel-80')" :href="require('@/assets/machine.png')" x="23%"  y="20%"  width="10%"  height="10%" />
                    <text fill="#121212" x="28%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >Engel-80</text>
                    <circle :fill="machinedata['Engel-80'][0]" class="breathing-circle" cx="26%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['Engel-80'][0]"  x="28.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-80'][1] }}</text>
                    <text  :fill="machinedata['Engel-80'][3]"  x="28%" y="19%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-80'][2] }}</text>             
                    <!-- FCS-Mucell -->
                    <image  @click="selectmachine('FCS-Mucell')" :href="require('@/assets/machine.png')" x="33%"  y="20%"  width="10%"  height="10%" />
                    <text fill="#121212" x="38%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >FCS-Mucell</text>
                    <circle :fill="machinedata['FCS-Mucell'][0]" class="breathing-circle" cx="36%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['FCS-Mucell'][0]"  x="38.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-Mucell'][1] }}</text>
                    <text  :fill="machinedata['FCS-Mucell'][3]"  x="38%" y="19%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-Mucell'][2] }}</text>    
                    <!-- FCS-150 -->
                    <image  @click="selectmachine('FCS-150')" :href="require('@/assets/machine.png')" x="75%"  y="20%"  width="10%"  height="10%" />
                    <text fill="#121212" x="80%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >FCS-150</text>
                    <circle :fill="machinedata['FCS-150'][0]" class="breathing-circle" cx="78%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['FCS-150'][0]"  x="80.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-150'][1] }}</text>
                    <text  :fill="machinedata['FCS-150'][3]"  x="80%" y="19%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-150'][2] }}</text>  
                    <!-- TOYO -->
                    <image  @click="selectmachine('TOYO')" :href="require('@/assets/machine.png')" x="85%"  y="20%"  width="10%"  height="10%" />
                    <text fill="#121212" x="90%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >TOYO</text>
                    <circle :fill="machinedata['TOYO'][0]" class="breathing-circle" cx="88%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['TOYO'][0]"  x="90.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['TOYO'][1] }}</text>
                    <!-- Tachung -->
                    <image  @click="selectmachine('Tachung')" :href="require('@/assets/machine.png')" x="75%"  y="65%"  width="10%"  height="10%" />
                    <text fill="#121212" x="80%" y="77%" font-size="40%" font-weight="bold" text-anchor="middle" >Tachung</text>
                    <circle :fill="machinedata['Tachung'][0]" class="breathing-circle" cx="78%" cy="80%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['Tachung'][0]"  x="80.5%" y="80.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['Tachung'][1] }}</text>
                    <text  :fill="machinedata['Tachung'][3]"  x="80%" y="64%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['Tachung'][2] }}</text>
                    <!-- WALL -->
                    <line x1="50%"  y1="5%"  x2="50%" y2="95%"  stroke="#DEDEF0" stroke-width="0.15%" />
                    <text fill="#74ACFA"   x="88%" y="99%" font-size="45%" font-weight="bold" text-anchor="middle" >Click the machine icon to view more information </text>
                </svg>
            </div>
        </v-col>
    </v-row>
</template>
  

  <style>
    .breathing-circle {
      animation: breathe 2s infinite ease-in-out;
      transform-origin: center;
    }

    @keyframes breathe {
      0% {
        opacity: 0.3;
      }
      50% {
        opacity: 1;
      }
      100% {
        opacity: 0.3;
      }
    }
    svg image {
      cursor: pointer;
    }
  </style>
  <script>
import axios from 'axios';
import UperNavbar  from './layout/UperNavbar.vue';
  export default {
    name: 'MachineOverviewPage',
    components: {
            UperNavbar
    },
    data: () => ({
        machinedata:{
            "MULTIPAS-MuCell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "Engel-120":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "Engel-80":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "FCS-Mucell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "FCS-150":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "TOYO":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "Tachung":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
        },
        offlinecolor:"rgba(182,182,180,0.6)",
        onlinecolor:"rgba(76,175,80,0.6)",
        workcolor: "rgba(255,196,51,0.6)",

    }),
    methods: {
        async getmachineonlinestatus(){
            const token = this.$store.getters.getToken;

            // const token = "8d6d4e85-b277-4102-8ffd-defcc7b7b9f9"
            await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/machineconnectstatus`,
            {
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status=='error'){
                this.machinedata = {
                    "MULTIPAS-MuCell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "Engel-120":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "Engel-80":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "FCS-Mucell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "FCS-150":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "TOYO":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "Tachung":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                }
            }
            else{
                var res = response.data.Data;
                Object.keys(res).forEach(key => {
                    var machinestatus = res[key]
                    if (machinestatus['Online'] == 'Offline'){
                        this.machinedata[key] =  [this.offlinecolor,'Offline','Sleep',"rgba(182,182,180,0.6)"];
                    }
                    else{
                        var machinework = machinestatus['Status'].charAt(0).toUpperCase() + machinestatus['Status'].slice(1)
                        var statuscolor = "rgba(182,182,180,0.6)"
                        if (machinework == "Stay"){
                            statuscolor = this.onlinecolor
                        }
                        if (machinework == "Work"){
                            statuscolor = this.workcolor
                        }
                        this.machinedata[key] =  [this.onlinecolor,'Online',machinework,statuscolor];
                    }
                });
                
            }
        })
        },
        selectmachine(name){
            var machinename = name;
            
            this.$cookies.set('setSelectMachine', machinename, '1d');
            this.$router.push({ name: 'MachineDashboard' });
        }
    },
    mounted(){   
        var token = this.$cookies.get('accesstoken');
        if (!token){
            console.log("Not Login");
            this.$router.push({ name: 'Login' });
        }
        else{
        this.getmachineonlinestatus();
        this.timer=setInterval(this.getmachineonlinestatus,1000);     
        }
    },
    beforeDestory(){
      clearInterval(this.timer);
  },    
  }
</script>
