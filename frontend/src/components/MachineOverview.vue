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
                    <rect x="0" y="0" width="100%" height="100%" fill="url(#grad1)" />

                    <text fill="#121212" x="2%" y="5%" font-size="12px" font-family="monospace" font-weight="bold">101 Factory</text>
                    <rect x="92%" y="7%" width="0.5%" height="40%" fill="rgba(227,118,18,0.4)" />

                    <text fill="#121212" x="95%" y="14%" font-size="12px" font-family="monospace" font-weight="bold">T</text>
                    <text fill="#121212" x="95%" y="18%" font-size="12px" font-family="monospace" font-weight="bold">V</text>
                    <text fill="#121212" x="95%" y="26%" font-size="12px" font-family="monospace" font-weight="bold">W</text>
                    <text fill="#121212" x="95%" y="30%" font-size="12px" font-family="monospace" font-weight="bold">A</text>
                    <text fill="#121212" x="95%" y="34%" font-size="12px" font-family="monospace" font-weight="bold">L</text>
                    <text fill="#121212" x="95%" y="38%" font-size="12px" font-family="monospace" font-weight="bold">L</text>
                    <line x1="15%" y1="53%" x2="95%" y2="53%" stroke="#616161" stroke-width="1" stroke-dasharray="5,5" />
                    <line x1="74%" y1="50%" x2="78.5%" y2="50%" stroke="#C5BBB8" stroke-width="4" />
                    <line x1="87%" y1="50%" x2="91.5%" y2="50%" stroke="#C5BBB8" stroke-width="4" />
                    <text fill="#121212" x="79.5%" y="50.5%" font-size="10px" font-family="monospace" font-weight="bold">Entrance</text>
                    <rect x="5%" y="10%" rx="10" ry="10" width="15%" height="12%" :fill="machinedata['MULTIPAS-MuCell']" @click="selectmachine('MULTIPAS-MuCell')"/>
                    <text fill="#121212" x="7%" y="17%" font-size="9px" font-family="monospace" font-weight="bold">MULTIPAS MuCell</text>

                    <rect x="25%" y="10%" rx="10" ry="10" width="15%" height="12%" :fill="machinedata['Engel-120']" @click="selectmachine('Engel-120')"/>
                    <text fill="#121212" x="29%" y="17%" font-size="9px" font-family="monospace" font-weight="bold">Engel-120</text>

                    <rect x="45%" y="10%" rx="10" ry="10" width="15%" height="12%" :fill="machinedata['Engel-80']" @click="selectmachine('Engel-80')"/>
                    <text fill="#121212" x="49.5%" y="17%" font-size="9px" font-family="monospace" font-weight="bold">Engel-80</text>

                    <rect x="65%" y="10%" rx="10" ry="10" width="15%" height="12%" :fill="machinedata['FCS-MuCell']" @click="selectmachine('FCS-MuCell')" />
                    <text fill="#121212" x="69%" y="17%" font-size="9px" font-family="monospace" font-weight="bold">FCS MuCell</text>

                    <text fill="#121212" x="2%" y="54%" font-size="12px" font-family="monospace" font-weight="bold">106 Factory</text>
                    <rect x="5%" y="56%" width="0.5%" height="39%" fill="rgba(227,118,18,0.4)" />
                    <text fill="#121212" x="2%" y="64%" font-size="12px" font-family="monospace" font-weight="bold">T</text>
                    <text fill="#121212" x="2%" y="68%" font-size="12px" font-family="monospace" font-weight="bold">V</text>
                    <text fill="#121212" x="2%" y="76%" font-size="12px" font-family="monospace" font-weight="bold">W</text>
                    <text fill="#121212" x="2%" y="80%" font-size="12px" font-family="monospace" font-weight="bold">A</text>
                    <text fill="#121212" x="2%" y="84%" font-size="12px" font-family="monospace" font-weight="bold">L</text>
                    <text fill="#121212" x="2%" y="88%" font-size="12px" font-family="monospace" font-weight="bold">L</text>

                    <line x1="7%" y1="96%" x2="11.5%" y2="96%" stroke="#C5BBB8" stroke-width="4" />
                    <line x1="20%" y1="96%" x2="24.5%" y2="96%" stroke="#C5BBB8" stroke-width="4" />
                    <text fill="#121212" x="12.5%" y="96.5%" font-size="10px" font-family="monospace" font-weight="bold">Entrance</text>

                    <rect x="75%" y="55%" rx="10" ry="10" width="15%" height="12%" :fill="machinedata['TOYO']" @click="selectmachine('TOYO')" />
                    <text fill="#121212" x="81%" y="62%" font-size="9px" font-family="monospace" font-weight="bold" >TOYO</text>
                    <rect x="55%" y="55%" rx="10" ry="10" width="15%" height="12%" :fill="machinedata['FCS-HT-150']"  @click="selectmachine('FCS HT-150')"/>
                    <text fill="#121212" x="59%" y="62%" font-size="9px" font-family="monospace" font-weight="bold" >FCS HT-150</text>
                </svg>
            </div>
        </v-col>
    </v-row>
</template>
  

<style scoped>
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
            "MULTIPAS-MuCell":"rgba(182,182,180,0.6)",
            "Engel-120":"rgba(182,182,180,0.6)",
            "Engel-80":"rgba(182,182,180,0.6)",
            "FCS-MuCell":"rgba(182,182,180,0.6)",
            "TOYO":"rgba(182,182,180,0.6)",
            "FCS-HT-150":"rgba(182,182,180,0.6)",
        },
        offlinecolor:"rgba(182,182,180,0.6)",
        onlinecolor:"rgba(76,175,80,0.6)"

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
                    "MULTIPAS-MuCell":"rgba(182,182,180,0.6)",
                    "Engel-120":"rgba(182,182,180,0.6)",
                    "Engel-80":"rgba(182,182,180,0.6)",
                    "FCS-MuCell":"rgba(182,182,180,0.6)",
                    "TOYO":"rgba(182,182,180,0.6)",
                    "FCS-HT-150":"rgba(182,182,180,0.6)",
                }
            }
            else{
                var res = response.data.Data;
                Object.keys(res).forEach(key => {
                    if (res[key] == 'Offline'){
                        this.machinedata[key] =  this.offlinecolor;
                    }
                    else{
                        this.machinedata[key] =  this.onlinecolor;
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
