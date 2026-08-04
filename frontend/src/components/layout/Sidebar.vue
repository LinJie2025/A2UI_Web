<template>
  <aside class="sidebar">
    <!-- New Chat -->
    <div class="sidebar-header">
      <button class="btn-new-chat" @click="handleNewChat">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        {{ $t('sidebar.newChat') }}
      </button>
    </div>

    <!-- Conversation list -->
    <nav class="conv-list">
      <div
        v-for="conv in convStore.conversations"
        :key="conv.id"
        :class="['conv-item', { active: conv.id === convStore.currentConversationId }]"
        @click="handleSelect(conv)"
      >
        <div class="conv-main">
          <svg class="conv-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
          <span class="conv-title">{{ conv.title || $t('sidebar.newSession') }}</span>
        </div>
        <button class="conv-delete" :title="$t('sidebar.deleteTitle')" @click.stop="handleDelete(conv.id)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
        </button>
      </div>

      <div v-if="convStore.conversations.length === 0" class="conv-empty">
        {{ $t('sidebar.empty') }}
      </div>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useConversationStore } from "@/stores/conversation";
import { useChatStore } from "@/stores/chat";

const convStore = useConversationStore();
const chatStore = useChatStore();

const emit = defineEmits<{
  (e: "new-chat"): void;
  (e: "select-conversation", id: number): void;
}>();

onMounted(() => {
  convStore.fetchConversations();
});

function handleNewChat() {
  convStore.setCurrentConversation(null);
  chatStore.clearMessages();
  emit("new-chat");
}

async function handleSelect(conv: { id: number }) {
  convStore.setCurrentConversation(conv.id);
  emit("select-conversation", conv.id);
}

async function handleDelete(id: number) {
  await convStore.deleteConversation(id);
  if (convStore.currentConversationId === id) {
    chatStore.clearMessages();
  }
}
</script>

<style scoped>
.sidebar {
  width: 256px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-right: 1px solid #e2e8f0;
  overflow: hidden;
}

.sidebar-header {
  padding: 0.75rem;
}
.btn-new-chat {
  font-family: 'Outfit', system-ui, sans-serif;
  font-weight: 600;
  font-size: 0.8125rem;
  padding: 0.55rem 0;
  border: none;
  border-radius: 8px;
  background: #2563eb;
  color: #fff;
  cursor: pointer;
  width: 100%;
  min-height: 44px;
  display: flex; align-items: center; justify-content: center; gap: 0.375rem;
  box-shadow: 0 1px 3px rgba(37,99,235,0.2);
  transition: all 0.15s ease;
}
.btn-new-chat:hover {
  background: #1d4ed8;
  box-shadow: 0 4px 12px rgba(37,99,235,0.25);
  transform: translateY(-1px);
}
.btn-new-chat:active { transform: scale(0.97); }

.conv-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 0.5rem 0.5rem;
}
.conv-list::-webkit-scrollbar { width: 4px; }
.conv-list::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

.conv-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.55rem 0.65rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.8125rem;
  color: #475569;
  transition: all 0.12s ease;
  margin-bottom: 2px;
}
.conv-item:hover { background: #f8fafc; color: #1e293b; }
.conv-item.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
  border: 1px solid rgba(37,99,235,0.12);
}

.conv-main {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  overflow: hidden;
  flex: 1;
}
.conv-icon { flex-shrink: 0; opacity: 0.5; }
.conv-item.active .conv-icon { opacity: 1; }
.conv-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-delete {
  background: none;
  border: none;
  color: #cbd5e1;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  flex-shrink: 0;
  opacity: 0;
  transition: all 0.15s;
}
.conv-item:hover .conv-delete { opacity: 1; }
.conv-delete:hover {
  color: #ef4444;
  background: #fef2f2;
}

.conv-empty {
  padding: 2rem 1rem;
  text-align: center;
  font-size: 0.8125rem;
  color: #94a3b8;
}
</style>
