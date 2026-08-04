/** vue-i18n initialization */
import { createI18n } from "vue-i18n";
import zhCN from "@/locales/zh-CN";
import zhTW from "@/locales/zh-TW";
import en from "@/locales/en";
import esMX from "@/locales/es-MX";

export type SupportedLocale = "zh-CN" | "zh-TW" | "en" | "es-MX";

export const SUPPORTED_LOCALES: { key: SupportedLocale; label: string; nativeLabel: string }[] = [
  { key: "zh-CN", label: "简体中文", nativeLabel: "简体中文" },
  { key: "zh-TW", label: "繁體中文", nativeLabel: "繁體中文" },
  { key: "en", label: "English", nativeLabel: "English" },
  { key: "es-MX", label: "Español (México)", nativeLabel: "Español (MX)" },
];

function getSavedLocale(): SupportedLocale {
  try {
    const saved = localStorage.getItem("locale");
    if (saved && ["zh-CN", "zh-TW", "en", "es-MX"].includes(saved)) {
      return saved as SupportedLocale;
    }
  } catch {
    // localStorage unavailable
  }
  return "zh-CN";
}

const i18n = createI18n({
  legacy: false,
  locale: getSavedLocale(),
  fallbackLocale: "zh-CN",
  messages: {
    "zh-CN": zhCN,
    "zh-TW": zhTW,
    en,
    "es-MX": esMX,
  },
});

export default i18n;
