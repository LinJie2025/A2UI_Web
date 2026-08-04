<template>
  <div class="flex flex-col gap-2">
    <A2UINode
      v-for="child in node.children"
      :key="child.id"
      :node="child"
    />
  </div>
</template>

<script setup lang="ts">
import type { RenderNode } from "@/types/a2ui";
import A2UINode from "./A2UINode.vue";

defineProps<{
  node: RenderNode;
}>();
</script>
