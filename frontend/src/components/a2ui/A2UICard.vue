<template>
  <div class="a2ui-card">
    <A2UINode v-if="node.children.length > 0" :node="node.children[0]" />
  </div>
</template>

<script setup lang="ts">
import type { RenderNode } from "@/types/a2ui";
import A2UINode from "./A2UINode.vue";
defineProps<{ node: RenderNode }>();
</script>

<style scoped>
.a2ui-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  transition: all 0.2s ease;
  margin-bottom: 0.5rem;
}
.a2ui-card:hover {
  border-color: #93c5fd;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
</style>
