import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Dashboard from "../views/Dashboard.vue";
import ExpensesManagement from "../views/ExpensesManagement.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import { useAuthStore } from "../stores/authStore";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { redirectIfAuth: true },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/expenses",
    name: "ExpensesManagement",
    component: ExpensesManagement,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const redirectIfAuth = to.matched.some(
    (record) => record.meta.redirectIfAuth
  );

  if (redirectIfAuth && authStore.isLoggedIn) {
    // Si está autenticado y va al home, redirigir a expenses
    next("/expenses");
  } else if (requiresAuth && !authStore.isLoggedIn) {
    // Si requiere auth y no está autenticado, redirigir a login
    next("/login");
  } else if (
    authStore.isLoggedIn &&
    (to.path === "/login" || to.path === "/register")
  ) {
    // Si está autenticado y va a login/register, redirigir a expenses
    next("/expenses");
  } else {
    next();
  }
});

export default router;
