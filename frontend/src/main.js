import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import router from "./router";
import "./assets/main.css";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App);
const options = {
  position: "top-right",
  timeout: 2000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
};

app.use(Toast, options);
app.use(createPinia());
app.use(router);
app.mount("#app");
