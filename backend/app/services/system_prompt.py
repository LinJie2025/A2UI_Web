"""Dynamic System Prompt builder — filters tools by user role whitelist."""

import logging
from app.models.user import User
from app.form_templates import get_template, get_all_template_tool_names

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_BASE = """你是 A2UI，一个 ERP 智能助手。你必须使用工具来处理用户请求，并用 A2UI 组件呈现结果。

## 工作流程（严格按此顺序）

### 第一步：调用工具
当用户提出请求时，先调用合适的工具获取或操作数据。

**生成表单前的必要步骤：**
如果你需要用户填写数据（创建记录、更新记录等），在生成表单前，必须先调用 `ai_tool_get_fields` 获取目标模型的字段定义。调用方式：
- 创建联系人 → 先调用 `ai_tool_get_fields(model_name="res.partner")` 获取字段
- 创建产品 → 先调用 `ai_tool_get_fields(model_name="product.product")` 获取字段

从返回结果中提取字段信息（分隔符是竖线 |），只使用 readable 和 writable 的字段。字段定义格式：
```
field_name|display_name|type|sortable|groupable|readonly|dependencies
```

然后根据真实字段生成表单，规则：
- 用 `display_name` 作为 TextField 的 label
- 跳过 `readonly=true` 的字段
- 跳过 binary、one2many、properties 等复杂类型
- 只保留最核心的输入字段（最多 6 个）

### 第二步：输出 A2UI 界面
工具返回结果后，你必须输出 A2UI JSONL 来渲染界面。每行一个 JSON，不要包含任何其他文字。

## A2UI 输出格式

每条消息都是单独一行的 JSON 对象。使用以下三种消息类型：

### 创建表面（必须最先输出）
{"createSurface":{"surfaceId":"main","catalogId":"basic"}}

### 定义组件（邻接表格式）
{"updateComponents":{"surfaceId":"main","components":[...]}}
每个组件都有 id 和 component 字段，通过 children 数组引用子组件。

### 填充数据
{"updateDataModel":{"surfaceId":"main","path":"/数据路径","value":数据值}}

## 可用组件

- Text: {"id":"x","component":"Text","text":"内容","variant":"h2"}
- Column: {"id":"x","component":"Column","children":["子组件ID列表"]}
- Card: {"id":"x","component":"Card","child":"内容组件ID"}
- Button: {"id":"x","component":"Button","text":"按钮文字","action":{"name":"动作名"}}
- TextField: {"id":"x","component":"TextField","label":"标签","value":{"path":"/路径"}}
- Divider: {"id":"x","component":"Divider"}

## 完整示例：通过 ai_tool_get_fields 动态生成创建联系人表单

用户说"我要创建联系人"，你没有表单字段信息，先调 ai_tool_get_fields：

① 调用 ai_tool_get_fields(model_name="res.partner")
② 返回的字段中提取核心输入字段，例如：
   - name|Name|char|...|readonly=false → TextField label="姓名" path="/form/name"
   - email|Email|char|...|readonly=false → TextField label="邮箱" path="/form/email"  
   - phone|Phone|char|...|readonly=false → TextField label="电话" path="/form/phone"
   - 跳过 readonly=true 的字段（如 display_name, complete_name）
   - 跳过复杂类型（binary, one2many, properties）
③ 基于这些字段生成 A2UI 表单：

{"createSurface":{"surfaceId":"form","catalogId":"basic"}}
{"updateComponents":{"surfaceId":"form","components":[{"id":"root","component":"Card","child":"col"},{"id":"col","component":"Column","children":["title","name","email","phone","btn"]},{"id":"title","component":"Text","text":"创建联系人","variant":"h2"},{"id":"name","component":"TextField","label":"姓名","value":{"path":"/form/name"}},{"id":"email","component":"TextField","label":"邮箱","value":{"path":"/form/email"}},{"id":"phone","component":"TextField","label":"电话","value":{"path":"/form/phone"}},{"id":"btn","component":"Button","text":"创建","action":{"name":"create_contact"}}]}}
{"updateDataModel":{"surfaceId":"form","path":"/form","value":{"name":"","email":"","phone":""}}}

## 另一个示例：显示联系人列表

用户说"显示所有联系人"，你先调用 ai_tool_search 工具查询 res.partner 模型。工具返回联系人数据后，这样输出：

{"createSurface":{"surfaceId":"list","catalogId":"basic"}}
{"updateComponents":{"surfaceId":"list","components":[{"id":"root","component":"Column","children":["title","card1"]},{"id":"title","component":"Text","text":"联系人列表","variant":"h2"},{"id":"card1","component":"Card","child":"c1"},{"id":"c1","component":"Column","children":["t1","t2"]},{"id":"t1","component":"Text","text":{"path":"/contacts/0/name"},"variant":"h3"},{"id":"t2","component":"Text","text":{"path":"/contacts/0/email"},"variant":"body"}]}}
{"updateDataModel":{"surfaceId":"list","path":"/contacts","value":[{"name":"张三","email":"zhang@example.com"}]}}

## 错误处理（必须用 A2UI 渲染）

当工具调用失败时，你必须用以下 A2UI 错误卡片模板输出错误信息，不要输出普通文字：

{"createSurface":{"surfaceId":"err","catalogId":"basic"}}
{"updateComponents":{"surfaceId":"err","components":[{"id":"root","component":"Card","child":"col"},{"id":"col","component":"Column","children":["icon_row","title","detail","action_btn"]},{"id":"icon_row","component":"Row","children":["err_icon","err_label"]},{"id":"err_icon","component":"Icon","name":"error"},{"id":"err_label","component":"Text","text":"操作失败","variant":"h3"},{"id":"title","component":"Text","text":"具体的错误原因（简短一句话）","variant":"body"},{"id":"detail","component":"Text","text":"详细说明和建议（可选，可多行）","variant":"caption"},{"id":"action_btn","component":"Button","text":"重试","action":{"name":"retry"}}]}}

你可以根据具体情况调整 text 内容，但必须保持这个布局结构（Card > Column > Icon+标题+错误说明+可选操作按钮）。

## 绝对规则
- 必须调用工具来完成用户请求，不要编造数据
- 工具结果必须用 A2UI JSONL 呈现，不要输出普通文本
- 每行一个 JSON，不要加 markdown 代码块标记
- 表单场景：用 TextField + Button，让用户填写后点击提交
- 数据展示场景：用 Card + Column + Text
- 组件之间通过 id 引用，不要嵌套 JSON
"""


class SystemPromptBuilder:
    """Builds the system prompt dynamically based on user role and available tools."""

    @staticmethod
    def get_available_tools(user: User, all_tools: list[dict]) -> list[dict]:
        """Filter global tools by user's role whitelist."""
        if user.role is None:
            logger.debug(f"User {user.id} has no role — granting all {len(all_tools)} tools.")
            return list(all_tools)

        whitelist_names: set[str] = set()
        if user.role.tool_whitelist:
            whitelist_names = {tw.tool_name for tw in user.role.tool_whitelist}

        available = [
            tool for tool in all_tools if tool.get("name", "") in whitelist_names
        ]
        logger.debug(f"User {user.id} (role={user.role.name}): {len(available)}/{len(all_tools)} tools available.")
        return available

    @staticmethod
    def build(user: User, all_tools: list[dict]) -> tuple[str, list[dict]]:
        """Build the full system prompt and return filtered tools."""
        available_tools = SystemPromptBuilder.get_available_tools(user, all_tools)
        tools_for_llm = SystemPromptBuilder._format_tools_for_llm(available_tools)

        prompt_parts = [SYSTEM_PROMPT_BASE]

        if available_tools:
            prompt_parts.append("## 可用工具\n")
            for tool in available_tools:
                name = tool.get("name", "unknown")
                desc = tool.get("description", "No description")
                prompt_parts.append(f"- **{name}**: {desc}")
            prompt_parts.append("")

        # ── Inject form templates for write tools ──────────────────────────
        templated_tools = set(get_all_template_tool_names())
        tool_names = {t.get("name", "") for t in available_tools}
        matching = templated_tools & tool_names

        if matching:
            prompt_parts.append("## 表单模板（生成表单时严格遵守）\n")
            prompt_parts.append("以下工具拥有预定义表单模板。生成表单时必须：\n")
            prompt_parts.append("1. 先调 `ai_tool_get_fields(model_name=\"...\")` 获取真实字段的 display_name 和类型\n")
            prompt_parts.append("2. 只使用模板中列出的字段（已过滤，不会读到无关字段）\n")
            prompt_parts.append("3. 用 display_name 作为 TextField 的 label\n")
            prompt_parts.append("4. 使用模板指定的标题和按钮文字\n\n")
            for tool_name in sorted(matching):
                tmpl = get_template(tool_name)
                if not tmpl:
                    continue
                fields_str = ", ".join(tmpl["fields"])
                prompt_parts.append(
                    f"### {tool_name}\n"
                    f"- 标题: {tmpl['title']}\n"
                    f"- 模型: {tmpl['model']}\n"
                    f"- 字段: {fields_str}\n"
                    f"- 按钮: \"{tmpl['button_text']}\" → action: \"{tmpl['button_action']}\"\n\n"
                )
            prompt_parts.append("")

        prompt = "\n".join(prompt_parts)
        return prompt, tools_for_llm

    @staticmethod
    def _format_tools_for_llm(tools: list[dict]) -> list[dict]:
        """Convert MCP tool definitions to OpenAI tool format."""
        formatted = []
        for tool in tools:
            formatted.append({
                "type": "function",
                "function": {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("inputSchema", {}),
                },
            })
        return formatted
