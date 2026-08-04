<template>
  <span class="streaming-text">{{ displayText }}</span>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  text: string;
}>();

const displayText = ref(props.text);

watch(
  () => props.text,
  (newText) => {
    displayText.value = newText;
  },
);
</script>

<style scoped>
.streaming-text {
  /* Subtle streaming cursor effect */
  animation: none;
}
</style>
