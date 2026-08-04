<template>
  <n-modal :show="visible" :mask-closable="false" @update:show="(v: boolean) => !v && $emit('close')">
    <n-card
      style="width: 600px"
      :title="user ? $t('admin.editUser') : $t('admin.createUser')"
      :bordered="false"
      size="huge"
      role="dialog"
      closable
      @close="$emit('close')"
    >
      <n-form ref="formRef" :model="formData" :rules="rules" label-placement="left" label-width="100">
        <n-form-item :label="$t('userForm.username')" path="username">
          <n-input v-model:value="formData.username" :placeholder="$t('userForm.username')" />
        </n-form-item>
        <n-form-item :label="$t('userForm.password')" path="password">
          <n-input v-model:value="formData.password" type="password" :placeholder="user ? $t('userForm.passwordPlaceholder') : $t('userForm.passwordCreatePlaceholder')" />
        </n-form-item>
        <n-form-item :label="$t('userForm.role')" path="role_id">
          <n-select
            v-model:value="formData.role_id"
            :options="roleOptions"
            :placeholder="$t('userForm.rolePlaceholder')"
            clearable
          />
        </n-form-item>
        <n-form-item :label="$t('userForm.odooApiKey')" path="odoo_api_key">
          <n-input v-model:value="formData.odoo_api_key" type="password" :placeholder="$t('userForm.odooApiKeyPlaceholder')" />
        </n-form-item>
        <n-form-item :label="$t('userForm.admin')" path="is_admin">
          <n-switch v-model:value="formData.is_admin" />
        </n-form-item>
        <n-form-item :label="$t('userForm.active')" path="is_active">
          <n-switch v-model:value="formData.is_active" />
        </n-form-item>
      </n-form>

      <template #footer>
        <div class="flex justify-end gap-2">
          <n-button @click="$emit('close')">{{ $t('userForm.cancel') }}</n-button>
          <n-button type="primary" :loading="saving" @click="handleSubmit">{{ $t('userForm.save') }}</n-button>
        </div>
      </template>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from "vue";
import { useI18n } from "vue-i18n";
import {
  NModal,
  NCard,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NSwitch,
  NButton,
  type FormInst,
  type FormRules,
} from "naive-ui";
import type { AdminUser, AdminRole, AdminUserCreate, AdminUserUpdate } from "@/types/admin";

const { t } = useI18n();

const props = defineProps<{
  visible: boolean;
  user: AdminUser | null;
  roles: AdminRole[];
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "save", data: AdminUserCreate | AdminUserUpdate): void;
}>();

const formRef = ref<FormInst | null>(null);
const saving = ref(false);

const roleOptions = computed(() =>
  props.roles.map((r) => ({ label: r.name, value: r.id })),
);

const formData = reactive({
  username: "",
  password: "",
  role_id: null as number | null,
  odoo_api_key: "" as string | null,
  is_admin: false,
  is_active: true,
});

const rules: FormRules = {
  username: [{ required: true, message: t("validation.usernameRequired") }],
};

watch(
  () => props.user,
  (u) => {
    if (u) {
      formData.username = u.username;
      formData.password = "";
      formData.role_id = u.role_id;
      formData.odoo_api_key = null;
      formData.is_admin = u.is_admin;
      formData.is_active = u.is_active;
    } else {
      formData.username = "";
      formData.password = "";
      formData.role_id = null;
      formData.odoo_api_key = null;
      formData.is_admin = false;
      formData.is_active = true;
    }
  },
  { immediate: true },
);

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  saving.value = true;
  const data: AdminUserCreate | AdminUserUpdate = {
    username: formData.username,
    role_id: formData.role_id,
    is_admin: formData.is_admin,
    is_active: formData.is_active,
  };

  if (!props.user) {
    (data as AdminUserCreate).password = formData.password;
    if (formData.odoo_api_key) (data as AdminUserCreate).odoo_api_key = formData.odoo_api_key;
  } else {
    if (formData.password) (data as AdminUserUpdate).password = formData.password;
    if (formData.odoo_api_key !== null) (data as AdminUserUpdate).odoo_api_key = formData.odoo_api_key;
  }

  emit("save", data);
  saving.value = false;
}
</script>
