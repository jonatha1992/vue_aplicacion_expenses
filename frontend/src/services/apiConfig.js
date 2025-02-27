import axios from "axios";

export const createAPI = () => {
  return axios.create({
    baseURL:
      "https://expenses-backend-396367934349.us-central1.run.app" ||
      "http://localhost:8080",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
