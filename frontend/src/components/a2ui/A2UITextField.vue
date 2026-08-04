<template>
  <div class="mb-2">
    <label class="block text-xs font-medium text-gray-600 mb-1">
      {{ displayLabel }}
    </label>
    <n-input
      v-model:value="inputValue"
      size="small"
      :placeholder="displayLabel"
      @update:value="onInput"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, inject, ref, watch } from "vue";
import { NInput } from "naive-ui";
import type { RenderNode } from "@/types/a2ui";

const props = defineProps<{
  node: RenderNode;
}>();

// ── Surface data store (provided by A2UIRenderer) ─────────────────────────
const surfaceData = inject<Record<string, Record<string, unknown>>>("a2uiSurfaceData", {});

// Determine which surface this component belongs to (from data bindings)
const surfaceId = computed(() => {
  // Use the first available surface ID
  const keys = Object.keys(surfaceData);
  return keys.length > 0 ? keys[0] : "main";
});

// The data path for this field (from the original component def)
const dataPath = computed(() => {
  const value = props.node.props.value;
  if (value && typeof value === "object" && "path" in value) {
    return String((value as { path: string }).path);
  }
  // Fallback: use the node id as the data key
  return props.node.id;
});

// Extract just the field key from the path (e.g., "/form/name" → "name")
const fieldKey = computed(() => {
  const parts = dataPath.value.split("/");
  return parts[parts.length - 1] || dataPath.value;
});

const displayLabel = computed(() => {
  const label = props.node.props.label;
  return label !== null && label !== undefined ? String(label) : "";
});

const initialValue = computed(() => {
  const val = props.node.props.value;
  return val !== null && val !== undefined ? String(val) : "";
});

const inputValue = ref(initialValue.value);

// Sync if data changes externally
watch(initialValue, (newVal) => {
  inputValue.value = newVal;
});

// Write value to surface data store on input
function onInput(value: string) {
  if (surfaceData[surfaceId.value]) {
    surfaceData[surfaceId.value][fieldKey.value] = value;
  }
}
</script>
