<template>
  <n-config-provider :locale="naiveLocale" :theme="null">
    <n-message-provider>
      <n-notification-provider>
        <router-view />
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useLocaleStore } from "@/stores/locale";
import { zhCN, enUS, zhTW, esAR, NConfigProvider, NMessageProvider, NNotificationProvider } from "naive-ui";

const localeStore = useLocaleStore();

const localeMap: Record<string, typeof zhCN> = {
  "zh-CN": zhCN,
  "zh-TW": zhTW,
  en: enUS,
  "es-MX": esAR,
};

const naiveLocale = computed(() => localeMap[localeStore.currentLocale] ?? zhCN);
</script>
