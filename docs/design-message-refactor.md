# A2UI_Web 消息对话存储重构 — 架构设计文档

> 版本：v2.0 | 日期：2026-08-04 | 基于 24 项需求盘问决策

---

## 1. 设计目标

解决当前消息存储的「三层断裂」问题：
- **数据库层**：缺少 tool 角色消息、A2UI surface 无持久化
- **后端层**：手写 dict 无 schema 验证、双端点代码重复
- **前端层**：类型不一致、Store 状态重复

---

## 2. 数据库设计

### 2.1 conversations 表（保持原有结构）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| user_id | INTEGER FK | 用户 ID |
| title | TEXT (nullable) | 自动标题 + 支持用户手动编辑 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 2.2 messages 表（全新设计）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER PK | AUTOINCREMENT | 主键 |
| conversation_id | INTEGER FK | NOT NULL, INDEXED | 所属对话 |
| role | TEXT | NOT NULL | `user` / `assistant` / `tool` |
| message_type | TEXT | DEFAULT "chat" | `chat` / `a2ui_action` |
| content | TEXT | nullable | 消息纯文本 |
| tool_calls_json | TEXT | nullable | assistant 消息的工具调用 JSON |
| tool_call_id | TEXT | nullable | tool 消息对应的 call ID |
| tool_name | TEXT | nullable | tool 消息对应的工具名 |
| a2ui_jsonl | TEXT | nullable | A2UI 原始 JSONL |
| action_name | TEXT | nullable | A2UI 表单 action 名 |
| action_status | TEXT | nullable | submitted / processing / done / failed |
| created_at | DATETIME | NOT NULL | 创建时间 |

**索引**：
- `idx_messages_conversation_id` ON (conversation_id)
- `idx_messages_created_at` ON (conversation_id, created_at)

**删除**：
- ~~a2ui_actions 表~~（功能合并到 messages）

### 2.3 消息类型说明

| message_type | role | 示例 | 前端展示 |
|---|---|---|---|
| chat | user | "帮我查联系人" | 用户气泡 |
| chat | assistant | "张三的电话是..." (+ a2ui_jsonl) | AI 气泡（文本 + A2UI） |
| chat | tool | tool_call 执行结果 | 默认隐藏 |
| a2ui_action | user | 用户点击提交按钮 | A2UI 表单提交气泡（横向 Stepper） |

---

## 3. 后端架构

### 3.1 API 端点

```
POST /api/chat              → 统一聊天端点（SSE 流式）
GET  /api/conversations      → 对话列表（Pydantic Schema）
GET  /api/conversations/{id} → 对话详情 + 消息列表
PUT  /api/conversations/{id} → 编辑对话标题
DELETE /api/conversations/{id} → 删除对话
```

**删除**：
- ~~POST /api/a2ui/submit~~ → 合并到 /api/chat
- ~~GET /api/conversations/{id}/messages~~ → 合并到对话详情
- ~~GET /api/conversations/{id}/actions~~ → 合并到对话详情的消息列表

### 3.2 统一请求格式

```json
POST /api/chat
{
  "conversation_id": 123 | null,
  "message": {
    "role": "user",
    "content": "帮我查联系人",
    "meta": {
      "action_name": "create_contact",     // 可选：A2UI 表单提交
      "form_data": {"name": "张三"}
    }
  },
  "context_messages": []     // 可选：多轮对话上下文
}
```

### 3.3 SSE 事件流

```
event: user_message_saved
data: {"conversation_id": 5}

event: text
data: {"delta": "好的"}

event: tool_call
data: {"id": "call_xxx", "name": "search", "arguments": {...}}

event: tool_result
data: {"id": "call_xxx", "name": "search", "result": {...}}

event: done
data: {"conversation_id": 5}
```

### 3.4 消息保存策略

**延迟批量保存**：
1. SSE 流开始时保存 user 消息
2. Agent loop 运行期间 tool 消息暂存内存
3. Agent loop 结束后，user + tool + assistant 在同一事务中批量写入
4. 避免孤立消息问题

### 3.5 LLM 上下文重建规则

从数据库加载历史消息 → 构建 LLM 上下文时：

| 条件 | 处理 |
|------|------|
| role=user, message_type=chat | ✅ content 加入上下文 |
| role=user, message_type=a2ui_action | 转为文本 "用户提交了表单：{action_name}，数据：{form_data}" |
| role=assistant, 有 content | ✅ content 加入上下文 |
| role=assistant, 有 a2ui_jsonl | ❌ a2ui_jsonl 不加入上下文 |
| role=tool | ✅ tool_call_id + content 加入上下文 |

---

## 4. 前端架构

### 4.1 Store 结构

```
chatStore（消息状态 - 唯一数据源）
  ├── messages: Message[]
  ├── currentConversationId: number | null
  ├── isStreaming: boolean
  ├── loadHistory(id)
  ├── sendMessage(body)
  └── clearMessages()

conversationStore（对话列表）
  ├── list: ConversationSummary[]
  └── fetchList() / delete(id) / updateTitle(id, title)

A2UIStore（Surface 管理）
  ├── surfaces: Map<surfaceId, SurfaceState>
  └── overlay: OverlayState
```

### 4.2 消息渲染规则

```
普通文字聊天：
  ┌──────────────────────┐
  │ 👤 用户气泡           │
  ├──────────────────────┤
  │ 🤖 AI 气泡            │
  │  "张三的电话是 138"    │
  │  ┌─────────────────┐ │
  │  │ A2UI 列表卡片    │ │  ← 来自 a2ui_jsonl
  │  └─────────────────┘ │
  └──────────────────────┘
  tool call 在气泡内显示小步骤指示器（🔧 正在查询... → ✅ 查询完成）

A2UI 表单提交：
  ┌──────────────────────┐
  │ 📋 创建联系人         │
  │ ●━━━●━━━○            │
  │ 提交  处理中  完成    │  ← 横向 Stepper
  │                      │
  │ [当前步骤内容区]       │
  │                      │
  │   [上一步] [下一步]    │
  └──────────────────────┘
  所有 tool call + assistant 回复合并为一个气泡
```

### 4.3 右侧操作面板

- 只展示 `message_type=a2ui_action` 的消息
- 显示内容：action_name（如 "创建联系人"）
- 点击跳转到对应气泡位置

### 4.4 tool 消息展示

- role=tool 的消息默认隐藏
- 前端根据 `role === "tool"` 判定，不渲染

---

## 5. 迁移策略

**推倒重来**：
1. 删除旧的 `conversations` 和 `messages` 表数据
2. 删除 `a2ui_actions` 表
3. 使用 `Base.metadata.create_all` 创建新表
4. 旧数据不保留（开发阶段，无生产数据）

---

## 6. 类型定义对照

### 6.1 后端 Pydantic Schema

```python
class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str                              # user / assistant / tool
    message_type: str = "chat"             # chat / a2ui_action
    content: str | None
    tool_calls_json: str | None
    tool_call_id: str | None
    tool_name: str | None
    a2ui_jsonl: str | None
    action_name: str | None
    action_status: str | None
    created_at: str                        # ISO format
    model_config = {"from_attributes": True}

class ConversationDetailResponse(BaseModel):
    id: int; user_id: int; title: str | None
    created_at: str; updated_at: str
    message_count: int; last_message: str | None
    messages: list[MessageResponse]
    model_config = {"from_attributes": True}
```

### 6.2 前端 TypeScript

```typescript
interface Message {
  id: number; conversation_id: number
  role: 'user' | 'assistant' | 'tool'
  message_type: 'chat' | 'a2ui_action'
  content: string | null
  tool_calls_json: string | null
  tool_call_id: string | null
  tool_name: string | null
  a2ui_jsonl: string | null
  action_name: string | null
  action_status: 'submitted' | 'processing' | 'done' | 'failed' | null
  created_at: string
}
```
