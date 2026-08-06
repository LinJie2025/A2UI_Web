# A2UI_Web 消息存储重构 — 实现计划

> 基于 design-message-refactor.md | 分 5 个阶段 | 约 60 个具体任务

---

## Phase 1: 数据库层

### 1.1 重写 Message 模型
- [ ] 1.1.1 重写 `backend/app/models/conversation.py` — 新的 Message 模型（11 个字段）
- [ ] 1.1.2 添加索引：`idx_messages_conversation_id`, `idx_messages_created_at`
- [ ] 1.1.3 更新 Conversation 模型 — 移除 a2ui_actions 关系引用

### 1.2 清理旧模型
- [ ] 1.2.1 删除 `backend/app/models/a2ui_action.py`
- [ ] 1.2.2 更新 `backend/app/models/__init__.py` — 移除 a2ui_action 导出

### 1.3 数据库初始化
- [ ] 1.3.1 删除旧数据库文件 `data/a2ui.db`
- [ ] 1.3.2 更新 `backend/app/database.py` — 添加 SQLite WAL 模式配置

---

## Phase 2: 后端 Schema 层

### 2.1 重写 Pydantic Schema
- [ ] 2.1.1 重写 `backend/app/schemas/conversation.py` — MessageResponse, ConversationResponse, ConversationDetailResponse
- [ ] 2.1.2 重写 `backend/app/schemas/chat.py` — 统一 ChatRequest（含 message + meta + context_messages）
- [ ] 2.1.3 删除 `backend/app/schemas/a2ui_action.py`

### 2.2 清理导入
- [ ] 2.2.1 更新 `backend/app/schemas/__init__.py`

---

## Phase 3: 后端 Service 层

### 3.1 重写核心服务
- [ ] 3.1.1 重写 `backend/app/services/conversation_service.py` — 适配新 Message 模型，添加 update_title 方法，last_message 过滤 tool 消息
- [ ] 3.1.2 重写 `backend/app/services/chat_service.py` — 统一流式聊天（支持普通聊天 + A2UI 表单提交），延迟批量保存
- [ ] 3.1.3 更新 `backend/app/services/agent_loop.py` — 捕获 tool_result，附带 tool_name 用于存储
- [ ] 3.1.4 更新 `backend/app/services/system_prompt.py` — LLM 上下文重建过滤 A2UI 内容
- [ ] 3.1.5 删除 `backend/app/services/a2ui_action_service.py`

### 3.2 清理导入
- [ ] 3.2.1 更新 `backend/app/services/__init__.py`

---

## Phase 4: 后端 API 层

### 4.1 统一聊天端点
- [ ] 4.1.1 重写 `backend/app/api/chat.py` — 统一 POST /api/chat（处理普通聊天 + A2UI 表单提交）
- [ ] 4.1.2 删除 `backend/app/api/a2ui.py`

### 4.2 重写对话 API
- [ ] 4.2.1 重写 `backend/app/api/conversations.py` — 使用 Pydantic Schema，添加 PUT 编辑标题
- [ ] 4.2.2 更新 `backend/app/api/tools.py` — 适配新结构

### 4.3 更新入口
- [ ] 4.3.1 更新 `backend/app/main.py` — 移除 a2ui_router 导入，更新路由注册
- [ ] 4.3.2 更新 `backend/app/errors.py` — 移除 A2UI 相关错误

---

## Phase 5: 前端层

### 5.1 类型定义
- [ ] 5.1.1 重写 `frontend/src/types/chat.ts` — 新 Message 接口
- [ ] 5.1.2 更新 `frontend/src/types/index.ts` — 清理旧类型
- [ ] 5.1.3 删除 `frontend/src/types/action.ts`

### 5.2 API 层
- [ ] 5.2.1 重写 `frontend/src/api/chat.ts` — 统一请求格式
- [ ] 5.2.2 重写 `frontend/src/api/conversation.ts` — 适配新响应格式
- [ ] 5.2.3 删除 `frontend/src/api/action.ts`

### 5.3 Store 重构
- [ ] 5.3.1 重写 `frontend/src/stores/chat.ts` — 单一消息源，移除 overlay 逻辑
- [ ] 5.3.2 重写 `frontend/src/stores/conversation.ts` — 只管理列表 + 标题编辑
- [ ] 5.3.3 创建 `frontend/src/stores/a2ui.ts` — Surface 状态管理 + Overlay 步骤
- [ ] 5.3.4 更新 `frontend/src/stores/auth.ts` — 兼容性检查

### 5.4 Composable
- [ ] 5.4.1 更新 `frontend/src/composables/useSSE.ts` — 适配新 SSE 事件（user_message_saved）
- [ ] 5.4.2 更新 `frontend/src/composables/useAuth.ts` — 兼容性检查

### 5.5 组件重构
- [ ] 5.5.1 重写 `frontend/src/components/chat/ChatMessage.vue` — 支持 A2UI 合并气泡 + Stepper
- [ ] 5.5.2 创建 `frontend/src/components/chat/A2UIActionBubble.vue` — A2UI 表单提交气泡（横向 Stepper）
- [ ] 5.5.3 更新 `frontend/src/components/chat/ChatInput.vue` — 适配新消息格式
- [ ] 5.5.4 更新 `frontend/src/components/chat/ToolCallBubble.vue` — 简化为气泡内小步骤指示器
- [ ] 5.5.5 更新 `frontend/src/components/chat/StreamingText.vue` — 兼容性检查
- [ ] 5.5.6 重写 `frontend/src/components/history/ActionSidebar.vue` — 只展示 a2ui_action，极简显示
- [ ] 5.5.7 更新 `frontend/src/components/layout/Sidebar.vue` — 添加编辑标题按钮

### 5.6 A2UI 组件
- [ ] 5.6.1 更新 `frontend/src/components/a2ui/A2UIRenderer.vue` — 支持从 a2ui_jsonl 回放渲染
- [ ] 5.6.2 更新 `frontend/src/utils/a2ui-parser.ts` — 兼容性检查

### 5.7 视图更新
- [ ] 5.7.1 更新 `frontend/src/views/ChatView.vue` — 适配新 Store 结构

### 5.8 清理
- [ ] 5.8.1 删除 `frontend/src/components/general/A2UIOverlay.vue`（如存在）
- [ ] 5.8.2 清理废弃的 dist 目录
- [ ] 5.8.3 验证 `vue-tsc --noEmit` 零错误
- [ ] 5.8.4 验证 `vite build` 成功
