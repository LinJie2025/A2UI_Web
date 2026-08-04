<template>
  <div class="h-screen flex flex-col">
    <TopNavbar />
    <div class="flex-1 overflow-hidden">
      <n-layout has-sider class="h-full">
        <n-layout-sider bordered width="200">
          <n-menu
            :value="currentRoute"
            :options="menuOptions"
            @update:value="handleMenu"
          />
        </n-layout-sider>
        <n-layout-content class="p-6 overflow-y-auto">
          <router-view />
        </n-layout-content>
      </n-layout>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import {
  NLayout,
  NLayoutSider,
  NLayoutContent,
  NMenu,
  NIcon,
  type MenuOption,
} from "naive-ui";
import { PeopleOutline, ShieldCheckmarkOutline } from "@vicons/ionicons5";
import TopNavbar from "@/components/layout/TopNavbar.vue";

const router = useRouter();
const route = useRoute();
const { t } = useI18n();

const currentRoute = computed(() => route.path);

const menuOptions = computed<MenuOption[]>(() => [
  {
    label: t("admin.userManagement"),
    key: "/admin/users",
    icon: () => h(NIcon, null, { default: () => h(PeopleOutline) }),
  },
  {
    label: t("admin.roleManagement"),
    key: "/admin/roles",
    icon: () => h(NIcon, null, { default: () => h(ShieldCheckmarkOutline) }),
  },
]);

function handleMenu(key: string) {
  router.push(key);
}
</script>
