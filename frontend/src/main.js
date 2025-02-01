import "./assets/main.css";
import "./assets/editor.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Vue3Toastify from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const app = createApp(App);

app.use(Vue3Toastify, {
  autoClose: 2500,
});

app.use(router);

app.mount("#app");
