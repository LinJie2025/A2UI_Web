import axios, { type AxiosInstance, type AxiosError } from "axios";
import { useAuthStore } from "@/stores/auth";

const client: AxiosInstance = axios.create({
  baseURL: "/api",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor — inject JWT Bearer token
client.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response interceptor — handle 401 redirect to login
client.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export default client;
