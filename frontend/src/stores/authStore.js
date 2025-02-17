import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    getToken: (state) => state.token,
  },
  actions: {
    setUser(user, token) {
      this.user = user;
      this.token = token;
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
    initializeAuth() {
      const token = localStorage.getItem("token");
      const userStr = localStorage.getItem("user");
      // Verificar que existan valores antes de asignar
      if (token && userStr) {
        try {
          const user = JSON.parse(userStr);
          this.user = user;
          this.token = token;
        } catch (error) {
          console.error("Error parsing user data from localStorage");
          this.logout(); // Limpiar datos inválidos
        }
      }
    },
  },
});
