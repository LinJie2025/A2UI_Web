<template>
  <div class="a2ui-stagger" :style="{ '--stagger-i': staggerIndex }">
    <component :is="componentMap[node.component]" :node="node">
      <template v-if="!componentMap[node.component]">
        <span class="unknown-component">[{{ node.component }}]</span>
      </template>
    </component>
  </div>
</template>

<script setup lang="ts">
import { computed, inject, type Component } from "vue";
import type { RenderNode } from "@/types/a2ui";
import A2UIText from "./A2UIText.vue";
import A2UIIcon from "./A2UIIcon.vue";
import A2UIColumn from "./A2UIColumn.vue";
import A2UIRow from "./A2UIRow.vue";
import A2UICard from "./A2UICard.vue";
import A2UIDivider from "./A2UIDivider.vue";
import A2UIList from "./A2UIList.vue";
import A2UIButton from "./A2UIButton.vue";
import A2UITextField from "./A2UITextField.vue";

defineProps<{
  node: RenderNode;
}>();

// ── Stagger index (depth-first, each node gets a unique index) ──────────
const getStaggerIndex = inject<() => number>("a2uiStaggerIndex", () => 0);
const staggerIndex = getStaggerIndex();

const componentMap: Record<string, Component> = {
  Text: A2UIText,
  Icon: A2UIIcon,
  Column: A2UIColumn,
  Row: A2UIRow,
  Card: A2UICard,
  Divider: A2UIDivider,
  List: A2UIList,
  Button: A2UIButton,
  TextField: A2UITextField,
};
</script>

<style scoped>
.a2ui-stagger {
  animation: a2uiFadeSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
  animation-delay: calc(var(--stagger-i, 0) * 60ms);
}
@keyframes a2uiFadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.unknown-component {
  font-size: 0.75rem;
  color: #94a3b8;
}
</style>
