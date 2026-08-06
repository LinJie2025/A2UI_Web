/** A2UI Store — manages surface state and overlay navigation. */

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { SurfaceState } from "@/types/a2ui";

/** A single step in the A2UI overlay stepper. */
export interface A2UIOverlayStep {
  id: string;
  title: string;
  content: string;
  status: "pending" | "active" | "done";
}

export const useA2UIStore = defineStore("a2ui", () => {
  /** Active surfaces keyed by surfaceId. */
  const surfaces = ref<Map<string, SurfaceState>>(new Map());

  // ── Overlay state ─────────────────────────────────────────────
  const showOverlay = ref(false);
  const overlaySteps = ref<A2UIOverlayStep[]>([]);
  const currentStepIndex = ref(0);

  const totalSteps = computed(() => overlaySteps.value.length);
  const hasNextStep = computed(() => currentStepIndex.value < totalSteps.value - 1);
  const hasPrevStep = computed(() => currentStepIndex.value > 0);
  const isLastStep = computed(() => currentStepIndex.value === totalSteps.value - 1);
  const currentStepContent = computed(() => overlaySteps.value[currentStepIndex.value]?.content ?? "");
  const overlayBadge = computed(() => {
    if (totalSteps.value === 0) return "";
    return isLastStep.value ? "done" : "active";
  });

  // ── Surface methods ───────────────────────────────────────────
  function setSurface(surfaceId: string, state: SurfaceState): void {
    surfaces.value.set(surfaceId, state);
  }
  function getSurface(surfaceId: string): SurfaceState | undefined {
    return surfaces.value.get(surfaceId);
  }
  function removeSurface(surfaceId: string): void {
    surfaces.value.delete(surfaceId);
  }

  // ── Overlay methods ───────────────────────────────────────────
  function openOverlay(rawText: string, title?: string): void {
    if (overlaySteps.value.length > 0) {
      showOverlay.value = true;
      return;
    }
    const extractedTitle = title || extractTitle(rawText) || "Step 1";
    overlaySteps.value = [{
      id: `step_${Date.now()}`,
      title: extractedTitle,
      content: rawText,
      status: totalSteps.value > 1 ? "done" : "active",
    }];
    currentStepIndex.value = 0;
    showOverlay.value = true;
  }

  function addStep(rawText: string, title?: string): void {
    const extractedTitle = title || extractTitle(rawText) || `Step ${overlaySteps.value.length + 1}`;
    overlaySteps.value.forEach((s) => { if (s.status === "active") s.status = "done"; });
    overlaySteps.value.push({
      id: `step_${Date.now()}`,
      title: extractedTitle,
      content: rawText,
      status: "active",
    });
    currentStepIndex.value = overlaySteps.value.length - 1;
  }

  function goToStep(index: number): void {
    if (index >= 0 && index < overlaySteps.value.length) {
      currentStepIndex.value = index;
    }
  }
  function prevStep(): void { if (hasPrevStep.value) currentStepIndex.value--; }
  function nextStep(): void { if (hasNextStep.value) currentStepIndex.value++; }
  function closeOverlay(): void { showOverlay.value = false; }

  function clear(): void {
    surfaces.value.clear();
    overlaySteps.value = [];
    currentStepIndex.value = 0;
    showOverlay.value = false;
  }

  /** Extract a title from A2UI JSONL text. */
  function extractTitle(text: string): string | null {
    if (!text) return null;
    try {
      for (const line of text.split("\n")) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        const parsed = JSON.parse(trimmed);
        if (parsed.updateComponents) {
          for (const comp of parsed.updateComponents.components || []) {
            if (comp.component === "Text" && typeof comp.text === "string") {
              return comp.text;
            }
          }
        }
      }
    } catch { /* not valid JSON */ }
    return null;
  }

  return {
    surfaces,
    showOverlay, overlaySteps, currentStepIndex,
    totalSteps, hasNextStep, hasPrevStep, isLastStep,
    currentStepContent, overlayBadge,
    setSurface, getSurface, removeSurface,
    openOverlay, addStep, goToStep, prevStep, nextStep, closeOverlay,
    clear,
  };
});
