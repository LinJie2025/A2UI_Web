import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes: RouteRecordRaw[] = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/LoginView.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("@/views/RegisterView.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/chat",
    name: "Chat",
    component: () => import("@/views/ChatView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    name: "Admin",
    component: () => import("@/views/AdminLayout.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
    redirect: "/admin/users",
    children: [
      {
        path: "users",
        name: "AdminUsers",
        component: () => import("@/views/admin/UserManagement.vue"),
        meta: { requiresAuth: true, requiresAdmin: true },
      },
      {
        path: "roles",
        name: "AdminRoles",
        component: () => import("@/views/admin/RoleManagement.vue"),
        meta: { requiresAuth: true, requiresAdmin: true },
      },
    ],
  },
  {
    path: "/",
    redirect: "/chat",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth === false) {
    // If already logged in, redirect to chat
    if (authStore.isLoggedIn && (to.name === "Login" || to.name === "Register")) {
      next("/chat");
    } else {
      next();
    }
    return;
  }

  if (!authStore.isLoggedIn) {
    next("/login");
    return;
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next("/chat");
    return;
  }

  next();
});

export default router;
