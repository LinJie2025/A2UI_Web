import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import type { SupportedLocale } from "@/plugins/i18n";
import { SUPPORTED_LOCALES } from "@/plugins/i18n";

export const useLocaleStore = defineStore("locale", () => {
  const { locale } = useI18n({ useScope: "global" });

  const currentLocale = computed(() => locale.value as SupportedLocale);

  const currentLocaleInfo = computed(() =>
    SUPPORTED_LOCALES.find((l) => l.key === currentLocale.value) ?? SUPPORTED_LOCALES[0],
  );

  function setLocale(lang: SupportedLocale) {
    locale.value = lang;
    try {
      localStorage.setItem("locale", lang);
    } catch {
      // localStorage unavailable
    }
  }

  return {
    currentLocale,
    currentLocaleInfo,
    setLocale,
  };
});
