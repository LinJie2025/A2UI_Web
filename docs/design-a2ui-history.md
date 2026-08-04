# A2UI 历史记录功能 — 设计文档

> **创建时间**: 2026-08-03  
> **状态**: 设计已确认（Grill Me 盘问通过）



---

## 一、需求概述

全链路记录用户在 A2UI 聊天中的操作留痕，包括：

- 聊天消息（已有）
- A2UI 表单填写数据（新增）
- 操作状态 / 结果（新增）

---

## 二、已确认的设计决策

| #  | 决策点               | 结论                                                               |
| -- | ----------------- | ---------------------------------------------------------------- |
| 1  | 数据范围              | **C — 全链路**：聊天 + 表单数据 + 操作状态                                     |
| 2  | 表单上报时机            | **A — 点击提交按钮时**                                                  |
| 3  | 提交后处理链路           | **A — 走 Agent Loop**：formData → user message → LLM → Odoo Tool   |
| 4  | 数据模型              | **B — 新建独立 `a2ui_actions` 表**                                    |
| 5  | 状态流转              | **B — 三态**：submitted → processing → done / failed，含 error_detail |
| 6  | 僵尸状态处理            | **A — finally 清扫**：stream_chat() finally 中超时未完成 → interrupted    |
| 7  | API 设计            | **B — 新建 `POST /api/a2ui/submit`**，内部调用 chat_service             |
| 8  | 提交 Payload        | **A — 简洁型**：`{ conversation_id, action_name, form_data }`        |
| 9  | 前端展示              | **B — 聊天 + 侧边操作日志**                                              |
| 10 | result_summary 来源 | 后端从 tool result 自动提取（非 LLM 生成）                                   |
| 11 | 多次 action         | 一个 conversation 允许多条 a2ui_actions 记录                             |

---

## 三、数据模型

### 3.1 新建表：`a2ui_actions`

```sql
CREATE TABLE a2ui_actions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    action_name     VARCHAR(128) NOT NULL,       -- 按钮 action.name，如 "create_order"
    form_data       TEXT,                         -- JSON: 用户提交的表单数据快照
    status          VARCHAR(32) NOT NULL DEFAULT 'submitted',
        -- submitted → processing → done / failed / interrupted
    result_summary  TEXT,                         -- 成功时的摘要（从 tool result 提取）
    error_detail    TEXT,                         -- 失败时的错误信息
    tool_call_id    VARCHAR(128),                 -- 关联 messages 表中的 tool 调用
    created_at      DATETIME NOT NULL DEFAULT (datetime('now')),
    updated_at      DATETIME NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_a2ui_actions_conv ON a2ui_actions(conversation_id);
CREATE INDEX idx_a2ui_actions_status ON a2ui_actions(status);
```

### 3.2 字段说明

| 字段               | 说明                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------- |
| `form_data`      | 用户填写的全部表单字段值，JSON 格式。例：`{"supplier":"深圳电子","qty":100}`                                  |
| `status`         | `submitted`（已提交）→ `processing`（Agent Loop 推理中）→ `done` / `failed`。超时未完成 → `interrupted` |
| `result_summary` | 从 Odoo tool 返回结果中截取，如 "PO-2024-001 创建成功"                                                |
| `error_detail`   | tool 调用失败或 LLM 异常时的错误原文                                                                 |
| `tool_call_id`   | 关联到 `messages` 表中 role=tool 的记录                                                         |

---

## 四、API 设计

### 4.1 `POST /api/a2ui/submit`

**请求体：**

```json
{
  "conversation_id": 42,
  "action_name": "create_order",
  "form_data": {
    "supplier": "深圳电子科技",
    "qty": 100,
    "amount": 50000
  }
}
```

**响应：** SSE 流（复用现有 `text/tool_call/tool_result/done/error` 事件格式）

**处理流程：**

1. 接收请求 → 验证 conversation 归属
2. 创建 `a2ui_actions` 记录（status=submitted）
3. 将 form_data 转换为自然语言 user message：
   > 用户提交了「create_order」操作，表单数据如下：供应商=深圳电子科技，数量=100，金额=50000
4. 调用 `chat_service.stream_chat()` 进入 Agent Loop
5. Agent Loop 中：
   - 状态更新为 `processing`
   - tool_call 执行后提取结果写入 `result_summary` / `error_detail`
   - done → `done`，failed → `failed`
6. finally 块清扫：超时未完成 → `interrupted`

### 4.2 `GET /api/conversations/{id}/actions`

返回指定 conversation 下的所有 a2ui_actions 记录（用于侧边操作日志）。

**响应：**

```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "action_name": "create_order",
      "form_data": { "supplier": "深圳电子科技", "qty": 100 },
      "status": "done",
      "result_summary": "采购订单 PO-2024-001 已创建",
      "created_at": "2026-08-03T09:00:00Z"
    }
  ],
  "message": "success"
}
```

---

## 五、状态流转

```
  ┌──────────┐     POST /a2ui/submit     ┌────────────┐
  │ (无记录)  │ ────────────────────────▶ │ submitted  │
  └──────────┘                            └─────┬──────┘
                                                │ Agent Loop 开始
                                         ┌──────▼──────┐
                                         │ processing  │
                                         └──────┬──────┘
                                    ┌───────────┼───────────┐
                                    │           │           │
                               tool 成功    tool 失败   finally 超时
                                    │           │           │
                              ┌─────▼──┐  ┌────▼────┐  ┌────▼───────┐
                              │  done  │  │ failed  │  │interrupted │
                              └────────┘  └─────────┘  └────────────┘
```

### 5.1 超时清扫逻辑（finally 块）

```python
# chat_service.stream_chat() finally:
TIMEOUT_MINUTES = 5
cutoff = datetime.now(timezone.utc) - timedelta(minutes=TIMEOUT_MINUTES)
await db.execute(
    update(A2UIAction)
    .where(
        A2UIAction.conversation_id == conversation_id,
        A2UIAction.status == "processing",
        A2UIAction.updated_at < cutoff,
    )
    .values(status="interrupted")
)
await db.commit()
```

---

## 六、前端展示方案

### 6.1 历史记录页面布局

```
┌──────────────────────────┬─────────────────────┐
│                          │                     │
│    聊天记录回放区         │   操作日志侧栏       │
│    (70% 宽度)             │   (30% 宽度)         │
│                          │                     │
│  User: 帮我创建采购订单   │  ┌─────────────────┐ │
│                          │  │ create_order    │ │
│  [A2UI 表单卡片]          │  │ ✅ 已完成        │ │
│  供应商: 深圳电子科技      │  │ PO-2024-001     │ │
│  数量: 100               │  │ 3分钟前          │ │
│  [提交按钮]               │  └─────────────────┘ │
│                          │  ┌─────────────────┐ │
│  Assistant: 已创建订单    │  │ check_stock     │ │
│  PO-2024-001 ...        │  │ ❌ 失败          │ │
│                          │  │ 库存不足         │ │
│                          │  └─────────────────┘ │
└──────────────────────────┴─────────────────────┘
```

### 6.2 侧栏操作日志每条显示

- **操作名**（action_name 的可读化，如 create_order → "创建采购订单"）
- **状态 Badge**：✅ 已完成 / ⏳ 处理中 / ❌ 失败 / ⚠️ 已中断
- **结果摘要**（done 时）或错误简述（failed 时）
- **时间**（相对时间或绝对时间）

点击任意条目可展开查看完整表单数据。

---

## 七、实现步骤

### Phase 1 — 后端数据层

1. 创建 `A2UIAction` ORM Model（`backend/app/models/`）
2. 生成数据库迁移（新增 `a2ui_actions` 表）
3. 创建 Pydantic Schema（`backend/app/schemas/`）

### Phase 2 — 后端 API

1. 实现 `POST /api/a2ui/submit`（`backend/app/api/`）
2. 实现 `GET /api/conversations/{id}/actions`
3. 在 `chat_service.stream_chat()` finally 块中加入超时清扫

### Phase 3 — 前端

1. 新建 `api/action.ts` 前端 API 模块
2. A2UI 渲染组件中监听 Button action，触发提交
3. 历史记录页面新增侧栏操作日志组件
4. 实现状态 Badge、展开详情等交互

### Phase 4 — 联调 & 测试

1. 端到端测试：对话 → 表单提交 → Agent Loop → 结果记录
2. 边界测试：SSE 中断 → interrupted 状态

---

## 八、待定事项

> 以下决策暂缓，后续由 PM 确认：

- **action_name 映射表**：前端展示时 `create_order` 是否需要映射为用户可读的中文名？如果 action 种类少（< 10），可以前端写死映射；如果多，需要后端维护映射表
- **form_data 是否加密**：Odoo API key 已加密，表单数据是否也需要（可能含敏感业务数据如金额、供应商）
