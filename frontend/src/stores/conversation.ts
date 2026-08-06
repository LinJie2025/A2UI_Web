import { defineStore } from "pinia";
import { ref } from "vue";
import type { ConversationSummary, ConversationDetail } from "@/api/conversation";
import {
  getConversationsApi,
  getConversationApi,
  updateConversationApi,
  deleteConversationApi,
} from "@/api/conversation";

export const useConversationStore = defineStore("conversation", () => {
  const conversations = ref<ConversationSummary[]>([]);
  const currentConversationId = ref<number | null>(null);
  const loading = ref(false);

  /** Fetch all conversations for the sidebar list. */
  async function fetchList(): Promise<void> {
    loading.value = true;
    try {
      const resp = await getConversationsApi();
      if (resp.code === 0) {
        conversations.value = resp.data;
      }
    } finally {
      loading.value = false;
    }
  }

  /** Update conversation title. */
  async function updateTitle(id: number, title: string): Promise<void> {
    await updateConversationApi(id, title);
    const idx = conversations.value.findIndex((c) => c.id === id);
    if (idx !== -1) {
      conversations.value[idx] = { ...conversations.value[idx], title };
    }
  }

  /** Delete a conversation and remove from list. */
  async function removeConversation(id: number): Promise<void> {
    await deleteConversationApi(id);
    conversations.value = conversations.value.filter((c) => c.id !== id);
    if (currentConversationId.value === id) {
      currentConversationId.value = null;
    }
  }

  /** Set active conversation, load if needed. */
  function select(id: number | null): void {
    currentConversationId.value = id;
  }

  return {
    conversations,
    currentConversationId,
    loading,
    fetchList,
    updateTitle,
    removeConversation,
    select,
  };
});
