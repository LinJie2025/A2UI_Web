/** Chat message role */
export type MessageRole = "user" | "assistant" | "system" | "tool";

/** Chat message from/to API */
export interface ChatMessage {
  role: MessageRole;
  content: string | null;
  tool_calls?: ToolCall[];
  tool_call_id?: string;
  name?: string;
}

/** Tool call within a message */
export interface ToolCall {
  id: string;
  function: {
    name: string;
    arguments: string;
  };
}

/** SSE event types */
export type SSEEventType = "text" | "tool_call" | "tool_result" | "done" | "error";

/** Parsed SSE event */
export interface ParsedSSEEvent {
  event: SSEEventType;
  data: Record<string, unknown>;
}

/** Chat request payload */
export interface ChatRequest {
  messages: ChatMessage[];
  conversation_id?: number | null;
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
