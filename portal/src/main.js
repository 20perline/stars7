import { createApp } from "vue";
import Toast from "vue-toastification";
import App from "./App.vue";
import router from "./router";

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import "vue-toastification/dist/index.css";
import "./assets/main.css";

const vuetify = createVuetify({
  components,
  directives,
})


const app = createApp(App);

app.use(router);
app.use(vuetify);
app.use(Toast, {
  maxToasts: 2,
  timeout: 2000,
  hideProgressBar: true,
  toastClassName: 'app-toast',
  bodyClassName: "app-toast-body",
});

app.mount("#app");
