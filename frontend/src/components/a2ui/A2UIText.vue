<template>
  <component :is="tag" :class="textClasses">
    {{ displayText }}
  </component>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { RenderNode } from "@/types/a2ui";

const props = defineProps<{ node: RenderNode }>();

const tag = computed(() => {
  const v = props.node.props.variant as string;
  return { h1: "h1", h2: "h2", h3: "h3", caption: "span" }[v] || "p";
});

const textClasses = computed(() => {
  const v = props.node.props.variant as string;
  switch (v) {
    case "h1": return "a2ui-text-h1";
    case "h2": return "a2ui-text-h2";
    case "h3": return "a2ui-text-h3";
    case "caption": return "a2ui-text-caption";
    default: return "a2ui-text-body";
  }
});

const displayText = computed(() => String(props.node.props.text ?? ""));
</script>

<style scoped>
.a2ui-text-h1 {
  font-family: 'Outfit', system-ui, sans-serif;
  font-size: 1.5rem; font-weight: 700;
  color: #1e293b; margin-bottom: 0.5rem; line-height: 1.3;
}
.a2ui-text-h2 {
  font-family: 'Outfit', system-ui, sans-serif;
  font-size: 1.25rem; font-weight: 600;
  color: #1e293b; margin-bottom: 0.25rem; line-height: 1.35;
}
.a2ui-text-h3 {
  font-family: 'Outfit', system-ui, sans-serif;
  font-size: 1.0625rem; font-weight: 600;
  color: #334155; margin-bottom: 0.25rem; line-height: 1.4;
}
.a2ui-text-caption {
  font-size: 0.75rem; color: #94a3b8; line-height: 1.5;
}
.a2ui-text-body {
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  font-size: 0.875rem; color: #475569; line-height: 1.6;
}
</style>
