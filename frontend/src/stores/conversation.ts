import { defineStore } from "pinia";
import { ref } from "vue";
import type { ConversationSummary, ConversationDetail } from "@/api/conversation";
import {
  getConversationsApi,
  getConversationApi,
  getConversationMessagesApi,
  deleteConversationApi,
} from "@/api/conversation";

export const useConversationStore = defineStore("conversation", () => {
  const conversations = ref<ConversationSummary[]>([]);
  const currentConversationId = ref<number | null>(null);
  const currentDetail = ref<ConversationDetail | null>(null);
  const loading = ref(false);

  async function fetchConversations(): Promise<void> {
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

  async function loadConversation(id: number): Promise<void> {
    currentConversationId.value = id;
    const resp = await getConversationApi(id);
    if (resp.code === 0) {
      currentDetail.value = resp.data;
    }
  }

  async function deleteConversation(id: number): Promise<void> {
    await deleteConversationApi(id);
    conversations.value = conversations.value.filter((c) => c.id !== id);
    if (currentConversationId.value === id) {
      currentConversationId.value = null;
      currentDetail.value = null;
    }
  }

  function setCurrentConversation(id: number | null) {
    currentConversationId.value = id;
    if (id === null) {
      currentDetail.value = null;
    }
  }

  return {
    conversations,
    currentConversationId,
    currentDetail,
    loading,
    fetchConversations,
    loadConversation,
    deleteConversation,
    setCurrentConversation,
  };
});
