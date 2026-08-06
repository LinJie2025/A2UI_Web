<template>
  <div :class="['msg-row', isUser ? 'msg-row-user' : 'msg-row-ai']">
    <div v-if="!isUser" class="msg-avatar msg-avatar-ai">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round">
        <path d="M12 2a4 4 0 014 4c0 2-2 6-4 8-2-2-4-6-4-8a4 4 0 014-4z"/><circle cx="12" cy="6" r="1.5" fill="#2563eb" stroke="none"/>
      </svg>
    </div>
    <div :class="['msg-bubble', isUser ? 'msg-bubble-user' : hasA2UI ? 'msg-bubble-ai-wide' : 'msg-bubble-ai']">
      <div class="msg-header">
        <span class="msg-sender">{{ isUser ? $t('chat.me') : $t('chat.assistantName') }}</span>
      </div>
      <div v-if="streaming && !isUser" class="a2ui-skeleton">
        <div class="skeleton-card">
          <div class="skeleton-shimmer"></div>
          <div class="skeleton-title"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line short"></div>
          <div class="skeleton-dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="skeleton-label">{{ $t('chat.generatingUI') }}</span></div>
        </div>
      </div>
      <div v-else-if="streaming" class="msg-text"><StreamingText :text="message.content || ''" /></div>
      <div v-else-if="!isUser && hasA2UI" class="a2ui-preview">
        <A2UIRenderer :key="contentHash" :raw-text="a2uiRawText" :readonly="readonly" @a2ui-action="onA2UIAction" />
        <!-- Action result banner shown below the form after submission -->
        <div v-if="message.action_result" class="action-result" :class="message.action_status === 'failed' ? 'result-failed' : 'result-done'">
          <span class="result-icon">{{ message.action_status === 'failed' ? '❌' : '✅' }}</span>
          <span class="result-text">{{ message.action_result }}</span>
        </div>
      </div>
      <div v-else class="msg-text">{{ message.content || '' }}</div>
    </div>
    <div v-if="isUser" class="msg-avatar msg-avatar-user">{{ (message.content || 'U')[0] }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import StreamingText from "./StreamingText.vue";
import { hasA2UIMessages } from "@/utils/a2ui-parser";
import A2UIRenderer from "@/components/a2ui/A2UIRenderer.vue";
import type { Message as ChatMessageType } from "@/types/chat";

const props = withDefaults(defineProps<{ message: ChatMessageType; streaming?: boolean; readonly?: boolean; }>(), { streaming: false, readonly: false });

const emit = defineEmits<{ (e: "a2ui-action", payload: { action: string; surfaceId: string; data: Record<string, unknown> }): void; }>();

const isUser = computed(() => props.message.role === "user");

/**
 * During streaming: content contains both plain text + A2UI JSONL (mixed).
 * From history / DB: backend stores them separately — content = text, a2ui_jsonl = A2UI.
 * We combine both so A2UI detection & rendering work in both scenarios.
 */
const effectiveContent = computed(() => {
  const parts: string[] = [];
  if (props.message.content) parts.push(props.message.content);
  if (props.message.a2ui_jsonl) parts.push(props.message.a2ui_jsonl);
  return parts.join("\n");
});

const hasA2UI = computed(() => hasA2UIMessages(effectiveContent.value));

/**
 * Raw text passed to A2UIRenderer:
 * - History messages: use a2ui_jsonl only (backend stores JSONL separately from text).
 *   This avoids the plain text from content being duplicated alongside the A2UI surface.
 * - Streaming messages: use content (JSONL is embedded in the streamed text).
 */
const a2uiRawText = computed(() => {
  return props.message.a2ui_jsonl || props.message.content || "";
});

const contentHash = computed(() => {
  const c = a2uiRawText.value;
  return c.length > 0 ? c.length + "_" + c.charCodeAt(c.length - 1) + "_" + c.charCodeAt(0) : "0";
});

function onA2UIAction(payload: { action: string; surfaceId: string; data: Record<string, unknown> }) { if (props.readonly) return; emit("a2ui-action", payload); }
</script>

<style scoped>
.msg-row { display: flex; gap: 0.75rem; margin-bottom: 1rem; }
.msg-row-user { flex-direction: row-reverse; }
.msg-row-ai { flex-direction: row; }
.msg-avatar { width: 32px; height: 32px; border-radius: 8px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
.msg-avatar-ai { background: #eff6ff; border: 1px solid rgba(37,99,235,0.15); }
.msg-avatar-user { background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #fff; font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 0.75rem; }
.msg-bubble { border-radius: 12px; padding: 0.625rem 0.875rem; font-size: 0.875rem; line-height: 1.6; min-width: 0; }
.msg-bubble-user { max-width: 70%; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: #fff; border-bottom-right-radius: 4px; }
.msg-bubble-ai { max-width: 70%; background: #fff; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
.msg-bubble-ai-wide { max-width: 85%; background: #fff; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.03); }
.msg-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem; }
.msg-bubble-user .msg-sender { color: rgba(255,255,255,0.6); }
.msg-sender { font-size: 0.6875rem; font-weight: 500; color: #94a3b8; font-family: 'Outfit', sans-serif; }
.msg-text { white-space: pre-wrap; word-break: break-word; }
.a2ui-preview { position: relative; }

/* ── Action result banner (form submission feedback) ────── */
.action-result {
  margin-top: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.8125rem;
  line-height: 1.5;
}
.result-done {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
}
.result-failed {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}
.result-icon {
  flex-shrink: 0;
  font-size: 0.875rem;
  line-height: 1.5;
}
.result-text {
  word-break: break-word;
}

.a2ui-skeleton { min-width: 260px; }
.skeleton-card { position: relative; background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; overflow: hidden; }
.skeleton-shimmer { position: absolute; inset: 0; background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.6) 45%, rgba(255,255,255,0.9) 50%, rgba(255,255,255,0.6) 55%, transparent 60%); animation: shimmerSweep 2s ease-in-out infinite; z-index: 1; pointer-events: none; }
.skeleton-title { width: 40%; height: 12px; background: #f1f5f9; border-radius: 4px; margin-bottom: 0.75rem; position: relative; z-index: 0; }
.skeleton-line { width: 100%; height: 10px; background: #f8fafc; border-radius: 3px; margin-bottom: 0.5rem; position: relative; z-index: 0; }
.skeleton-line.short { width: 60%; }
.skeleton-dots { display: flex; align-items: center; gap: 4px; margin-top: 0.75rem; position: relative; z-index: 0; }
.skeleton-dots .dot { width: 6px; height: 6px; border-radius: 50%; background: #cbd5e1; animation: dotPulse 1.2s ease-in-out infinite; }
.skeleton-dots .dot:nth-child(2) { animation-delay: 0.2s; }
.skeleton-dots .dot:nth-child(3) { animation-delay: 0.4s; }
.skeleton-label { font-size: 0.6875rem; color: #94a3b8; margin-left: 4px; }
@keyframes shimmerSweep { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
@keyframes dotPulse { 0%, 100% { opacity: 0.3; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }
</style>
