import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { UserInfo } from "@/types";
import { loginApi, getMeApi } from "@/api/auth";

const TOKEN_KEY = "a2ui_token";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string>(localStorage.getItem(TOKEN_KEY) || "");
  const user = ref<UserInfo | null>(null);
  const loading = ref(false);

  const isLoggedIn = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.is_admin ?? false);

  function setToken(newToken: string) {
    token.value = newToken;
    localStorage.setItem(TOKEN_KEY, newToken);
  }

  async function login(username: string, password: string): Promise<void> {
    loading.value = true;
    try {
      const resp = await loginApi({ username, password });
      if (resp.code === 0) {
        setToken(resp.data.access_token);
        user.value = resp.data.user;
      } else {
        throw new Error(resp.message);
      }
    } finally {
      loading.value = false;
    }
  }

  async function fetchMe(): Promise<void> {
    if (!token.value) return;
    try {
      const resp = await getMeApi();
      if (resp.code === 0) {
        user.value = resp.data;
      }
    } catch {
      logout();
    }
  }

  function logout() {
    token.value = "";
    user.value = null;
    localStorage.removeItem(TOKEN_KEY);
  }

  return {
    token,
    user,
    loading,
    isLoggedIn,
    isAdmin,
    login,
    fetchMe,
    logout,
    setToken,
  };
});
