import { defineStore } from "pinia";
import { ref } from "vue";
import type { Message, StreamingMessage } from "@/types/chat";
import { getConversationApi } from "@/api/conversation";

export const useChatStore = defineStore("chat", () => {
  /** All messages in the current conversation (single source of truth). */
  const messages = ref<Message[]>([]);
  /** The streaming message being built from SSE. */
  const currentStreamingMessage = ref<StreamingMessage | null>(null);
  /** Whether SSE stream is active. */
  const isStreaming = ref(false);
  /** Current conversation ID. */
  const currentConversationId = ref<number | null>(null);

  /** Load messages from backend for a given conversation. */
  async function loadHistory(conversationId: number): Promise<void> {
    currentConversationId.value = conversationId;
    try {
      const resp = await getConversationApi(conversationId);
      if (resp.code === 0 && resp.data) {
        const rawMessages: Message[] = resp.data.messages || [];

        // Post-process: map a2ui_action results to the preceding assistant
        // message that contains the A2UI form, then remove a2ui_action messages.
        const processed: Message[] = [];
        let lastFormIndex = -1; // index in processed[] of the last assistant message with A2UI form

        for (const msg of rawMessages) {
          if (msg.message_type === "a2ui_action") {
            // Map action results onto the preceding form-bearing assistant message
            if (lastFormIndex >= 0) {
              const patch: Partial<Message> = {};
              if (msg.action_result) {
                patch.action_result = msg.action_result;
                patch.action_status = msg.action_status;
              }
              // Append result A2UI JSONL (error / success card) to the form
              // message so it renders below the form in the same bubble.
              if (msg.a2ui_jsonl) {
                const existing = processed[lastFormIndex].a2ui_jsonl || "";
                patch.a2ui_jsonl = existing
                  ? existing + "\n" + msg.a2ui_jsonl
                  : msg.a2ui_jsonl;
              }
              if (Object.keys(patch).length > 0) {
                processed[lastFormIndex] = {
                  ...processed[lastFormIndex],
                  ...patch,
                };
              }
            }
            // Skip a2ui_action messages — they are not displayed in the chat
            continue;
          }

          processed.push(msg);

          // Track the last assistant message that has a2ui form content
          if (msg.role === "assistant" && msg.a2ui_jsonl) {
            lastFormIndex = processed.length - 1;
          }
        }

        messages.value = processed;
      }
    } catch {
      messages.value = [];
    }
  }

  /** Update a message in-place by id (merge patch fields). */
  function updateMessage(id: number | string, patch: Partial<Message>): void {
    const idx = messages.value.findIndex((m) => m.id === id);
    if (idx !== -1) {
      messages.value[idx] = { ...messages.value[idx], ...patch };
    }
  }

  /** Append a completed message (from streaming or manual). */
  function addMessage(msg: Message): void {
    messages.value.push(msg);
  }

  /** Replace all messages. */
  function setMessages(msgs: Message[]): void {
    messages.value = msgs;
  }

  /** Set streaming state. */
  function setStreamingMessage(msg: StreamingMessage | null): void {
    currentStreamingMessage.value = msg;
  }
  function setStreaming(active: boolean): void {
    isStreaming.value = active;
  }

  /** Clear all state (used when switching conversations). */
  function clearMessages(): void {
    messages.value = [];
    currentStreamingMessage.value = null;
    isStreaming.value = false;
    currentConversationId.value = null;
  }

  return {
    messages,
    currentStreamingMessage,
    isStreaming,
    currentConversationId,
    loadHistory,
    addMessage,
    updateMessage,
    setMessages,
    setStreamingMessage,
    setStreaming,
    clearMessages,
  };
});
