# A2UI 开发文档细则

> **版本：v1.0** | **最后更新：2026-08-04**
>
> 本文档基于 A2UI 官方网站 (https://a2ui.org/) 的完整内容编写，涵盖 v0.8 至 v1.0 所有协议版本。
> 目标读者：需要理解并开发 A2UI 的 AI 模型、前端工程师、后端工程师。

---

## 目录

1. [A2UI 概述](#1-a2ui-概述)
2. [核心理念](#2-核心理念)
3. [协议版本概览](#3-协议版本概览)
4. [核心概念](#4-核心概念)
5. [协议消息详解](#5-协议消息详解)
6. [组件完整参考](#6-组件完整参考)
7. [数据绑定机制](#7-数据绑定机制)
8. [函数系统与校验](#8-函数系统与校验)
9. [传输协议](#9-传输协议)
10. [Agent 开发指南](#10-agent-开发指南)
11. [客户端集成指南](#11-客户端集成指南)
12. [自定义组件目录](#12-自定义组件目录)
13. [主题与样式](#13-主题与样式)
14. [安全设计](#14-安全设计)
15. [最佳实践](#15-最佳实践)
16. [完整示例](#16-完整示例)

---

## 1. A2UI 概述

### 1.1 什么是 A2UI

**A2UI (Agent-to-UI)** 是一个开源的、声明式的 UI 协议，由 Google 创建并采用 Apache 2.0 许可。它解决的核心问题是：

> **AI Agent 如何安全地跨信任边界发送富交互 UI？**

A2UI 让 Agent 发送**声明式组件描述**（纯 JSON 数据），客户端使用自己的原生组件来渲染这些描述。这就像让 Agent 说一种"通用的 UI 语言"——Agent 只描述 UI 的结构和数据，而渲染端负责实际的外观和行为。

### 1.2 A2UI 不是什么

- **不是** UI 框架（不是 React/Vue/Angular 的替代品）
- **不是** 代码生成器（Agent 不生成 HTML/CSS/JS 代码）
- **不是** 通用 UI 描述语言（它专门为 AI Agent 生成 UI 设计）

### 1.3 典型交互流程

```
用户发送消息 → AI Agent 理解意图 → Agent 生成 A2UI JSON 消息 
→ 消息流式传输到客户端 → 客户端用原生组件渲染 → 用户交互 
→ 操作事件发送回 Agent → Agent 返回更新的 A2UI 消息
```

---

## 2. 核心理念

A2UI 建立在四大核心设计理念之上：

### 2.1 安全设计 (Secure by Design)

- A2UI 使用**声明式数据格式**，不是可执行代码
- Agent 只能使用预先审批的组件目录（Catalog）中定义的组件
- **不存在 UI 注入攻击**：即使恶意 Agent 尝试发送危险内容，渲染器也只会使用允许的组件

### 2.2 LLM 友好 (LLM-Friendly)

- 使用**扁平化的流式 JSON 结构**，专为 LLM 生成而设计
- 采用**邻接表模型**代替深层嵌套的组件树，LLM 不需要一次性生成完美嵌套的 JSON
- 支持渐进式生成，LLM 可以增量构建 UI

### 2.3 框架无关 (Framework-Agnostic)

- 一个 Agent 响应可在所有平台工作
- 相同的 A2UI 消息可在 Angular、Flutter、React、Lit 或原生移动端渲染
- 渲染器使用各平台的原生组件，保持最佳性能和原生体验

### 2.4 渐进式渲染 (Progressive Rendering)

- UI 更新以流的方式逐步到达客户端
- 用户在 UI 实时构建过程中即可看到界面，无需等待完整响应
- 支持增量更新：只更新变化的部分，不需要重新生成整个 UI

---

## 3. 协议版本概览

| 版本 | 状态 | 关键特性 |
|------|------|----------|
| **v1.0** | 候选发布 | 双向 RPC (actionResponse)、单消息创建 UI、解耦品牌样式、增强目录 Schema |
| **v0.9.1** | 当前生产版本 | 标准化 MIME 类型 `application/a2ui+json`、放宽 surfaceId 约束 |
| **v0.9** | 稳定版 | Prompt-First 理念、createSurface、客户端函数、自定义目录、模块化 Schema |
| **v0.8** | 旧版 | 结构化输出优先、基础 Surface/组件/数据绑定/邻接表模型 |

> **推荐：新项目使用 v0.9.1**（稳定），前瞻性项目参考 v1.0 候选规范。

### v0.8 vs v0.9+ 关键差异

| 方面 | v0.8 | v0.9+ |
|------|------|-------|
| 组件包装 | `"component": { "Text": {...} }` | `"component": "Text", ...props` |
| 字符串值 | `{ "literalString": "Hello" }` | `"Hello"` |
| 子组件列表 | `{ "explicitList": ["a","b"] }` | `["a", "b"]` |
| 表面创建 | `beginRendering`（隐式创建） | `createSurface`（显式创建） |
| 按钮样式 | `primary: true` | `variant: "primary"` |
| 布局对齐 | `distribution`, `alignment` | `justify`, `align` |
| 文本样式 | `usageHint` | `variant` |
| 操作格式 | `{ "name": "..." }` | `{ "event": { "name": "..." } }` |
| 选择组件 | `MultipleChoice` | `ChoicePicker` |

---

## 4. 核心概念

### 4.1 Surface（表面）

Surface 是 A2UI 中的**独立 UI 容器/画布**，Agent 可以在其中生成 UI。

**关键特性：**
- 一个连接中可以存在多个 Surface
- 每个 Surface 拥有自己独立的组件树和数据模型
- 创建 Surface 时必须指定使用的组件目录（catalogId）
- 通过 `createSurface` 创建，通过 `deleteSurface` 销毁

**v1.0 增强：**
- `createSurface` 可直接内嵌初始组件树 (`components`) 和数据模型 (`dataModel`)，实现一条消息创建完整 UI

### 4.2 Component（组件）

组件是用 JSON 描述的 UI 元素（按钮、文本、列表、卡片等）。

**关键特性：**
- 每个组件有一个**唯一 ID**（在一个 Surface 内唯一）
- 组件**不直接包含子组件**，而是通过 ID 引用
- 组件属性可以是**字面值**或**数据绑定路径**

**组件对象基本结构：**
```json
{
  "id": "组件唯一ID",
  "component": "组件类型名称",
  "属性1": "值1",
  "属性2": { "path": "/data/path" }
}
```

### 4.3 Adjacency List Model（邻接表模型）

这是 A2UI **最重要的设计决策之一**。组件树不通过嵌套 JSON 表示，而是通过扁平列表 + ID 引用。

**传统嵌套方式的问题：**
- LLM 必须一次性生成完美嵌套的 JSON
- 难以更新深层嵌套的组件
- 难以增量流式传输

**A2UI 邻接表模型的优势：**
- 扁平结构，LLM 容易生成
- 可以增量发送组件
- 通过 ID 更新任意组件
- 结构与状态清晰分离

**示例对比：**

```json
// ❌ 传统嵌套方式
{
  "component": "Column",
  "children": [
    {
      "component": "Text",
      "text": "Hello"
    },
    {
      "component": "Button",
      "child": {
        "component": "Text",
        "text": "Click"
      }
    }
  ]
}

// ✅ A2UI 邻接表方式
{
  "updateComponents": {
    "surfaceId": "main",
    "components": [
      { "id": "root", "component": "Column", "children": ["greeting", "btn"] },
      { "id": "greeting", "component": "Text", "text": "Hello" },
      { "id": "btn", "component": "Button", "child": "btn-text", "action": { "event": { "name": "click" } } },
      { "id": "btn-text", "component": "Text", "text": "Click" }
    ]
  }
}
```

**必备规则：**
- 每个 Surface 必须有且仅有一个 `id` 为 `root` 的组件作为根节点
- 所有组件存储在平面 Map 中，客户端在渲染时重建树结构

### 4.4 Data Model（数据模型）

每个 Surface 维护一个独立的 JSON 对象作为数据模型，存储应用状态。

**示例数据模型：**
```json
{
  "user": {
    "name": "Alice",
    "email": "alice@example.com"
  },
  "cart": {
    "items": [
      { "name": "Widget", "price": 9.99, "quantity": 2 }
    ],
    "total": 19.98
  },
  "formData": {
    "name": "",
    "email": "",
    "agreedToTerms": false
  }
}
```

**数据模型操作：**
- 通过 `updateDataModel` 消息更新
- 支持增量更新（指定 JSON Pointer 路径）
- 遵循 **upsert 语义**：路径存在则更新，不存在则创建；值为空则删除键

### 4.5 Data Binding（数据绑定）

数据绑定使用 **JSON Pointer (RFC 6901)** 路径连接组件属性到数据模型。

**路径语法：**
| 路径 | 含义 | 取值示例 |
|------|------|----------|
| `/user/name` | 对象属性 | `"Alice"` |
| `/cart/items/0` | 数组索引（从0开始） | `{"name":"Widget",...}` |
| `/cart/items/0/price` | 嵌套路径 | `9.99` |
| `name` | 相对路径（模板内） | 相对于当前迭代项 |

**字面值 vs 数据绑定：**
```json
// 字面值（固定）
{ "id": "title", "component": "Text", "text": "Welcome" }

// 数据绑定（响应式）
{ "id": "title", "component": "Text", "text": { "path": "/user/name" } }
```

当 `/user/name` 从 "Alice" 变为 "Bob" 时，文本**自动更新**——无需修改组件定义，只需更新数据。

### 4.6 Catalog（组件目录）

Catalog 是组件类型、函数和样式的集合定义，是 Agent 和渲染器之间的**契约**。

**关键概念：**
- 每个 Surface 绑定一个 Catalog
- Agent 只能使用 Catalog 中定义的组件
- 基础目录 (Basic Catalog) 预置了通用组件，但生产项目应定义自己的目录
- Catalog ID 约定使用 URI 格式（如 `https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json`）

### 4.7 Progressive Rendering（渐进式渲染）

渐进式渲染允许 UI 分步呈现，而不是等待整个界面构建完成。

**工作机制：**
- Agent 先发送 `createSurface` 创建容器
- 然后逐步发送 `updateComponents` 添加组件
- 用户可以立即看到框架，组件逐步填充
- 引用的子组件或数据绑定尚不存在时可显示占位符

---

## 5. 协议消息详解

A2UI 协议定义了服务器到客户端和客户端到服务器两类消息。

### 5.1 消息信封格式 (v0.9+)

每个消息是一个 JSON 对象，必须包含 `version` 字段和以下**四个操作之一**：
`createSurface` | `updateComponents` | `updateDataModel` | `deleteSurface`

流式传输时，消息通常以 **JSONL（JSON Lines）格式**发送，每行一个完整的 JSON 对象。

---

### 5.2 createSurface — 创建表面

**描述：** 通知客户端创建一个新的 UI Surface。必须在任何 `updateComponents` / `updateDataModel` 之前发送。

**v0.9.1 参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `surfaceId` | string | ✅ | Surface 唯一标识符 |
| `catalogId` | string | ✅ | 组件目录标识符（URI 格式） |
| `theme` | object | ❌ | 主题参数（如 `primaryColor`） |
| `sendDataModel` | boolean | ❌ | 是否在客户端消息中附带数据模型，默认 false |

**v1.0 新增参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `components` | array | ❌ | 初始组件列表（单消息创建） |
| `dataModel` | object | ❌ | 初始数据模型（单消息创建） |

> ⚠️ **v1.0 重要变化：** `surfaceProperties` 对象已移除，其字段提升为 `createSurface` 的顶层属性。

**示例 (v0.9.1)：**
```json
{
  "version": "v0.9.1",
  "createSurface": {
    "surfaceId": "user_profile_card",
    "catalogId": "https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json",
    "theme": {
      "primaryColor": "#00BFFF",
      "agentDisplayName": "餐厅助手"
    },
    "sendDataModel": true
  }
}
```

**示例 (v1.0 单消息创建)：**
```json
{
  "version": "v1.0",
  "createSurface": {
    "surfaceId": "greeting_demo",
    "catalogId": "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json",
    "components": [
      { "id": "root", "component": "Column", "children": ["msg"] },
      { "id": "msg", "component": "Text", "text": { "path": "/message" } }
    ],
    "dataModel": { "message": "Hello, A2UI!" }
  }
}
```

---

### 5.3 updateComponents — 更新组件

**描述：** 向 Surface 中添加或更新组件。使用邻接表模型。

**v0.9.1 参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `surfaceId` | string | ✅ | 目标 Surface ID |
| `components` | array | ✅ | 组件对象数组 |

**增量更新操作：**
- **添加**：发送包含新 ID 的组件定义
- **更新**：发送包含现有 ID 和新属性的组件定义
- **删除**：更新父组件的 `children` 列表，排除要删除的 ID

**示例：**
```json
{
  "version": "v0.9.1",
  "updateComponents": {
    "surfaceId": "contact_form",
    "components": [
      {
        "id": "root",
        "component": "Column",
        "children": ["title", "name_field", "email_field", "submit_btn"]
      },
      {
        "id": "title",
        "component": "Text",
        "text": "Contact Us",
        "variant": "h1"
      },
      {
        "id": "name_field",
        "component": "TextField",
        "label": "Your Name",
        "value": { "path": "/form/name" },
        "textFieldType": "shortText"
      },
      {
        "id": "email_field",
        "component": "TextField",
        "label": "Email Address",
        "value": { "path": "/form/email" },
        "textFieldType": "shortText",
        "checks": [
          {
            "call": "required",
            "args": { "value": { "path": "/form/email" } },
            "message": "Email is required"
          },
          {
            "call": "email",
            "args": { "value": { "path": "/form/email" } },
            "message": "Invalid email format"
          }
        ]
      },
      {
        "id": "submit_text",
        "component": "Text",
        "text": "Submit"
      },
      {
        "id": "submit_btn",
        "component": "Button",
        "child": "submit_text",
        "variant": "primary",
        "action": {
          "event": {
            "name": "submit_form",
            "context": {
              "formData": { "path": "/form" }
            }
          }
        }
      }
    ]
  }
}
```

---

### 5.4 updateDataModel — 更新数据模型

**描述：** 发送或更新数据模型。支持增量更新和全量替换。

**v0.9.1 参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `surfaceId` | string | ✅ | 目标 Surface ID |
| `path` | string | ❌ | JSON Pointer 路径，默认 "/"（全量替换） |
| `value` | any | ❌ | 新值；省略则删除指定路径的键 |

**示例：**

```json
// 增量更新 — 只更新用户名
{
  "version": "v0.9.1",
  "updateDataModel": {
    "surfaceId": "user_profile",
    "path": "/user/name",
    "value": "Jane Doe"
  }
}

// 全量替换 — 替换整个数据模型
{
  "version": "v0.9.1",
  "updateDataModel": {
    "surfaceId": "user_profile",
    "value": {
      "user": { "name": "Jane Doe", "email": "jane@example.com" },
      "settings": { "theme": "dark" }
    }
  }
}

// 删除 — 删除指定路径的键
{
  "version": "v0.9.1",
  "updateDataModel": {
    "surfaceId": "user_profile",
    "path": "/tempData"
  }
}
```

---

### 5.5 deleteSurface — 删除表面

**描述：** 移除指定 Surface 及其所有组件和数据。

**参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `surfaceId` | string | ✅ | 要删除的 Surface ID |

```json
{
  "version": "v0.9.1",
  "deleteSurface": {
    "surfaceId": "contact_form_1"
  }
}
```

---

### 5.6 action — 客户端操作（客户端 → 服务器）

**描述：** 当用户触发定义了 `action` 的交互组件（如 Button）时，客户端向服务器发送此消息。

**参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `actionId` | string | 条件必需 | v1.0 新增，当 `wantResponse` 为 true 时必填 |
| `name` | string | ✅ | 操作名称（来自组件 action.event.name） |
| `surfaceId` | string | ✅ | 来源 Surface ID |
| `sourceComponentId` | string | ✅ | 触发操作的组件 ID |
| `timestamp` | string | ✅ | ISO 8601 时间戳 |
| `context` | object | ✅ | 操作上下文（来自组件的 action.event.context） |
| `wantResponse` | boolean | ❌ | 是否需要 Agent 返回 `actionResponse` |

**示例 (v0.9.1)：**
```json
{
  "version": "v0.9.1",
  "action": {
    "name": "submit_form",
    "surfaceId": "contact_form",
    "sourceComponentId": "submit_btn",
    "timestamp": "2025-12-03T10:30:00Z",
    "context": {
      "formData": {
        "name": "Alice",
        "email": "alice@example.com"
      }
    }
  }
}
```

**示例 (v1.0，含 actionId 和 wantResponse)：**
```json
{
  "version": "v1.0",
  "actionId": "submit_form_1",
  "action": {
    "name": "submit_form",
    "surfaceId": "contact_form",
    "sourceComponentId": "submit_btn",
    "timestamp": "2025-12-03T10:30:00Z",
    "context": { "formData": { "name": "Alice", "email": "alice@example.com" } }
  },
  "wantResponse": true
}
```

---

### 5.7 actionResponse — 操作响应（v1.0 新增，服务器 → 客户端）

**描述：** 当 Renderer 发送带有 `wantResponse: true` 的 `action` 时，Agent 可用此消息同步返回结果。

**参数：**

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `actionId` | string | ✅ | 与 Renderer 发来的 actionId 一致 |
| `actionResponse.value` | any | 二选一 | 成功返回值 |
| `actionResponse.error` | object | 二选一 | 错误信息 |

```json
{
  "version": "v1.0",
  "actionId": "get_typeahead_suggestions_1",
  "actionResponse": {
    "value": ["apple", "application", "approved"]
  }
}
```

---

### 5.8 error — 错误消息（客户端 → 服务器）

**描述：** 客户端向服务器报告错误。

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "surfaceId": "user_profile_card",
    "path": "/components/0/text",
    "message": "Expected stringOrPath, got integer"
  }
}
```

---

## 6. 组件完整参考

> 以下组件定义基于 v0.9.1 Basic Catalog。v0.8 的差异已在版本差异表中列出。

### 6.1 所有组件通用属性

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `id` | string | ✅ | Surface 内唯一标识符 |
| `component` | string | ✅ | 组件类型名 |
| `weight` | number | ❌ | 在 Row/Column 中的 flex-grow 值 |
| `accessibility` | object | ❌ | 无障碍属性 (`label`, `role`) |

---

### 6.2 布局组件

#### Row — 水平布局

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `children` | array 或 template | ✅ | 子组件 ID 列表或动态模板 |
| `justify` | string | ❌ | 主轴对齐：`start`、`center`、`end`、`spaceBetween`、`spaceAround`、`spaceEvenly` |
| `align` | string | ❌ | 交叉轴对齐：`start`、`center`、`end`、`stretch` |

```json
{ "id": "toolbar", "component": "Row", "children": ["btn1", "btn2", "btn3"], "justify": "spaceBetween", "align": "center" }
```

#### Column — 垂直布局

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `children` | array 或 template | ✅ | 子组件 ID 列表或动态模板 |
| `justify` | string | ❌ | 主轴对齐 |
| `align` | string | ❌ | 交叉轴对齐 |

```json
{ "id": "content", "component": "Column", "children": ["header", "body", "footer"], "justify": "start", "align": "stretch" }
```

#### List — 可滚动列表

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `children` | array 或 template | ✅ | 子组件或动态模板 |
| `direction` | string | ❌ | `vertical` 或 `horizontal` |
| `align` | string | ❌ | 对齐方式 |

```json
{
  "id": "message_list",
  "component": "List",
  "children": { "componentId": "message_item", "path": "/messages" },
  "direction": "vertical"
}
```

---

### 6.3 显示组件

#### Text — 文本显示

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `text` | string 或 DataBinding | ✅ | 文本内容，支持简单 Markdown |
| `variant` | string | ❌ | `h1`、`h2`、`h3`、`h4`、`h5`、`caption`、`body`（默认） |

```json
{ "id": "title", "component": "Text", "text": "Welcome to A2UI", "variant": "h1" }
{ "id": "dynamic_text", "component": "Text", "text": { "path": "/user/name" } }
```

#### Image — 图片显示

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `url` | string 或 DataBinding | ✅ | 图片 URL |
| `fit` | string | ❌ | `cover`、`contain`、`fill`、`none`、`scaleDown` |
| `variant` | string | ❌ | `hero`、`thumbnail`、`avatar`、`icon` |

```json
{ "id": "hero_img", "component": "Image", "url": "https://example.com/hero.png", "fit": "cover", "variant": "hero" }
```

#### Icon — 图标

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `name` | string 或 DataBinding | ✅ | 预定义图标名称 |

```json
{ "id": "check_icon", "component": "Icon", "name": "check" }
```

#### Video — 视频

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `url` | string 或 DataBinding | ✅ | 视频 URL |

#### AudioPlayer — 音频播放器

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `url` | string 或 DataBinding | ✅ | 音频 URL |

#### Divider — 分割线

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `axis` | string | ❌ | `horizontal`（默认）或 `vertical` |

```json
{ "id": "separator", "component": "Divider", "axis": "horizontal" }
```

---

### 6.4 交互组件

#### Button — 按钮

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `child` | string | ✅ | 按钮内显示的组件 ID（通常是 Text） |
| `variant` | string | ❌ | `primary`、`borderless` |
| `action` | object | ✅ | 操作定义 |
| `checks` | array | ❌ | 按钮禁用条件校验列表 |

**action 对象结构（服务器操作）：**
```json
{
  "event": {
    "name": "操作名称",
    "context": { "key": "value 或 DataBinding" }
  }
}
```

**action 对象结构（本地操作）：**
```json
{
  "functionCall": {
    "call": "函数名",
    "args": { "参数": "值" }
  }
}
```

**完整示例：**
```json
{
  "id": "submit_btn",
  "component": "Button",
  "child": "submit_text",
  "variant": "primary",
  "action": {
    "event": {
      "name": "submit_form",
      "context": {
        "formData": { "path": "/form" },
        "timestamp": "2025-12-03T10:00:00Z"
      }
    }
  },
  "checks": [
    {
      "call": "and",
      "args": {
        "values": [
          { "call": "required", "args": { "value": { "path": "/form/name" } } },
          { "call": "required", "args": { "value": { "path": "/form/email" } } }
        ]
      }
    }
  ]
}
```

#### TextField — 文本输入框

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `label` | string | ✅ | 标签文本 |
| `value` | DataBinding | ✅ | 绑定数据路径（双向绑定） |
| `textFieldType` | string | ❌ | `shortText`、`longText`、`number`、`obscured`（密码）、`date` |
| `validationRegexp` | string | ❌ | 正则校验模式 |
| `checks` | array | ❌ | 校验函数列表 |

```json
{
  "id": "email_input",
  "component": "TextField",
  "label": "Email Address",
  "value": { "path": "/form/email" },
  "textFieldType": "shortText",
  "checks": [
    { "call": "required", "args": { "value": { "path": "/form/email" } }, "message": "Email is required" },
    { "call": "email", "args": { "value": { "path": "/form/email" } }, "message": "Invalid email format" }
  ]
}
```

#### CheckBox — 复选框

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `label` | string | ✅ | 标签文本 |
| `value` | DataBinding | ✅ | 绑定布尔值路径（双向绑定） |

```json
{ "id": "terms_cb", "component": "CheckBox", "label": "I agree to terms", "value": { "path": "/form/agreed" } }
```

#### Slider — 滑动条

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `value` | DataBinding | ✅ | 绑定数值路径（双向绑定） |
| `minValue` | number | ✅ | 最小值 |
| `maxValue` | number | ✅ | 最大值 |

```json
{ "id": "volume_slider", "component": "Slider", "value": { "path": "/settings/volume" }, "minValue": 0, "maxValue": 100 }
```

#### DateTimeInput — 日期/时间选择器

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `label` | string | ❌ | 标签 |
| `value` | DataBinding | ✅ | 绑定日期值路径（双向绑定） |
| `enableDate` | boolean | ❌ | 启用日期选择 |
| `enableTime` | boolean | ❌ | 启用时间选择 |

```json
{ "id": "date_picker", "component": "DateTimeInput", "label": "Select Date", "value": { "path": "/booking/date" }, "enableDate": true, "enableTime": true }
```

#### ChoicePicker — 选择器

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `label` | string | ❌ | 标签 |
| `options` | array | ✅ | 选项列表 `[{ "label": "显示名", "value": "值" }]` |
| `value` | DataBinding | ✅ | 绑定选中值路径（双向绑定） |
| `maxAllowedSelections` | number | ❌ | 最大可选数量（1=单选） |

```json
{
  "id": "country_select",
  "component": "ChoicePicker",
  "label": "Country",
  "options": [
    { "label": "United States", "value": "us" },
    { "label": "Canada", "value": "ca" },
    { "label": "China", "value": "cn" }
  ],
  "value": { "path": "/form/country" },
  "maxAllowedSelections": 1
}
```

---

### 6.5 容器组件

#### Card — 卡片容器

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `child` | string | ✅ | 卡片内的子组件 ID |

```json
{ "id": "info_card", "component": "Card", "child": "card_content" }
```

#### Modal — 模态对话框

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `entryPointChild` | string | ✅ | 触发模态框的组件 ID（通常是按钮） |
| `contentChild` | string | ✅ | 模态框内容组件 ID |

```json
{
  "id": "confirm_modal",
  "component": "Modal",
  "entryPointChild": "open_modal_btn",
  "contentChild": "modal_content"
}
```

#### Tabs — 标签页

| 属性 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `tabItems` | array | ✅ | `[{ "title": "标签名", "child": "内容组件ID" }]` |

```json
{
  "id": "settings_tabs",
  "component": "Tabs",
  "tabItems": [
    { "title": "General", "child": "general_content" },
    { "title": "Privacy", "child": "privacy_content" }
  ]
}
```

---

### 6.6 静态子组件 vs 动态子组件

**静态（固定列表）：**
```json
{ "children": ["back_btn", "title", "menu_btn"] }
```

**动态（从数据生成）：**
```json
{
  "children": {
    "componentId": "item_template",
    "path": "/products"
  }
}
```

动态模板中，路径 `name` 会解析为 `/products/0/name`、`/products/1/name` 等（相对于每个迭代项）。

---

## 7. 数据绑定机制

### 7.1 动态类型系统

A2UI 定义了以下动态类型，任何可绑定数据的属性都使用这些类型：

| 类型 | 接受的值 |
|------|----------|
| `string` | 字面字符串 或 `{ "path": "..." }` 或 `{ "call": "...", "args": {...} }` |
| `number` | 字面数字 或 `{ "path": "..." }` 或 `{ "call": "...", "args": {...} }` |
| `boolean` | 字面布尔值 或 `{ "path": "..." }` 或 `{ "call": "...", "args": {...} }` |
| `array` | 字面数组 或 `{ "path": "..." }` |

### 7.2 JSON Pointer 路径

**绝对路径（以 `/` 开头）：** 从数据模型根解析
```
/text → 数据模型根下的 text 属性
/user/name → 数据模型根下 user.name
/items/0/title → 数组 items 第 0 个元素的 title
```

**相对路径（不以 `/` 开头）：** 在模板作用域内解析
```
// 当 List 使用 children.path="/products" 和 children.componentId="product_card" 时
name  → /products/0/name, /products/1/name...
price → /products/0/price, /products/1/price...
```

### 7.3 作用域规则

```
根作用域（绝对路径）
  │
  ├── /user/name → 数据模型根
  ├── /settings/theme → 数据模型根
  │
  └── 集合作用域（相对路径）
        │
        └── 模板内部：price → /products/N/price
```

**混合访问：** 模板内的组件仍可通过绝对路径访问根作用域：
```json
// 在列表模板内
{ "id": "item_name", "component": "Text", "text": { "path": "name" } },        // 相对：当前项名称
{ "id": "app_title", "component": "Text", "text": { "path": "/app/title" } }   // 绝对：全局应用标题
```

### 7.4 双向绑定（输入组件）

以下组件建立与数据模型的**双向绑定**：

| 组件 | 绑定属性 | 用户操作 | 数据更新 |
|------|----------|----------|----------|
| TextField | `value` | 输入 "Alice" | `/form/name` = "Alice" |
| CheckBox | `value` | 勾选 | `/form/agreed` = true |
| Slider | `value` | 拖动到 50 | `/settings/volume` = 50 |
| ChoicePicker | `value` | 选择 "cn" | `/form/country` = ["cn"] |
| DateTimeInput | `value` | 选择日期 | `/booking/date` = "2025-12-15" |

**双向绑定规则：**
- **读（Model → View）：** 根据绑定路径的值渲染组件
- **写（View → Model）：** 用户交互立即更新本地数据模型
- **响应性：** 绑定相同路径的其他组件实时更新
- **服务器同步：** 仅当触发显式操作（如按钮点击）时才将数据发送回服务器

### 7.5 formatString 语法

在字符串内嵌入动态表达式，使用 `formatString` 函数：

```json
{
  "id": "welcome_msg",
  "component": "Text",
  "text": {
    "call": "formatString",
    "args": {
      "value": "Hello, ${/user/firstName}! You have ${/notifications/count} new messages."
    }
  }
}
```

**语法规则：**
- 插值：`${expression}`
- 转义字面 `${`：`\${`
- 数据绑定：`${/user/name}`（绝对）或 `${firstName}`（相对）
- 函数调用：`${formatDate(value:${/date}, format:'yyyy-MM-dd')}`
- 嵌套：支持 `${upper(${now()})}`

---

## 8. 函数系统与校验

### 8.1 基础目录函数一览

#### 校验函数

| 函数 | 描述 | 参数 |
|------|------|------|
| `required` | 检查值非 null/undefined/空 | `value` |
| `regex` | 正则匹配检查 | `value`, `pattern` |
| `length` | 字符串长度约束 | `value`, `minLength`, `maxLength` |
| `numeric` | 数值范围约束 | `value`, `min`, `max` |
| `email` | 验证邮箱格式 | `value` |

#### 逻辑组合函数

| 函数 | 描述 | 参数 |
|------|------|------|
| `and` | 逻辑与 | `values`（列表） |
| `or` | 逻辑或 | `values`（列表） |
| `not` | 逻辑非 | `value` |

#### 格式化函数

| 函数 | 描述 | 参数 |
|------|------|------|
| `formatString` | 字符串插值 | `value`（含 `${...}` 表达式） |
| `formatNumber` | 数字格式化 | `value`, `grouping`, `precision` |
| `formatCurrency` | 货币格式化 | `value`, `currency` |
| `formatDate` | 日期/时间格式化 | `value`, `format` |
| `pluralize` | 复数选择 | `value`, `singular`, `plural` |

#### 操作函数

| 函数 | 描述 | 参数 |
|------|------|------|
| `openUrl` | 打开 URL | `url` |

### 8.2 校验的使用方式

**输入组件校验（显示错误信息）：**
```json
{
  "id": "zip_input",
  "component": "TextField",
  "label": "Zip Code",
  "value": { "path": "/form/zip" },
  "checks": [
    {
      "call": "required",
      "args": { "value": { "path": "/form/zip" } },
      "message": "Zip code is required"
    },
    {
      "call": "regex",
      "args": {
        "value": { "path": "/form/zip" },
        "pattern": "^[0-9]{5}$"
      },
      "message": "Must be a 5-digit zip code"
    }
  ]
}
```

**按钮校验（禁用逻辑）：**
```json
{
  "id": "submit_btn",
  "component": "Button",
  "child": "submit_text",
  "variant": "primary",
  "action": { "event": { "name": "submit" } },
  "checks": [
    {
      "call": "and",
      "args": {
        "values": [
          { "call": "required", "args": { "value": { "path": "/form/name" } } },
          { "call": "required", "args": { "value": { "path": "/form/email" } } },
          { "call": "email", "args": { "value": { "path": "/form/email" } } }
        ]
      }
    }
  ]
}
```
> 若 checks 中的任何一个条件失败，按钮自动禁用。

---

## 9. 传输协议

A2UI 是**传输无关**的协议，只定义 JSON 消息结构和语义契约。

### 9.1 传输协议必须满足的契约

1. **可靠传递**：保证消息顺序
2. **消息帧定界**：如 JSONL 换行、WebSocket 帧、SSE 事件
3. **元数据支持**：数据模型同步、能力交换
4. **双向能力（可选）**：客户端到服务器的 `action` 消息

### 9.2 常用传输绑定

| 传输方式 | 特点 | 适用场景 |
|----------|------|----------|
| **A2A Protocol** | 标准化 Agent 间通信，内建 A2UI 支持 | Agent-to-Agent 场景 |
| **AG-UI** | 双向实时 Agent-UI 协议 | 低延迟、共享状态的前端-后端通信 |
| **SSE + JSON RPC** | 服务器到客户端单向流 | 简单流式响应 |
| **WebSocket** | 持久双向连接 | 实时更新和用户操作回传 |
| **MCP** | 作为工具输出或资源订阅交付 | MCP 生态系统集成 |

### 9.3 JSONL 流式格式

A2UI 消息在流式传输时推荐使用 **JSONL (JSON Lines)** 格式：

```
{"version":"v0.9.1","createSurface":{"surfaceId":"main","catalogId":"..."}}
{"version":"v0.9.1","updateComponents":{"surfaceId":"main","components":[...]}}
{"version":"v0.9.1","updateDataModel":{"surfaceId":"main","path":"/user","value":{...}}}
```

每行是一个完整的 JSON 对象，便于：
- 逐行解析
- 增量生成
- 错误隔离（一行出错不影响其他行）

---

## 10. Agent 开发指南

### 10.1 开发流程

构建 A2UI Agent 的四个步骤：

1. **理解用户意图** → 决定展示什么 UI
2. **生成 A2UI JSON** → 使用 LLM 结构化输出或 Prompt 工程
3. **验证与流式传输** → 校验 Schema，发送到客户端
4. **处理操作** → 响应用户交互

### 10.2 Prompt 工程策略

A2UI 采用 **Prompt-First** 方式（v0.9+），将 A2UI 协议 Schema 和示例直接嵌入 LLM 的 System Prompt 中，让 LLM 生成符合规范的 JSON。

**核心工具：A2uiSchemaManager**

```python
from a2ui.schema.constants import VERSION_0_9
from a2ui.strategies.schema import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog

# 定义 Agent 角色
ROLE_DESCRIPTION = "You are a helpful assistant. Your final output MUST be A2UI JSON."

# 定义 UI 模板选择规则
UI_DESCRIPTION = """
- For search results, use the SEARCH_RESULTS_TEMPLATE.
- For forms, use the FORM_TEMPLATE.
- For confirmation dialogs, use the CONFIRMATION_TEMPLATE.
"""

# 初始化 Schema 管理器
schema_manager = A2uiSchemaManager(
    version=VERSION_0_9,
    catalogs=[
        BasicCatalog.get_config(
            version=VERSION_0_9, 
            examples_path="examples/0.9"
        )
    ],
)

# 生成 System Prompt
system_prompt = schema_manager.generate_system_prompt(
    role_description=ROLE_DESCRIPTION,
    ui_description=UI_DESCRIPTION,
    include_schema=True,      # 包含 JSON Schema
    include_examples=True,    # 包含示例
    validate_examples=True,   # 验证示例有效性
)
```

### 10.3 Prompt-Generate-Validate 循环

这是 A2UI Agent 的核心工作循环：

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ 1.Prompt │────▶│ 2.Generate   │────▶│ 3.Validate   │
│ 构建提示 │     │ LLM 生成 JSON│     │ 对照Schema校验│
└──────────┘     └──────────────┘     └──────┬───────┘
       ▲                                     │
       │          ┌──────────────┐            │
       └──────────│ 4.Fix Errors │◀───────────┘
                  │ 返回错误修正  │  校验失败
                  └──────────────┘
                         │
                         │ 校验通过
                         ▼
                  ┌──────────────┐
                  │ 5.Send to    │
                  │   Client     │
                  └──────────────┘
```

1. **Prompt**：构建包含 UI 描述、A2UI JSON Schema 和示例的提示
2. **Generate**：LLM 生成 JSON 输出
3. **Validate**：对照 A2UI Schema 验证
4. **Fix**：若无效，将标准格式错误返回给 LLM 进行自我纠正
5. **Send**：有效则发送至客户端渲染

### 10.4 消息生成顺序

**标准流程 (v0.9+)：**
1. 先发送 `createSurface`（创建 UI 容器）
2. 再发送 `updateComponents`（定义 UI 结构）
3. 然后发送 `updateDataModel`（填充数据）
4. 最后根据需要发送更多更新或 `deleteSurface`

**最佳实践：**
- 先发结构，再发数据
- 使用增量更新，只更新变化的路径
- 批量操作尽量合并到一个 `updateComponents` 消息中

### 10.5 输出验证要点

```python
import json
import jsonschema

# 1. 清理 LLM 输出（移除 Markdown 代码块标记等）
cleaned = llm_output.strip()
if cleaned.startswith("```"):
    cleaned = cleaned.split("\n", 1)[1]
if cleaned.endswith("```"):
    cleaned = cleaned.rsplit("\n", 1)[0]

# 2. 解析 JSON
parsed = json.loads(cleaned)

# 3. 验证 Schema
jsonschema.validate(instance=parsed, schema=A2UI_SCHEMA)

# 4. 发送到客户端
send_to_client(parsed)
```

### 10.6 常见 Agent 设计模式

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **模板选择** | 预定义 UI 模板，LLM 选择并填充数据 | 结构化场景（表单、列表） |
| **自由生成** | LLM 完全自由生成组件树 | 高度动态的 UI 需求 |
| **逐步构建** | 多轮交互，逐步完善 UI | 复杂表单、多步骤流程 |
| **混合模式** | 模板 + 自由生成结合 | 大部分实际应用 |

---

## 11. 客户端集成指南

### 11.1 支持的渲染器

| 渲染器 | 平台 | v0.8 | v0.9 | 状态 |
|--------|------|------|------|------|
| **Lit (Web Components)** | Web | ✅ | ✅ | 稳定 |
| **Angular** | Web | ✅ | ✅ | 稳定 |
| **React** | Web | ✅ | ✅ | 稳定 |
| **Flutter (GenUI SDK)** | 移动/桌面/Web | ✅ | ✅ | 稳定 |
| **Jetpack Compose** | Android | — | — | 计划中 |

### 11.2 Web 核心库

所有 Web 渲染器共用 `@a2ui/web_core`，提供：
- **MessageProcessor**：管理 A2UI 状态并处理传入消息
- **状态管理**：组件树和数据模型的响应式管理
- **数据绑定引擎**：路径解析和响应式更新

```bash
npm install @a2ui/lit @a2ui/web_core    # Lit
npm install @a2ui/angular @a2ui/web_core # Angular
npm install @a2ui/react @a2ui/web_core   # React
```

### 11.3 框架集成要点

#### React

```tsx
import { MessageProcessor } from '@a2ui/react';
import { A2UISurface } from '@a2ui/react';

// 使用 Hook
const { processMessage, surfaces } = useA2UI({
  catalogs: [new BasicCatalog()],
  actionHandler: (action) => {
    // 处理用户操作，发送到 Agent
    sendToAgent(action);
  }
});

// 渲染 Surface
<A2UISurface surfaceId="main" />
```

#### Angular

```typescript
import { ApplicationConfig } from '@angular/core';
import { provideA2Ui, BasicCatalog } from '@a2ui/angular/v0_9';

export const appConfig: ApplicationConfig = {
  providers: [
    provideA2Ui({
      catalogs: [new BasicCatalog()],
      actionHandler: action => {
        console.log('Action:', action);
        // 发送到 Agent
      },
    }),
  ],
};
```

```html
<!-- 模板中使用 -->
<a2ui-surface surfaceId="main"></a2ui-surface>
```

#### Lit (Web Components)

```html
<a2ui-surface surfaceId="main"></a2ui-surface>
```

```javascript
import { A2uiMessageProcessor } from '@a2ui/lit';

const processor = new A2uiMessageProcessor({
  catalogs: [new BasicCatalog()],
  actionHandler: (action) => sendToAgent(action),
});

// 处理流式消息
for (const message of stream) {
  processor.processMessage(message);
}
```

#### Flutter

```bash
flutter pub add flutter_genui
```

参考 GenUI SDK 官方文档进行 Flutter 集成。

### 11.4 连接 Agent

客户端需要：
1. **接收 A2UI 消息**：通过 SSE/WebSocket/A2A 等传输层接收
2. **处理消息**：使用 MessageProcessor 逐条处理
3. **回传操作**：将用户的 `action` 事件发送回 Agent

### 11.5 客户端能力声明

```json
{
  "supportedCatalogIds": [
    "https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json",
    "https://mycompany.com/catalogs/custom/catalog.json"
  ],
  "inlineCatalogs": false
}
```

---

## 12. 自定义组件目录

### 12.1 为什么需要自定义目录

生产应用应定义自己的目录，这样：
- **设计系统对齐**：限制 Agent 只能使用应用中实际存在的组件
- **安全性**：只渲染经过审批的组件
- **无需适配器**：直接映射到客户端设计系统，而不是先映射通用目录再适配

### 12.2 目录工作原理

1. **定义目录**：创建 JSON Schema 文件，列出组件、函数、样式
2. **注册目录**：在客户端应用中注册目录及其对应的组件实现
3. **声明支持**：客户端告知 Agent 支持哪些目录
4. **Agent 选择目录**：Agent 通过 `catalogId` 选择使用哪个目录
5. **Agent 生成 UI**：Agent 使用该目录中定义的组件生成消息

### 12.3 目录 JSON Schema 结构

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://mycompany.com/catalogs/custom/catalog.json",
  "title": "My Custom Catalog",
  "components": {
    "CustomButton": {
      "type": "object",
      "properties": {
        "id": { "$ref": "common_types.json#/$defs/ComponentId" },
        "component": { "const": "CustomButton" },
        "label": { "$ref": "common_types.json#/$defs/DynamicString" },
        "color": { "$ref": "common_types.json#/$defs/DynamicString" },
        "children": { "$ref": "common_types.json#/$defs/ChildList" }
      },
      "required": ["id", "component", "label"]
    }
  },
  "functions": {
    "myValidation": {
      "type": "object",
      "properties": {
        "call": { "const": "myValidation" },
        "args": {
          "type": "object",
          "properties": {
            "value": { "$ref": "common_types.json#/$defs/DynamicValue" }
          }
        }
      }
    }
  }
}
```

### 12.4 必须遵循的验证器规则

- 引用另一个组件的属性必须用 `ComponentId` 类型（不能是原始 `string`）
- 列表子元素引用必须用 `ChildList` 类型
- 禁止自定义 `$defs`
- 组件必须使用 `discriminator` 字段（`component` 字段作为类型区分）

### 12.5 安全考虑

1. **白名单组件**：只注册可信组件，不暴露危险能力
2. **验证属性**：始终验证来自 Agent 消息的组件属性
3. **净化文本**：除非建立了安全边界，否则不要渲染 Agent 提供的未经净化的内容

---

## 13. 主题与样式

### 13.1 样式哲学

A2UI 采用**渲染器控制样式**的默认方式：
- **Agent 描述 *展示什么***（组件和结构）
- **渲染器决定 *如何展示***（颜色、字体、间距）

### 13.2 样式层级

```
Layer 1: 语义提示（Semantic Hints）
  └── Agent 提供 variant/usageHint（如 "h1", "primary"）
      └── 目录元素将这些语义映射到实际组件并应用样式

Layer 2: createSurface theme 属性
  └── Agent 可传递的主题参数（如 primaryColor）
      └── 渲染器目录定义如何应用这些参数

Layer 3: 渲染器全局样式
  └── CSS 变量（Web）/ ThemeData（Flutter）
      └── 应用开发者完全控制
```

### 13.3 Web 主题定制

通过 CSS 变量覆盖 Basic Catalog 的默认样式：

```css
:root {
  --a2ui-color-primary: #ff5722;
  --a2ui-font-family-title: 'Your Title Font', sans-serif;
  --a2ui-font-family-monospace: 'Your Mono Font', monospace;
  --a2ui-card-background: #ffffff;
}
```

### 13.4 暗色模式

Web 渲染器默认支持根据系统偏好自动切换暗色模式 (`prefers-color-scheme`)。

强制暗色或亮色模式：
```html
<div class="a2ui-dark">
  <a2ui-surface surfaceId="main"></a2ui-surface>
</div>
```

### 13.5 createSurface 主题参数

v0.9.1 支持的 Basic Catalog 主题属性：

| 属性 | 类型 | 描述 |
|------|------|------|
| `primaryColor` | string | 主品牌色（十六进制） |
| `iconUrl` | URI | 代理/工具的图标 URL |
| `agentDisplayName` | string | 代理/工具的显示名称 |

> **v1.0 变化：** 移除了硬编码的主题颜色，视觉风格完全交由目标平台本地主题决定。

---

## 14. 安全设计

### 14.1 四层安全防线

```
Layer 1: 声明式格式
  └── A2UI 是数据，不是代码——Agent 无法发送可执行指令

Layer 2: 组件白名单
  └── Agent 只能使用 Catalog 中定义的组件
  └── 渲染器只渲染注册过的组件

Layer 3: 属性验证
  └── 所有组件属性通过 JSON Schema 验证
  └── 未知属性被忽略

Layer 4: 操作边界
  └── 用户交互通过 action 事件明确定义
  └── 敏感操作需要用户确认
```

### 14.2 安全最佳实践

1. **身份验证**：在多代理系统中，编排器负责验证 `agentDisplayName` 和 `iconUrl`，防止恶意代理冒充
2. **组件白名单**：只注册必需的组件，不暴露危险能力
3. **内容净化**：不渲染未经净化的 Agent 提供的内容
4. **操作确认**：对销毁性操作要求用户确认
5. **速率限制**：对 Agent 的消息频率进行限制

---

## 15. 最佳实践

### 15.1 组件设计

- ✅ **使用描述性 ID**：用 `"user-profile-card"` 而不是 `"c1"`
- ✅ **浅层层级**：避免深层嵌套的组件树
- ✅ **分离结构与内容**：使用数据绑定而非字面值
- ✅ **模板复用**：一个模板，多个实例（通过动态子组件）

### 15.2 数据绑定

- ✅ **粒度更新**：只更新变化的路径，如 `/user/name` 而非整个 `/` 模型
- ✅ **领域分组**：按业务领域组织数据 `{"user":{...}, "cart":{...}, "ui":{...}}`
- ✅ **预计算展示值**：在 Agent 端格式化数据（货币、日期等）后再发送
- ✅ **增量更新**：每次只发送变化的数据

### 15.3 性能优化

- ✅ **批处理**：缓冲 16ms 内的更新，批量渲染
- ✅ **差异比较**：比较新旧组件，只更新变化的属性
- ✅ **粒度更新**：更新 `/user/name` 而非整个数据模型
- ✅ **懒加载**：大型列表使用虚拟滚动

### 15.4 无障碍

- ✅ 确保足够的颜色对比度（WCAG AA 标准）
- ✅ 支持屏幕阅读器测试
- ✅ 支持键盘导航
- ✅ 在亮色和暗色模式下都测试

### 15.5 消息设计

- ✅ 先发结构（updateComponents），再发数据（updateDataModel）
- ✅ 使用语义提示（variant），而非视觉属性（fontSize, color）
- ✅ 为交互组件提供清晰的 action 定义
- ✅ 为输入组件添加校验（checks）

---

## 16. 完整示例

### 16.1 简单问候 (v0.9.1)

```jsonl
{"version":"v0.9.1","createSurface":{"surfaceId":"greeting","catalogId":"https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json"}}
{"version":"v0.9.1","updateComponents":{"surfaceId":"greeting","components":[{"id":"root","component":"Column","children":["greeting_text","action_row"]},{"id":"greeting_text","component":"Text","text":{"path":"/message"},"variant":"h1"},{"id":"action_text","component":"Text","text":"Click Me"},{"id":"action_btn","component":"Button","child":"action_text","variant":"primary","action":{"event":{"name":"greeting_click","context":{"timestamp":"2025-12-03T10:00:00Z"}}}}]}}
{"version":"v0.9.1","updateDataModel":{"surfaceId":"greeting","value":{"message":"Hello, A2UI!","clickCount":0}}}
```

### 16.2 餐厅搜索 + 预订 (v0.9.1)

**步骤 1 — 创建 Surface：**
```json
{"version":"v0.9.1","createSurface":{"surfaceId":"restaurant_app","catalogId":"https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json","theme":{"primaryColor":"#E53935","agentDisplayName":"餐厅助手"}}}
```

**步骤 2 — 搜索结果列表：**
```json
{
  "version": "v0.9.1",
  "updateComponents": {
    "surfaceId": "restaurant_app",
    "components": [
      {
        "id": "root",
        "component": "Column",
        "children": ["page_title", "restaurant_list"]
      },
      {
        "id": "page_title",
        "component": "Text",
        "text": { "path": "/search/title" },
        "variant": "h2"
      },
      {
        "id": "restaurant_list",
        "component": "List",
        "children": {
          "componentId": "restaurant_card",
          "path": "/restaurants"
        }
      },
      {
        "id": "restaurant_card",
        "component": "Card",
        "child": "card_content"
      },
      {
        "id": "card_content",
        "component": "Column",
        "children": ["card_image", "card_name", "card_detail", "card_rating", "book_btn"]
      },
      {
        "id": "card_image",
        "component": "Image",
        "url": { "path": "imageUrl" },
        "fit": "cover",
        "variant": "hero"
      },
      {
        "id": "card_name",
        "component": "Text",
        "text": { "path": "name" },
        "variant": "h3"
      },
      {
        "id": "card_detail",
        "component": "Text",
        "text": { "path": "detail" },
        "variant": "body"
      },
      {
        "id": "card_rating",
        "component": "Text",
        "text": { "path": "rating" },
        "variant": "caption"
      },
      {
        "id": "book_text",
        "component": "Text",
        "text": "预订"
      },
      {
        "id": "book_btn",
        "component": "Button",
        "child": "book_text",
        "variant": "primary",
        "action": {
          "event": {
            "name": "start_booking",
            "context": {
              "restaurantId": { "path": "id" },
              "restaurantName": { "path": "name" }
            }
          }
        }
      }
    ]
  }
}
```

**步骤 3 — 填充搜索结果数据：**
```json
{
  "version": "v0.9.1",
  "updateDataModel": {
    "surfaceId": "restaurant_app",
    "path": "/",
    "value": {
      "search": {
        "title": "为您找到 3 家餐厅"
      },
      "restaurants": [
        {
          "id": "r1",
          "name": "西安名吃",
          "detail": "香辣手拉面，正宗西北风味",
          "imageUrl": "https://example.com/xianfoods.jpg",
          "rating": "★★★★☆",
          "address": "纽约曼哈顿 St Marks Pl 81号"
        },
        {
          "id": "r2",
          "name": "汉朝",
          "detail": "正宗四川料理，麻辣鲜香",
          "imageUrl": "https://example.com/handynasty.jpg",
          "rating": "★★★★☆",
          "address": "纽约曼哈顿 3rd Ave 90号"
        },
        {
          "id": "r3",
          "name": "红农场",
          "detail": "现代中式料理，农场到餐桌",
          "imageUrl": "https://example.com/redfarm.jpg",
          "rating": "★★★★☆",
          "address": "纽约曼哈顿 Hudson St 529号"
        }
      ]
    }
  }
}
```

**步骤 4 — 用户选择预订后，更新为预订表单：**
```json
{
  "version": "v0.9.1",
  "updateComponents": {
    "surfaceId": "restaurant_app",
    "components": [
      {
        "id": "root",
        "component": "Column",
        "children": ["booking_title", "restaurant_info", "divider_1", "date_picker", "time_picker", "guests_slider", "divider_2", "submit_btn"]
      },
      {
        "id": "booking_title",
        "component": "Text",
        "text": { "path": "/booking/title" },
        "variant": "h2"
      },
      {
        "id": "restaurant_info",
        "component": "Text",
        "text": { "call": "formatString", "args": { "value": "餐厅：${/booking/restaurantName}" } },
        "variant": "body"
      },
      {
        "id": "divider_1",
        "component": "Divider"
      },
      {
        "id": "date_picker",
        "component": "DateTimeInput",
        "label": "选择日期",
        "value": { "path": "/booking/date" },
        "enableDate": true,
        "enableTime": false
      },
      {
        "id": "time_picker",
        "component": "DateTimeInput",
        "label": "选择时间",
        "value": { "path": "/booking/time" },
        "enableDate": false,
        "enableTime": true
      },
      {
        "id": "guests_slider",
        "component": "Slider",
        "value": { "path": "/booking/guests" },
        "minValue": 1,
        "maxValue": 10
      },
      {
        "id": "guests_label",
        "component": "Text",
        "text": { "call": "formatString", "args": { "value": "用餐人数：${/booking/guests}" } },
        "variant": "caption"
      },
      {
        "id": "divider_2",
        "component": "Divider"
      },
      {
        "id": "submit_text",
        "component": "Text",
        "text": "确认预订"
      },
      {
        "id": "submit_btn",
        "component": "Button",
        "child": "submit_text",
        "variant": "primary",
        "action": {
          "event": {
            "name": "confirm_booking",
            "context": {
              "booking": { "path": "/booking" }
            }
          }
        }
      }
    ]
  }
}
```

```json
{
  "version": "v0.9.1",
  "updateDataModel": {
    "surfaceId": "restaurant_app",
    "path": "/booking",
    "value": {
      "title": "预订餐桌",
      "restaurantId": "r1",
      "restaurantName": "西安名吃",
      "date": "2025-12-15",
      "time": "19:00",
      "guests": 2
    }
  }
}
```

**步骤 5 — 预订确认后清理：**
```json
{"version":"v0.9.1","deleteSurface":{"surfaceId":"restaurant_app"}}
```

### 16.3 联系表单（完整流程，v0.9.1 JSONL）

```jsonl
{"version":"v0.9.1","createSurface":{"surfaceId":"contact_form","catalogId":"https://a2ui.org/specification/v0_9_1/catalogs/basic/catalog.json","theme":{"primaryColor":"#2563EB","agentDisplayName":"客服助手"}}}
{"version":"v0.9.1","updateComponents":{"surfaceId":"contact_form","components":[{"id":"root","component":"Card","child":"card_col"},{"id":"card_col","component":"Column","children":["title","name_field","email_field","msg_field","submit_btn"]},{"id":"title","component":"Text","text":"联系我们","variant":"h2"},{"id":"name_field","component":"TextField","label":"您的姓名","value":{"path":"/form/name"},"textFieldType":"shortText","checks":[{"call":"required","args":{"value":{"path":"/form/name"}},"message":"请输入姓名"}]},{"id":"email_field","component":"TextField","label":"电子邮箱","value":{"path":"/form/email"},"textFieldType":"shortText","checks":[{"call":"required","args":{"value":{"path":"/form/email"}},"message":"请输入邮箱"},{"call":"email","args":{"value":{"path":"/form/email"}},"message":"邮箱格式不正确"}]},{"id":"msg_field","component":"TextField","label":"留言内容","value":{"path":"/form/message"},"textFieldType":"longText","checks":[{"call":"required","args":{"value":{"path":"/form/message"}},"message":"请输入留言内容"}]},{"id":"submit_text","component":"Text","text":"提交"},{"id":"submit_btn","component":"Button","child":"submit_text","variant":"primary","action":{"event":{"name":"submit_contact","context":{"formData":{"path":"/form"}}}},"checks":[{"call":"and","args":{"values":[{"call":"required","args":{"value":{"path":"/form/name"}}},{"call":"required","args":{"value":{"path":"/form/email"}}},{"call":"email","args":{"value":{"path":"/form/email"}}},{"call":"required","args":{"value":{"path":"/form/message"}}}]}}]}]}}
{"version":"v0.9.1","updateDataModel":{"surfaceId":"contact_form","value":{"form":{"name":"","email":"","message":""}}}}
```

---

## 附录 A：关键 Schema 文件列表

| 文件 | 用途 |
|------|------|
| `common_types.json` | 可复用类型（ComponentId, ChildList, DynamicString 等） |
| `server_to_client.json` | 信封 Schema（消息 dispatching） |
| `catalogs/basic/catalog.json` | 基础组件、函数和主题定义 |
| `client_to_server.json` | 客户端到服务器消息定义 |
| `client_capabilities.json` | 客户端能力声明 |
| `server_capabilities.json` | 服务器能力声明 |
| `client_data_model.json` | 客户端附带的数据模型格式 |

## 附录 B：错误码参考

| 错误码 | 含义 |
|--------|------|
| `VALIDATION_FAILED` | Schema 验证失败 |
| `SURFACE_NOT_FOUND` | 引用的 Surface 不存在 |
| `COMPONENT_NOT_FOUND` | 引用的组件 ID 不存在 |
| `CATALOG_NOT_SUPPORTED` | 请求的目录不被客户端支持 |
| `INVALID_FUNCTION_CALL` | 函数调用不合法（v1.0） |

## 附录 C：资源链接

| 资源 | URL |
|------|-----|
| 官方网站 | https://a2ui.org/ |
| GitHub 仓库 | https://github.com/a2ui-project/a2ui |
| A2UI Composer | https://a2ui-composer.ag-ui.com/ |
| CopilotKit Widget Builder | https://go.copilotkit.ai/A2UI-widget-builder |
| A2A Protocol | https://a2a-protocol.org/ |
| AG-UI | https://ag-ui.com/ |
| JSON Pointer (RFC 6901) | https://tools.ietf.org/html/rfc6901 |
| GenUI SDK (Flutter) | https://docs.flutter.dev/ai/genui |
