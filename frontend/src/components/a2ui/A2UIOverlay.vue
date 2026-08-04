<template>
  <Teleport to="body">
    <Transition name="overlay">
      <div v-if="chatStore.showA2UIOverlay" class="a2ui-overlay" @click.self="chatStore.closeA2UIOverlay()">
        <div class="a2ui-overlay-card">
          <header class="a2ui-overlay-topbar">
            <div class="flex items-center gap-2">
              <button class="a2ui-overlay-close-btn" @click="chatStore.closeA2UIOverlay()" :title="$t('chat.closeOverlay')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
              <span class="a2ui-overlay-title">{{ currentStep?.title || 'A2UI Form' }}</span>
            </div>
            <div v-if="chatStore.totalSteps > 1" class="a2ui-overlay-badge" :class="'badge-' + chatStore.overlayBadge">
              {{ badgeText }}
            </div>
          </header>
          <div v-if="chatStore.totalSteps > 1" class="a2ui-step-indicator">
            <div class="a2ui-step-track">
              <template v-for="(step, idx) in chatStore.a2uiOverlaySteps" :key="step.id">
                <div :class="['a2ui-step-dot', stepClass(step, idx)]" @click="chatStore.goToStep(idx)">
                  <span v-if="step.status === 'done'" class="a2ui-step-check">&#10003;</span>
                  <span v-else>{{ idx + 1 }}</span>
                </div>
                <div v-if="idx < chatStore.a2uiOverlaySteps.length - 1" :class="['a2ui-step-line', step.status === 'done' ? 'line-done' : '']"></div>
              </template>
            </div>
            <div class="a2ui-step-labels">
              <span v-for="(step, idx) in chatStore.a2uiOverlaySteps" :key="'l' + step.id" :class="['a2ui-step-label', stepLabelClass(step, idx)]" @click="chatStore.goToStep(idx)">{{ step.title }}</span>
            </div>
          </div>
          <div class="a2ui-overlay-body" :key="chatStore.currentStepIndex">
            <A2UIRenderer :raw-text="chatStore.currentStepContent" @a2ui-action="handleAction" />
          </div>
          <footer v-if="chatStore.totalSteps > 1" class="a2ui-overlay-footer">
            <button class="a2ui-step-btn a2ui-step-btn-prev" :disabled="!chatStore.hasPrevStep" @click="chatStore.prevStep()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
              {{ $t('overlay.prevStep') }}
            </button>
            <span class="a2ui-step-counter">{{ chatStore.currentStepIndex + 1 }} / {{ chatStore.totalSteps }}</span>
            <button class="a2ui-step-btn a2ui-step-btn-next" :disabled="!chatStore.hasNextStep" @click="chatStore.nextStep()">
              {{ $t('overlay.nextStep') }}
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useChatStore, type A2UIOverlayStep } from "@/stores/chat";
import A2UIRenderer from "./A2UIRenderer.vue";

const { t } = useI18n();
const chatStore = useChatStore();

const emit = defineEmits<{ (e: "a2ui-action", payload: { action: string; surfaceId: string; data: Record<string, unknown> }): void; }>();

const currentStep = computed(() => chatStore.a2uiOverlaySteps[chatStore.currentStepIndex] ?? null);
const badgeText = computed(() => { if (chatStore.isLastStep) return t("overlay.statusDone"); return `${chatStore.currentStepIndex + 1}/${chatStore.totalSteps}`; });

function stepClass(step: A2UIOverlayStep, idx: number): string {
  if (step.status === "done") return "dot-done"; if (idx === chatStore.currentStepIndex) return "dot-active"; return "";
}
function stepLabelClass(step: A2UIOverlayStep, idx: number): string {
  if (step.status === "done") return "label-done"; if (idx === chatStore.currentStepIndex) return "label-active"; return "";
}
function handleAction(payload: { action: string; surfaceId: string; data: Record<string, unknown> }) { emit("a2ui-action", payload); }
</script>

<style scoped>
.a2ui-overlay { position: fixed; inset: 0; z-index: 1000; display: flex; align-items: flex-start; justify-content: center; padding: 2rem 1rem; background: rgba(248,250,252,0.85); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); overflow-y: auto; }
.a2ui-overlay-card { width: 100%; max-width: 672px; background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04); overflow: hidden; display: flex; flex-direction: column; animation: overlaySlideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
.a2ui-overlay-topbar { height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 1.25rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; flex-shrink: 0; }
.a2ui-overlay-close-btn { width: 36px; height: 36px; border-radius: 8px; border: none; background: transparent; color: #94a3b8; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
.a2ui-overlay-close-btn:hover { background: #f1f5f9; color: #475569; }
.a2ui-overlay-title { font-family: 'Outfit', system-ui, sans-serif; font-size: 0.9375rem; font-weight: 600; color: #1e293b; }
.a2ui-overlay-badge { font-family: 'Outfit', system-ui, sans-serif; font-size: 0.6875rem; font-weight: 600; padding: 0.2rem 0.625rem; border-radius: 999px; }
.badge-active { background: #eff6ff; color: #2563eb; }
.badge-done { background: #d1fae5; color: #065f46; }
.a2ui-step-indicator { padding: 1rem 2rem 0.5rem; flex-shrink: 0; }
.a2ui-step-track { display: flex; align-items: center; justify-content: center; max-width: 360px; margin: 0 auto; }
.a2ui-step-dot { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; border: 2px solid #e2e8f0; background: #fff; color: #94a3b8; cursor: pointer; transition: all 0.25s ease; flex-shrink: 0; position: relative; z-index: 2; }
.a2ui-step-dot:hover { border-color: #93c5fd; }
.dot-active { border-color: #2563eb; background: #eff6ff; color: #2563eb; animation: dotPulse 2s ease-in-out infinite; }
.dot-done { border-color: #10b981; background: #d1fae5; color: #10b981; }
.a2ui-step-line { flex: 1; height: 2px; background: #e2e8f0; margin: 0 -2px; transition: background 0.3s ease; }
.line-done { background: #10b981; }
.a2ui-step-check { font-size: 0.75rem; line-height: 1; }
.a2ui-step-labels { display: flex; justify-content: center; max-width: 420px; margin: 0.375rem auto 0; }
.a2ui-step-label { font-size: 0.6875rem; color: #94a3b8; text-align: center; flex: 1; cursor: pointer; transition: color 0.2s; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding: 0 4px; }
.a2ui-step-label:hover { color: #64748b; }
.label-active { color: #2563eb; font-weight: 600; }
.label-done { color: #10b981; }
@keyframes dotPulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(37,99,235,0.3); } 50% { box-shadow: 0 0 0 6px rgba(37,99,235,0); } }
.a2ui-overlay-body { padding: 1.5rem 1.75rem; flex: 1; overflow-y: auto; min-height: 200px; }
.a2ui-overlay-body::-webkit-scrollbar { width: 4px; }
.a2ui-overlay-body::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.a2ui-overlay-footer { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1.75rem; border-top: 1px solid #f1f5f9; flex-shrink: 0; background: #fafbfc; }
.a2ui-step-btn { font-family: 'Outfit', system-ui, sans-serif; font-weight: 600; font-size: 0.75rem; padding: 0.5rem 0.875rem; border-radius: 8px; cursor: pointer; display: inline-flex; align-items: center; gap: 0.375rem; transition: all 0.15s; border: 1px solid #e2e8f0; background: #fff; color: #475569; min-height: 36px; }
.a2ui-step-btn:hover:not(:disabled) { border-color: #93c5fd; background: #eff6ff; color: #2563eb; }
.a2ui-step-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.a2ui-step-btn-next { background: #2563eb; color: #fff; border-color: #2563eb; }
.a2ui-step-btn-next:hover:not(:disabled) { background: #1d4ed8; border-color: #1d4ed8; }
.a2ui-step-counter { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94a3b8; }
@keyframes overlaySlideUp { from { opacity: 0; transform: translateY(24px) scale(0.97); } to { opacity: 1; transform: translateY(0) scale(1); } }
.overlay-enter-active { transition: opacity 0.2s ease; }
.overlay-leave-active { transition: opacity 0.15s ease; }
.overlay-enter-from, .overlay-leave-to { opacity: 0; }
@media (max-width: 768px) {
  .a2ui-overlay { padding: 0; align-items: stretch; }
  .a2ui-overlay-card { border-radius: 0; max-width: 100%; min-height: 100svh; box-shadow: none; }
  .a2ui-overlay-body { padding: 1.25rem 1rem; }
  .a2ui-step-indicator { padding: 0.75rem 1rem 0.25rem; }
  .a2ui-overlay-footer { padding: 0.75rem 1rem; }
}
@media (prefers-reduced-motion: reduce) { .a2ui-overlay-card { animation: none; } .overlay-enter-active, .overlay-leave-active { transition: none; } .dot-active { animation: none; } }
</style>
