# A2UI 协议调研报告

> 日期: 2026-07-31
> 来源: https://a2ui.org/ + GitHub https://github.com/a2ui-project/a2ui

---

## 1. A2UI 是什么

**A2UI (Agent-to-User Interface)** 是 Google 开源的协议标准，让 AI Agent 能够生成丰富的、交互式的用户界面，并通过声明式 JSON 数据跨 Web/移动/桌面原生渲染——**不执行任何代码**。

- 开源协议：Apache 2.0
- 当前版本：v0.9.1（生产），v1.0（候选）
- 创建者：Google，CopilotKit 和开源社区贡献

### 核心设计理念

| 原则 | 说明 |
|------|------|
| **安全优先** | 声明式数据格式，非可执行代码。Agent 只能使用客户端预批准的组件目录 |
| **LLM 友好** | 扁平 JSON 结构 + 邻接表模型，LLM 可增量生成，不需要一次性输出完美嵌套 JSON |
| **框架无关** | 同一 Agent 响应可在 Angular / Flutter / React / Lit 等渲染器上工作 |
| **渐进渲染** | 流式传输 UI 更新，用户实时看到界面构建过程 |

---

## 2. 真实 A2UI 协议格式

### 2.1 消息类型（v0.9.1）

**服务器 → 客户端** 共 4 种消息：

```
createSurface     → 创建渲染表面，指定组件目录
updateComponents  → 添加/更新组件（邻接表模型）
updateDataModel   → 更新数据模型（JSON Pointer 路径）
deleteSurface     → 删除表面
```

**客户端 → 服务器**：

```
action  → 用户交互（按钮点击等）
error   → 客户端错误报告
```

### 2.2 完整 JSONL 流示例

```jsonl
{"version":"v0.9.1","createSurface":{"surfaceId":"contact_form","catalogId":"https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json"}}
{"version":"v0.9.1","updateComponents":{"surfaceId":"contact_form","components":[
  {"id":"root","component":"Card","child":"card_content"},
  {"id":"card_content","component":"Column","children":["title","name_field","email_field","submit_btn"]},
  {"id":"title","component":"Text","text":"Contact Form","variant":"h2"},
  {"id":"name_field","component":"TextField","label":"Name","value":{"path":"/form/name"}},
  {"id":"email_field","component":"TextField","label":"Email","value":{"path":"/form/email"}},
  {"id":"submit_btn","component":"Button","text":"Submit","action":{"event":{"name":"submit_form","context":{"formData":{"path":"/form"}}}}}
]}}
{"version":"v0.9.1","updateDataModel":{"surfaceId":"contact_form","path":"/form","value":{"name":"","email":""}}}
```

### 2.3 基本组件目录（Basic Catalog）

| 分类 | 组件 |
|------|------|
| 布局 | Column, Row, List, Card, Tabs, Modal, Divider |
| 显示 | Text, Image, Icon, Video, AudioPlayer |
| 输入 | TextField, CheckBox, Slider, ChoicePicker, DateTimeInput |
| 交互 | Button（支持 server action / local function call） |
| 数据绑定 | 所有组件支持 JSON Pointer 路径（`/user/name`）和字面量 |
| 函数 | required, regex, email, formatString, formatDate, openUrl, and/or/not 等 |

### 2.4 邻接表模型（核心创新）

**传统嵌套** (LLM 很难生成)：
```json
{"Column": {"children": [{"Text": {"text": "Hello"}}]}}
```

**A2UI 邻接表** (LLM 友好)：
```json
{"id":"root","component":"Column","children":["greeting"]}
{"id":"greeting","component":"Text","text":"Hello"}
```

组件通过 ID 引用建立关系，而非嵌套。这让 LLM 可以增量生成，逐条输出组件定义。

### 2.5 数据绑定

```json
{"id":"name_display","component":"Text","text":{"path":"/user/name"}}
```

- 绝对路径 `/user/name`：从数据模型根解析
- 相对路径 `name`：在列表模板作用域内解析
- 双向绑定：TextField 等输入组件的值变化自动同步到数据模型

---

## 3. 我们当前代码库的问题

### 3.1 我们的自定义 "A2UI" 格式（完全不兼容 A2UI 协议）

**当前 system_prompt.py 第 24-28 行：**
```jsonl
{"type":"card","data":{"title":"...","body":"...","fields":[...]}}
{"type":"table","data":{"columns":[...],"rows":[...]}}
{"type":"chart","data":{"option":{...}}}
```

**真实 A2UI 协议应该是：**
```jsonl
{"createSurface":{"surfaceId":"main","catalogId":"..."}}
{"updateComponents":{"surfaceId":"main","components":[...]}}
{"updateDataModel":{"surfaceId":"main","path":"/data","value":...}}
```

**结论：我们实现了一个"名叫 A2UI 但格式完全不同"的自定义协议。**

### 3.2 具体问题清单

| # | 组件 | 问题 | 严重程度 |
|---|------|------|---------|
| 1 | `system_prompt.py:14-28` | System Prompt 教的格式不是 A2UI 协议 | 🔴 致命 |
| 2 | `types/a2ui.ts` | 类型定义只有 `card/table/chart`，缺失整个 A2UI 消息类型体系 | 🔴 致命 |
| 3 | `a2ui-parser.ts` | 解析逻辑基于 `{"type":"card"}` 检测，而非 `createSurface`/`updateComponents` 消息分发 | 🔴 致命 |
| 4 | `A2UIRenderer.vue` | 渲染器不支持邻接表模型、数据绑定、渐进渲染 | 🔴 致命 |
| 5 | `ChatMessage.vue` | hasA2UI 检测 + 渲染分支（我之前修复的）只是隐藏了原始 JSON 的显示问题 | 🟡 治标 |
| 6 | `useSSE.ts` | SSE 事件只有 text/tool_call/tool_result，没有 A2UI 消息分发 | 🟡 需增强 |
| 7 | `chat_service.py` / `agent_loop.py` | 后端没有引导 LLM 输出标准 A2UI JSONL | 🔴 致命 |

### 3.3 用户说的 "Bug" 的真正含义

用户说："和 A2UI 对话，A2UI 要渲染出界面 UI，而不是直接返回 JSON 数据"

这个"Bug"其实是**整个 A2UI 渲染管道从一开始就走错了方向**：

1. 后端 System Prompt 教 LLM 输出自定义 `{"type":"card"}` 格式
2. 前端尝试解析这个自定义格式  
3. 但 `ChatMessage.vue` 渲染逻辑有 Bug 导致原始 JSON 也显示了

我之前修复的 `ChatMessage.vue` 只是让原始 JSON "不可见"——并没有解决"渲染真正的 A2UI 界面"这个核心需求。

---

## 4. 正确的修复方案

### 方案选择：继续自定义格式 vs 迁移到标准 A2UI

| 维度 | 继续自定义 | 迁移到标准 A2UI |
|------|-----------|----------------|
| LLM 兼容性 | 需自己写 Prompt | 有现成 Catalog Schema |
| 组件丰富度 | 只有 card/table/chart | 20+ 组件（Button/Form/List/Modal...） |
| 数据绑定 | 无 | JSON Pointer + 双向绑定 |
| 渐进渲染 | 无 | 原生支持 |
| 交互性 | 无 | Button Action + 表单 |
| 生态系统 | 零 | CopilotKit / AG-UI / A2A 集成 |
| 工作量 | 小 | 中等 |

**建议：迁移到标准 A2UI 协议**，因为这才是真正有价值的方案。

### 迁移步骤

#### Step 1: 修复 System Prompt（后端）
```python
SYSTEM_PROMPT_A2UI = """You are A2UI, an intelligent ERP assistant.
When presenting structured data, you MUST output A2UI protocol JSONL messages.

## A2UI Protocol (v0.9.1)
You MUST follow this exact format. Each line is a complete JSON object:

### 1. Create Surface
{"version":"v0.9.1","createSurface":{"surfaceId":"main","catalogId":"..."}}

### 2. Define Components (adjacency list)
{"version":"v0.9.1","updateComponents":{"surfaceId":"main","components":[
  {"id":"root","component":"Column","children":["title","card"]},
  {"id":"title","component":"Text","text":"Results","variant":"h2"},
  {"id":"card","component":"Card","child":"card_content"},
  ...
]}}

### 3. Populate Data
{"version":"v0.9.1","updateDataModel":{"surfaceId":"main","path":"/data","value":{...}}}

Available components: Column, Row, Card, Text, Button, TextField, List, Table, ...
"""
```

#### Step 2: 重写前端类型和解析器
- `types/a2ui.ts` → 定义所有 A2UI 消息类型
- `a2ui-parser.ts` → 改为消息分发模式（createSurface → updateComponents → updateDataModel）
- 构建邻接表 → 组件树

#### Step 3: 实现真正的 A2UI 渲染器
- 组件目录（Catalog）：Column, Row, Card, Text, Button, TextField, List, Table
- 数据绑定引擎：JSON Pointer 路径解析
- 渐进渲染：逐条消息处理
- 交互支持：Button action → SSE 发送回服务器

#### Step 4: 增强 SSE 事件流
- 添加 `a2ui` 事件类型，或让 `text` 事件携带标准 A2UI JSONL

---

## 5. 参考资料

- 官网：https://a2ui.org/
- GitHub：https://github.com/a2ui-project/a2ui
- 协议 v0.9.1：https://a2ui.org/specification/v0.9.1-a2ui/
- 数据流：https://a2ui.org/concepts/data-flow
- 组件结构：https://a2ui.org/concepts/components/
- 基本目录：https://a2ui.org/specification/v0.9.1/catalogs/basic/catalog.json
- CopilotKit 集成：https://docs.copilotkit.ai/generative-ui/a2ui
- A2UI Composer（可视化编辑器）：https://a2ui-composer.ag-ui.com/
