<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold m-0">{{ $t('admin.userManagement') }}</h2>
      <n-button type="primary" @click="showCreateModal = true">
        <template #icon><n-icon><AddOutline /></n-icon></template>
        {{ $t('admin.createUser') }}
      </n-button>
    </div>

    <UserTable
      :users="users"
      :loading="loading"
      @edit="handleEdit"
      @toggle-active="handleToggleActive"
      @refresh="fetchUsers"
    />

    <UserFormModal
      :visible="showCreateModal"
      :user="editingUser"
      :roles="roles"
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
import UserTable from "@/components/admin/UserTable.vue";
import UserFormModal from "@/components/admin/UserFormModal.vue";
import { getUsersApi, createUserApi, updateUserApi, toggleUserActiveApi } from "@/api/admin";
import { getRolesApi } from "@/api/admin";
import type { AdminUser, AdminUserCreate, AdminUserUpdate, AdminRole } from "@/types/admin";

const { t } = useI18n();
const message = useMessage();
const users = ref<AdminUser[]>([]);
const roles = ref<AdminRole[]>([]);
const loading = ref(false);
const showCreateModal = ref(false);
const editingUser = ref<AdminUser | null>(null);

onMounted(() => {
  fetchUsers();
  fetchRoles();
});

async function fetchUsers() {
  loading.value = true;
  try {
    const resp = await getUsersApi();
    if (resp.code === 0) users.value = resp.data;
  } finally {
    loading.value = false;
  }
}

async function fetchRoles() {
  const resp = await getRolesApi();
  if (resp.code === 0) roles.value = resp.data;
}

function handleEdit(user: AdminUser) {
  editingUser.value = user;
  showCreateModal.value = true;
}

async function handleToggleActive(userId: number) {
  const resp = await toggleUserActiveApi(userId);
  if (resp.code === 0) {
    message.success(t("admin.statusUpdated"));
    fetchUsers();
  }
}

function closeModal() {
  showCreateModal.value = false;
  editingUser.value = null;
}

async function handleSave(data: AdminUserCreate | AdminUserUpdate) {
  if (editingUser.value) {
    const resp = await updateUserApi(editingUser.value.id, data as AdminUserUpdate);
    if (resp.code === 0) {
      message.success(t("admin.userUpdated"));
      closeModal();
      fetchUsers();
    }
  } else {
    const resp = await createUserApi(data as AdminUserCreate);
    if (resp.code === 0) {
      message.success(t("admin.userCreated"));
      closeModal();
      fetchUsers();
    }
  }
}
</script>
