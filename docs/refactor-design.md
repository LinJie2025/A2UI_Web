# A2UI 历史消息存储重构 — 完整设计文档

> **作者**: 吴八哥 (Senior Developer)
> **日期**: 2026-08-04
> **版本**: v2.0 — 推翻旧架构重建

---

## 一、问题诊断

### 旧架构的 5 个核心问题

| # | 问题 | 表现 |
|---|------|------|
| 1 | **双表冗余** | messages 存对话上下文 + a2ui_actions 存业务状态，前端需要 mapActionsToMessages 手动对齐 |
| 2 | **跳过保存逻辑** | ChatService 通过 `if a2ui_action_id: skip` 避免重复存 user 消息，耦合严重 |
| 3 | **客户端过滤** | filterHistoryMessages() 在前端过滤 "用户提交了..." 自动生成消息 |
| 4 | **content 字段过载** | 纯文本、A2UI JSONL、tool_calls_json 全塞一个字段，类型混乱 |
| 5 | **状态追踪脆弱** | a2uiStatuses Map + pendingSubmitMsgIdx + error watcher 三重机制追踪状态，bug 多发 |

### 根因

**同一件事（表单提交）同时服务于「LLM 对话上下文」和「业务状态追踪」两种需求，但没有明确的数据边界。**

---

## 二、新架构设计原则

1. **一个事实，一处存储** — 消除双表冗余
2. **消息是消息，事务是事务** — messages 管对话流，actions 管业务状态，通过 FK 关联
3. **摘要优先，详情按需** — 列表页只加载摘要，详情页按需加载完整数据
4. **后端 JOIN，前端消费** — 不再需要客户端映射和对齐

---

## 三、数据库设计（7 表）

### 3.1 conversations (不变)

```sql
CREATE TABLE conversations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    title       VARCHAR(256),
    created_at  DATETIME NOT NULL DEFAULT (datetime('now')),
    updated_at  DATETIME NOT NULL DEFAULT (datetime('now'))
);
```

### 3.2 messages (简化)

```sql
CREATE TABLE messages (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id   INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role              VARCHAR(32) NOT NULL,  -- 'user' | 'assistant' | 'tool'
    created_at        DATETIME NOT NULL DEFAULT (datetime('now'))
);
```

**变化**: 移除 `content` / `tool_calls_json` / `tool_call_id` 列。

### 3.3 message_blocks (新增)

```sql
CREATE TABLE message_blocks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id    INTEGER NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    block_type    VARCHAR(32) NOT NULL,  -- 'text' | 'a2ui'
    sort_order    INTEGER NOT NULL DEFAULT 0,
    text_content  TEXT,
    a2ui_jsonl   TEXT,
    created_at    DATETIME NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_message_blocks_message_id ON message_blocks(message_id);
```

**示例**: 一条 assistant 消息 = 2 个 blocks（text + a2ui），sort_order 保序。

### 3.4 actions (新增，替代旧 a2ui_actions)

```sql
CREATE TABLE actions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id     INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    action_name         VARCHAR(128) NOT NULL,
    status              VARCHAR(32) NOT NULL DEFAULT 'submitted',
    latest_attempt      INTEGER NOT NULL DEFAULT 1,
    trigger_message_id  INTEGER REFERENCES messages(id),
    result_message_id   INTEGER REFERENCES messages(id),
    parent_action_id    INTEGER REFERENCES actions(id),  -- 未来: Tool 链
    created_at          DATETIME NOT NULL DEFAULT (datetime('now')),
    updated_at          DATETIME NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_actions_conv ON actions(conversation_id);
CREATE INDEX idx_actions_trigger ON actions(trigger_message_id);
CREATE INDEX idx_actions_result ON actions(result_message_id);
```

**status 状态机**: `submitted → processing → done | failed | interrupted`

### 3.5 action_attempts (新增)

```sql
CREATE TABLE action_attempts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    action_id       INTEGER NOT NULL REFERENCES actions(id) ON DELETE CASCADE,
    attempt_number  INTEGER NOT NULL,
    form_data       TEXT,         -- JSON
    status          VARCHAR(32) NOT NULL DEFAULT 'submitted',
    error_detail    TEXT,
    created_at      DATETIME NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_attempts_action ON action_attempts(action_id);
```

### 3.6 action_results (新增)

```sql
CREATE TABLE action_results (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    action_id         INTEGER NOT NULL UNIQUE REFERENCES actions(id) ON DELETE CASCADE,
    title             VARCHAR(256),
    summary           TEXT,
    a2ui_steps        TEXT,         -- JSON: [{title, status, jsonl}, ...]
    tool_call_count   INTEGER DEFAULT 0,
    total_duration_ms INTEGER DEFAULT 0,
    created_at        DATETIME NOT NULL DEFAULT (datetime('now'))
);
```

### 3.7 action_events (新增，按需加载)

```sql
CREATE TABLE action_events (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    action_id       INTEGER NOT NULL REFERENCES actions(id) ON DELETE CASCADE,
    event_type      VARCHAR(32) NOT NULL,  -- 'tool_call' | 'tool_result' | 'llm_response' | 'error'
    sort_order      INTEGER NOT NULL,
    summary         VARCHAR(256),
    detail          TEXT,         -- JSON
    duration_ms     INTEGER,
    parent_event_id INTEGER REFERENCES action_events(id),
    created_at      DATETIME NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_events_action ON action_events(action_id);
```

---

## 四、API 设计

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat` | SSE 流式聊天 |
| POST | `/api/a2ui/submit` | A2UI 表单提交 SSE |
| GET | `/api/conversations/{id}/messages` | 获取消息（含 blocks + 关联 action 摘要）|
| GET | `/api/actions/{id}` | 获取 action 概览（含 latest_attempt + result 摘要）|
| GET | `/api/actions/{id}/detail` | 获取 action 详情（含所有 attempts + a2ui_steps）|
| GET | `/api/actions/{id}/events` | 获取事件流（管理后台按需加载）|
| POST | `/api/actions/{id}/retry` | 重试失败的 action |

### 消息列表响应格式

```json
{
  "code": 0,
  "data": [
    {
      "id": 42,
      "role": "assistant",
      "created_at": "2026-08-04T10:00:00",
      "blocks": [
        {"type": "text", "text_content": "已为您创建采购订单："},
        {"type": "a2ui", "a2ui_jsonl": "{...}"}
      ],
      "action": {
        "id": 7,
        "name": "create_purchase_order",
        "status": "done",
        "summary": "PO-20240001 创建成功",
        "trigger_message_id": 41,
        "result_message_id": 42
      }
    }
  ]
}
```

---

## 五、前端组件变化

```
旧:                             新:
ChatView.vue                    ChatView.vue (删 60% 逻辑)
├─ filterHistoryMessages()      (删除)
├─ mapActionsToMessages()       (删除)
├─ a2uiStatuses Map             (删除)
├─ pendingSubmitMsgIdx          (删除)
├─ isSubmittingA2UI             (删除)
├─ extractActionSummary()       (删除)
├─ formatErrorAsA2UI()          (删除)
└─ handleA2UIAction()           (简化 → 只调 API + 更新 store)

ChatMessage.vue                 ChatMessage.vue
├─ v-if="hasA2UI"               (保留)
├─ A2UIRenderer                 (保留)
├─ statusBadge prop              → message.action?.status
└─ content 字段                  → message.blocks[] 遍历

A2UIOverlay.vue               → ActionDetailDrawer.vue (全新)
                               ├─ 左: 步骤列表 + 元信息
                               ├─ 中: A2UI 渲染 + 原始数据
                               └─ 右/底: 操作栏 (重试/复制/分享)
```

---

## 六、删减清单

| 删除的文件 |
|------------|
| `backend/app/models/a2ui_action.py` |
| `backend/app/services/a2ui_action_service.py` |

| 删除的代码 (ChatView.vue) |
|---------------------------|
| `filterHistoryMessages()` |
| `mapActionsToMessages()` |
| `a2uiStatuses` ref |
| `pendingSubmitMsgIdx` ref |
| `isSubmittingA2UI` ref |
| `extractActionSummary()` |
| `formatErrorAsA2UI()` |
| `handleA2UIAction()` (重写) |
| error watch 中的复杂逻辑 |

| 删除的组件 |
|------------|
| `A2UIOverlay.vue` |
