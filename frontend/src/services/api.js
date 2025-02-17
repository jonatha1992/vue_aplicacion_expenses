import axios from "axios";
import { useAuthStore } from "../stores/authStore.js";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para agregar el token a todas las peticiones
api.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  const token = authStore.getToken;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

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
