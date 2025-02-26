import { createRouter, createWebHistory } from "vue-router";
import { getAuth } from "firebase/auth"; // Add this import
import Dashboard from "../views/Dashboard.vue";
import ExpensesManagement from "../views/ExpensesManagement.vue";
import Login from "../views/Login.vue";
import { useAuthStore } from "../stores/authStore";
import Register from "../views/Register.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
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

// Agrega protección de rutas
router.beforeEach((to, from, next) => {
  const auth = getAuth();
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  auth.onAuthStateChanged((user) => {
    if (requiresAuth && !user) {
      next("/login");
    } else if (!requiresAuth && user) {
      next("/expenses");
    } else {
      next();
    }
  });
});

export default router;
