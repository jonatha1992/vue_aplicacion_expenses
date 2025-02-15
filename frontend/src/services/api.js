import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
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
