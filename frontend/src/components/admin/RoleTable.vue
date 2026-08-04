<template>
  <n-data-table
    :columns="columns"
    :data="roles"
    :loading="loading"
    :pagination="false"
    striped
  />
</template>

<script setup lang="ts">
import { h } from "vue";
import { useI18n } from "vue-i18n";
import { NDataTable, NButton, NIcon, NTag, useMessage } from "naive-ui";
import { PencilOutline, TrashOutline } from "@vicons/ionicons5";
import type { DataTableColumns } from "naive-ui";
import type { AdminRole } from "@/types/admin";

const { t } = useI18n();

defineProps<{
  roles: AdminRole[];
  loading: boolean;
}>();

const emit = defineEmits<{
  (e: "edit", role: AdminRole): void;
  (e: "delete", roleId: number): void;
  (e: "refresh"): void;
}>();

const columns: DataTableColumns<AdminRole> = [
  {
    title: t("roleTable.id"),
    key: "id",
    width: 60,
  },
  {
    title: t("roleTable.name"),
    key: "name",
  },
  {
    title: t("roleTable.description"),
    key: "description",
    render(row) {
      return row.description || "-";
    },
  },
  {
    title: t("roleTable.whitelistTools"),
    key: "tool_names",
    render(row) {
      if (!row.tool_names || row.tool_names.length === 0) {
        return h(NTag, { type: "warning", size: "small" }, { default: () => t("roleTable.noTools") });
      }
      return h(
        "div",
        { class: "flex flex-wrap gap-1" },
        row.tool_names.map((name) =>
          h(NTag, { type: "info", size: "small" }, { default: () => name }),
        ),
      );
    },
  },
  {
    title: t("roleTable.createdAt"),
    key: "created_at",
    width: 160,
    render(row) {
      return row.created_at?.slice(0, 19) || "-";
    },
  },
  {
    title: t("roleTable.actions"),
    key: "actions",
    width: 120,
    render(row) {
      return h("div", { class: "flex gap-1" }, [
        h(
          NButton,
          { text: true, type: "primary", onClick: () => emit("edit", row) },
          { icon: () => h(NIcon, null, { default: () => h(PencilOutline) }) },
        ),
        h(
          NButton,
          { text: true, type: "error", onClick: () => emit("delete", row.id) },
          { icon: () => h(NIcon, null, { default: () => h(TrashOutline) }) },
        ),
      ]);
    },
  },
];
</script>
