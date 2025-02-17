import { defineStore } from "pinia";
import { categoryApi } from "../services/api"; // Asegúrate de tener categoryApi implementado

export const useCategoryStore = defineStore("category", {
  state: () => ({
    categories: [],
  }),
  actions: {
    async fetchCategories() {
      try {
        const response = await categoryApi.getAll();
        this.categories = response.data;
      } catch (e) {
        console.error("Error fetching categories", e);
      }
    },
  },
});
