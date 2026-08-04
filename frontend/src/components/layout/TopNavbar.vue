<template>
  <header class="topnav">
    <div class="topnav-left">
      <div class="logo-icon">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
          <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
        </svg>
      </div>
      <span class="logo-text">A2UI <span class="logo-accent">Chat</span></span>
    </div>

    <div class="topnav-center">
      <router-link to="/chat" class="nav-link active">{{ $t('nav.chat') }}</router-link>
      <router-link v-if="authStore.isAdmin" to="/admin" class="nav-link">{{ $t('nav.admin') }}</router-link>
    </div>

    <div class="topnav-right">
      <LanguageSwitcher />
      <span v-if="authStore.isAdmin" class="admin-badge">{{ $t('nav.adminBadge') }}</span>
      <span class="username">{{ authStore.user?.username || $t('nav.defaultUser') }}</span>
      <div class="user-avatar">
        {{ (authStore.user?.username || 'U')[0].toUpperCase() }}
      </div>
      <button class="logout-btn" :title="$t('nav.logout')" @click="handleLogout()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuth } from "@/composables/useAuth";
import LanguageSwitcher from "@/components/common/LanguageSwitcher.vue";

const { authStore, handleLogout } = useAuth();
</script>

<style scoped>
.topnav {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
  gap: 1rem;
}

.topnav-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.logo-icon {
  width: 30px; height: 30px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #2563eb, #0d9488);
}
.logo-text {
  font-family: 'Outfit', system-ui, sans-serif;
  font-weight: 700;
  font-size: 1.05rem;
  color: #1e293b;
  letter-spacing: -0.01em;
}
.logo-accent {
  color: #0d9488;
}

.topnav-center {
  flex: 1;
  display: flex;
  gap: 2px;
}
.nav-link {
  padding: 0.35rem 0.85rem;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  transition: all 0.15s;
}
.nav-link:hover {
  background: #f8fafc;
  color: #1e293b;
}
.nav-link.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
}

.topnav-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.admin-badge {
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
  background: #ede9fe;
  color: #5b21b6;
  font-family: 'Outfit', system-ui, sans-serif;
}
.username {
  font-size: 0.8125rem;
  color: #64748b;
}
.user-avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Outfit', system-ui, sans-serif;
  font-weight: 700;
  font-size: 0.75rem;
  color: white;
  background: linear-gradient(135deg, #f97316, #f59e0b);
}
.logout-btn {
  background: none; border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  min-width: 32px; min-height: 32px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.logout-btn:hover {
  color: #ef4444;
  background: #fef2f2;
}
</style>
