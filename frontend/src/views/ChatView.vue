<template>
  <div class="chat-page">
    <TopNavbar />
    <div class="chat-body">
      <div class="panel panel-left" :class="{ collapsed: leftCollapsed }">
        <button class="panel-toggle" @click="leftCollapsed = !leftCollapsed" :title="leftCollapsed ? $t('sidebar.expand') : $t('sidebar.collapse')">
          <svg v-if="leftCollapsed" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
          </svg>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="15 18 9 12 15 6" />
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
                <div v-else class="messages-list">
              <ChatMessage
                v-for="msg in visibleMessages"
                :key="msg.id"
                :ref="(el) => setMsgRef(msg.id, el)"
                :data-msg-id="msg.id"
                :message="msg"
                :readonly="!!msg.action_result"
                @a2ui-action="(payload: any) => handleA2UIAction(payload, msg.id)"
              />
              <ChatMessage
                v-if="chatStore.currentStreamingMessage && !a2uiStore.showOverlay && submittingMessageIds.size === 0"
                :key="'streaming'"
                :message="{
                  id: 0, conversation_id: 0, role: 'assistant', message_type: 'chat',
                  content: chatStore.currentStreamingMessage.content,
                  tool_calls_json: null, tool_call_id: null, tool_name: null,
                  a2ui_jsonl: null, action_name: null, action_status: null,
                  action_result: null, created_at: ''
                }"
                :streaming="true"
                :readonly="false"
              />
            </div>
          </div>
        </div>
        <ChatInput :disabled="chatStore.isStreaming || a2uiStore.showOverlay" @send="handleSend" />
      </main>
    </div>
    <A2UIOverlay @a2ui-action="handleA2UIAction" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch, onBeforeUnmount, type ComponentPublicInstance } from "vue";
import TopNavbar from "@/components/layout/TopNavbar.vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import ChatMessage from "@/components/chat/ChatMessage.vue";
import ChatInput from "@/components/chat/ChatInput.vue";
import A2UIOverlay from "@/components/a2ui/A2UIOverlay.vue";
import { useChatStore } from "@/stores/chat";
import { useConversationStore } from "@/stores/conversation";
import { useA2UIStore } from "@/stores/a2ui";
import { useSSE } from "@/composables/useSSE";
import { buildChatRequest, buildActionRequest } from "@/api/chat";
import { parseA2UI } from "@/utils/a2ui-parser";

const chatStore = useChatStore();
const conversationStore = useConversationStore();
const a2uiStore = useA2UIStore();
const { isStreaming, streamingMessage, error, startStream, abort } = useSSE();
const messagesContainer = ref<HTMLElement | null>(null);

const leftCollapsed = ref(false);
const loadingHistory = ref(false);

/** IDs of messages whose A2UI forms have been successfully submitted.
 *  Once a form is submitted, its submit button stays disabled.
 *  This replaces the old historyMessageIds approach — now both historical
 *  and new messages use the SAME logic: submit once → readonly forever. */
// Messages currently streaming a form submission (to disable buttons during stream)
const submittingMessageIds = ref<Set<number | string>>(new Set());

/** Filtered visible messages (exclude tool & a2ui_action messages). */
const visibleMessages = computed(() =>
  chatStore.messages.filter(
    (msg) => msg.role !== "tool" && msg.message_type !== "a2ui_action",
  ),
);

const msgRefs = ref<Map<number, ComponentPublicInstance | Element>>(new Map());

function setMsgRef(id: number, el: unknown) {
  if (el) {
    msgRefs.value.set(id, el as ComponentPublicInstance | Element);
  } else {
    // Clean up stale ref when the component unmounts
    msgRefs.value.delete(id);
  }
}

watch(isStreaming, (val) => chatStore.setStreaming(val));

// Only propagate streamingMessage to store when no error has occurred.
// This prevents a race condition where the SSE finally block updates the
// streamingMessage (e.g. setting isComplete=true) after the error handler
// has already cleared the store's streaming message.
watch(streamingMessage, (val) => {
  if (!error.value) {
    chatStore.setStreamingMessage(val);
  }
});

watch(error, (val) => {
  if (val && typeof val === "string") {
    // Clear the streaming display immediately so the skeleton is replaced
    chatStore.setStreamingMessage(null);
    chatStore.setStreaming(false);

    // Render the error as an error card using A2UI JSONL format
    const errLines = [
      '{"createSurface":{"surfaceId":"err","catalogId":"basic"}}',
      '{"updateComponents":{"surfaceId":"err","components":[' +
        '{"id":"root","component":"Card","child":"col"},' +
        '{"id":"col","component":"Column","children":["icon","msg"]},' +
        '{"id":"icon","component":"Icon","name":"error"},' +
        `{"id":"msg","component":"Text","text":"${val.replace(/"/g, '\\"')}","variant":"body"}` +
      ']}}',
    ].join("\n");
    chatStore.addMessage({
      id: -Date.now(),
      conversation_id: chatStore.currentConversationId ?? 0,
      role: "assistant",
      message_type: "chat",
      content: errLines,
      tool_calls_json: null,
      tool_call_id: null,
      tool_name: null,
      a2ui_jsonl: null,
      action_name: null,
      action_status: null,
      action_result: null,
      created_at: new Date().toISOString(),
    });
  }
});

// Auto-scroll when messages change
watch(
  () => [chatStore.messages.length, chatStore.currentStreamingMessage?.content.length],
  async () => {
    await nextTick();
    if (messagesContainer.value)
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  },
  { deep: true },
);

/** Send a normal text message. */
async function handleSend(content: string) {
  if (!content.trim() || chatStore.isStreaming || a2uiStore.showOverlay) return;

  // 1. Immediately add user message to the chat (before SSE streaming starts)
  chatStore.addMessage({
    id: -Date.now(),
    conversation_id: conversationStore.currentConversationId ?? 0,
    role: "user",
    message_type: "chat",
    content: content.trim(),
    tool_calls_json: null,
    tool_call_id: null,
    tool_name: null,
    a2ui_jsonl: null,
    action_name: null,
    action_status: null,
    action_result: null,
    created_at: new Date().toISOString(),
  });

  // 2. Start SSE streaming for the AI response
  const req = buildChatRequest(content, conversationStore.currentConversationId);
  await startStream(req);

  // 3. After streaming finishes, add AI response ONLY if no error occurred
  //    (error watcher handles adding error message when error is set)
  if (!error.value && streamingMessage.value?.content) {
    chatStore.addMessage({
      id: -(Date.now() + 1),
      conversation_id: streamingMessage.value.conversationId ?? 0,
      role: "assistant",
      message_type: "chat",
      content: streamingMessage.value.content,
      tool_calls_json: null,
      tool_call_id: null,
      tool_name: null,
      a2ui_jsonl: null,
      action_name: null,
      action_status: null,
      action_result: null,
      created_at: new Date().toISOString(),
    });
    if (streamingMessage.value.conversationId && !conversationStore.currentConversationId) {
      conversationStore.select(streamingMessage.value.conversationId);
    }
  }

  // 4. Always clean up streaming state
  chatStore.setStreamingMessage(null);
}

/** Load conversation history. */
async function onSelectConversation(id: number) {
  // Abort any active SSE stream to prevent background reactivity updates
  // that would race with clearMessages + loadHistory
  abort();
  chatStore.setStreamingMessage(null);
  chatStore.setStreaming(false);
  submittingMessageIds.value.clear();

  loadingHistory.value = true;
  chatStore.clearMessages();
  conversationStore.select(id);
  // Wait for Vue to finish removing old DOM nodes before loading new ones
  await nextTick();
  await chatStore.loadHistory(id);
  // action_result is now mapped directly onto form messages by the store,
  // and a2ui_action messages are filtered out — no additional detection needed.
  loadingHistory.value = false;
  await nextTick();
  if (messagesContainer.value)
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
}

async function onNewChat() {
  // Abort any active SSE stream to prevent background reactivity race
  abort();
  chatStore.setStreamingMessage(null);
  chatStore.setStreaming(false);
  submittingMessageIds.value.clear();

  chatStore.clearMessages();
  conversationStore.select(null);
  // Wait for Vue to finish removing old DOM nodes
  await nextTick();
  // Also clear stale msg refs to prevent stale references
  msgRefs.value.clear();
}

// Clean up on component unmount (e.g., route navigation away while streaming)
onBeforeUnmount(() => {
  abort();
  chatStore.setStreamingMessage(null);
  chatStore.setStreaming(false);
});

/** Handle A2UI form submission action.
 *  @param messageId - the ID of the chat message containing the submitted form.
 *                     Used to update the form's action_result in-place. */
async function handleA2UIAction(
  payload: { action: string; surfaceId: string; data: Record<string, unknown> },
  messageId?: number,
) {
  if (chatStore.isStreaming) return;
  const convId = conversationStore.currentConversationId;

  const wasOverlayOpen = a2uiStore.showOverlay;
  
  // Track submitting state
  if (messageId !== undefined) {
    submittingMessageIds.value.add(messageId);
  }
  
  const req = buildActionRequest(payload.action, payload.data, convId ?? 0);
  await startStream(req, "/api/chat");

  // Update conversation ID if it was newly created by this action
  if (!convId && streamingMessage.value?.conversationId) {
    conversationStore.select(streamingMessage.value.conversationId);
  }

  // Only process result if no error occurred (error watcher handles error display)
  if (!error.value && streamingMessage.value?.content) {
    if (wasOverlayOpen && a2uiStore.showOverlay) {
      // When overlay is open: result goes to overlay steps only
      a2uiStore.addStep(streamingMessage.value.content);
    } else if (messageId !== undefined) {
      const rawContent = streamingMessage.value.content;

      // Split content: A2UI JSONL messages → result surfaces; text → action_result on source message
      const parsed = parseA2UI(rawContent);
      const textResult = parsed.textLines.join('\n').trim();

      // Clean action_result: if A2UI result cards exist, use a brief status
      // message instead of the LLM's chain-of-thought text.
      const hasResultA2UI = parsed.messages.length > 0;
      const cleanResult = hasResultA2UI ? "操作完成" : textResult;

      // Update the source form message with the action result text
      chatStore.updateMessage(messageId, {
        action_result: cleanResult || null,
        action_status: "done",
      });

      // If the LLM returned new A2UI surfaces, append them to the source
      // form message so the result card renders inside the original bubble
      // (instead of creating a separate new message).
      if (hasResultA2UI) {
        const a2uiLines = parsed.messages.map((m) => JSON.stringify(m)).join('\n');
        const sourceMsg = chatStore.messages.find(m => m.id === messageId);
        if (sourceMsg) {
          const newA2uiJsonl = sourceMsg.a2ui_jsonl
            ? sourceMsg.a2ui_jsonl + '\n' + a2uiLines
            : a2uiLines;
          chatStore.updateMessage(messageId, { a2ui_jsonl: newA2uiJsonl });
        }
      }
    }
  } else if (error.value && messageId !== undefined) {
    // On error, mark the source form as failed
    chatStore.updateMessage(messageId, {
      action_result: error.value,
      action_status: "failed",
    });
  }

  // Clear submitting state
  if (messageId !== undefined) {
    submittingMessageIds.value.delete(messageId);
  }

  // Always clean up streaming state
  chatStore.setStreamingMessage(null);
}

</script>

<style scoped>
.chat-page { height: 100vh; display: flex; flex-direction: column; background: #f8fafb; font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
.chat-body { flex: 1; display: flex; overflow: hidden; min-height: 0; }

/* Panel – remove overflow:hidden from panel itself so toggle button can protrude */
.panel { position: relative; width: 256px; flex-shrink: 0; background: #fff; border-color: #e2e8f0; transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1); display: flex; flex-direction: column; }
.panel-left { border-right: 1px solid #e2e8f0; }
.panel.collapsed { width: 40px; }

/* Toggle button – slides with panel, moves inside when collapsed */
.panel-toggle {
  position: absolute; top: 50%; z-index: 10;
  width: 20px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  background: #fff; border: 1px solid #e2e8f0;
  cursor: pointer; color: #94a3b8; padding: 0;
  transform: translateY(-50%);
  transition: color 0.15s, background 0.15s, right 0.25s cubic-bezier(0.16, 1, 0.3, 1), left 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.panel-left .panel-toggle { right: -20px; border-left: none; border-radius: 0 6px 6px 0; }
.panel-left.collapsed .panel-toggle { right: 10px; border-left: 1px solid #e2e8f0; border-radius: 6px; }
.panel-toggle:hover { color: #2563eb; background: #f8fafb; }

/* Panel content – overflow hidden applies here, not on panel */
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
