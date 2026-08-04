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
        <span v-if="statusBadge" class="a2ui-status-badge" :class="'badge-' + statusBadge.status">
          {{ badgeLabel(statusBadge) }}
        </span>
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
        <A2UIRenderer :key="contentHash" :raw-text="message.content || ''" :readonly="readonly" @a2ui-action="onA2UIAction" />
        <div v-if="!readonly" class="a2ui-expand-row">
          <button class="a2ui-expand-btn" @click="openOverlay" :title="$t('chat.expandFullscreen')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
            {{ $t('chat.expandFullscreen') }}
          </button>
        </div>
      </div>
      <div v-else class="msg-text">{{ message.content || '' }}</div>
    </div>
    <div v-if="isUser" class="msg-avatar msg-avatar-user">{{ (message.content || 'U')[0] }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useChatStore } from "@/stores/chat";
import StreamingText from "./StreamingText.vue";
import { hasA2UIMessages } from "@/utils/a2ui-parser";
import A2UIRenderer from "@/components/a2ui/A2UIRenderer.vue";
import type { ChatMessage as ChatMessageType } from "@/types/chat";

const { t } = useI18n();

export interface A2uiStatusBadge {
  status: "processing" | "done" | "failed" | "interrupted";
  summary: string | null;
}

const props = withDefaults(defineProps<{ message: ChatMessageType; streaming?: boolean; readonly?: boolean; statusBadge?: A2uiStatusBadge | null; }>(), { streaming: false, readonly: false, statusBadge: null });

const emit = defineEmits<{ (e: "a2ui-action", payload: { action: string; surfaceId: string; data: Record<string, unknown> }): void; }>();

const chatStore = useChatStore();
const isUser = computed(() => props.message.role === "user");
const hasA2UI = computed(() => hasA2UIMessages(props.message.content || ""));
const contentHash = computed(() => { const c = props.message.content || ""; return c.length > 0 ? c.length + "_" + c.charCodeAt(c.length - 1) + "_" + c.charCodeAt(0) : "0"; });

function badgeLabel(badge: A2uiStatusBadge): string {
  if (badge.status === "processing") return "⏳ " + t("actionLog.statusProcessing");
  if (badge.status === "done") return "✅ " + t("actionLog.statusDone");
  if (badge.status === "failed") return "❌ " + t("actionLog.statusFailed");
  return "⚠️ " + t("actionLog.statusInterrupted");
}

function onA2UIAction(payload: { action: string; surfaceId: string; data: Record<string, unknown> }) { if (props.readonly) return; emit("a2ui-action", payload); }
function openOverlay() { if (props.readonly) return; chatStore.openA2UIOverlay(props.message.content || ""); }
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
.a2ui-status-badge { font-size: 0.625rem; font-weight: 600; padding: 0.125rem 0.5rem; border-radius: 999px; line-height: 1.4; white-space: nowrap; }
.badge-done { background: #dcfce7; color: #16a34a; }
.badge-failed { background: #fef2f2; color: #dc2626; }
.badge-processing { background: #dbeafe; color: #2563eb; }
.badge-interrupted { background: #fef9c3; color: #ca8a04; }
.msg-text { white-space: pre-wrap; word-break: break-word; }
.a2ui-preview { position: relative; }
.a2ui-expand-row { margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #f1f5f9; display: flex; justify-content: flex-end; }
.a2ui-expand-btn { font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 0.75rem; padding: 0.375rem 0.75rem; border: 1px solid #e2e8f0; border-radius: 8px; background: #f8fafc; color: #64748b; cursor: pointer; display: inline-flex; align-items: center; gap: 0.375rem; min-height: 36px; transition: all 0.15s ease; }
.a2ui-expand-btn:hover { border-color: #93c5fd; background: #eff6ff; color: #2563eb; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1); }
.a2ui-expand-btn:active { transform: scale(0.97); }
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
