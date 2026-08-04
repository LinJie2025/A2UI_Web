<template>
  <div class="a2ui-renderer space-y-4">
    <!-- A2UI surfaces: pure UI, no text lines -->
    <template v-if="result.surfaces.size > 0">
      <div
        v-for="[surfaceId, surface] in result.surfaces"
        :key="surfaceId"
        class="a2ui-surface"
      >
        <A2UINode
          v-if="rootNodes.get(surfaceId)"
          :node="rootNodes.get(surfaceId)!"
        />
        <div v-else class="text-xs" style="color:#94a3b8;font-style:italic;">
          Surface "{{ surfaceId }}" — no root component
        </div>
      </div>
    </template>

    <!-- No surfaces: fallback to text lines -->
    <template v-else>
      <div v-for="(line, idx) in result.textLines" :key="'text-' + idx" class="a2ui-text-body">
        {{ line }}
      </div>
    </template>

    <!-- Parse errors (always show) -->
    <div v-if="result.errors.length > 0" class="mt-2">
      <div v-for="(err, idx) in result.errors" :key="'err-' + idx" class="error-text">
        {{ err }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, provide, reactive, ref } from "vue";
import { parseA2UI, buildRenderTree } from "@/utils/a2ui-parser";
import A2UINode from "./A2UINode.vue";
import type { RenderNode } from "@/types/a2ui";

const props = defineProps<{
  rawText: string;
  readonly?: boolean;
}>();

const emit = defineEmits<{
  (e: "a2ui-action", payload: { action: string; surfaceId: string; data: Record<string, unknown> }): void;
}>();

const result = computed(() => parseA2UI(props.rawText));

/** Build render tree for each surface */
const rootNodes = computed(() => {
  const nodes = new Map<string, RenderNode | null>();
  for (const [surfaceId, surface] of result.value.surfaces) {
    nodes.set(surfaceId, buildRenderTree(surface));
  }
  return nodes;
});

// ── Stagger animation counter (depth-first index) ────────────────────────
let _stagger = 0;
function getStaggerIndex(): number {
  return _stagger++;
}
provide("a2uiStaggerIndex", getStaggerIndex);

// ── Surface data store (TextField values collected here) ──────────────────

/** Per-surface reactive data model — TextFields write to this, Buttons read from it */
const surfaceData = reactive<Record<string, Record<string, unknown>>>({});

// Initialize data stores for each surface
for (const [surfaceId] of result.value.surfaces) {
  if (!(surfaceId in surfaceData)) {
    surfaceData[surfaceId] = reactive({});
  }
}

provide("a2uiSurfaceData", surfaceData);

// ── Action handler (called by A2UIButton via inject) ──────────────────────

function handleAction(action: string, surfaceId: string) {
  const data = surfaceData[surfaceId] ? { ...surfaceData[surfaceId] } : {};
  emit("a2ui-action", { action, surfaceId, data });
}

provide("a2uiHandleAction", handleAction);

// ── Readonly mode (history viewing) ─────────────────────────────────
provide("a2uiReadonly", computed(() => props.readonly ?? false));
</script>

<style scoped>
.a2ui-text-body {
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  font-size: 0.875rem;
  color: #475569;
  line-height: 1.6;
  white-space: pre-wrap;
}
.error-text {
  font-size: 0.75rem;
  color: #ef4444;
}
</style>
