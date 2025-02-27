import { createAPI } from "./apiConfig";
import { useAuthStore } from "../stores/authStore.js";

const api = createAPI();

// Interceptor para agregar el token a todas las peticiones
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

export const expenseApi = {
  getAll: () => api.get("/expenses/"),
  create: (expense) => api.post("/expenses/", expense),
  update: (id, expense) => api.put(`/expenses/${id}/`, expense),
  delete: (id) => api.delete(`/expenses/${id}/`),
  getById: (id) => api.get(`/expenses/${id}/`),
};

export const categoryApi = {
  getAll: () => api.get("/categories/"),
  getById: (id) => api.get(`/categories/${id}/`),
};
