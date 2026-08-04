<template>
  <aside class="action-sidebar">
    <div class="sidebar-header">
      <h3 class="sidebar-title">{{ $t('actionLog.title') }}</h3>
      <span v-if="actions.length > 0" class="action-count">{{ actions.length }}</span>
    </div>

    <div v-if="loading" class="sidebar-loading">
      <div class="skeleton-item" v-for="i in 3" :key="i">
        <div class="skeleton-line w-3/4"></div>
        <div class="skeleton-line w-1/2"></div>
      </div>
    </div>

    <div v-else-if="error" class="sidebar-error">
      {{ $t('actionLog.loadError') }}
    </div>

    <div v-else-if="actions.length === 0" class="sidebar-empty">
      <span class="empty-icon">📋</span>
      <span>{{ $t('actionLog.empty') }}</span>
    </div>

    <ul v-else class="action-list">
      <li
        v-for="(action, idx) in actions"
        :key="action.id"
        class="action-item"
        :class="{ 'is-expanded': expandedId === action.id }"
        @click="handleClick(action, idx)"
      >
        <div class="action-row">
          <span class="action-name">{{ formatActionName(action.action_name) }}</span>
          <span class="action-status" :class="`status-${action.status}`">
            {{ statusLabel(action.status) }}
          </span>
        </div>

        <div class="action-summary">
          <template v-if="action.status === 'done'">
            {{ action.result_summary || $t('actionLog.noSummary') }}
          </template>
          <template v-else-if="action.status === 'failed'">
            {{ action.error_detail || $t('actionLog.unknownError') }}
          </template>
          <template v-else-if="action.status === 'processing'">
            {{ $t('actionLog.processingHint') }}
          </template>
          <template v-else-if="action.status === 'interrupted'">
            {{ $t('actionLog.interruptedHint') }}
          </template>
        </div>

        <div class="action-time">
          {{ formatTime(action.created_at) }}
        </div>

        <!-- Expanded detail -->
        <div v-if="expandedId === action.id" class="action-detail">
          <div v-if="action.form_data && Object.keys(action.form_data).length > 0" class="detail-section">
            <h4>{{ $t('actionLog.formData') }}</h4>
            <table class="form-data-table">
              <tr v-for="(value, key) in action.form_data" :key="key">
                <td class="field-key">{{ key }}</td>
                <td class="field-value">{{ value }}</td>
              </tr>
            </table>
          </div>

          <div v-if="action.tool_call_id" class="detail-section">
            <span class="detail-label">Tool Call ID:</span>
            <code>{{ action.tool_call_id }}</code>
          </div>

          <div class="detail-section">
            <span class="detail-label">{{ $t('actionLog.updatedAt') }}:</span>
            <span>{{ formatTime(action.updated_at) }}</span>
          </div>
        </div>
      </li>
    </ul>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useI18n } from "vue-i18n";
import type { A2UIAction } from "@/types/action";
import { getConversationActionsApi } from "@/api/action";

const { t } = useI18n();

const props = defineProps<{
  conversationId: number;
}>();

const emit = defineEmits<{
  (e: "scroll-to", index: number): void;
}>();

const actions = ref<A2UIAction[]>([]);
const loading = ref(false);
const error = ref(false);
const expandedId = ref<number | null>(null);

/** Load actions from API */
async function loadActions() {
  if (!props.conversationId) return;
  loading.value = true;
  error.value = false;
  try {
    const resp = await getConversationActionsApi(props.conversationId);
    actions.value = resp.data ?? [];
  } catch {
    error.value = true;
  } finally {
    loading.value = false;
  }
}

/** Handle click: toggle expand + scroll to position */
function handleClick(action: A2UIAction, idx: number) {
  expandedId.value = expandedId.value === action.id ? null : action.id;
  // Scroll center chat to the corresponding message
  // Actions are ordered chronologically, message index ~= action index * 2 (user+assistant per action)
  // plus any preceding messages. Use a rough mapping: action_idx * 3 as approximate position.
  emit("scroll-to", idx * 3);
}

/** Format action_name for display */
function formatActionName(raw: string): string {
  const map: Record<string, string> = {
    create_order: t('actionLog.createOrder'),
    check_stock: t('actionLog.checkStock'),
    search: t('actionLog.search'),
    create: t('actionLog.create'),
    update: t('actionLog.update'),
    delete: t('actionLog.delete'),
  };
  return map[raw] || raw;
}

/** Get human-readable status label */
function statusLabel(status: string): string {
  const map: Record<string, string> = {
    submitted: t('actionLog.statusSubmitted'),
    processing: t('actionLog.statusProcessing'),
    done: t('actionLog.statusDone'),
    failed: t('actionLog.statusFailed'),
    interrupted: t('actionLog.statusInterrupted'),
  };
  return map[status] || status;
}

/** Format ISO time to relative or absolute */
function formatTime(iso: string): string {
  if (!iso) return "";
  const date = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);

  if (diffMin < 1) return t('actionLog.justNow');
  if (diffMin < 60) return `${diffMin}${t('actionLog.minAgo')}`;
  if (diffMin < 1440) return `${Math.floor(diffMin / 60)}${t('actionLog.hourAgo')}`;
  return date.toLocaleDateString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

onMounted(loadActions);
watch(() => props.conversationId, loadActions);
</script>

<style scoped>
.action-sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--sidebar-bg, #f8fafb);
  border-left: 1px solid var(--border-color, #e2e8f0);
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1rem 0.75rem;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.sidebar-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
  margin: 0;
}

.action-count {
  font-size: 0.75rem;
  background: #2563eb;
  color: #fff;
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
  font-weight: 500;
}

.sidebar-loading,
.sidebar-error,
.sidebar-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 2rem 1rem;
  color: var(--text-secondary, #64748b);
  font-size: 0.813rem;
}

.skeleton-item {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
}

.skeleton-line {
  height: 0.75rem;
  background: var(--skeleton-bg, #e2e8f0);
  border-radius: 4px;
  animation: shimmer 1.5s infinite;
}

.w-3\/4 { width: 75%; }
.w-1\/2 { width: 50%; }

@keyframes shimmer {
  0% { opacity: 1; }
  50% { opacity: 0.4; }
  100% { opacity: 1; }
}

.action-list {
  flex: 1;
  overflow-y: auto;
  list-style: none;
  margin: 0;
  padding: 0.5rem;
}

.action-item {
  padding: 0.625rem 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s;
  margin-bottom: 0.25rem;
}

.action-item:hover {
  background: var(--hover-bg, rgba(37, 99, 235, 0.04));
  transform: translateY(-1px);
}

.action-item.is-expanded {
  background: var(--hover-bg, rgba(37, 99, 235, 0.06));
}

.action-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.action-name {
  font-size: 0.813rem;
  font-weight: 600;
  color: var(--text-primary, #1e293b);
}

.action-status {
  font-size: 0.688rem;
  font-weight: 500;
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
  white-space: nowrap;
}

.status-done {
  background: #dcfce7;
  color: #16a34a;
}

.status-failed {
  background: #fef2f2;
  color: #dc2626;
}

.status-processing {
  background: #dbeafe;
  color: #2563eb;
}

.status-submitted {
  background: #f3f4f6;
  color: #6b7280;
}

.status-interrupted {
  background: #fef9c3;
  color: #ca8a04;
}

.action-summary {
  font-size: 0.75rem;
  color: var(--text-secondary, #64748b);
  line-height: 1.4;
  margin-bottom: 0.25rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.action-item.is-expanded .action-summary {
  -webkit-line-clamp: unset;
}

.action-time {
  font-size: 0.688rem;
  color: var(--text-tertiary, #94a3b8);
}

.action-detail {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border-color, #e2e8f0);
  font-size: 0.75rem;
}

.detail-section {
  margin-bottom: 0.5rem;
}

.detail-section h4 {
  font-size: 0.75rem;
  font-weight: 600;
  margin: 0 0 0.375rem;
  color: var(--text-primary, #1e293b);
}

.form-data-table {
  width: 100%;
  border-collapse: collapse;
}

.form-data-table td {
  padding: 0.25rem 0.5rem;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.field-key {
  font-weight: 500;
  color: var(--text-primary, #1e293b);
  width: 40%;
}

.field-value {
  color: var(--text-secondary, #64748b);
  word-break: break-word;
}

.detail-label {
  font-weight: 500;
  color: var(--text-primary, #1e293b);
  margin-right: 0.25rem;
}

code {
  font-size: 0.688rem;
  background: var(--code-bg, #f1f5f9);
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-family: "JetBrains Mono", monospace;
}
</style>
