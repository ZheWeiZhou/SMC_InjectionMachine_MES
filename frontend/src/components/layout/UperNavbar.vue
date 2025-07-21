<template>
<v-app-bar color="primary" dark>
    <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    <v-app-bar-title>SMC Injection Machine Monitor System</v-app-bar-title>
    <v-spacer></v-spacer>
    <v-btn to="/" text>Home</v-btn>
</v-app-bar>
<v-navigation-drawer 
        class="bg-blue-grey-lighten-5"
        v-model="drawer"
        :location="$vuetify.display.mobile ? 'bottom' : undefined"
        temporary>
  <v-list nav dense shaped>
    <v-list-item-group >
      <v-list-item  link :to="{ name: 'HistoryDashboard'}">
        <v-list-item-title class="text-subtitle-1"  >HistoryData</v-list-item-title>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</v-navigation-drawer>
</template>
<script>

    export default {
      name: 'UperNavbar',
      data: () => ({
          account:'',
          password:'',
          error_message:'',
          drawer: false,
      }),
      methods: {
  }
    }
</script>