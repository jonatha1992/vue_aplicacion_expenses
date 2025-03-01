import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Dashboard from "../views/Dashboard.vue";
import ExpensesManagement from "../views/ExpensesManagement.vue";
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
  // Eliminamos las rutas de login y register ya que usaremos modales
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

  if (requiresAuth && !authStore.isLoggedIn) {
    // Si requiere autenticación y no está autenticado, permanece en la ruta actual
    // y el modal se mostrará automáticamente
    next(false);
  } else if (redirectIfAuth && authStore.isLoggedIn) {
    next("/expenses");
  } else {
    next();
  }
});

export default router;
