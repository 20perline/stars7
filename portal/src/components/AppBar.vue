<script setup>
import { onMounted, reactive } from "vue";
import http from "@/utils/http";

defineProps({
  title: {
    type: String,
    default: "Star7",
  },
});

const drawer = reactive({
  state: false,
  items: [],
});

onMounted(() => {
  // http.get("/map.json").then((response) => {
  //   drawer.items = response.data.items
  // });
});

const toggle = function () {
  drawer.state = !drawer.state;
};
</script>

<template>
  <!-- <v-card color="grey-lighten-4" flat height="48px" rounded="0"> -->
    <!-- <v-toolbar density="compact"> -->
      <v-app-bar :elevation="2" height="50px" class="bg-light-green-lighten-2">
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click="toggle"></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title>{{ title }}</v-app-bar-title>
      </v-app-bar>
    <!-- </v-toolbar> -->
  <!-- </v-card> -->

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
