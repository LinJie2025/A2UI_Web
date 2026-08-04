<template>
  <div class="lang-switcher">
    <button class="lang-btn" @click="open = !open" :title="$t('language.switchTo')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/>
      </svg>
      <span class="lang-label">{{ localeStore.currentLocaleInfo.nativeLabel }}</span>
      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="6 9 12 15 18 9"/></svg>
    </button>

    <Transition name="dropdown">
      <div v-if="open" class="lang-dropdown">
        <button
          v-for="l in locales"
          :key="l.key"
          :class="['lang-option', { active: l.key === localeStore.currentLocale }]"
          @click="switchTo(l.key)"
        >
          <span class="lang-native">{{ l.nativeLabel }}</span>
          <span class="lang-en">{{ l.label }}</span>
          <svg v-if="l.key === localeStore.currentLocale" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useLocaleStore } from "@/stores/locale";
import { SUPPORTED_LOCALES, type SupportedLocale } from "@/plugins/i18n";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const localeStore = useLocaleStore();
const open = ref(false);
const locales = SUPPORTED_LOCALES;

function switchTo(lang: SupportedLocale) {
  localeStore.setLocale(lang);
  open.value = false;
}

function closeOnClickOutside(e: MouseEvent) {
  const target = e.target as HTMLElement;
  if (!target.closest(".lang-switcher")) {
    open.value = false;
  }
}

onMounted(() => document.addEventListener("click", closeOnClickOutside));
onUnmounted(() => document.removeEventListener("click", closeOnClickOutside));
</script>

<style scoped>
.lang-switcher {
  position: relative;
}

.lang-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.3rem 0.55rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  color: #475569;
  font-size: 0.75rem;
  font-weight: 500;
  font-family: 'Outfit', system-ui, sans-serif;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.lang-btn:hover {
  border-color: #cbd5e1;
  background: #fff;
  color: #1e293b;
}

.lang-label {
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.lang-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  min-width: 220px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04);
  padding: 0.375rem;
  z-index: 100;
}

.lang-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #475569;
  font-size: 0.8125rem;
  cursor: pointer;
  text-align: left;
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  transition: all 0.1s;
}
.lang-option:hover {
  background: #f8fafc;
  color: #1e293b;
}
.lang-option.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
}

.lang-native {
  flex: 1;
}
.lang-en {
  font-size: 0.7rem;
  color: #94a3b8;
}
.lang-option.active .lang-en {
  color: #60a5fa;
}

/* Transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.15s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
