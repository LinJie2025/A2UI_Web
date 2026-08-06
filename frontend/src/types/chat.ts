/** Chat message types — v2 unified format */

export type MessageRole = "user" | "assistant" | "system" | "tool";
export type MessageType = "chat" | "a2ui_action";
export type ActionStatus = "submitted" | "processing" | "done" | "failed";

/** Message from backend API */
export interface Message {
  id: number;
  conversation_id: number;
  role: MessageRole;
  message_type: MessageType;
  content: string | null;
  tool_calls_json: string | null;
  tool_call_id: string | null;
  tool_name: string | null;
  a2ui_jsonl: string | null;
  action_name: string | null;
  action_status: ActionStatus | null;
  action_result: string | null;
  created_at: string;
}

/** Tool call within a message (parsed from tool_calls_json) */
export interface ToolCall {
  id: string;
  function: {
    name: string;
    arguments: string;
  };
}

/** SSE event types */
export type SSEEventType = "user_message_saved" | "text" | "tool_call" | "tool_result" | "done" | "error";

/** Parsed SSE event */
export interface ParsedSSEEvent {
  event: SSEEventType;
  data: Record<string, unknown>;
}

/** Unified chat request payload */
export interface ChatRequest {
  conversation_id?: number | null;
  message: {
    role: string;
    content: string | null;
    meta?: {
      action_name?: string;
      form_data?: Record<string, unknown>;
    };
  };
}

/** Streaming message being built from SSE */
export interface StreamingMessage {
  id: string;
  role: "assistant";
  content: string;
  toolCalls: ToolCallStatus[];
  isComplete: boolean;
  conversationId: number | null;
}

/** Tool call status during streaming */
export interface ToolCallStatus {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
  status: "pending" | "running" | "success" | "error";
  result?: unknown;
}
