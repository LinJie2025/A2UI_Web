<template>
  <div class="tool-bubble ml-11">
    <div class="tool-card">
      <div :class="['tool-header', 'tool-status-' + toolCall.status]">
        <span class="tool-dot"></span>
        <span class="tool-name">{{ $t('toolCall.prefix') }} {{ toolCall.name }}</span>
        <span class="tool-status-text">
          {{ toolCall.status === 'running' ? $t('toolCall.running') : toolCall.status === 'success' ? $t('toolCall.success') : $t('toolCall.error') }}
        </span>
      </div>
      <div class="tool-body">
        <div v-if="toolCall.arguments" class="tool-section">
          <div class="tool-label">{{ $t('toolCall.arguments') }}</div>
          <pre class="tool-pre">{{ safeStringify(toolCall.arguments) }}</pre>
        </div>
        <div v-if="toolCall.result" class="tool-section">
          <div class="tool-label">{{ $t('toolCall.result') }}</div>
          <pre class="tool-pre">{{ JSON.stringify(toolCall.result, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ToolCallStatus } from "@/types/chat";

defineProps<{
  toolCall: ToolCallStatus;
}>();

function safeStringify(obj: unknown): string {
  try { return JSON.stringify(obj, null, 2); }
  catch { return String(obj); }
}
</script>

<style scoped>
.tool-bubble {
  margin-top: 0.5rem;
}

.tool-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  max-width: 480px;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.45rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
  border-bottom: 1px solid #f1f5f9;
}
.tool-status-running {
  background: #fef3c7;
  color: #92400e;
}
.tool-status-success {
  background: #d1fae5;
  color: #065f46;
}
.tool-status-error {
  background: #fee2e2;
  color: #991b1b;
}

.tool-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
.tool-status-running .tool-dot {
  background: #f59e0b;
  animation: pulse 1.2s ease-in-out infinite;
}
.tool-status-success .tool-dot { background: #10b981; }
.tool-status-error .tool-dot { background: #ef4444; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.tool-name {
  flex: 1;
}
.tool-status-text {
  font-size: 0.6875rem;
  opacity: 0.6;
  font-weight: 500;
}

.tool-body {
  padding: 0.5rem 0.75rem;
}
.tool-section {
  margin-bottom: 0.375rem;
}
.tool-section:last-child { margin-bottom: 0; }

.tool-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
  font-family: 'Outfit', system-ui, sans-serif;
}

.tool-pre {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6875rem;
  color: #475569;
  background: #f8fafc;
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  max-height: 160px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
}
.tool-pre::-webkit-scrollbar { width: 4px; }
.tool-pre::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
</style>
