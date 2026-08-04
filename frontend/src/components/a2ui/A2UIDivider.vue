<template>
  <hr class="a2ui-divider" />
</template>

<script setup lang="ts">
import type { RenderNode } from "@/types/a2ui";
defineProps<{ node: RenderNode }>();
</script>

<style scoped>
.a2ui-divider {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 0.75rem 0;
}
</style>
