<template>
<v-app-bar color="primary" dark>
    <v-app-bar-title>SMC Injection Machine Monitor System</v-app-bar-title>
    <v-spacer></v-spacer>
    <v-btn to="/" text>Home</v-btn>
</v-app-bar>
</template>
    <script>
    export default {
      name: 'UperNavbar',
      data: () => ({
          account:'',
          password:'',
          error_message:''
      }),
      methods: {
  }
    }
  </script>