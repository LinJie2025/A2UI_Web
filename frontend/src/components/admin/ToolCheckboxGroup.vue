<template>
  <div class="tool-checkbox-group">
    <n-checkbox-group v-model:value="selectedTools">
      <n-space vertical>
        <n-checkbox
          v-for="tool in allTools"
          :key="tool"
          :value="tool"
          :label="tool"
        />
      </n-space>
    </n-checkbox-group>
    <div v-if="allTools.length === 0" class="text-gray-400 text-sm">
      {{ $t('admin.noTools') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { NCheckboxGroup, NCheckbox, NSpace } from "naive-ui";

const props = defineProps<{
  allTools: string[];
}>();

const selectedTools = defineModel<(string | number)[]>();
</script>
