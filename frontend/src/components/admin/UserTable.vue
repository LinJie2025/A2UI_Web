<template>
  <n-data-table
    :columns="columns"
    :data="users"
    :loading="loading"
    :pagination="false"
    striped
  />
</template>

<script setup lang="ts">
import { h } from "vue";
import { useI18n } from "vue-i18n";
import { NDataTable, NButton, NSwitch, NIcon, NTag } from "naive-ui";
import { PencilOutline } from "@vicons/ionicons5";
import type { DataTableColumns } from "naive-ui";
import type { AdminUser } from "@/types/admin";

const { t } = useI18n();

defineProps<{
  users: AdminUser[];
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: "edit", user: AdminUser): void;
  (e: "toggle-active", userId: number): void;
  (e: "refresh"): void;
}>();

const columns: DataTableColumns<AdminUser> = [
  {
    title: t("userTable.id"),
    key: "id",
    width: 60,
  },
  {
    title: t("userTable.username"),
    key: "username",
  },
  {
    title: t("userTable.role"),
    key: "role_name",
    render(row) {
      return row.role_name
        ? h(NTag, { type: "info", size: "small" }, { default: () => row.role_name })
        : "-";
    },
  },
  {
    title: t("userTable.admin"),
    key: "is_admin",
    width: 80,
    render(row) {
      return h(NTag, { type: row.is_admin ? "success" : "default", size: "small" }, {
        default: () => (row.is_admin ? t("userTable.yes") : t("userTable.no")),
      });
    },
  },
  {
    title: t("userTable.status"),
    key: "is_active",
    width: 80,
    render(row) {
      return h(NSwitch, {
        value: row.is_active,
        onUpdateValue: () => emit("toggle-active", row.id),
      });
    },
  },
  {
    title: t("userTable.createdAt"),
    key: "created_at",
    width: 160,
    render(row) {
      return row.created_at?.slice(0, 19) || "-";
    },
  },
  {
    title: t("userTable.actions"),
    key: "actions",
    width: 80,
    render(row) {
      return h(
        NButton,
        { text: true, type: "primary", onClick: () => emit("edit", row) },
        { icon: () => h(NIcon, null, { default: () => h(PencilOutline) }) },
      );
    },
  },
];
</script>
