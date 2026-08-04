<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold m-0">{{ $t('admin.roleManagement') }}</h2>
      <n-button type="primary" @click="showCreateModal = true">
        <template #icon><n-icon><AddOutline /></n-icon></template>
        {{ $t('admin.createRole') }}
      </n-button>
    </div>

    <RoleTable
      :roles="roles"
      :loading="loading"
      @edit="handleEdit"
      @delete="handleDelete"
      @refresh="fetchRoles"
    />

    <RoleFormModal
      :visible="showCreateModal"
      :role="editingRole"
      :all-tools="allTools"
      @close="closeModal"
      @save="handleSave"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { NButton, NIcon, useMessage } from "naive-ui";
import { AddOutline } from "@vicons/ionicons5";
import RoleTable from "@/components/admin/RoleTable.vue";
import RoleFormModal from "@/components/admin/RoleFormModal.vue";
import {
  getRolesApi,
  createRoleApi,
  updateRoleApi,
  deleteRoleApi,
} from "@/api/admin";
import client from "@/api/client";
import type { AdminRole, AdminRoleCreate, AdminRoleUpdate } from "@/types/admin";
import type { ApiResponse } from "@/types";

const { t } = useI18n();
const message = useMessage();
const roles = ref<AdminRole[]>([]);
const allTools = ref<string[]>([]);
const loading = ref(false);
const showCreateModal = ref(false);
const editingRole = ref<AdminRole | null>(null);

onMounted(() => {
  fetchRoles();
  fetchTools();
});

async function fetchRoles() {
  loading.value = true;
  try {
    const resp = await getRolesApi();
    if (resp.code === 0) roles.value = resp.data;
  } finally {
    loading.value = false;
  }
}

async function fetchTools() {
  try {
    const resp = await client.get<ApiResponse<{ tools: { name: string }[] }>>("/tools");
    if (resp.data.code === 0) {
      allTools.value = resp.data.data.tools.map((t) => t.name);
    }
  } catch {
    allTools.value = [];
  }
}

function handleEdit(role: AdminRole) {
  editingRole.value = role;
  showCreateModal.value = true;
}

async function handleDelete(roleId: number) {
  const resp = await deleteRoleApi(roleId);
  if (resp.code === 0) {
    message.success(t("admin.roleDeleted"));
    fetchRoles();
  }
}

function closeModal() {
  showCreateModal.value = false;
  editingRole.value = null;
}

async function handleSave(data: AdminRoleCreate | AdminRoleUpdate) {
  if (editingRole.value) {
    const resp = await updateRoleApi(editingRole.value.id, data as AdminRoleUpdate);
    if (resp.code === 0) {
      message.success(t("admin.roleUpdated"));
      closeModal();
      fetchRoles();
    }
  } else {
    const resp = await createRoleApi(data as AdminRoleCreate);
    if (resp.code === 0) {
      message.success(t("admin.roleCreated"));
      closeModal();
      fetchRoles();
    }
  }
}
</script>
