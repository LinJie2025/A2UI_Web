<template>
  <n-modal :show="visible" :mask-closable="false" @update:show="(v: boolean) => !v && $emit('close')">
    <n-card
      style="width: 600px"
      :title="role ? $t('admin.editRole') : $t('admin.createRole')"
      :bordered="false"
      size="huge"
      role="dialog"
      closable
      @close="$emit('close')"
    >
      <n-form ref="formRef" :model="formData" :rules="rules" label-placement="left" label-width="100">
        <n-form-item :label="$t('roleForm.name')" path="name">
          <n-input v-model:value="formData.name" :placeholder="$t('roleForm.namePlaceholder')" />
        </n-form-item>
        <n-form-item :label="$t('roleForm.description')" path="description">
          <n-input v-model:value="formData.description" :placeholder="$t('roleForm.descriptionPlaceholder')" />
        </n-form-item>
        <n-form-item :label="$t('roleForm.toolWhitelist')">
          <ToolCheckboxGroup
            v-model="formData.tool_names"
            :all-tools="allTools"
          />
        </n-form-item>
      </n-form>

      <template #footer>
        <div class="flex justify-end gap-2">
          <n-button @click="$emit('close')">{{ $t('roleForm.cancel') }}</n-button>
          <n-button type="primary" :loading="saving" @click="handleSubmit">{{ $t('roleForm.save') }}</n-button>
        </div>
      </template>
    </n-card>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from "vue";
import { useI18n } from "vue-i18n";
import {
  NModal,
  NCard,
  NForm,
  NFormItem,
  NInput,
  NButton,
  type FormInst,
  type FormRules,
} from "naive-ui";
import ToolCheckboxGroup from "./ToolCheckboxGroup.vue";
import type { AdminRole, AdminRoleCreate, AdminRoleUpdate } from "@/types/admin";

const { t } = useI18n();

const props = defineProps<{
  visible: boolean;
  role: AdminRole | null;
  allTools: string[];
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "save", data: AdminRoleCreate | AdminRoleUpdate): void;
}>();

const formRef = ref<FormInst | null>(null);
const saving = ref(false);

const formData = reactive({
  name: "",
  description: "" as string | null,
  tool_names: [] as string[],
});

const rules: FormRules = {
  name: [{ required: true, message: t("validation.roleNameRequired") }],
};

watch(
  () => props.role,
  (r) => {
    if (r) {
      formData.name = r.name;
      formData.description = r.description;
      formData.tool_names = [...(r.tool_names || [])];
    } else {
      formData.name = "";
      formData.description = null;
      formData.tool_names = [];
    }
  },
  { immediate: true },
);

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  saving.value = true;
  emit("save", {
    name: formData.name,
    description: formData.description,
    tool_names: formData.tool_names,
  });
  saving.value = false;
}
</script>
