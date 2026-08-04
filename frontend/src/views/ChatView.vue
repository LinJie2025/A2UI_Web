<template>
  <div class="chat-page">
    <TopNavbar />
    <div class="chat-body">
      <div class="panel panel-left" :class="{ collapsed: leftCollapsed }">
        <button class="panel-toggle" @click="leftCollapsed = !leftCollapsed" :title="leftCollapsed ? 'Expand' : 'Collapse'">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline v-if="leftCollapsed" points="9 18 15 12 9 6" />
            <polyline v-else points="15 18 9 12 15 6" />
          </svg>
        </button>
        <div v-show="!leftCollapsed" class="panel-content">
          <Sidebar @new-chat="onNewChat" @select-conversation="onSelectConversation" />
        </div>
      </div>
      <main class="chat-main">
        <div class="chat-bg"></div>
        <div ref="messagesContainer" class="messages-area">
          <div class="messages-inner">
            <div v-if="loadingHistory" class="loading-state">
              <div class="skeleton-item" v-for="i in 3" :key="i">
                <div class="skeleton-line w-3/4"></div>
                <div class="skeleton-line w-1/2"></div>
              </div>
            </div>
            <div v-else-if="chatStore.messages.length === 0 && !chatStore.currentStreamingMessage" class="welcome-state">
              <div class="welcome-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-linecap="round">
                  <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                  <path d="M8 9h8M8 13h6"/>
                </svg>
              </div>
              <h2 class="welcome-title">{{ $t('chat.welcome') }}</h2>
              <p class="welcome-desc">{{ $t('chat.welcomeDesc') }}</p>
            </div>
            <template v-else>
              <ChatMessage
                v-for="(msg, idx) in chatStore.messages"
                :key="idx"
                :ref="(el) => setMsgRef(idx, el)"
                :data-index="idx"
                :message="msg"
                :readonly="isHistorical"
                :status-badge="getA2uiStatus(idx)"
                @a2ui-action="(payload) => { pendingSubmitMsgIdx = idx; handleA2UIAction(payload) }"
              />
              <template v-if="chatStore.currentStreamingMessage && !chatStore.showA2UIOverlay">
                <ChatMessage :message="{ role: 'assistant', content: chatStore.currentStreamingMessage.content }" :streaming="true" :readonly="false" />
              </template>
            </template>
          </div>
        </div>
        <ChatInput :disabled="chatStore.isStreaming || chatStore.showA2UIOverlay" @send="handleSend" />
      </main>
      <div class="panel panel-right" :class="{ collapsed: rightCollapsed }">
        <button class="panel-toggle" @click="rightCollapsed = !rightCollapsed" :title="rightCollapsed ? 'Expand' : 'Collapse'">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline v-if="rightCollapsed" points="15 18 9 12 15 6" />
            <polyline v-else points="9 18 15 12 9 6" />
          </svg>
        </button>
        <div v-show="!rightCollapsed" class="panel-content">
          <ActionSidebar v-if="conversationStore.currentConversationId" :conversation-id="conversationStore.currentConversationId" @scroll-to="scrollToIndex" />
        </div>
      </div>
    </div>
    <A2UIOverlay @a2ui-action="handleA2UIAction" />
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch, type ComponentPublicInstance } from "vue";
import TopNavbar from "@/components/layout/TopNavbar.vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import ChatMessage from "@/components/chat/ChatMessage.vue";
import ChatInput from "@/components/chat/ChatInput.vue";
import A2UIOverlay from "@/components/a2ui/A2UIOverlay.vue";
import ActionSidebar from "@/components/history/ActionSidebar.vue";
import { useChatStore } from "@/stores/chat";
import { useConversationStore } from "@/stores/conversation";
import { useSSE } from "@/composables/useSSE";
import { getConversationMessagesApi } from "@/api/conversation";
import { getConversationActionsApi } from "@/api/action";
import { hasA2UIMessages } from "@/utils/a2ui-parser";
import type { ChatMessage as ChatMessageType } from "@/types/chat";
import type { A2UIAction } from "@/types/action";
import type { A2uiStatusBadge } from "@/components/chat/ChatMessage.vue";

const chatStore = useChatStore();
const conversationStore = useConversationStore();
const { isStreaming, streamingMessage, error, startStream } = useSSE();
const messagesContainer = ref<HTMLElement | null>(null);

const leftCollapsed = ref(false);
const rightCollapsed = ref(false);
const isHistorical = ref(false);
const loadingHistory = ref(false);
const pendingSubmitMsgIdx = ref(-1);

const a2uiStatuses = ref<Map<number, A2uiStatusBadge>>(new Map());

function getA2uiStatus(idx: number): A2uiStatusBadge | null {
  return a2uiStatuses.value.get(idx) ?? null;
}
const msgRefs = ref<Map<number, ComponentPublicInstance | Element>>(new Map());

function setMsgRef(idx: number, el: unknown) {
  if (el) msgRefs.value.set(idx, el as ComponentPublicInstance | Element);
}

watch(isStreaming, (val) => chatStore.setStreaming(val));
watch(streamingMessage, (val) => chatStore.setStreamingMessage(val));
watch(error, (val) => {
  if (val && typeof val === "string") {
    chatStore.setStreamingMessage(null);
    chatStore.setStreaming(false);
    const escaped = val.replace(/"/g, '\\"');
    const errContent = [
      '{"createSurface":{"surfaceId":"err","catalogId":"basic"}}',
      '{"updateComponents":{"surfaceId":"err","components":[' +
        '{"id":"root","component":"Card","child":"col"},' +
        '{"id":"col","component":"Column","children":["icon","msg"]},' +
        '{"id":"icon","component":"Icon","name":"error"},' +
        '{"id":"msg","component":"Text","text":"' + escaped + '","variant":"body"}' +
      ']}}',
    ].join("\n");
    chatStore.addMessage({ role: "assistant", content: errContent });
  }
});

watch(
  () => [chatStore.messages.length, chatStore.currentStreamingMessage?.content.length],
  async () => { await nextTick(); if (messagesContainer.value) messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight; },
  { deep: true },
);

async function handleSend(content: string) {
  if (!content.trim() || chatStore.isStreaming || chatStore.showA2UIOverlay) return;
  chatStore.addMessage({ role: "user", content });
  const req = chatStore.messages.map((m) => ({ role: m.role, content: m.content }));
  await startStream({ messages: req, conversation_id: conversationStore.currentConversationId });
  if (streamingMessage.value && streamingMessage.value.content) {
    chatStore.addMessage({ role: "assistant", content: streamingMessage.value.content });
    chatStore.setStreamingMessage(null);
    if (streamingMessage.value.conversationId && !conversationStore.currentConversationId)
      conversationStore.setCurrentConversation(streamingMessage.value.conversationId);
  }
}

async function onSelectConversation(id: number) {
  loadingHistory.value = true; chatStore.clearMessages(); isHistorical.value = true; conversationStore.setCurrentConversation(id);
  try {
    const resp = await getConversationMessagesApi(id);
    if (resp.code === 0 && resp.data) { chatStore.setMessages(filterHistoryMessages(resp.data as any[])); }
    try { const aResp = await getConversationActionsApi(id); if (aResp.code === 0 && aResp.data) mapActionsToMessages(aResp.data); } catch {}
  } catch {} finally {
    loadingHistory.value = false; await nextTick(); if (messagesContainer.value) messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
}

function onNewChat() { chatStore.clearMessages(); conversationStore.setCurrentConversation(null); isHistorical.value = false; }

async function handleA2UIAction(payload: { action: string; surfaceId: string; data: Record<string, unknown> }) {
  if (chatStore.isStreaming) return;
  const wasOverlayOpen = chatStore.showA2UIOverlay;
  const convId = conversationStore.currentConversationId;
  const msgIdx = pendingSubmitMsgIdx.value; pendingSubmitMsgIdx.value = -1;
  await startStream({ conversation_id: convId ?? 0, action_name: payload.action, form_data: payload.data }, "/api/a2ui/submit");
  if (streamingMessage.value && streamingMessage.value.content) {
    if (!convId && streamingMessage.value.conversationId) conversationStore.currentConversationId = streamingMessage.value.conversationId;
    if (msgIdx >= 0) { const s = extractActionSummary(streamingMessage.value.content); a2uiStatuses.value.set(msgIdx, { status: "done", summary: s }); }
    if (wasOverlayOpen && chatStore.showA2UIOverlay) chatStore.addOverlayStep(streamingMessage.value.content);
    chatStore.setStreamingMessage(null);
  }
}

function scrollToIndex(index: number) {
  const el = msgRefs.value.get(index); if (el) { const d = (el as any).$el || el; d.scrollIntoView({ behavior: "smooth", block: "center" }); }
}

function filterHistoryMessages(msgs: any[]): ChatMessageType[] {
  const r: ChatMessageType[] = [];
  for (const m of msgs) { if (m.role === "user" && m.content && /^用户提交了/.test(m.content)) continue; r.push({ role: m.role, content: m.content || "" }); }
  return r;
}

function mapActionsToMessages(actions: A2UIAction[]) {
  a2uiStatuses.value.clear(); let ai = 0;
  for (let i = 0; i < chatStore.messages.length && ai < actions.length; i++) {
    if (chatStore.messages[i].role === "assistant" && hasA2UIMessages(chatStore.messages[i].content || "")) {
      const a = actions[ai]; if (a) { a2uiStatuses.value.set(i, { status: a.status as any, summary: a.result_summary || null }); ai++; }
    }
  }
}

function extractActionSummary(content: string): string | null {
  if (!content) return null;
  for (const line of content.split("\n")) { try { const o = JSON.parse(line.trim()); if (o.updateComponents) for (const c of o.updateComponents.components || []) { if (c.component === "Text" && c.text) { const t = c.text.trim(); if (t && t.length <= 50) return t; } } } catch {} }
  return null;
}
</script>

<style scoped>
.chat-page { height: 100vh; display: flex; flex-direction: column; background: #f8fafb; font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
.chat-body { flex: 1; display: flex; overflow: hidden; min-height: 0; }
.panel { position: relative; width: 256px; flex-shrink: 0; background: #fff; border-color: #e2e8f0; transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1); overflow: hidden; display: flex; flex-direction: column; }
.panel-left { border-right: 1px solid #e2e8f0; }
.panel-right { border-left: 1px solid #e2e8f0; }
.panel.collapsed { width: 36px; }
.panel-toggle { position: absolute; top: 50%; z-index: 10; width: 20px; height: 40px; display: flex; align-items: center; justify-content: center; background: #fff; border: 1px solid #e2e8f0; border-radius: 0 6px 6px 0; cursor: pointer; color: #94a3b8; transition: color 0.15s, background 0.15s; transform: translateY(-50%); padding: 0; }
.panel-left .panel-toggle { right: -20px; border-left: none; }
.panel-right .panel-toggle { left: -20px; border-right: none; border-radius: 6px 0 0 6px; }
.panel-toggle:hover { color: #2563eb; background: #f8fafb; }
.panel-content { flex: 1; overflow: hidden; display: flex; flex-direction: column; }
.chat-main { flex: 1; display: flex; flex-direction: column; min-width: 0; position: relative; }
.chat-bg { position: absolute; inset: 0; background: radial-gradient(circle at 20% 30%, rgba(37,99,235,0.03) 0%, transparent 50%), radial-gradient(circle at 80% 70%, rgba(13,148,136,0.03) 0%, transparent 50%); pointer-events: none; }
.messages-area { flex: 1; overflow-y: auto; padding: 1.5rem 2rem; }
.messages-inner { max-width: 720px; margin: 0 auto; }
.loading-state, .welcome-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 4rem 2rem; text-align: center; }
.skeleton-item { width: 100%; display: flex; flex-direction: column; gap: 0.375rem; padding: 0.5rem 0; }
.skeleton-line { height: 0.75rem; background: #e2e8f0; border-radius: 4px; animation: shimmer 1.5s infinite; }
.w-3\/4 { width: 75%; }
.w-1\/2 { width: 50%; }
@keyframes shimmer { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
.welcome-icon { width: 56px; height: 56px; background: rgba(37,99,235,0.08); border-radius: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem; }
.welcome-title { font-size: 1.125rem; font-weight: 600; color: #1e293b; margin: 0 0 0.5rem; }
.welcome-desc { font-size: 0.875rem; color: #64748b; max-width: 320px; margin: 0; }
</style>
