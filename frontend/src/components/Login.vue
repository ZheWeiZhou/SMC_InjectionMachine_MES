<template>
    <div class="login-background fill-height">
    <v-container class="fill-height">
        <v-card class = "login-card">
            <v-card-title class = "text-h4 text-center text-white font-weight-bold"> SMC Injection Machine Monitor System</v-card-title>
            <v-card-text>
                <v-row style="margin-top: 8%; margin-left: 10%; width: 80%;">
                    <v-text-field label="Account" v-model="account"></v-text-field>
                </v-row>
                <v-row style="margin-top: 5%; margin-left: 10%; width: 80%;">
                    <v-text-field label="Password" type="password" v-model="password"></v-text-field>
                </v-row>
                <v-row>
                <v-btn size="large" @click="login" style="margin-top: 5%; margin-left: 12%; background: rgba(59,181,229,0.5); width: 76%;">Login</v-btn>
                </v-row>              
            </v-card-text>
            <v-card-actions>
                <v-alert class="login-alert text-error text-center font-weight-bold" :text=error_message></v-alert>
            </v-card-actions>
        </v-card>

    </v-container>
    </div>
  </template>
  

<style scoped>
    .login-background {
        position: relative;
        background: linear-gradient(to bottom, #349cc4,#47c7d8,#3173b0);
        min-height: 100vh;
    }
    .login-card {
        position: absolute; 
        top: 50%;           
        left: 50%;         
        transform: translate(-50%, -50%); 
        background: rgba(247,208,201,0.5);
        min-height: 60vh;
        min-width: 40%;
    }
    .login-alert{
        background: rgba(247,208,201,0);
        margin-top: 2%;
        font-size: 18px;
    }
</style>
  <script>
  import axios from 'axios';
  export default {
    name: 'LoginPage',
  
    data: () => ({
        account:'',
        password:'',
        error_message:''
    }),
    methods: {
    login() {

    if (this.account === '' || this.password === '') {
        this.error_message = '請輸入帳號與密碼';
    } 
    else {
        var requestbody = {"useraccount":this.account,"userpassword":this.password}
        axios.post(`${this.$store.getters.getHost}/smc/injectionmachinemes/user/login`,requestbody)
        .then( (response) => {
        if (response.data.status=='error'){
            this.error_message = '登入失敗';
        }
        else{
            var token = response.data.Data.token;
            this.$cookies.set('accesstoken', token, '1d');
            this.$router.push({ name: 'MachineOverview' });
        }
      })
    }
  }
}
  }
</script>