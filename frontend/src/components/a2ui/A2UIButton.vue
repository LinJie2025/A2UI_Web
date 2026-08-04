<template>
  <n-button
    :type="buttonType"
    :text="isBorderless"
    :loading="loading"
    :disabled="isReadonly"
    size="small"
    @click="handleClick"
  >
    {{ displayText }}
  </n-button>
</template>

<script setup lang="ts">
import { computed, inject, ref } from "vue";
import { NButton, useNotification } from "naive-ui";
import type { RenderNode } from "@/types/a2ui";

const props = defineProps<{
  node: RenderNode;
}>();

const notification = useNotification();
const loading = ref(false);

// ── Surface data store & action handler (provided by A2UIRenderer) ────────
const surfaceData = inject<Record<string, Record<string, unknown>>>("a2uiSurfaceData", {});
const handleA2UIAction = inject<(action: string, surfaceId: string) => void>("a2uiHandleAction", () => {});
const a2uiReadonly = inject<{ value: boolean }>("a2uiReadonly", { value: false });

const isReadonly = computed(() => a2uiReadonly.value);

const buttonType = computed(() => {
  const variant = props.node.props.variant as string;
  return variant === "primary" ? "primary" : "default";
});

const isBorderless = computed(() => {
  return props.node.props.variant === "borderless";
});

const displayText = computed(() => {
  const text = props.node.props.text;
  if (text === null || text === undefined) return "Button";
  return String(text);
});

const surfaceId = computed(() => {
  const keys = Object.keys(surfaceData);
  return keys.length > 0 ? keys[0] : "main";
});

const actionName = computed(() => {
  const action = props.node.props.action as { name?: string } | undefined;
  return action?.name || "unknown_action";
});

function handleClick() {
  if (isReadonly.value) return;
  loading.value = true;

  // Collect data from this surface
  const data = surfaceData[surfaceId.value] ? { ...surfaceData[surfaceId.value] } : {};

  // Call the provided action handler
  handleA2UIAction(actionName.value, surfaceId.value);

  notification.info({
    content: `Action: ${actionName.value} — sending to server...`,
    duration: 2000,
  });

  setTimeout(() => {
    loading.value = false;
  }, 800);
}
</script>
