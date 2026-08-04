import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { onMounted } from "vue";

/**
 * Composable for authentication-related logic.
 * Initializes user state on mount and provides login/logout helpers.
 */
export function useAuth() {
  const authStore = useAuthStore();
  const router = useRouter();

  /** Fetch current user on mount if token exists. */
  onMounted(async () => {
    if (authStore.isLoggedIn && !authStore.user) {
      await authStore.fetchMe();
    }
  });

  /** Login and redirect to chat. */
  async function handleLogin(username: string, password: string): Promise<string | null> {
    try {
      await authStore.login(username, password);
      router.push("/chat");
      return null;
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: { message?: string } } }; message?: string };
      return (
        err?.response?.data?.detail?.message ||
        (err instanceof Error ? err.message : "Login failed")
      );
    }
  }

  /** Logout and redirect to login. */
  function handleLogout() {
    authStore.logout();
    router.push("/login");
  }

  return {
    authStore,
    handleLogin,
    handleLogout,
  };
}
