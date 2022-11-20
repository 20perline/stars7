<script setup>
import { reactive } from "vue";
import store from "@/store/index";

const drawer = reactive({
  state: false,
  items: [],
});

const toggle = function () {
  drawer.state = !drawer.state;
};
</script>

<template>
  <v-app-bar :elevation="2" height="50px" class="bg-light-green-lighten-2">
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="toggle"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title class="text-body-2">
      {{ store.num > 0 ? "第 " + store.num + " 期" : "Stars7" }}
    </v-app-bar-title>
  </v-app-bar>

  <v-navigation-drawer
    v-model="drawer.state"
    location="start"
    temporary
    width="100"
  >
    <v-list lines="one">
      <v-list-item
        v-for="item in drawer.items"
        :key="item"
        :title="item"
        :to="'/album/' + item"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped></style>
