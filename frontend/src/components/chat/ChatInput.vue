<template>
  <div class="chat-input-wrap">
    <textarea
      ref="textareaRef"
      v-model="inputText"
      class="chat-textarea"
      :disabled="disabled"
      :placeholder="$t('chat.inputPlaceholder')"
      rows="1"
      @keydown="handleKeydown"
      @input="autoResize"
    ></textarea>
    <button
      class="send-btn"
      :disabled="disabled || !inputText.trim()"
      @click="handleSend"
      :aria-label="$t('chat.sendAria')"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue";

defineProps<{
  disabled: boolean;
}>();

const emit = defineEmits<{
  (e: "send", content: string): void;
}>();

const inputText = ref("");
const textareaRef = ref<HTMLTextAreaElement | null>(null);

function autoResize() {
  nextTick(() => {
    const el = textareaRef.value;
    if (el) {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 140) + "px";
    }
  });
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
}

function handleSend() {
  const text = inputText.value.trim();
  if (!text) return;
  emit("send", text);
  inputText.value = "";
  nextTick(autoResize);
}
</script>

<style scoped>
.chat-input-wrap {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #fff;
  border-top: 1px solid #e2e8f0;
}

.chat-textarea {
  flex: 1;
  min-height: 44px;
  max-height: 140px;
  padding: 0.6rem 0.85rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #f8fafc;
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  font-size: 0.875rem;
  color: #1e293b;
  resize: none;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  line-height: 1.5;
}
.chat-textarea:focus {
  border-color: #93c5fd;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.08);
}
.chat-textarea::placeholder { color: #94a3b8; }
.chat-textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn {
  width: 44px; height: 44px;
  flex-shrink: 0;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: #fff;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 1px 3px rgba(37,99,235,0.2);
  transition: all 0.15s ease;
}
.send-btn:hover:not(:disabled) {
  background: #1d4ed8;
  box-shadow: 0 4px 12px rgba(37,99,235,0.25);
  transform: translateY(-1px);
}
.send-btn:active:not(:disabled) { transform: scale(0.95); }
.send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
