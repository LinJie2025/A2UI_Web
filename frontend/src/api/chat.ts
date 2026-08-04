import client from "./client";
import type { ChatRequest } from "@/types/chat";

/**
 * Send a chat request via SSE and return the fetch Response for streaming.
 * Note: Axios doesn't support ReadableStream well, so we use fetch directly
 * in the useSSE composable. This file provides the typed request builder.
 */
export function buildChatRequest(
  messages: { role: string; content: string | null }[],
  conversationId: number | null = null,
): ChatRequest {
  return {
    messages: messages.map((m) => ({
      role: m.role as "user" | "assistant" | "system" | "tool",
      content: m.content,
    })),
    conversation_id: conversationId,
  };
}
